# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
from time_utils import datetime2ts, ts2HourlyTime
from dynamic_xapian_weibo import getXapianWeiboByDate, getXapianWeiboByDuration

Minute = 60
Fifteenminutes = 15 * 60
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24

TOP_KEYWORDS_LIMIT = 50
TOP_WEIBOS_LIMIT = 50

RESP_ITER_KEYS = ['_id', 'user', 'retweeted_uid', 'retweeted_mid', 'text', 'timestamp', 'reposts_count', 'bmiddle_pic', 'geo', 'comments_count', 'sentiment', 'terms']
SORT_FIELD = 'reposts_count'
emotion_kv = {'happy':1, 'angry':2, 'sad':3, 'none':0}

def sentimentCronTopic(topic,xapian_search_weibo, start_ts, over_ts, sort_field=SORT_FIELD, save_fields=RESP_ITER_KEYS, during=Fifteenminutes, w_limit=TOP_WEIBOS_LIMIT, k_limit=TOP_KEYWORDS_LIMIT):
    query_dict = {
        'timestamp':{'$gt':start_ts, '$lt':over_ts},
        'topics': [topic]
        }
    print 'query_dict:', query_dict
    result_dict = {}
    s = 0
    for k, v in emotion_kv.iteritems():
        query_dict['sentiment'] = v
        scount = xapian_search_weibo.search(query=query_dict, count_only=True)
        result_dict[v] = scount
        s = s + scount
    print 'result_dict:', result_dict
    result_ratio_dict = {}
    for k, v in result_dict.iteritems():
        result_ratio_dict[k] = float(v) / float(s)
    print 'result_ratio_dict:', result_ratio_dict

def cal_topic_sentiment_by_date(topic, datestr, duration):
    start_ts = datetime2ts(datestr)
    end_ts = start_ts + Fifteenminutes
    datestr = datestr.replace('-', '')
    xapian_search_weibo = getXapianWeiboByDate(datestr)
    if xapian_search_weibo:
        sentimentCronTopic(topic, xapian_search_weibo, start_ts=start_ts, over_ts=end_ts, during=duration)

def worker(topic, datestr):
    print 'topic: ', topic.encode('utf8'), 'datestr:', datestr, 'Fifteenminutes: '
    cal_topic_sentiment_by_date(topic, datestr, Fifteenminutes)

if __name__=='__main__':
    datestr = '2013-09-01'
    topic = u'中国'
    worker(topic, datestr)
