# -*- coding:utf-8 -*-

import os
import sys
import types
import time
import datetime
import IP
import json
import random
import pymongo
from config import MONGODB_HOST, MONGODB_PORT, db

sys.path.append('../../')
from time_utils import datetime2ts
from model import CityRepostNews
from global_utils import getTopicByName
from dynamic_xapian_weibo import getXapianWeiboByTopic
from utils import get_dynamic_mongo, media_dict_init

SECOND = 1
TENSECONDS = 10 * SECOND
MINUTE = 60
FIFTEENMINUTES = 15 * MINUTE
HOUR = 3600
SIXHOURS = 6 * HOUR
DAY = 24 * HOUR

fields_list=['_id', 'url', 'timestamp', 'content168', 'relative_news', 'transmit_name', 'user_name', 'source_from_name', 'title', 'showurl']
SORT_FIELD = 'timestamp'

conn = pymongo.Connection(host=MONGODB_HOST, port=MONGODB_PORT)
mongodb = conn['news']

def get_filter_dict():
    fields_dict = {}
    for field in fields_list:
        fields_dict[field] = 1
    return fields_dict

def news_repost_search(topic, mongo_collection, startts, endts):
    repost_list = []
    ts_arr = []
    if topic and topic != '':
        startts = int(startts)
        endts = int(endts)

        query_dict = {
            "timestamp": {
                "$gte": startts,
                "$lte": endts
            }
        }
        fields_dict = get_filter_dict()

        results_list = mongo_collection.find(query_dict, fields_dict).sort([(SORT_FIELD,1)])
        count = results_list.count()
        print 'count',count

        for r in results_list:
            location_dict = results_gen(r)
            if location_dict:
                repost_list.append(location_dict)
                ts_arr.append(r['timestamp'])

        print len(repost_list)

        save_rt_results(topic, repost_list)

    return sorted(list(set(ts_arr))), repost_list


def save_rt_results(topic, repost_list):

    for location in repost_list:
        item = CityRepostNews(location['original'], topic, location['_id'], location['timestamp'],\
                        location['origin_location'], location['repost_location'])
        item_exist = db.session.query(CityRepostNews).filter(CityRepostNews.topic == topic, CityRepostNews.mid == location['_id']).first()

        if item_exist:
            db.session.delete(item_exist)
        db.session.add(item)

    db.session.commit()
    print 'commited'


def media2city(media): #解析为地址
    media = media.split('-')[0]
    if media in media_dict:
        geo = u'中国 ' + media_dict[media]
        geo = '\t'.join(geo.split())
        # print media.encode('utf-8'),geo.encode('utf-8')
    else:
        geo = None
        print media.encode('utf-8'),geo
    return geo

def check_location(locations):
    for location in locations:
        if (location == '') or (location == None):
            return False
        try:
            tokens = location.split('\t')
            if tokens[0] == u'中国':
                if len(tokens) == 1:
                    return False

                elif len(tokens) == 2:
                    province, district = tokens[1], None

                elif len(tokens) == 3:
                    province, district = tokens[1], tokens[2]
            else:
                return False
        except:
            return False
    return True


def results_gen(r):
    # 处理字段source_from_name, transmit_name, original
    location_dict = {}
    if r['source_from_name'] and r['transmit_name']:
        source = media2city(r['source_from_name'])
        transmit = media2city(r['transmit_name'])
        if check_location([transmit, source]):
            r['original'] = 0 # 非原创
            r['origin_location'] = transmit.split('\t')[1]
            r['repost_location'] = source.split('\t')[1]
            return r
    elif r['source_from_name']:
        source = media2city(r['source_from_name'])
        if check_location([source]):
            r['original'] = 1
            r['origin_location'] = source.split('\t')[1]
            r['repost_location'] = None
            return r

    return None


if __name__ == '__main__':
    start_ts = datetime2ts('2015-03-02')
    end_ts = datetime2ts('2015-03-15')

    topic = u'两会2015'
    media_dict = media_dict_init()
    mongo_collection = get_dynamic_mongo(mongodb, topic, start_ts, end_ts)

    print 'topic: ', topic.encode('utf8'), 'from %s to %s' % (start_ts, end_ts)
    news_repost_search(topic, mongo_collection, start_ts, end_ts)
