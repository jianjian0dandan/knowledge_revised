# -*- coding: utf-8 -*-

import json
import csv
import os
import time
import math
import re
import heapq
from datetime import date
from datetime import datetime
from elasticsearch.helpers import scan
from get_result import uid_name_list,event_id_name
import knowledge.model
from knowledge.model import *
from knowledge.extensions import db
from knowledge.global_config import *
from knowledge.global_utils import *
from knowledge.global_utils import R_RECOMMENTATION as r,ES_CLUSTER_FLOW1 as es_cluster
from knowledge.parameter import DAY
from knowledge.time_utils import ts2datetime, datetime2ts, get_db_num

people_es_dict = ['hashtag_dict','online_pattern','topic','school_dict','domain_v3','keywords','sensitive_dict']
event_es_dict = ['geo_results','topics','keywords_list','hashtag_dict','user_results','time_results','sentiment_results']
people_normal_dict = ['importance', 'influence', 'activeness', 'sensitive']
people_tag = 'function_mark'
event_tag = 'work_tag'

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0][0]
            if elem[0] > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

def search_person_by_id(uid,user_name):#根据uid查询用户属性

    uid_list = [uid]
    result = dict()
    flag = 0
    evaluate_max = get_evaluate_max()
    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            return result
        else:
            data = item['_source']
            for k,v in data.iteritems():
                if k in people_es_dict:
                    result[k] = json.loads(v)
                elif k == people_tag:
                    flag = 1
                    work_tag = v
                    tags = work_tag.split('&')
                    tag_list = []
                    for tag in tags:
                        u,t = tag.split('_')
                        if u == user_name:
                            tag_str.append(t)
                    result[people_tag] = tag_str
                elif k in people_normal_dict:
                    result[k] = normal_index(v,evaluate_max[k])
                elif k == 'activity_geo_dict':
                    result[k] = get_people_org_track(json.loads(v))
                else:
                    if v == 'NULL':
                        result[k] = ''
                    else:
                        result[k] = v

    if flag == 0:
        result[people_tag] = []
    
    return result

def search_org_by_id(uid,user_name):#根据uid查询用户属性

    uid_list = [uid]
    result = dict()
    flag = 0
    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            return result
        else:
            data = item['_source']
            for k,v in data.iteritems():
                if k in people_es_dict:
                    result[k] = json.loads(v)
                elif k == event_tag:
                    flag = 1
                    work_tag = v
                    tags = work_tag.split('&')
                    tag_list = []
                    for tag in tags:
                        u,t = tag.split('_')
                        if u == user_name:
                            tag_str.append(t)
                    result[event_tag] = tag_str
                elif k in people_normal_dict:
                    result[k] = normal_index(v,evaluate_max[k])
                elif k == 'activity_geo_dict':
                    result[k] = get_people_org_track(json.loads(v))
                else:
                    if v == 'NULL':
                        result[k] = ''
                    else:
                        result[k] = v

    if flag == 0:
        result[event_tag] = []
        
    return result

def search_bci(uid):#获取用户的粉丝数、关注数和微博数

    uid_list = [uid]
    date = 1480176000#time.time()
    bci_date = ts2datetime(date - DAY)
    index_name = 'bci_' + ''.join(bci_date.split('-'))
    index_type = 'bci'
    user_bci_result = es_cluster.mget(index=index_name, doc_type=index_type, body={'ids':uid_list})['docs']
    if len(user_bci_result):
        return {'fansnum':'', 'statusnum':'', 'friendnum':''}
    result = {'fansnum':'', 'statusnum':'', 'friendnum':''}
    for item in user_bci_result:
        if not item['found']:
            return result
        else:
            data = item['_source']
            fansnum = data['user_fansnum']
            friendsnum = data['user_friendsnum']
            statusnum = data['origin_weibo_number']+data['retweeted_weibo_number']
    result = {'fansnum':fansnum, 'statusnum':statusnum, 'friendnum':friendsnum}
    return result

def get_interaction(uid):#获取用户的交互情况

    uidlist = [uid]
    ts = get_db_num(time.time())    
    retweet_uid = []
    search_result = es_retweet.mget(index=retweet_index_name_pre+str(ts), doc_type=retweet_index_type, body={"ids": uidlist})["docs"]
    keyword = TopkHeap(10)
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_retweet']
            data = eval(data)
            for k,v in data.iteritems():
                if uid == k:
                    continue                    
                keyword.Push((v,k))
            keyword_data = keyword.TopK()
            for item in keyword_data:
                retweet_uid.append(item[1])

    search_result = es_retweet.mget(index=be_retweet_index_name_pre+str(ts), doc_type=be_retweet_index_type, body={"ids": uidlist})["docs"]
    beretweet_uid = []
    keyword = TopkHeap(10)
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_be_retweet']
            data = eval(data)
            for k,v in data.iteritems():
                if uid == k:
                    continue
                keyword.Push((v,k))
            keyword_data = keyword.TopK()
            for item in keyword_data:
                beretweet_uid.append(item[1])
  
    search_result = es_comment.mget(index=comment_index_name_pre+str(ts), doc_type=comment_index_type, body={"ids": uidlist})["docs"]
    comment_uid = []
    keyword = TopkHeap(10)
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_comment']
            data = eval(data)
            for k,v in data.iteritems():
                if uid == k:
                    continue
                keyword.Push((v,k))
            keyword_data = keyword.TopK()
            for item in keyword_data:
                comment_uid.append(item[1])

    search_result = es_comment.mget(index=be_comment_index_name_pre+str(ts), doc_type=be_comment_index_type, body={"ids": uidlist})["docs"]
    becomment_uid = []
    keyword = TopkHeap(10)
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_be_comment']
            data = eval(data)
            for k,v in data.iteritems():
                if uid == k:
                    continue
                keyword.Push((v,k))
            keyword_data = keyword.TopK()
            for item in keyword_data:
                becomment_uid.append(item[1])

    if len(retweet_uid):
        retweet_list = uid_name_list(retweet_uid)
        if retweet_list == '-1':
            retweet_list = []
    else:
        retweet_list = []

    if len(beretweet_uid):
        beretweet_list = uid_name_list(beretweet_uid)
        if beretweet_list == '-1':
            beretweet_list = []
    else:
        beretweet_list = []

    if len(comment_uid):
        comment_list = uid_name_list(comment_uid)
        if comment_list == '-1':
            comment_list = []
    else:
        comment_list = []

    if len(becomment_uid):
        becomment_list = uid_name_list(becomment_uid)
        if becomment_list == '-1':
            becomment_list = []
    else:
        becomment_list = []

    return {'retweet':retweet_list,'beretweet':beretweet_list,'comment':comment_list,'becomment':becomment_list}

def get_people_org_track(activity_geo_dict):#根据用户地理位置计算轨迹

    results = []
    now_date_ts = datetime2ts(ts2datetime(int(time.time())))
    start_ts = now_date_ts - DAY * len(activity_geo_dict)
    #step2: iter date to get month track
    for geo_item in activity_geo_dict:
        iter_date = ts2datetime(start_ts)
        sort_day_dict = sorted(geo_item.items(), key=lambda x:x[1], reverse=True)
        if sort_day_dict:
            results.append([iter_date, sort_day_dict[0][0]])
        else:
            results.append([iter_date, ''])
        start_ts = start_ts + DAY

    geolist = []
    line_list = []
    index_city = 0
    for i in results:
        if i[1] and i[1].split('\t')[0] == u'中国':
            geolist.append(i[1])
    geolist = [i for i in set(geolist)]
    for x in range(len(results)-1):
        if results[x][1] != '' and results[x+1][1]!='' and results[x][1].split('\t')[0] == u'中国' and results[x+1][1].split('\t')[0] == u'中国':
            if results[x][1] !=  results[x+1][1]:
                line_list.append([results[x][1], results[x+1][1]])
    return {'city':geolist, 'line':line_list}

def search_event_by_id(uid,user_name):#根据uid查询事件属性

    uid_list = [uid]
    result = dict()
    flag = 0
    search_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            return result
        else:
            data = item['_source']
            for k,v in data.iteritems():
                if k in event_es_dict:
                    result[k] = json.loads(v)
                elif k == people_tag:
                    flag = 1
                    work_tag = v
                    tags = work_tag.split('&')
                    tag_list = []
                    for tag in tags:
                        u,t = tag.split('_')
                        if u == user_name:
                            tag_str.append(t)
                    result[people_tag] = tag_str
                else:
                    if v == 'NULL':
                        result[k] = ''
                    else:
                        result[k] = v

    return result

def search_neo4j_by_uid(uid,index_name,index_primary):

    p_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-(m) return m LIMIT 10' % (index_name,index_primary,uid,node_index_name,people_primary)
    p_result = graph.run(p_string)
    peo_list = []
    for item in p_result:
        id_key = dict(item[0]).values()[0]
        if id_key not in peo_list:
            peo_list.append(id_key)
        else:
            continue

    if len(peo_list):
        peo_name = uid_name_list(peo_list)
        if peo_name == '-1':
            peo_name = {}
    else:
        peo_name = {}

    p_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-(m) return m LIMIT 10' % (index_name,index_primary,uid,org_index_name,org_primary)
    p_result = graph.run(p_string)
    org_list = []
    for item in p_result:
        id_key = dict(item[0]).values()[0]
        if id_key not in org_list:
            org_list.append(id_key)
        else:
            continue

    if len(org_list):
        org_name = uid_name_list(org_list)
        if org_name == '-1':
            org_name = {}
    else:
        org_name = {}

    p_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-(m) return m LIMIT 10' % (index_name,index_primary,uid,event_index_name,event_primary)
    p_result = graph.run(p_string)
    event_list = []
    for item in p_result:
        id_key = dict(item[0]).values()[0]
        if id_key not in event_list:
            event_list.append(id_key)
        else:
            continue

    if len(event_list):
        event_name = event_id_name(event_list)
    else:
        event_name = {}

    relation_name = {'people':peo_name.values(),'org':org_name.values(),'event':event_name.values()}

    return relation_name


def search_related_docs(uid,es_host,es_name,es_type):
    
    uid_list = [uid]
    result = []
    search_result = es_host.mget(index=es_name, doc_type=es_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            return result
        else:
            data = item['_source']
            docs = data['related_docs']
            result = docs.split('+')

    return result



    
    
