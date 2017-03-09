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

def people_similarity(p_first,p_second):
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

    ##身份、注册地是否相同：取值{0,0.5,1}，占比0.1
    s1 = 0
    if p_first.has_key('domain') and p_second.has_key('domain'):
        if p_first['domain'] == p_second['domain']:
            s1 = s1 + 0.5
        else:
            s1 = s1 + 0
    else:
        s1 = s1 + 0

    if p_first.has_key('location') and p_second.has_key('location'):
        if p_first['location'] == p_second['location']:
            s1 = s1 + 0.5
        else:
            s1 = s1 + 0
    else:
        s1 = s1 + 0

    ##话题、hashtag、业务标签的重合度：取值[0,1]，占比0.3
    s2 = 0
    if p_first.has_key('topic') and p_second.has_key('topic'):
        topic1 = set(p_first['topic'].split('&'))
        topic2 = set(p_second['topic'].split('&'))
        max_data = max(len(topic1),len(topic2))
        if max_data > 0:
            s2 = s2 + float(len(topic1 & topic2))/float(max_data)
        else:
            s2 = s2 + 0
    else:
        s2 = s2 + 0

    if p_first.has_key('hashtag') and p_second.has_key('hashtag'):
        topic1 = set(p_first['hashtag'].split('&'))
        topic2 = set(p_second['hashtag'].split('&'))
        max_data = max(len(topic1),len(topic2))
        if max_data > 0:
            s2 = s2 + float(len(topic1 & topic2))/float(max_data)
        else:
            s2 = s2 + 0
    else:
        s2 = s2 + 0

    if p_first.has_key('label') and p_second.has_key('label'):
        topic1 = set(p_first['label'].split('&'))
        topic2 = set(p_second['label'].split('&'))
        max_data = max(len(topic1),len(topic2))
        if max_data > 0:
            s2 = s2 + float(len(topic1 & topic2))/float(max_data)
        else:
            s2 = s2 + 0
    else:
        s2 = s2 + 0

    ##人物权重之差/权重最大值：取值[0,1]，占比0.2
    s3 = 0
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
        s3 = 1 - float(weight_dis)/float(max_data)
    else:
        s3 = 0

    ##共同关联的事件权重之和/关联的事件权重之和的最小值：取值[0,1]，占比0.2
    s4 = 0
    if p_first.has_key('event') and p_second.has_key('event'):
        event_first = set(p_first['event'].keys())
        event_second = set(p_second['event'].keys())
        weight = max(sum(p_first['event'].values()),sum(p_second['event'].values()))
        union_set = event_first & event_second
        if len(union_set) > 0 and weight > 0:
            total = 0
            for key in list(union_set):
                total = total + p_first['event'][key]
            s4 = float(total)/float(weight)
        else:
            s4 = 0
    else:
        s4 = 0
        
        
    ##共同关联的人物权重之和/关联的人物权重之和的最小值：取值[0,1]，占比0.2
    s5 = 0
    if p_first.has_key('people') and p_second.has_key('people'):
        event_first = set(p_first['people'].keys())
        event_second = set(p_second['people'].keys())
        weight = max(sum(p_first['people'].values()),sum(p_second['people'].values()))
        union_set = event_first & event_second
        if len(union_set) > 0 and weight > 0:
            total = 0
            for key in list(union_set):
                total = total + p_first['people'][key]
            s5 = float(total)/float(weight)
        else:
            s5 = 0
    else:
        s5 = 0

    
    similarity = s1*p1_weight + s2*p2_weight/float(3) + s3*p3_weight + s4*p4_weight + s5*p5_weight

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
    












        
