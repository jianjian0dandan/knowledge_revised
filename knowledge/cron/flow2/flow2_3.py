# -*- coding: UTF-8 -*-
import re
import time
import urllib
import json
import sys

from mention import accumulate_at
from area import accumulate_ip
from activity import accumulate_activity

ORIGIN_KEYS = ['user', 'retweeted_uid', '_id', 'retweeted_mid', 'timestamp',
               'input_time', 'geo', 'province', 'city', 'message_type', 'user_fansnum',
               'user_friendsnum', 'comments_count', 'reposts_count',
               'retweeted_comments_count', 'retweeted_reposts_count', 'text', 'is_long',
               'bmiddle_pic', 'pic_content', 'audio_url', 'audio_content', 'video_url',
               'video_content', 'sp_type']
RESP_ITER_KEYS = ['_id', 'user', 'retweeted_uid', 'retweeted_mid', 'text',
                  'timestamp', 'reposts_count', 'source', 'bmiddle_pic',
                  'geo', 'attitudes_count', 'comments_count', 'message_type']
CONVERT_TO_INT_KEYS = ['_id', 'user', 'retweeted_uid', 'retweeted_mid',
                       'reposts_count', 'comments_count', 'timestamp', 'message_type']
ABSENT_KEYS = ['attitudes_count', 'source']
IP_TO_GEO_KEY = 'geo'
MID_STARTS_WITH_C = '_id'  # weibo mid starts with 'c_'
SP_TYPE_KEYS = '1'  # 1代表新浪微博

punc_dict = {'comma':',', 'period':'。', 'colon':'：', 'semic':'；', 'qmark':'？', 'exclam':'！', 'dash':'——', 'quote':'“'}

# IP address manipulation functions
def numToDottedQuad(n):
    "convert long int to dotted quad string"

    d = 256 * 256 * 256
    q = []
    while d > 0:
        m, n = divmod(n, d)
        q.append(str(m))
        d = d / 256

    return '.'.join(q)

def ip2geo(ip_addr):
    # ip_addr: '236112240'
    DottedIpAddr = numToDottedQuad(int(ip_addr))
    return DottedIpAddr


def WeiboItem(itemList):
    weibo = dict()

    for key in RESP_ITER_KEYS:

        value = None

        if key not in ABSENT_KEYS:
            value = itemList[ORIGIN_KEYS.index(key)]

            if key == IP_TO_GEO_KEY:
                value = ip2geo(value)

            elif key == MID_STARTS_WITH_C:
                if value[:2] == 'c_':
                    value = int(value[2:])
                else:
                    value = int(value)

            elif key in CONVERT_TO_INT_KEYS:
                value = int(value) if value != '' else 0

        if value is not None:
            weibo[key] = value

    return weibo


class UnkownParseError(Exception):
    pass


def itemLine2Dict(line):
    line = line.decode("utf8", "ignore")
    itemlist = line.strip().split(',')
    if itemlist[-1] == SP_TYPE_KEYS:
        if len(itemlist) != 25:
            try:
                tp = line.strip().split('"')
                if len(tp) != 3:
                    raise UnkownParseError()
                field_0_15, field_16, field_17_24 = tp
                field_0_15 = field_0_15[:-1].split(',')
                field_17_24 = field_17_24[1:].split(',')
                field_0_15.extend([field_16])
                field_0_15.extend([field_17_24])
                itemlist = field_0_15
                if len(itemlist) != 25:
                    raise UnkownParseError()
            except UnkownParseError:
                return None
    else:
        return None

    try:
        itemdict = WeiboItem(itemlist)
    except:
        itemdict = None

    return itemdict

def csv2dict(file_path):
    f = open(file_path, 'r')
    count = 0
    ts = time.time()
    r_ts = time.time()
    r_count = 0
    try:
        for line in f:
            count += 1
            if count % 10000 ==0:
                te = time.time()
                print 'all_count:', count, '%s sec' % (te - ts)
                ts = te
            # acturally there need a sent and recieve procession!!!!!    
            itemdict = itemLine2Dict(line)
            # attribute of city
            if count == 100:
                break
            if itemdict and itemdict['text']:
                text = itemdict['text']
                #print 'text:', text.encode('utf-8')
                #print 'text:', type(text)
                '''
                for emo_class in emoticon_dict:
                    emoticons = emoticon_dict[emo_class]
                    for emoticon in emoticons:
                        count = text.count(emoticon.decode('utf-8'))
                        if count != 0:
                            print 'emoticon:', emoticon, count
                            print 'text:', text.encode('utf-8')
                '''
                #if isinstance(text, str):
                #    text = text.decode('utf-8', 'ignore')
                #RE = re.compile(r'[\u3000-\u303f\ufb00-\ufffd]+')
                #m = RE.search(text, 0)
                #print m.group()
                for punc in punc_dict:
                    value = punc_dict[punc]
                    if value in text:
                        print 'punc:', punc
                '''
                if len(punc_list)!=0:
                    print 'punc_list:', len(punc_list), punc_list
                    print 'text:', text.encode('utf-8')
                #
                if isinstance(text, str):
                    text = text.decode('utf-8', 'ignore')
                #print 'text:', type(text)
                RE = re.compile(u'#([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
                hashtag_list = RE.findall(text)
                #hashtag_list = RE.findall(text)
                #print 'len_hashtag_list:', len(hashtag_list)
                if len(hashtag_list)!=0:
                    for hashtag in hashtag_list:
                        print 'hashtage:', hashtag.encode('utf-8')
                    print 'text:', text.encode('utf-8')
                accumulate_ip(itemdict)
                # attribute of @ social
                accumulate_at(itemdict)
                # attribtue of activity
                accumulate_activity(itemdict)
                '''
    except:
        pass
                       
if __name__=='__main__':
    for j in range(1,2):
        for i in range(1,2):
            print 'start compute:', str(j) + '_' + str(i)
            file_path = '/home/ubuntu8/data1309/20130901/MB_QL_9_'+ str(j) +'_NODE'+ str(i) + '.csv' 
            f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/emoticons.txt', 'rb')
            emoticon_dict = dict()
            for line in f:
                line_list = line.split(':')
                emoticon = line_list[0]
                count = line_list[1]
                #print 'emoticon:', type(emoticon), emoticon
                try:
                    emoticon_dict[count].append(emoticon)
                except:
                    emoticon_dict[count] = [emoticon]

            csv2dict(file_path)
            
