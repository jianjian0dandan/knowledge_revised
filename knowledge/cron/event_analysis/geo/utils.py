# -*- coding:utf-8 -*-

import IP   #引入IP，对'geo'字段进行解析
from config import MEDIA_FILE

def media_dict_init():
    f = open(MEDIA_FILE, 'r')
    media_dict = dict()
    for line in f:
        line = line.lstrip().lstrip('"').rstrip().rstrip('",')
        media, geo = line.split('":"')
        media = media.decode('gb18030')
        geo = geo.decode('gb18030')
        media_dict[media] = geo
    return media_dict

def get_dynamic_mongo(mongodb, topic, start_ts, end_ts):
    topic_collection = mongodb.news_topic
    topic_news = topic_collection.find_one({'topic':topic})
    if not topic_news:
        print 'no this topic'
        return None
    else:
        print 'exists'
        topic_news_id = topic_news['_id']
        news_collection_name = 'post_' + str(topic_news_id)
        topic_news_collection = mongodb[news_collection_name]
    return topic_news_collection

def geo2city(geo,use_split=''): #将weibo中的'geo'字段解析为地址
    try:
        province, city = geo.split(use_split)
        if province in [u'内蒙古自治区', u'黑龙江省']:
            province = province[:3]
        else:
            province = province[:2]

        city = city.strip(u'市').strip(u'区')

        geo = province + ' ' + city
    except:
        pass

    if isinstance(geo, unicode):
        geo = geo.encode('utf-8')

    if geo.split()[0] not in ['海外', '其他']:
        geo = '中国 ' + geo
    geo = '\t'.join(geo.split())

    return geo

def IP2city(geo):
    try:
        city=IP.find(str(geo))
        if city:
            city=city.encode('utf-8')
        else:
            return None
    except Exception,e:
        return None

    return city

def split_city(geo):
    geo = geo.split('&')
    if geo[0] == '中国':
        province = geo[1]
        try:
            city = geo[2]
        except:
            city = 'unknown'
    else:
        province = 'unknown'
        city = 'unknown'
    return province,city