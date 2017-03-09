# -*- coding: utf-8 -*-

import sys
import json
import datetime
#from topics import _all_topics

sys.path.append('../../../')
from time_utils import datetime2ts, ts2HourlyTime
#from global_utils import getTopicByNameStEt
#from dynamic_xapian_weibo import getXapianWeiboByTopic
from global_config import mtype_kv, weibo_es,weibo_index_name,weibo_index_type
from global_config import index_event_geo_province_weibos,type_event_geo_province_weibos,\
                         index_event_geo_city_topic_count,type_event_geo_city_topic_count
from global_config import index_event_analysis_results,type_event_analysis_results

#from model import CityTopicCount, CityWeibos,ProvinceWeibos
from utils import geo2city, IP2city,split_city

Minute = 60
Fifteenminutes = 15 * 60
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24


TOP_WEIBOS_LIMIT = 50
RESP_ITER_KEYS = ['_id', 'user', 'retweeted_uid', 'retweeted_mid', 'text', 'timestamp', 'reposts_count', 'bmiddle_pic', 'geo', 'comments_count', 'sentiment', 'terms']
fields_list=['_id', 'user', 'retweeted_uid', 'retweeted_mid', 'text', 'timestamp', 'reposts_count', 'source', 'bmiddle_pic', 'geo', 'attitudes_count', 'comments_count', 'sentiment', 'topics', 'message_type', 'terms']
SORT_FIELD = 'timestamp'


def save_rt_results_es(topic, results, during, first_item):

    #mappings_event_geo_city_topic_count()
    #index_name = index_event_geo_city_topic_count
    #index_type = type_event_geo_city_topic_count

    mappings_event_analysis_results(topic)
    index_name = index_event_analysis_results
    index_type = type_event_analysis_results

    item = {}

    for mtype, time_geo in results.iteritems():##{'message_type':[timestamp,{['province':('provice':cishu),()],'city':[(city:cishu)}]}
        item['en_name'] = topic
        item['end_ts'] = time_geo[0]
        item['range'] = during
        item['mtype'] = mtype
        item['ccount'] = time_geo[1]
        item['first_item'] = first_item

        id = topic + '_' + ts

        try:
            item_exist = weibo_es.get(index=index_name,doc_type=index_type,id=id)['_source']
            weibo_es.update(index=index_name,doc_type=index_type,id=id,body={'doc':item})
        except Exception,e:
            weibo_es.index(index=index_name,doc_type=index_type,id=id,body=item)

'''
def save_rt_results(topic, results, during, first_item):
    for k, time_geo in results.iteritems():##{'message_type':[timestamp,{['province':('provice':cishu),()],'city':[(city:cishu)}]}
        mtype = k
        ts = time_geo[0]
        ccount = time_geo[1]
        item = CityTopicCount(topic, during, ts, mtype, json.dumps(ccount), json.dumps(first_item))
        item_exist = db.session.query(CityTopicCount).filter(CityTopicCount.topic==topic, \
                                                                            CityTopicCount.range==during, \
                                                                            CityTopicCount.end==ts, \
                                                                            CityTopicCount.mtype==mtype).first()
        if item_exist:
            db.session.delete(item_exist)
        db.session.add(item)
    db.session.commit()
'''

def save_ws_results_es(topic, ts, during, n_limit, province,city,weibos):

    #mappings_event_geo_province_weibos()
    #index_name = index_event_geo_province_weibos
    #index_type = type_event_geo_province_weibos

    #mappings_event_analysis_results(topic)
    index_name = index_event_analysis_results
    index_type = type_event_analysis_results

    item = {}

    item['en_name'] = topic
    item['end_ts'] = ts
    item['range'] = during
    item['limit'] = n_limit
    item['province'] = province
    item['city'] = city
    item['weibo'] = json.dumps(weibos)
    
    id = topic + '_' + ts

    try:
        item_exist = weibo_es.get(index=index_name,doc_type=index_type,id=id)['_source']
        weibo_es.update(index=index_name,doc_type=index_type,id=id,body={'doc':item})
    except Exception,e:
        weibo_es.index(index=index_name,doc_type=index_type,id=id,body=item)

'''

def save_ws_results(topic, ts, during, n_limit, province,city,weibos):
    item = ProvinceWeibos(topic,ts, during, n_limit, province,city,json.dumps(weibos))
    item_exist = db.session.query(ProvinceWeibos).filter(ProvinceWeibos.topic==topic, \
                                                          ProvinceWeibos.range==during, \
                                                          ProvinceWeibos.end==ts, \
                                                          ProvinceWeibos.city==city,\
                                                          ProvinceWeibos.limit==n_limit).first()
    # item_exist = db.session.query(CityWeibos).filter(CityWeibos.topic==topic, \
    #                                                       CityWeibos.range==during, \
    #                                                       CityWeibos.end==ts, \
    #                                                       CityWeibos.city=city,\
    #                                                       CityWeibos.limit==n_limit).first()
    if item_exist:
        db.session.delete(item_exist)
    db.session.add(item)
    db.session.commit()
'''

def cityTopic(topic,start_ts,over_ts,during=Fifteenminutes, n_limit=TOP_WEIBOS_LIMIT):
    if topic and topic != '':
        start_ts = int(start_ts)
        over_ts = int(over_ts)

        over_ts = ts2HourlyTime(over_ts, during)
        interval = (over_ts - start_ts) / during

        geo_cityTopic_results = {}
        geo_cityTopic_results['geo_weibos'] = {}
        geo_cityTopic_results['geo_cityCount'] = {}

        #geo_weibos = {}
        #geo_cityCounts = {}

        #topics = topic.strip().split(',')
        for i in range(interval, 0, -1):
            mtype_ccount = {}  # mtype为message_type，ccount为{city：count}
            begin_ts = over_ts - during * i
            end_ts = begin_ts + during
            print begin_ts,end_ts,topic
            weibos = []
            first_item = {}
            geo_cityTopic_results['geo_weibos'][end_ts] = {}
            geo_cityTopic_results['geo_cityCount'][end_ts] = {}
            
            for k,v in mtype_kv.iteritems(): #v代表转发、评论、原创

                geo_cityTopic_results['geo_weibos'][end_ts][v] = []
                #geo_cityTopic_results['geo_cityCount'][end_ts][v] = []

                province_dict = {}
                city_dict = {}
                query_body = {   #按message_type得到微博
                    'query':{
                        'bool':{
                            'must':[
                                {'term':{'message_type':v}},  
                                {'range':{
                                    'timestamp':{'gte': begin_ts, 'lt':end_ts} 
                                }
                            }]
                        }
                    },
                    'sort':{SORT_FIELD:{"order":"desc"}},
                    'size':n_limit
                    }
                mtype_weibo = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)['hits']['hits']
                #save_ws_results(topic, end_ts, during, n_limit, mtype_weibo)    
                #微博直接保存下来
                if len(mtype_weibo) == 0:
                    continue
                first_item = mtype_weibo[0]['_source']
                #数每个地方的不同类型的数量
                for weibo in mtype_weibo:  #对于每条微博
                    try:
                        geo = weibo['_source']['geo'].encode('utf8')
                    except:
                        continue
                    #print geo,type(geo)
                    province,city = split_city(geo)
                    #print province,city

                    try:
                        geo_cityTopic_results['geo_weibos'][end_ts][v].append([end_ts,province,city,weibo])
                    except:
                        geo_cityTopic_results['geo_weibos'][end_ts][v] = [[end_ts,province,city,weibo]]

                    if province != 'unknown':
                        try:
                            province_dict[province][city] += 1  
                        except:

                            try:
                                province_dict[province][city] = 1
                              
                            except:
                                province_dict[province] = {city:1}
                               

                        try:
                            province_dict[province]['total'] += 1
                        except:

                            try:
                              
                                province_dict[province]['total'] = 1
                            except:
                            
                                province_dict[province] = {'total':1}


                        #save_ws_results(topic, end_ts, during, n_limit,province,city,weibo)
                        
                        #save_ws_results_es(topic, end_ts, during, n_limit,province,city,weibo)
                        
                        # try:
                        #     city_dict[city] += 1
                        # except:
                        #     city_dict[city] = 1
                        # try:
                        #     province_dict[province].append(city_dict)
                        # except:
                        #     province_dict[province] = []
                        #     province_dict[province].append(city_dict)
                        # try:
                        #     province_dict[province] += 1
                        # except:
                        #     province_dict[province] = 1
                # sorted_province_dict = sorted(province_dict.items(), key=lambda x: x[0], reverse=False)[:n_limit]  #就是x[0]
                # sorted_city_dict = sorted(city_dict.items(), key=lambda x: x[0], reverse=False)[:n_limit]
                # print sorted_province_dict
                # print sorted_city_dict
                #ccount = province_dict
                # ccount['province'] = sorted_province_dict
                # ccount['city'] = sorted_city_dict
                #mtype_ccount[v] = [end_ts,ccount]   #{'message_type':[shijian,{['province':('provice':cishu),()],'city':[(city:cishu)}]}
                
                geo_cityTopic_results['geo_cityCount'][end_ts][v] = province_dict
                #print mtype_ccount
                #save_rt_results(topic, mtype_ccount, during, first_item)
                
                save_rt_results_es(topic, mtype_ccount, during, first_item)
        return geo_cityTopic_results



if __name__ == '__main__':
    #START_TS = datetime2ts('2016-07-20')
    #END_TS = datetime2ts('2016-08-20')

    START_TS = '1469763900'
    END_TS = '1470293340' 


    # topic = u'奥运会'
    # topic_id = getTopicByNameStEt(topic,START_TS,END_TS) #通过中文名得到英文名
    # topic = topic_id[0]['_source']['index_name']

    #print topic_id, START_TS, END_TS
    #xapian_search_weibo = getXapianWeiboByTopic(topic_id)   #用英文名去es查对应的表
    #print 'topic: ', topic.encode('utf8')
    #cityCronTopic(topic, xapian_search_weibo, start_ts=START_TS, over_ts=END_TS, during=Fifteenminutes)
    topic='laohu'
    cityTopic(topic, start_ts=START_TS, over_ts=END_TS, during=Fifteenminutes)
    """
    item_exist = db.session.query(CityWeibos).filter(CityWeibos.topic==topic).all()
    if item_exist:
        for item in item_exist:
            db.session.delete(item)
    db.session.commit()
    """

