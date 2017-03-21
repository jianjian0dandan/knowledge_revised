# -*- coding: UTF-8 -*-

import os
import time
import scws
import csv
import sys
import json
import heapq
from elasticsearch import Elasticsearch
from config_relation import *
#sys.path.append('../manage_neo4j/')
from neo4j_relation import *

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

def get_profile_by_uid(uidlist):#根据uid查询用户的背景信息

    user_dict = dict()
    search_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            user_dict[str(uid)] = {'verified_type':'Null','description':set()}
            continue
        else:
            data = item['_source']
            des = data['description'].encode('utf-8')
            v_type = data['verify_type']
            if len(des) > 0:
                des_set = cut_des(des)
            else:
                des_set = set()
            user_dict[str(uid)] = {'verified_type':v_type,'description':des_set}

    return user_dict

def get_interaction_by_uid(uidlist):#根据uid查询用户的交互情况

    s_uid = uidlist[0]
    ts = get_db_num(time.time())    
    friend_dict = dict()
    search_result = es_retweet.mget(index=retweet_index_name_pre+str(ts), doc_type=retweet_index_type, body={"ids": uidlist})["docs"]
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
                uid_str = uid + '&' + k
                uid_str2 = k + '&' + uid
                if friend_dict.has_key(uid_str):
                    friend_dict[uid_str] = friend_dict[uid_str] + int(v)
                elif friend_dict.has_key(uid_str2):
                    friend_dict[uid_str2] = friend_dict[uid_str2] + int(v)
                else:
                    friend_dict[uid_str] = int(v)

    search_result = es_retweet.mget(index=be_retweet_index_name_pre+str(ts), doc_type=be_retweet_index_type, body={"ids": uidlist})["docs"]
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
                uid_str = uid + '&' + k
                uid_str2 = k + '&' + uid
                if friend_dict.has_key(uid_str):
                    friend_dict[uid_str] = friend_dict[uid_str] + int(v)
                elif friend_dict.has_key(uid_str2):
                    friend_dict[uid_str2] = friend_dict[uid_str2] + int(v)
                else:
                    friend_dict[uid_str] = int(v)
  
    search_result = es_comment.mget(index=comment_index_name_pre+str(ts), doc_type=comment_index_type, body={"ids": uidlist})["docs"]
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
                uid_str = uid + '&' + k
                uid_str2 = k + '&' + uid
                if friend_dict.has_key(uid_str):
                    friend_dict[uid_str] = friend_dict[uid_str] + int(v)
                elif friend_dict.has_key(uid_str2):
                    friend_dict[uid_str2] = friend_dict[uid_str2] + int(v)
                else:
                    friend_dict[uid_str] = int(v)

    search_result = es_comment.mget(index=be_comment_index_name_pre+str(ts), doc_type=be_comment_index_type, body={"ids": uidlist})["docs"]
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
                uid_str = uid + '&' + k
                uid_str2 = k + '&' + uid
                if friend_dict.has_key(uid_str):
                    friend_dict[uid_str] = friend_dict[uid_str] + int(v)
                elif friend_dict.has_key(uid_str2):
                    friend_dict[uid_str2] = friend_dict[uid_str2] + int(v)
                else:
                    friend_dict[uid_str] = int(v)

    if not len(friend_dict):
        return [],[]

    keyword = TopkHeap(interaction_count)    
    for k,v in friend_dict.iteritems():
        if v >= inter_sta:
            keyword.Push((v,k))

    friend_list = []
    keyword_data = keyword.TopK()
    if not len(keyword_data):
        return [],[]
    
    for item in keyword_data:
        k1,k2 = item[1].split('&') 
        if k1 == s_uid:
            friend_list.append(k2)
        elif k2 == s_uid:
            friend_list.append(k1)
        else:
            continue

    profile_result = get_profile_by_uid(friend_list)
    people_list = []
    organization_list = []
    for k,v in profile_result.iteritems():
        if v['verified_type'] == 'Null':
            continue
        if v['verified_type'] in org_list:
            organization_list.append(k)
        else:
            people_list.append(k)
    
    return people_list,organization_list

def get_colleague_r(des,s_uid):#提取业务关联关系（人物与人物、人物与机构）

    people_list = []
    organization_list = []
    w_list = []

    if len(des) == 0:
        return []
    elif len(des) > 0 and len(des) <= 3:
        n = 1
    else:
        n = float(len(des))*event_sta
        n = int(n)
            
    for w in des:
        w_list.append({"term":{"description":w}})
            
    query_body = {
        "query":{
            "bool":{
                "should":w_list,
                "minimum_should_match": n
            }
        },
        "size":2000
    }
    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
    n = len(search_results)
    if n > 0:
        for item in search_results:
            uid = item['_id'].encode('utf-8')
            if uid == s_uid:
                continue
            data = item['_source']
            if data['verify_type'] in org_list:
                organization_list.append(uid)
            else:
                people_list.append(uid)

    return people_list,organization_list

def get_ip_r(uidlist,s_uid):#IP关联关系

    user_dict = dict()
    people_list = []
    search_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return []
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            user_dict[str(uid)] = {}
            continue
        else:
            data = item['_source']
            a_ip = data['activity_ip']
            h_ip = data['home_ip']
            j_ip = data['job_ip']
            user_dict[str(uid)] = {'activity_ip':a_ip,'home_ip':h_ip,'job_ip':j_ip}

    for k,v in user_dict.iteritems():
        if len(v):#有数据
            w_list = []
            for k1,v1 in v.iteritems():
                if len(v1):#不为空
                    w_list.append({"term":{k1:v1}})
                else:
                    continue
            if not len(w_list):
                return []
            query_body = {
            "query":{
                "bool":{
                    "should":w_list,
                    "minimum_should_match": 1
                }
            },
            "size":2000
            }
            search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_type, body=query_body)['hits']['hits']
            if len(search_results) > 0:
                for item in search_results:
                    uid = item['_id'].encode('utf-8')
                    if uid == s_uid:
                        continue
                    data = item['_source']
                    if data['verify_type'] not in org_list:
                        people_list.append(uid)
                    else:
                        continue
        else:
            return []

    return people_list

def person_organization(uid_list,relation_dict):#计算人物-人物，人物-机构之间的关系
    '''
        输入数据：
        uid 人物或机构
        relation_dict 关系字典

        输出数据:
        字符串提示语：
        'Empty Uid List'  数据为空
        'Partly Success'  部分成功
        'Totally Success'  节点和关系建立成功
    '''

    if len(uid_list) == 0:
        return 'Empty Uid List'#数据为空

    if len(relation_dict) == 0:
        r_flag = 1
    else:
        r_flag = 0

    count = 1
    for uid in uid_list:
        profile = get_profile_by_uid([uid])

        if r_flag == 1:#关系字典没有数据
            relation_list = [colleague,friend,ip_relation]
        else:
            try:
                relation_list = relation_dict[uid]
            except KeyError:
                relation_list = [colleague,friend,ip_relation]
        
        if len(profile[uid]['description']):
            p1,o1 = get_colleague_r(profile[uid]['description'],uid)#自述关联关系
        else:
            p1 = []
            o1 = []
        p2,o2 = get_interaction_by_uid([uid])#交互关系

        if profile[uid]['verified_type'] == 'Null':#没有数据
            p3 = get_ip_r([uid],uid)#IP关联关系
            relation_dict = {colleague:{'person':p1,'organization':o1},friend:{'person':p2,'organization':o2},ip_relation:{'people':p3}}
            flag = '-1'
        else:
            if profile[uid]['verified_type'] not in org_list:#输入的为人物
                p3 = get_ip_r([uid],uid)#IP关联关系
                relation_dict = {colleague:{'person':p1,'organization':o1},friend:{'person':p2,'organization':o2},ip_relation:{'people':p3}}
                flag = '1'
            else:
                relation_dict = {or_colleague:{'person':p1,'organization':o1},or_friend:{'person':p2,'organization':o2}}
                flag = '0'
       
        if flag == '0':#节点类型为机构
            r = create_person(org_node, org_primary, uid, org_index_name)
            if r == 'Node Wrong' or r == 'Node Type Wrong':
                continue
        
            input_list = []
            for k,v in relation_dict.iteritems():
                if k in relation_list:
                    try:
                        person_list = v['person']
                    except KeyError:
                        person_list = []

                    try:
                        organ_list = v['organization']
                    except KeyError:
                        organ_list = []

                    for p in person_list:
                        r = create_person(people_node, people_primary, p, node_index_name)
                        if r == 'Wrong' or r == 'Node Type Wrong':
                            continue
                        input_list.append([[0,uid],k,[1,p]])

                    for o in organ_list:
                        r = create_person(org_node, org_primary, o, org_index_name)
                        if r == 'Wrong' or r == 'Node Type Wrong':
                            continue
                        input_list.append([[0,uid],k,[0,o]])
                else:
                    continue
        else:
            r = create_person(people_node, people_primary, uid, node_index_name)
            if r == 'Node Wrong' or r == 'Node Type Wrong':
                continue
        
            input_list = []
            for k,v in relation_dict.iteritems():
                if k in relation_list:
                    try:
                        person_list = v['person']
                    except KeyError:
                        person_list = []

                    try:
                        organ_list = v['organization']
                    except KeyError:
                        organ_list = []

                    for p in person_list:
                        r = create_person(people_node, people_primary, p, node_index_name)
                        if r == 'Wrong' or r == 'Node Type Wrong':
                            continue
                        input_list.append([[0,uid],k,[1,p]])

                    for o in organ_list:
                        r = create_person(org_node, org_primary, o, org_index_name)
                        if r == 'Wrong' or r == 'Node Type Wrong':
                            continue
                        input_list.append([[0,uid],k,[0,o]])
                else:
                    continue

        if len(input_list) > 0:
            nodes_rels(input_list)

        count = count + 1

    if  count < len(uid_list):
        return 'Partly Success'
    else:
        return 'Totally Success'
    
    
if __name__ == '__main__':

    result = person_organization(['2117306420','5779325975'],{'2117306420':['friend','colleague'],'5779325975':['friend','colleague']})
    print result
##    relation_list = [[[0,'5779325975'],'friend',[0,'1703371307']]]
##    result = nodes_rels(relation_list)
##    print result
##    p_list = get_colleague_r(["消失","命运"])
##    print p_list
