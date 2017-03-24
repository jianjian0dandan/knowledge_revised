# -*- coding: utf-8 -*-

import json
import csv
import os
import time
import math
import re
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
from knowledge.time_utils import ts2datetime, datetime2ts

def search_person_by_id(uid):#根据uid查询用户属性

    uid_list = [uid]
    result = dict()
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
                result[k] = json.dumps(v)

    return result

def search_org_by_id(uid):#根据uid查询用户属性

    uid_list = [uid]
    result = dict()
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
                result[k] = json.dumps(v)

    return result

def search_event_by_id(uid):#根据uid查询用户属性

    uid_list = [uid]
    result = dict()
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
                result[k] = json.dumps(v)

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







    
    
