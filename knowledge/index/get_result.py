# -*- coding: utf-8 -*-

import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from elasticsearch.helpers import scan
import knowledge.model
from knowledge.model import *
from knowledge.extensions import db
from knowledge.global_config import *
from knowledge.global_utils import *

def uid_name(uid_list,result):

    search_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']
            try:
                result[uid]['name'] = data['uname'].encode('utf-8')
            except:
                pass

    return result

def eventid_name(uid_list,result):

    search_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']
            try:
                result[uid]['name'] = data['uname'].encode('utf-8')
            except:
                pass

    return result
            
def get_people(name):

    infors = db.session.query(PeopleAttention).filter(PeopleAttention.name==name).all()
    result = dict()
    uid_list = []
    for infor in infors:
        uid = infor.peopleID
        uid_list.append(uid)
        result[uid] = {'label':infor.label,'time':infor.attentionTime,'name':''}

    if len(uid_list) > 0:
        result = uid_name(uid_list,result)
    
    return result

def get_event(name):

    infors = db.session.query(EventAttention).filter(EventAttention.name==name).all()
    result = dict()
    uid_list = []
    for infor in infors:
        uid = infor.eventID
        uid_list.append(uid)
        result[uid] = {'label':infor.label,'time':infor.attentionTime,'name':''}

    if len(uid_list) > 0:
        result = eventid_name(uid_list,result)
    
    return result

def get_org(name):

    infors = db.session.query(OrgAttention).filter(OrgAttention.name==name).all()
    result = dict()
    uid_list = []
    for infor in infors:
        uid = infor.orgID
        uid_list.append(uid)
        result[uid] = {'label':infor.label,'time':infor.attentionTime,'name':''}

    if len(uid_list) > 0:
        result = uid_name(uid_list,result)
    
    return result

def get_hot_weibo():
    
##    end_ts = time.time()
##    start_ts = 1479312000#2016-11-17  end_ts-24*3600        
##        
##    query_body = {
##        "query":{
##            "bool":{
##                "must":[{'range':{'detect_ts':{'gt':start_ts,'lt':end_ts}}}],
##            }
##        },
##        "size":10
##    }
##    search_results = es_social_sensing_text.search(index=social_sensing_index_name, doc_type=social_sensing_index_type, body=query_body)['hits']['hits']
##    n = len(search_results)
##    result = []
##    if n > 0:
##        for item in search_results:
##            mid = item['_id'].encode('utf-8')
##            data = item['_source']
##            text = data['text'].encode('utf-8')
##            uid = data['uid'].encode('utf-8')
##            ts = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(data['timestamp'])))
##            result.append({'mid':mid,'text':text,'uid':uid,'time':ts})

    return []#result    

def get_hot_people():

    return []

def get_map_count():

    location = dict()
    no_location_count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}}, index=portrait_index_name, doc_type=portrait_index_type)
    while True:
        try:
            scan_re = s_re.next()['_source']
            try:
                location = scan_re['location']
                if not location:
                    no_location_count += 1
                if len(location.split(' '))>1:
                    location = location.split(' ')[0]
                try:
                    location_result[location] += 1
                except:
                    location_result[location] = 1
            except:
                no_location_count += 1
        except StopIteration:
            print 'ALL done'
            break

    return location
    


    

