# -*- coding: UTF-8 -*-

import os
import time
import scws
import csv
import sys
import json
from elasticsearch import Elasticsearch
from config import contain,re_cut,SW,black_word,cx_dict,N_GRAM,WORD_N,TOPIC_N,event_type_dict,\
                     type_weight,weibo_weight,people_weight
from topic_rank import get_topic_word,get_graph,get_final_result

def list2dict(data):

    data_item = data[0]
    item_dict = dict()
    for k,v in data_item:
        item_dict[k] = v

    return item_dict

def use_topicrank(text_list,tr_list,n_gram,word_n,topic_n):

    result = get_topic_word(text_list,topic_n)
    document_dis = list2dict(result[1])
    word_list = []
    for item in result[0]:#计算每个话题下的关键词
        topic_id = item[0]
        word_dis = item[1]
        try:
            d_weight = document_dis[topic_id]
        except KeyError:
            d_weight = 0#需要在确定
        if d_weight == 0:                        
            continue
        sort_word = get_graph(tr_list,n_gram,word_dis)
        for w1,w2 in sort_word:
            word_list.append([w1,w2*d_weight])#结果乘上该话题的概率
    keyword = get_final_result(word_list)

    wordlist = []
    for i in range(0,len(keyword)):
        if keyword[i][1] not in wordlist:
            wordlist.append(keyword[i][1])
            if len(wordlist) >= word_n:
                break

    return set(wordlist)

def get_keyword(weibo_text):#事件关键词提取

    tr_list = []
    text_list = []
    for text in weibo_text:
        w_text = re_cut(text)
        if not len(w_text):
            continue
        words = SW.participle(w_text)
        word_list = []
        for word in words:
            if word[0] not in black_word and word[1] in cx_dict and len(word[0])>3:
                word_list.append(word[0])
                text_list.append(word[0])
        tr_list.append(word_list)

    keywords = use_topicrank([text_list],tr_list,N_GRAM,WORD_N,TOPIC_N)

    return keywords

def get_keywords_relationship(event_keywords):

    contain_list = []
    contain_dict = dict()
    for k,v in event_keywords.iteritems():
        for k1,v1 in event_keywords.iteritems():
            if k1 != k:#有重叠
                key_str = k + '&' + k1
                key_str2 = k1 + '&' + k
                if contain_dict.has_key(key_str) or contain_dict.has_key(key_str2):#已经判定过了
                    continue
                else:
                    if len(v&v1) > 0:
                        contain_list.append([k,k1,contain])
                    key_str = k + '&' + k1
                    contain_dict[key_str] = 1

    return contain_list

def event_input(event_dict,max_data):
    '''
        输入数据：
        event_dict 事件属性字典
        键是事件关键词或者区分事件的东西，值是事件的属性，包括微博文本、事件类型、微博数、参与人数
        示例：
        {event1:{'text':[text1,text2,...],'type':type,'weibo':weibo,'people':people},
        event2:{'text':[text1,text2,...],'type':type,'weibo':weibo,'people':people},...}

        max_data 事件属性对应的最大值，字典类型，示例：{'weibo':max_weibo,'people':max_people}

        输出数据：
        event_dis 事件描述和权重字典
        示例：
        {event1:{'dis':string,'weight':weight},event2:{'dis':string,'weight':weight},...}

        contain_list 事件关系列表
        示例：[[event1,event2,'contain'],[event1,event2,'contain'],...]
    '''
    data_keys = ['weibo','people']

    if len(event_dict) == 0:
        return {},[]

    if len(max_data) == 0:#没有最大值的处理方式
        max_data = {'weibo':0,'people':0}

    if len(max_data) < 2:#有的键没有
        for key in data_keys:
            if not max_data.has_key(key):
                max_data[key] = 0
    
    event_keywords = dict()
    event_dis = dict()
    for k,v in event_dict.iteritems():
        if not v.has_key('text'):#没有文本
            keywords = set()
        elif len(v['text']) == 0:#没有文本
            keywords = set()
        else:
            keywords = get_keyword(v['text'])#提取关键词
        event_keywords[k] = keywords

        row = dict()
        row['des'] = '&'.join(list(keywords)[0:10])
        weight = float(0)
        if not v.has_key('type'):
            weight = weight + 0
        elif event_type_dict.has_key(v['type']):
            weight = weight + event_type_dict[v['type']]*type_weight
        else:
            weight = weight + 0

        if not v.has_key('weibo'):
            weight = weight + 0
        elif max_data['weibo'] > 0:
            weight = weight + (float(v['weibo'])/float(max_data['weibo'])*4)*weibo_weight
        else:
            weight = weight + 0

        if not v.has_key('people'):
            weight = weight + 0
        elif max_data['people'] > 0:
            weight = weight + (float(v['people'])/float(max_data['people'])*4)*people_weight
        else:
            weight = weight + 0

        row['weight'] = weight
        event_dis[k] = row
        

    contain_list = get_keywords_relationship(event_keywords)#根据关键词判定事件之间的关系

    return event_dis,contain_list

if __name__ == '__main__':
    event_dict = {'111':{'text':['新苏联慢慢浮出水面，二代要完成一代未尽之事//@阑夕:制度自信[偷笑]','马书记啊，你还坚守阵地啊，盈利多少了华信'],'type':'rights','weibo':2,'people':10},\
                   '222':{'text':['福建南平浦城人，与叶选宁叶飞无关','真真切切时能力之外的资本等于零','很多人在妄猜其家族身份渊源，但忽视最重要的华信能源的业务核心，很多事国家没法以国家名义去做，会被西方国家以安全为由阻止，只能他这种企业做，比如在欧洲法国、西班牙等国家拥有与石油炼化、销售终端系统相配套的百万吨级石油储运系统。依托欧洲终端，重点获取中亚、中东、非洲地区上游资源'],'type':'diplomacy','weibo':5,'people':100}}
    max_data = {'weibo':100,'people':1000}
    event_dis,contain_list = event_input(event_dict,max_data)

    print event_dis,    
