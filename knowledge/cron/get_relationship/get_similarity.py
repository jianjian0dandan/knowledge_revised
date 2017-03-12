# -*- coding: UTF-8 -*-

import os
import time
import scws
import csv
import sys
import json
import heapq
from config import p1_weight,p2_weight,p3_weight,p4_weight,p5_weight,\
                     e1_weight,e2_weight,e3_weight,e4_weight,\
                     t1_weight,t2_weight,t3_weight,q1_weight,q2_weight,q3_weight

def search_es_by_name(dict_name,dict_value,s_uid):#根据对应的属性查询es_user_portrait

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
                result_uid.append(uid)

    return result_uid

def search_bci(dict_name,max_influenc,min_influence,s_uid):#根据对应的属性查询es_bci

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

    return result_uid

def people_similarity(s_uid):
    '''
        人物相似度计算主函数
        输入数据：
        p_first 第一个用户的属性字典
        p_second 第二个用户的属性字典
        示例：
        {'domain':domain,'location':location,'topic':topic_string,'hashtag':hashtag_string,'label':label_string,\
        'weight':weight,'event':{event1:weight,event2:weight,...},'people':{people1:weight,people2:weight,...}}

        注意：
        topic_string,hashtag_string,label_string是以"&"链接的字符串，utf-8
        
        输出数据：
        similarity 两个用户的相似度（一个0到1的数字），数字小于0.5的不在数据库里面建立相似关系
    '''

    if s_uid == '':
        return []

    ##从es中获取属性相近的用户
    search_result = es_user_portrait.mget(index=remote_portrait_name, doc_type=portrait_type, body={"ids": [s_uid]})["docs"]
    if len(search_result) == 0:#查询结果为空
        domain_uid = []
        location_uid = []
        a_ip_uid = []
    else:
        for item in search_result:
            uid = item['_id']
            if not item['found']:#未找到对应的属性
                domain = ''
                location = ''
                a_ip = ''
            else:
                data = item['_source']
                domain = data['domain']
                location = data['location']
                a_ip = data['activity_ip']
        
        if not domain:#查找domain相同的用户
            domain_uid = search_es_by_name('domain',domain,s_uid)
        else:
            domain_uid = []

        if not location:#查找location相同的用户
            location_uid = search_es_by_name('location',location,s_uid)
        else:
            location_uid = []

        if not activity_ip:#查找activity_ip相同的用户
            activity_ip_uid = search_es_by_name('activity_ip',a_ip,s_uid)
        else:
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
            influence_uid = search_bci('user_index',max_influenc,min_influence,s_uid)
        else:
            influence_uid = []

    ##从neo4j中获取有关联的用户
    

    return similarity

def event_similarity(p_first,p_second):
    '''
        事件相似度计算主函数
        输入数据：
        p_first 第一个事件的属性字典
        p_second 第二个事件的属性字典
        示例：
        {'des':des_string,'label':label_string,\
        'weight':weight,'event':{event1:weight,event2:weight,...},'people':{people1:weight,people2:weight,...}}

        注意：
        des_string,label_string是以"&"链接的字符串，utf-8
        
        输出数据：
        similarity 两个事件的相似度（一个0到1的数字），数字小于0.5的不在数据库里面建立相似关系
    '''

    ##关键词、业务标签的重合度：取值[0,1]，占比0.2
    s1 = 0
    if p_first.has_key('des') and p_second.has_key('des'):
        topic1 = set(p_first['des'].split('&'))
        topic2 = set(p_second['des'].split('&'))
        max_data = max(len(topic1),len(topic2))
        if max_data > 0:
            s1 = s1 + float(len(topic1 & topic2))/float(max_data)
        else:
            s1 = s1 + 0
    else:
        s1 = s1 + 0

    if p_first.has_key('label') and p_second.has_key('label'):
        topic1 = set(p_first['label'].split('&'))
        topic2 = set(p_second['label'].split('&'))
        max_data = max(len(topic1),len(topic2))
        if max_data > 0:
            s1 = s1 + float(len(topic1 & topic2))/float(max_data)
        else:
            s1 = s1 + 0
    else:
        s1 = s1 + 0

    ##事件权重之差/权重最大值：取值[0,1]，占比0.2
    s2 = 0
    if p_first.has_key('weight') and p_second.has_key('weight'):
        weight_dis = abs(p_first['weight'] - p_second['weight'])
        max_data = max(p_first['weight'],p_second['weight'])
    elif p_first.has_key('weight') and not p_second.has_key('weight'):
        weight_dis = p_first['weight']
        max_data = p_first['weight']
    elif not p_first.has_key('weight') and p_second.has_key('weight'):
        weight_dis = p_second['weight']
        max_data = p_second['weight']
    else:
        weight_dis = -1
        max_data = -1
        
    if max_data >= 0:
        s2 = 1 - float(weight_dis)/float(max_data)
    else:
        s2 = 0

    ##共同关联的事件权重之和/关联的事件权重之和的最小值：取值[0,1]，占比0.3
    s3 = 0
    if p_first.has_key('event') and p_second.has_key('event'):
        event_first = set(p_first['event'].keys())
        event_second = set(p_second['event'].keys())
        weight = max(sum(p_first['event'].values()),sum(p_second['event'].values()))
        union_set = event_first & event_second
        if len(union_set) > 0 and weight > 0:
            total = 0
            for key in list(union_set):
                total = total + p_first['event'][key]
            s3 = float(total)/float(weight)
        else:
            s3 = 0
    else:
        s3 = 0
        
        
    ##共同关联的人物权重之和/关联的人物权重之和的最小值：取值[0,1]，占比0.3
    s4 = 0
    if p_first.has_key('people') and p_second.has_key('people'):
        event_first = set(p_first['people'].keys())
        event_second = set(p_second['people'].keys())
        weight = max(sum(p_first['people'].values()),sum(p_second['people'].values()))
        union_set = event_first & event_second
        if len(union_set) > 0 and weight > 0:
            total = 0
            for key in list(union_set):
                total = total + p_first['people'][key]
            s4 = float(total)/float(weight)
        else:
            s4 = 0
    else:
        s4 = 0

    
    similarity = s1*e1_weight/float(2) + s2*e2_weight + s3*e3_weight + s4*e4_weight

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
    












        
