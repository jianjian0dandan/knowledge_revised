# -*- coding:utf-8 -*-

import os
import types
import time
import datetime
import IP
import sys
sys.path.append('../../../')
from config import db
from utils import geo2city, IP2city,split_city
#from model import CityRepost
#from global_utils import getTopicByNameStEt
from global_config import weibo_es,weibo_index_name,weibo_index_type,MAX_REPOST_SEARCH_SIZE
from global_config import index_event_geo_city_repost,type_event_geo_city_repost
from dynamic_xapian_weibo import getXapianWeiboByTopic

from global_config import index_event_analysis_results,type_event_analysis_results



RESP_ITER_KEYS = ['_id', 'retweeted_mid', 'timestamp', 'geo', 'message_type']
SORT_FIELD = '-timestamp'

SECOND = 1
TENSECONDS = 10 * SECOND
MINUTE = 60
FIFTEENMINUTES = 15 * MINUTE
HOUR = 3600
SIXHOURS = 6 * HOUR
DAY = 24 * HOUR

def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))



def repost_search(topic, startts, endts):
    repost_list = []
    ts_arr = []
    if topic and topic != '':
        query_body = {   #把原创和转发的数据都取出来 （有size的限制，有没有需要分别取转发和原创？）
            'query':{
                'bool':{
                    'must':[
                        {'terms':{'message_type':[1,3]}}, 
                        {'range':{
                            'timestamp':{'gte': startts, 'lt':endts} 
                        }
                    }]
                }
            },
            #'sort':{"message_type":{"order":"desc"}},
            'size':MAX_REPOST_SEARCH_SIZE
        }
        repost_search = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)['hits']['hits']
        #print repost_search
        for weibo in repost_search:
            location_dict = geo_list(weibo['_source'],topic)
            if location_dict:
                repost_list.append(location_dict)
                ts_arr.append(weibo['_source']['timestamp'])
            #print len(repost_list)

        #save_rt_results(topic, repost_list)

        #save_rt_results_es(topic, repost_list)

    return sorted(list(set(ts_arr))), repost_list

def save_rt_results_es(topic, repost_list):

    #mappings_event_geo_city_repost()
    #index_name = index_event_geo_city_repost
    #index_type = type_event_geo_city_repost

    #mappings_event_analysis_results(topic)
    index_name = index_event_analysis_results
    index_type = type_event_analysis_results

    item = {}

    for location in repost_list:

        item['en_name'] = topic
        item['original'] = location['original']
        item['mid'] = location['mid']
        item['timestamp'] = location['ts']
        item['origin_location'] = location['origin_location']
        item['repost_location'] = location['repost_location']
        id = location['mid']
        try:
            item_exist = weibo_es.get(index=index_name,doc_type=index_type,id=id)['_source']
            weibo_es.update(index=index_name,doc_type=index_type,id=id,body={'doc':item})
        except Exception,e:
            weibo_es.index(index=index_name,doc_type=index_type,id=id,body=item)


'''
def save_rt_results(topic, repost_list):

    for location in repost_list:
        #print location
        item = CityRepost(location['original'], topic, location['mid'], location['ts'],\
                       location['origin_location'], location['repost_location'])
        item_exist = db.session.query(CityRepost).filter(CityRepost.topic == topic, CityRepost.mid == location['mid']).first()

        if item_exist:
           db.session.delete(item_exist)
        db.session.add(item)

    db.session.commit()
    print 'commited'
'''


def geo_list(r, topic):   #对每条微博得到转微博、mid、话题、时间、原地理位置、转发地理位置
    # {original:xx, mid:xx, topic:xx, ts:xx, origin_location:xx, repost_location:xx}
    location_dict = {}
    message_type = r['message_type']
    if message_type == 3: # 转发
        geo = r['geo'].encode('utf8')
        try:
            repost_location = str(split_city(geo))  #把元组转换成了字符串
        except:
            return None
        #print r['mid'],r['root_mid']
        if r['root_mid']:
            query_body = {
                'query':{
                    'filtered':{
                        'filter':{
                            'term':{'mid':r['root_mid']}
                        }
                    }
                }
            }
            item = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)['hits']['hits']
            if item != []:
                try:
                    origin_location = str(split_city(item[0]['_source']['geo'].encode('utf8')))
                except: 
                    return None
                #if repost_location[2:4] != 'unknown' and origin_location[2:4] != 'un': 
                if repost_location[2:4] != 'un' and origin_location[2:4] != 'un':  # str(['unknown','unknown'])所以2,3位‘un’
                    location_dict['original'] = 0
                    location_dict['mid'] = r['mid']
                    location_dict['topic'] = topic
                    location_dict['ts'] = r['timestamp']
                    location_dict['origin_location'] = origin_location
                    location_dict['repost_location'] = repost_location
                    return location_dict           
    else :
        geo = r['geo'].encode('utf8')
        try:
            origin_location = str(split_city(geo))
        except:
            return None
        if origin_location[2:4] != 'un':
            location_dict['original'] = 1
            location_dict['mid'] = r['mid']
            location_dict['topic'] = topic
            location_dict['ts'] = r['timestamp']
            location_dict['origin_location'] = origin_location
            location_dict['repost_location'] = None
            return location_dict

    return None


if __name__ == '__main__':
    START_TS = datetime2ts('2016-07-20')
    END_TS = datetime2ts('2016-08-20')

    # topic = u'奥运会'
    # START_TS = '1467648000'
    # END_TS = '1470900837' 


    #topic_id = getTopicByNameStEt(topic,START_TS,END_TS) #通过中文名得到英文名
    #topic0 = topic_id[0]['_source']['index_name']
    #print 'topic: ', topic.encode('utf8')
    #print topic_id, START_TS, END_TS

    #xapian_search = getXapianWeiboByTopic(topic_id)
    topic0 = 'aoyunhui'
    repost_search(topic0, START_TS, END_TS)
    """
    item_exist = db.session.query(CityRepost).filter(CityRepost.topic == topic).all()

    if item_exist:
        for item in item_exist:
            db.session.delete(item)
    db.session.commit()
    print 'commited'
    """
