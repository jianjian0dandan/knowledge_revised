# -*- coding: UTF-8 -*-

import os
import time
import scws
import csv
import sys
import json
import heapq
from config import *
sys.path.append('../manage_neo4j/')
from neo4j_relation import *

def search_es_by_name(dict_name,dict_value,s_uid,type_list):#根据对应的属性查询es_user_portrait

    result_uid = []
    query_body = {
        "query":{
            "bool":{
                "should":[{"term":{dict_name:dict_value}}],
                "minimum_should_match": 1
            }
        },
        "size":2000
    }
    search_results = es_user_portrait.search(index=remote_portrait_name, doc_type=portrait_type, body=query_body)['hits']['hits']
    n = len(search_results)
    if n > 0:
        for item in search_results:
            uid = item['_id'].encode('utf-8')
            if uid == s_uid:
                continue
            else:
                data = item['_source']
                if data['verified_type'] in type_list:
                    result_uid.append(uid)

    return result_uid

def search_bci(dict_name,max_influenc,min_influence,s_uid,type_list):#根据对应的属性查询es_bci

    result_uid = []
    query_body = {
        "query":{
            "bool":{
                "must":[{"range":{dict_name:{"from":max_influenc,"to":min_influence}}}],
            }
        },
        "size":2000
    }
    search_results = es_bci.search(index=bci_day_pre+TIME_STR, doc_type=bci_day_type, body=query_body)['hits']['hits']
    n = len(search_results)
    if n > 0:
        for item in search_results:
            uid = item['_id'].encode('utf-8')
            if uid == s_uid:
                continue
            else:
                result_uid.append(uid)

    r_list = []
    search_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids": result_uid})["docs"]#判断哪些是人物，哪些是机构
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']
            if data['verified_type'] in type_list:
                r_list.append(uid)

    return r_list

def get_interaction_by_uid(uidlist):#根据uid查询用户的交互情况

    s_uid = uidlist[-1]
    ts = get_db_num(time.time())    
    ori_list = set()
    other_dict = dict()
    search_result = es_retweet.mget(index=retweet_index_name_pre+str(ts), doc_type=retweet_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_retweet']
            data = eval(data)
            if uid == s_uid:
                ori_list = ori_list|set(data.keys())
            else:
                if other_dict.has_key(uid):
                    other_dict[uid].extend(data.keys())
                else:
                    other_dict[uid] = data.keys()

    search_result = es_retweet.mget(index=be_retweet_index_name_pre+str(ts), doc_type=be_retweet_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_be_retweet']
            data = eval(data)
            if uid == s_uid:
                ori_list = ori_list|set(data.keys())
            else:
                if other_dict.has_key(uid):
                    other_dict[uid].extend(data.keys())
                else:
                    other_dict[uid] = data.keys()
  
    search_result = es_comment.mget(index=comment_index_name_pre+str(ts), doc_type=comment_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_comment']
            data = eval(data)
            if uid == s_uid:
                ori_list = ori_list|set(data.keys())
            else:
                if other_dict.has_key(uid):
                    other_dict[uid].extend(data.keys())
                else:
                    other_dict[uid] = data.keys()

    search_result = es_comment.mget(index=be_comment_index_name_pre+str(ts), doc_type=be_comment_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_be_comment']
            data = eval(data)
            if uid == s_uid:
                ori_list = ori_list|set(data.keys())
            else:
                if other_dict.has_key(uid):
                    other_dict[uid].extend(data.keys())
                else:
                    other_dict[uid] = data.keys()

    result = []
    for k,v in other_dict.iteritems():
        union_set = set(v)&set(ori_list)
        if float(len(union_set))/float(len(ori_list)) >= person_sta:
            result.append(k)
    
    return result

def scan_event_node(uidlist):#从事件中获取共同参与的用户

    s_uid = uidlist[-1]
    event_result = dict()
    s_re = scan(es_event, query={'query':{'match_all':{}}}, index=event_analysis_name, doc_type=event_text_type)
    while True:
        try:
            scan_re = s_re.next()['_source']
            data = eval(scan_re['user_results']).keys()
            union_set = set(data)&set(uidlist)
            if len(union_set) > 0:
                for u in union_set:
                    if event_result.has_key(u):
                        event_result[u].append(scan_re['en_name'])
                    else:
                        event_result[u] = [scan_re['en_name']]
            else:
                pass
        except StopIteration:
            print 'ALL done'
            break

    try:
        s_event = event_result[s_uid]
    except KeyError:
        return []

    result = []
    for k,v in event_result.iteritems():
        if k != s_uid:
            if float(len(set(v)&set(s_event)))/eve_sta:
                result.append(k)

    return result
    

def people_similarity(node_dict):
    '''
        人物相似度计算主函数
        输入数据：
        node_dict 节点属性字典（一个节点），没有该属性对应的值写空（''）
        示例:{'uid':uid,'domain':domain,'location':location,'activity_ip':activity_ip,'verified_type':type}
        
        输出数据：
        similarity_list 与该用户相似的用户
    '''

    if len(node_dict) < 5:
        return []

    try:
        s_uid = node_dict['uid']
        if not s_uid:
            return []
    except KeyError:
        return []

    try:
        node_type = node_dict['verified_type']        
    except KeyError:
        return []
    
    if node_type in org_list:#人物节点
        type_list = org_list
    else:#机构节点
        type_list = peo_list

    try:
        domain = node_dict['domain']
        if not domain:#查找domain相同的用户
            domain_uid = search_es_by_name('domain',domain,s_uid,type_list)
        else:
            domain_uid = []
    except KeyError:
        domain_uid = []
        
    try:
        location = node_dict['location']
        if not location:#查找location相同的用户
            location_uid = search_es_by_name('location',location,s_uid,type_list)
        else:
            location_uid = []
    except KeyError:
        location_uid = []

    try:
        activity_ip = node_dict['activity_ip']
        if not activity_ip:#查找activity_ip相同的用户
            activity_ip_uid = search_es_by_name('activity_ip',activity_ip,s_uid,type_list)
        else:
            activity_ip_uid = []
    except KeyError:
        activity_ip_uid = []
        
    search_result = es_bci.mget(index=bci_day_pre+TIME_STR, doc_type=bci_day_type, body={"ids": [s_uid]})["docs"]
    if len(search_result) == 0:
        influence_uid = []
    else:
        for item in search_result:
            uid = item['_id']
            if not item['found']:
                influence = ''
            else:
                data = item['_source']
                influence = data['user_index']

        if not influence:#查找影响力在一定范围内的用户
            max_influence = influence*MAX_I
            min_influence = influence*MIN_I
            influence_uid = search_bci('user_index',max_influenc,min_influence,s_uid,type_list)
        else:
            influence_uid = []

    total_uid = ((set(domain_uid)|set(location_uid))|set(activity_ip_uid))|set(influence_uid)#求uid的并集

    i_list = get_interaction_by_uid(list(total_uid))
    e_list = scan_event_node(list(total_uid))

    whole_result = domain_uid
    whole_result.extend(location_uid)
    whole_result.extend(activity_ip_uid)
    whole_result.extend(influence_uid)
    whole_result.extend(i_list)
    whole_result.extend(e_list)

    result_dict = dict()
    similarity = []
    for u in whole_result:
        try:
            result_dict[u] = result_dict[u] + 1
        except KeyError:
            result_dict[u] = 1

    for k,v in result_dict.iteritems():
        if v >= com_sta:
            similarity.appeend(k)

    return similarity

def search_event_es(dict_name,dict_value,s_uid):#根据对应的属性查询es_event

    result_uid = []
    if dict_name == 'keywords':
        words = keywords.split('&')
        w_list = []
        for w in words:
            w_list.append({"term":{"keywords":w}})
        n = int(len(words)*0.5)

        query_body = {
            "query":{
                "bool":{
                    "should":w_list,
                    "minimum_should_match": n
                }
            },
            "size":2000
        }
    else:
        query_body = {
            "query":{
                "bool":{
                    "should":[{"term":{dict_name:dict_value}}],
                    "minimum_should_match": 1
                }
            },
            "size":2000
        }
    search_results = es_event.search(index=event_analysis_name, doc_type=event_text_type, body=query_body)['hits']['hits']
    n = len(search_results)
    if n > 0:
        for item in search_results:
            uid = item['_id'].encode('utf-8')
            if uid == s_uid:
                continue
            else:
                result_uid.append(uid)

    return result_uid

def search_event_people(uid_result,s_uid):#根据对应的人物查找相似事件

    result = []
    s_re = scan(es_event, query={'query':{'match_all':{}}}, index=event_analysis_name, doc_type=event_text_type)
    while True:
        try:
            scan_re = s_re.next()['_source']
            id_str = scan_re["en_name"]+'-'+scan_re["submit_ts"]
            if id_str == s_uid:
                continue
            data = eval(scan_re['user_results']).keys()
            union_set = set(data)&set(uid_result.keys())
            if len(union_set) > 0:
                result.append(id_str)
            else:
                pass
        except StopIteration:
            print 'ALL done'
            break

    return result

def event_similarity(node_dict):
    '''
        事件相似度计算主函数
        输入数据：
        e_dict 节点属性字典（一个节点），没有该属性对应的值写空（''）
        示例:{'event_id':uid,'type':type,'location':location,'keyword':keyword,'user_results':user_results}
        keyword是以"&"连接的字符串
        user_results是一个字典（按照事件es里面的格式）
        
        输出数据：
        similarity_list 与该事件相似的事件
    '''

    if len(node_dict) < 5:
        return []

    try:
        s_uid = node_dict['event_id']
        if not s_uid:
            return []
    except KeyError:
        return []

    try:
        e_type = node_dict['type']
        if not e_type:#查找type相同的用户
            type_uid = search_event_es('category',e_type,s_uid)
        else:
            type_uid = []
    except KeyError:
        type_uid = []
        
    try:
        location = node_dict['location']
        if not location:#查找location相同的用户
            location_uid = search_event_es('real_geo',location,s_uid)
        else:
            location_uid = []
    except KeyError:
        location_uid = []

    try:
        keyword = node_dict['keyword']
        if not keyword:#查找keyword相同的用户
            keyword_uid = search_event_es('keywords',keywords,s_uid)
        else:
            keyword_uid = []
    except KeyError:
        keyword_uid = []

    try:
        user_results = node_dict['user_results']
        if not user_results:#查找user_results相同的用户
            user_results_uid = search_event_people(user_results,s_uid)
        else:
            user_results_uid = []
    except KeyError:
        user_results_uid = []

    whole_result = type_uid
    whole_result.extend(location_uid)
    whole_result.extend(keyword_uid)
    whole_result.extend(user_results_uid)

    result_dict = dict()
    similarity = []
    for u in whole_result:
        try:
            result_dict[u] = result_dict[u] + 1
        except KeyError:
            result_dict[u] = 1

    for k,v in result_dict.iteritems():
        if v >= com_sta_eve:
            similarity.appeend(k)

    return similarity

def topic_similarity(p_first,p_second,event_average):
    '''
        专题相似度计算主函数
        输入数据：
        p_first 第一个专题的属性字典
        p_second 第二个专题的属性字典
        event_average 专题间事件相似度平均值
        示例：
        {'event':{event1:weight,event2:weight,...},'people':{people1:weight,people2:weight,...}}
        
        输出数据：
        similarity 两个专题的相似度（一个0到1的数字），数字小于0.5的不在数据库里面建立相似关系
    '''

    ##共同关联的事件权重之和/关联的事件权重之和的最小值：取值[0,1]，占比0.4
    s1 = 0
    if p_first.has_key('event') and p_second.has_key('event'):
        event_first = set(p_first['event'].keys())
        event_second = set(p_second['event'].keys())
        weight = max(sum(p_first['event'].values()),sum(p_second['event'].values()))
        union_set = event_first & event_second
        if len(union_set) > 0 and weight > 0:
            total = 0
            for key in list(union_set):
                total = total + p_first['event'][key]
            s1 = float(total)/float(weight)
        else:
            s1 = 0
    else:
        s1 = 0
        
        
    ##共同关联的人物权重之和/关联的人物权重之和的最小值：取值[0,1]，占比0.3
    s2 = 0
    if p_first.has_key('people') and p_second.has_key('people'):
        event_first = set(p_first['people'].keys())
        event_second = set(p_second['people'].keys())
        weight = max(sum(p_first['people'].values()),sum(p_second['people'].values()))
        union_set = event_first & event_second
        if len(union_set) > 0 and weight > 0:
            total = 0
            for key in list(union_set):
                total = total + p_first['people'][key]
            s2 = float(total)/float(weight)
        else:
            s2 = 0
    else:
        s2 = 0

    
    similarity = s1*t1_weight + s2*t2_weight + event_average*t3_weight

    return similarity

def crowd_similarity(p_first,p_second,event_average):
    '''
        群体相似度计算主函数
        输入数据：
        p_first 第一个群体的属性字典
        p_second 第二个群体的属性字典
        event_average 群体间人物相似度平均值
        示例：
        {'event':{event1:weight,event2:weight,...},'people':{people1:weight,people2:weight,...}}
        
        输出数据：
        similarity 两个专题的相似度（一个0到1的数字），数字小于0.5的不在数据库里面建立相似关系
    '''

    ##共同关联的事件权重之和/关联的事件权重之和的最小值：取值[0,1]，占比0.4
    s1 = 0
    if p_first.has_key('event') and p_second.has_key('event'):
        event_first = set(p_first['event'].keys())
        event_second = set(p_second['event'].keys())
        weight = max(sum(p_first['event'].values()),sum(p_second['event'].values()))
        union_set = event_first & event_second
        if len(union_set) > 0 and weight > 0:
            total = 0
            for key in list(union_set):
                total = total + p_first['event'][key]
            s1 = float(total)/float(weight)
        else:
            s1 = 0
    else:
        s1 = 0
        
        
    ##共同关联的人物权重之和/关联的人物权重之和的最小值：取值[0,1]，占比0.3
    s2 = 0
    if p_first.has_key('people') and p_second.has_key('people'):
        event_first = set(p_first['people'].keys())
        event_second = set(p_second['people'].keys())
        weight = max(sum(p_first['people'].values()),sum(p_second['people'].values()))
        union_set = event_first & event_second
        if len(union_set) > 0 and weight > 0:
            total = 0
            for key in list(union_set):
                total = total + p_first['people'][key]
            s2 = float(total)/float(weight)
        else:
            s2 = 0
    else:
        s2 = 0

    
    similarity = s1*q1_weight + s2*q2_weight + event_average*q3_weight

    return similarity


if __name__ == '__main__':
    p_1 = {'domain':'草根','location':'北京','topic':'媒体&娱乐&鹿晗','hashtag':'演唱会&音乐会','label':'娱乐分子&娱乐达人',\
        'weight':89,'event':{'111':2,'222':2.5},'people':{'111':73,'222':65,'333':33}}
    p_2 = {'domain':'草根','location':'重庆','topic':'政治&习近平&鹿晗','hashtag':'演唱会&两会','label':'政治&社会主义',\
        'weight':89,'event':{'111':2,'333':1},'people':{'111':73,'444':65,'333':33}}
    e_1 = {'des':'土耳其&爆炸&大使馆','label':'政治安全',\
        'weight':4,'event':{'111':2,'222':2.5},'people':{'111':73,'222':65,'333':33}}
    e_2 = {'des':'台湾&大巴&爆炸','label':'车祸',\
        'weight':3,'event':{'111':2,'333':1},'people':{'111':73,'444':65,'333':33}}
    t_1 = {'event':{'111':2,'222':2.5},'people':{'111':73,'222':65,'333':33}}
    t_2 = {'event':{'111':2,'333':1},'people':{'111':73,'444':65,'333':33}}
    q_1 = {'event':{'111':2,'222':2.5},'people':{'111':73,'222':65,'333':33}}
    q_2 = {'event':{'111':2,'333':1},'people':{'111':73,'444':65,'333':33}}

    s = people_similarity(p_1,p_2)
    print s
    s = event_similarity(e_1,e_2)
    print s
    s = topic_similarity(t_1,t_2,0.3)
    print s
    s = crowd_similarity(q_1,q_2,0.7)
    print s
    












        
