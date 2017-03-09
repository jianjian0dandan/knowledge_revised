# -*- coding: UTF-8 -*-
import time
import urllib
import json
import sys

from retweet import accumulate_retweet
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts

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
    for line in f:
        count += 1
        if count % 10000 ==0:
            te = time.time()
            print 'all_count:', count, '%s sec' % (te - ts)
            ts = te
        # acturally there need a sent and recieve procession!!!!!    
        itemdict = itemLine2Dict(line)

        # attribute of retweet social
        if itemdict and itemdict['message_type']==3:
            accumulate_retweet(itemdict)
        
                       
if __name__=='__main__':
    for j in range(1,2):
        for i in range(1,2):
            print 'start compute:', str(j) + '_' + str(i)
            file_path = '/home/ubuntu4/huxiaoqian/portrait/MB_QL_9_'+str(j) +'_NODE'+ str(i) + '.csv'  
            csv2dict(file_path)
