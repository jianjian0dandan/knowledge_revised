# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv
import time
from elasticsearch import Elasticsearch
sys.path.append('../../')
from global_config import join,pusher,maker,contain,friend,relative,colleague,\
                         user_profile_host,profile_index_name,profile_index_type,\
                         retweet_comment_es_host,retweet_comment_port,\
                         retweet_index_name_pre,retweet_index_type,be_retweet_index_name_pre,be_retweet_index_type,\
                         comment_index_name_pre,comment_index_type,be_comment_index_name_pre,be_comment_index_type

#for test
RUN_TYPE = 0 #0 mark run for test; 1 mark run for operation
R_BEGIN_TIME = '2013-09-01'
DAY = 24*3600

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

#use to get retweet/be_retweet/comment/be_comment db_number
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    r_beigin_ts = datetime2ts(R_BEGIN_TIME)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) % 2 + 1
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number

es_user_profile = Elasticsearch(user_profile_host, timeout = 600)
es_retweet = Elasticsearch(retweet_comment_es_host, timeout = 600)
es_comment = Elasticsearch(retweet_comment_es_host, timeout = 600)

##对微博文本进行预处理

def cut_filter(text):
    pattern_list = [r'\（分享自 .*\）', r'http://\w*']
    for i in pattern_list:
        p = re.compile(i)
        text = p.sub('', text)
    return text

def re_cut(w_text):#根据一些规则把无关内容过滤掉
    
    w_text = cut_filter(w_text)
    w_text = re.sub(r'[a-zA-z]','',w_text)
    a1 = re.compile(r'\[.*?\]' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'回复' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'\@.*?\:' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'\@.*?\s' )
    w_text = a1.sub('',w_text)
    if w_text == u'转发微博':
        w_text = ''

    return w_text

##微博文本预处理结束

## 加载分词工具

SCWS_ENCODING = 'utf-8'
SCWS_RULES = '/usr/local/scws/etc/rules.utf8.ini'
CHS_DICT_PATH = '/usr/local/scws/etc/dict.utf8.xdb'
CHT_DICT_PATH = '/usr/local/scws/etc/dict_cht.utf8.xdb'
IGNORE_PUNCTUATION = 1
abs_path = './'
ABSOLUTE_DICT_PATH = os.path.abspath(os.path.join(abs_path, 'dict'))
CUSTOM_DICT_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'userdic.txt')
EXTRA_STOPWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'stopword.txt')
EXTRA_EMOTIONWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'emotionlist.txt')
EXTRA_ONE_WORD_WHITE_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'one_word_white_list.txt')
EXTRA_BLACK_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'black.txt')

cx_dict = ['an','Ng','n','nr','ns','nt','nz','vn','@']#关键词词性词典

def load_one_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_EMOTIONWORD_PATH)]
    return one_words

def load_black_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_BLACK_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
black_word = set(load_black_words())

def load_scws():
    s = scws.Scws()
    s.set_charset(SCWS_ENCODING)

    s.set_dict(CHS_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CHT_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CUSTOM_DICT_PATH, scws.XDICT_TXT)

    # 把停用词全部拆成单字，再过滤掉单字，以达到去除停用词的目的
    s.add_dict(EXTRA_STOPWORD_PATH, scws.XDICT_TXT)
    # 即基于表情表对表情进行分词，必要的时候在返回结果处或后剔除
    s.add_dict(EXTRA_EMOTIONWORD_PATH, scws.XDICT_TXT)

    s.set_rules(SCWS_RULES)
    s.set_ignore(IGNORE_PUNCTUATION)
    return s

SW = load_scws()

def cut_des(text):

    des_dict = ['nr','ns','nt','nz']
    tks = [token[0] for token
            in SW.participle(text)
            if token[1] in des_dict]

    return set(tks)

##加载分词工具结束

##加载事件类别对应的权重
EVENT_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'event_type.csv')

def load_event_type():
    reader = csv.reader(file(EVENT_PATH, 'rb'))
    event_type = dict()
    for e_t,weight in reader:
        event_type[e_t] = float(weight)
    return event_type

event_type_dict = load_event_type()

##加载事件类别对应的权重结束

or_list = [1,2,3,4,5,6,7,8]#新浪企业账户类型
interaction_count = 100
N_GRAM = 5#词共现窗口长度
WORD_N = 30#提取关键词的数量
TOPIC_N = 10#lda话题数量
MAX_COUNT = 500#最大的词语数量(topic pagerank)
COUNT_RATE = 0.1#限制交互数量的比例

#人物各指标权重
influence_weight = 0.3
importance_weight = 0.3
activeness_weight = 0.1
sensitive_weight = 0.3

#事件各指标权重
type_weight = 0.6
weibo_weight = 0.2
people_weight = 0.2

#人物相似度各指标权重
p1_weight = 0.1
p2_weight = 0.3
p3_weight = 0.2
p4_weight = 0.2
p5_weight = 0.2

#事件相似度各指标权重
e1_weight = 0.2
e2_weight = 0.2
e3_weight = 0.3
e4_weight = 0.3

#专题相似度各指标权重
t1_weight = 0.4
t2_weight = 0.3
t3_weight = 0.3

#群体相似度各指标权重
q1_weight = 0.4
q2_weight = 0.3
q3_weight = 0.3



