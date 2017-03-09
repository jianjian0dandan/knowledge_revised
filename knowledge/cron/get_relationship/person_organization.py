# -*- coding: UTF-8 -*-

import os
import time
import scws
import csv
import sys
import json
import heapq
from elasticsearch import Elasticsearch
from config import get_db_num,cut_des,or_list,interaction_count,friend,colleague,COUNT_RATE,\
                    influence_weight,importance_weight,activeness_weight,sensitive_weight,\
                    es_user_profile,es_retweet,es_comment,profile_index_name,profile_index_type,\
                    retweet_index_name_pre,retweet_index_type,be_retweet_index_name_pre,be_retweet_index_type,\
                    comment_index_name_pre,comment_index_type,be_comment_index_name_pre,be_comment_index_type

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
    search_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']
            des = data['description'].encode('utf-8')
            v_type = data['verified_type']
            if len(des) > 0:
                des_set = cut_des(des)
            else:
                des_set = set()
            user_dict[str(uid)] = {'verified_type':v_type,'description':des_set}

    return user_dict

def get_interaction_by_uid(uidlist):#根据uid查询用户的交互情况

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
                uid_str = uid + '&' + k
                uid_str2 = k + '&' + uid
                if friend_dict.has_key(uid_str):
                    friend_dict[uid_str] = friend_dict[uid_str] + int(v)
                elif friend_dict.has_key(uid_str2):
                    friend_dict[uid_str2] = friend_dict[uid_str2] + int(v)
                else:
                    friend_dict[uid_str] = int(v)
    
    return friend_dict

def get_colleague_r(uid_profile):#提取业务关联关系（人物与人物、人物与机构）

    people_list = []
    organization_list = []
    colleague_list = []
    colleague_dict = dict()
    for k,v in uid_profile.iteritems():
        if v['verified_type'] in or_list:
            organization_list.append(k)
        else:
            people_list.append(k)
        for k1,v1 in uid_profile.iteritems():            
            if k1 != k:#有重叠
                key_str = k + '&' + k1
                key_str2 = k1 + '&' + k
                if colleague_dict.has_key(key_str) or colleague_dict.has_key(key_str2):#已经判定过了
                    continue
                else:
                    if len(v['description']&v1['description']) > 0:
                        colleague_list.append([k,k1,colleague])
                    key_str = k + '&' + k1
                    colleague_dict[key_str] = 1

    return people_list,organization_list,colleague_list

def get_interaction_r(uid_interaction):#提取交互关系

    n = int(len(uid_interaction)*COUNT_RATE)
    if n < interaction_count:
        total_number = interaction_count
    else:
        total_number = n
    
    keyword = TopkHeap(total_number)
    for k,v in uid_interaction.iteritems():
        keyword.Push((v,k))

    interaction_list = []
    keyword_data = keyword.TopK()
    for item in keyword_data:
        k1,k2 = item[1].split('&')
        interaction_list.append([k1,k2,friend,item[0]])

    return interaction_list

def person_organization(people_dict,max_data):#计算人物-人物，人物-机构之间的关系
    '''
        输入数据：
        people_dict 人物属性字典，键是人物uid，值是人物对应的属性
        需要的属性：influence,importance,activeness,sensitive
        示例：
        {uid1:{'influence':influence,'importance':importance,'activeness':activeness,'sensitive':sensitive},
         uid2:{'influence':influence,'importance':importance,'activeness':activeness,'sensitive':sensitive},...}

        max_data 每个字段对应的最大值，类型是字典
        示例：{'influence':influence,'importance':importance,'activeness':activeness,'sensitive':sensitive}

        输出数据:
        node_weight 节点权重字典，键是uid，值是该节点对应的权重
        people_list 人物节点列表，存储人物uid
        organization_list 机构节点列表，存储机构uid
        colleague_list 业务关联关系列表，示例：[[uid1,uid2,'colleague'],[uid1,uid2,'colleague'],...]
        interaction_list 交互关系列表,示例：[[uid1,uid2,'friend',weight],[uid1,uid2,'friend',weight],...]
    '''
    data_keys = ['influence','importance','activeness','sensitive']

    if len(people_dict) == 0:#没有人物信息直接返回空
        return {},[],[],[],[]

    if len(max_data) == 0:#没有最大值的处理方式
        max_data = {'influence':0,'importance':0,'activeness':0,'sensitive':0}

    if len(max_data) < 4:#有的键没有
        for key in data_keys:
            if not max_data.has_key(key):
                max_data[key] = 0
        
    
    uidlist = []
    node_weight = dict()
    
    for k,v in people_dict.iteritems():
        if k not in uidlist:
            uidlist.append(k)
        else:
            continue
        weight = float(0)
        if max_data['influence'] > 0:
            weight = weight + (float(v['influence'])/float(max_data['influence'])*100)*influence_weight
        else:
            weight = weight + 0

        if max_data['importance'] > 0:
            weight = weight + (float(v['importance'])/float(max_data['importance'])*100)*influence_weight
        else:
            weight = weight + 0

        if max_data['activeness'] > 0:
            weight = weight + (float(v['activeness'])/float(max_data['activeness'])*100)*influence_weight
        else:
            weight = weight + 0

        if max_data['sensitive'] > 0:
            weight = weight + (float(v['sensitive'])/float(max_data['sensitive'])*100)*influence_weight
        else:
            weight = weight + 0

        node_weight[k] = weight
    
    uid_profile = get_profile_by_uid(uidlist)
    people_list,organization_list,colleague_list = get_colleague_r(uid_profile)
    uid_interaction = get_interaction_by_uid(uidlist)
    interaction_list = get_interaction_r(uid_interaction)

    return node_weight,people_list,organization_list,colleague_list,interaction_list
    
if __name__ == '__main__':
    people_dict = {'3223562613':{'influence':0,'importance':37.714825735460565,'activeness':0.9760479129604838,'sensitive':0},\
                   '2668385597':{'influence':239.14604181492643,'importance':37.92910857314217,'activeness': 3.8413448092288176,'sensitive':0},\
                   '1875189917':{'influence':35.14293596094034,'importance': 75.00237282450387,'activeness':3.069333012116046,'sensitive':1},\
                   '1743112547':{'influence':748.9551196012842,'importance':39.0233041893824,'activeness':2.0765276967147064,'sensitive':0}}
    max_data = {'influence':748.9551196012842,'importance':75.00237282450387,'activeness':3.8413448092288176,'sensitive':1}
    node_weight,people_list,organization_list,colleague_list,interaction_list = person_organization(people_dict,max_data)

    print node_weight
