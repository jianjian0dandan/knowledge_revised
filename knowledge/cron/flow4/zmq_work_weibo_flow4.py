# -*- coding=utf-8 -*-

import re
import sys
import zmq
import time
import json
import math
from datetime import datetime

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts, ts2date
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from triple_sentiment_classifier import triple_classifier
from global_config import ZMQ_VENT_PORT_FLOW4, ZMQ_CTRL_VENT_PORT_FLOW4,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_utils import R_DOMAIN, r_domain_name, R_TOPIC, r_topic_name,\
                         R_DOMAIN_SENTIMENT, r_domain_sentiment_pre, \
                         R_TOPIC_SENTIMENT, r_topic_sentiment_pre,\
                         R_SENTIMENT_ALL
#from global_config import SENSITIVE_WORDS_PATH
from parameter import Fifteen, RUN_TYPE, RUN_TEST_TIME

#abandon in version-160312
'''
f = open(SENSITIVE_WORDS_PATH, 'rb')

def load_sensitive_words():
    ZZ_WORD = []
    for line in f:
        line_list = line.split('=')
        word = line_list[0]
        ZZ_WORD.append(word.decode('utf-8'))
    f.close()
    return ZZ_WORD

SENSITIVE_WORD = load_sensitive_words()
'''

def cal_text_work(item):
    uid = item['uid']
    timestamp = item['timestamp']
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    text = item['text']
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    RE = re.compile(u'#([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
    hashtag_list = RE.findall(text)
    if hashtag_list:
        # there all use unicode·
        hashtag_dict = dict()
        for hashtag in hashtag_list:
            try:
                hashtag_dict[hashtag] += 1
            except:
                hashtag_dict[hashtag] = 1
        try:
            hashtag_count_string = r_cluster.hget('hashtag_'+str(ts), str(uid))
            hashtag_count_dict = json.loads(hashtag_count_string)
            for hashtag in hashtag_dict:
                count = hashtag_dict[hashtag]
                try:
                    hashtag_count_dict[hashtag] += count
                except:
                    hashtag_count_dict[hashtag] = count
            r_cluster.hset('hashtag_'+str(ts), str(uid), json.dumps(hashtag_count_dict))
        except:
            r_cluster.hset('hashtag_'+str(ts), str(uid), json.dumps(hashtag_dict))

#abandon in version-160312
''' 
def cal_text_sensitive(item):
    text = item['text']
    uid = item['uid']
    timestamp = item['timestamp']
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    sensitive_result = [word for word in SENSITIVE_WORD if word in text]
    if sensitive_result:
        sensitive_dict = dict()
        for word in sensitive_result:
            try:
                sensitive_dict[word] += 1
            except:
                sensitive_dict[word] = 1
        try:
            sensitive_count_string = r_cluster.hget('sensitive_'+str(ts), str(uid))
            sensitive_count_dict = json.loads(sensitive_count_string)
            for word in sensitive_dict:
                count = sensitive_dict[word]
                try:
                    sensitive_count_dict[word] += count
                except:
                    sensitive_count_dict[word] = count
            r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_count_dict))
        except:
            r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_dict))
'''

#use to compute sentiment trend for all
def save_sentiment_all(date, new_timestamp, sentiment):
    if sentiment != 0 and sentiment != 1:
        sentiment = 7
    r_name = date + '_' + str(sentiment) + '_all' #2016-03-3_0_all
    R_SENTIMENT_ALL.hincrby(r_name, new_timestamp, 1)
    #{'2016-03-03_0_all': {135840000: 1}}

#use to compute domain sentiment trend for user in user_portrait
def save_sentiment_domain(date, new_timestamp, sentiment, uid):
    #step1: get uid domain
    user_domain = R_DOMAIN.hget(r_domain_name, uid)
    if user_domain:
        #step2: save sentiment to domain
        if sentiment != 0 and sentiment != 1:
            sentiment = 7
        r_domain_sentiment_name = r_domain_sentiment_pre + date + '_' + str(sentiment) + '_' + user_domain
        R_DOMAIN_SENTIMENT.hincrby(r_domain_sentiment_name, new_timestamp, 1)
        

#use to compute topic sentiment trend for user in user_portrait
def save_sentiment_topic(date, new_timestamp, sentiment, uid):
    #step1: get uid topic
    user_topic_string = R_TOPIC.hget(r_topic_name, uid)
    if user_topic_string:
        if sentiment != 0 and sentiment != 1:
            sentiment = 7
        #step2: save sentiment to topic
        topic_list = json.loads(user_topic_string)
        for topic_item in topic_list:
            r_topic_sentiment_name = r_topic_sentiment_pre + date + '_' + str(sentiment) + '_' + topic_item
            R_TOPIC_SENTIMENT.hincrby(r_topic_sentiment_name, new_timestamp, 1)

if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW4))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW4))

    count = 0
    tb = time.time()
    ts = tb
    while 1:
        item = receiver.recv_json()

        if not item:
            continue 

        if int(item['sp_type']) == 1:
            #step1: compute hashtag to save redis
            cal_text_work(item)
            #step2: compute sentiment to redis
            uid = item['uid']
            text = item['text']
            sentiment, keywords_list = triple_classifier(item)
            #step3: compute time_segment
            timestamp = item['timestamp']
            date = ts2datetime(timestamp)
            date_ts = datetime2ts(date)
            time_segment = (timestamp - date_ts) / Fifteen
            new_timestamp = date_ts + time_segment * Fifteen
            #step4: save to sentiment_all
            save_sentiment_all(date, new_timestamp, sentiment)
            #step5: save to sentiment in domain
            save_sentiment_domain(date, new_timestamp, sentiment, uid)
            #step6: save to sentiment in topic
            save_sentiment_topic(date, new_timestamp, sentiment, uid)

        count += 1
        #run_type
        if count % 10000 == 0 and RUN_TYPE == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
