# -*- coding: utf-8 -*-
import sys
import IP   #引入IP，对'geo'字段进行解析
import json
import datetime
import pymongo
import random
from topics import _all_topics
from config import MONGODB_HOST, MONGODB_PORT, db, mtype_kv_news

sys.path.append('../../')
from time_utils import datetime2ts, ts2HourlyTime
from global_utils import getTopicByName
from dynamic_xapian_weibo import getXapianWeiboByTopic
from model import CityTopicCountNews, CityNews
from utils import get_dynamic_mongo, media_dict_init

Minute = 60
Fifteenminutes = 15 * 60
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24

TOP_NEWS_LIMIT = 50
fields_list=['_id', 'url', 'timestamp', 'content168', 'relative_news', 'transmit_name', 'user_name', 'source_from_name', 'title', 'showurl']
SORT_FIELD = 'timestamp'

conn = pymongo.Connection(host=MONGODB_HOST, port=MONGODB_PORT)
mongodb = conn['news']


def get_filter_dict():
    fields_dict = {}
    for field in fields_list:
        fields_dict[field] = 1
    return fields_dict

def media2city(media): #解析为地址
    media = media.split('-')[0]
    if media in media_dict:
        geo = u'中国 ' + media_dict[media]
        geo = '\t'.join(geo.split())
    else:
        geo = None
    return geo

def save_rt_results(topic, mtype, results, during, first_item):
    ts, ccount = results
    item = CityTopicCountNews(topic, during, ts, mtype, json.dumps(ccount), json.dumps(first_item))
    item_exist = db.session.query(CityTopicCountNews).filter(CityTopicCountNews.topic==topic, \
                                                                    CityTopicCountNews.range==during, \
                                                                    CityTopicCountNews.end==ts, \
                                                                    CityTopicCountNews.mtype==mtype).first()
    if item_exist:
        db.session.delete(item_exist)
    db.session.add(item)
    db.session.commit()

def save_ns_results(topic, ts, during, n_limit, news):
    item = CityNews(topic , ts, during, n_limit, json.dumps(news))
    item_exist = db.session.query(CityNews).filter(CityNews.topic==topic, \
                                                          CityNews.range==during, \
                                                          CityNews.end==ts, \
                                                          CityNews.limit==n_limit).first()
    if item_exist:
        db.session.delete(item_exist)
    db.session.add(item)
    db.session.commit()

def cityCronTopicNews(topic, mongo_collection, start_ts, over_ts, during=Fifteenminutes, n_limit=TOP_NEWS_LIMIT):
    if topic and topic != '':
        start_ts = int(start_ts)
        over_ts = int(over_ts)

        over_ts = ts2HourlyTime(over_ts, during)
        interval = (over_ts - start_ts) / during

        topics = topic.strip().split(',')
        for i in range(interval, 0, -1):
            ccount_dict = {}
            for k, v in mtype_kv_news.iteritems():
                ccount_dict[k] = {}

            begin_ts = over_ts - during * i
            end_ts = begin_ts + during
            first_timestamp = end_ts
            first_item = {}
            news = []

            query_dict = {
                'timestamp': {'$gt': begin_ts, '$lt': end_ts},
            }
            fields_dict = get_filter_dict()

            results_list = mongo_collection.find(query_dict, fields_dict).sort([(SORT_FIELD,1)])

            for weibo_result in results_list:
                if (weibo_result['timestamp'] <= first_timestamp ):
                    first_timestamp = weibo_result['timestamp']
                    first_item = weibo_result

                if weibo_result['source_from_name'] and weibo_result['transmit_name']:
                    source = media2city(weibo_result['source_from_name'])
                    if source:
                        try:
                            ccount_dict['forward'][source] += 1
                        except KeyError:
                            ccount_dict['forward'][source] = 1
                        """
                        try:
                            ccount_dict['sum'][source] += 1
                        except KeyError:
                            ccount_dict['sum'][source] = 1
                        """
                elif weibo_result['source_from_name']:
                    source = media2city(weibo_result['source_from_name'])
                    if source:
                        try:
                            ccount_dict['origin'][source] += 1
                        except KeyError:
                            ccount_dict['origin'][source] = 1
                        """
                        try:
                            ccount_dict['sum'][source] += 1
                        except KeyError:
                            ccount_dict['sum'][source] = 1
                        """
                else:
                    continue

                weibo_result['source_from_area'] = source # 添加区域字段
                news.append(weibo_result)

            for k, v in mtype_kv_news.iteritems():
                results = [end_ts, ccount_dict[k]]
                save_rt_results(topic,v, results, during, first_item)

            sorted_news = sorted(news, key=lambda k: k[SORT_FIELD], reverse=True)
            sorted_news = sorted_news[:n_limit]
            save_ns_results(topic, end_ts, during, n_limit, sorted_news)


if __name__ == '__main__':
    start_ts = datetime2ts('2015-03-02')
    end_ts = datetime2ts('2015-03-15')

    topic = u'两会2015'
    media_dict = media_dict_init()
    mongo_collection = get_dynamic_mongo(mongodb, topic, start_ts, end_ts)

    print 'topic: ', topic.encode('utf8'), 'from %s to %s' % (start_ts, end_ts)
    cityCronTopicNews(topic, mongo_collection, start_ts=start_ts, over_ts=end_ts, during=Fifteenminutes)

