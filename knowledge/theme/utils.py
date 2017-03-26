# -*- coding: UTF-8 -*-
'''
recommentation
save uid list should be in
'''
import  os
import IP
import sys
import time
import datetime
import math
import json
import redis
import math
from xpinyin import Pinyin
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
from py2neo.ogm import GraphObject, Property
from py2neo import Node, Relationship
from elasticsearch import Elasticsearch
# from update_activeness_record import update_record_index
from knowledge.global_utils import es_event, graph, R_RECOMMENTATION as r
# from knowledge.global_utils import R_RECOMMENTATION_OUT as r_out
from knowledge.global_utils import R_CLUSTER_FLOW3 as r_cluster
from knowledge.global_utils import R_CLUSTER_FLOW2 as r_cluster2
from knowledge.global_utils import es_user_portrait as es
from knowledge.global_utils import es_recommendation_result, recommendation_index_name, recommendation_index_type
from knowledge.global_utils import es_user_profile, portrait_index_name, portrait_index_type, profile_index_name, profile_index_type
from knowledge.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from knowledge.global_utils import es_bci_history, sensitive_index_name, sensitive_index_type
from knowledge.time_utils import ts2datetime, datetime2ts, ts2date
from knowledge.global_utils import event_detail_search
from knowledge.global_config import event_task_name, event_task_type, event_analysis_name, event_text_type
from knowledge.global_config import special_event_name, special_event_type
from knowledge.global_config import node_index_name, event_index_name, special_event_node, group_node, people_primary
from knowledge.parameter import DAY, WEEK, RUN_TYPE, RUN_TEST_TIME,MAX_VALUE,sensitive_score_dict
# from knowledge.cron.event_analysis.event_compute import immediate_compute
p = Pinyin()
WEEK = 7

def deal_event_tag(tag ,submit_user):
    # tag = es_event.get(index=event_analysis_name,doc_type=event_text_type, id=item)['_source']['work_tag'][0]
    # return result
    # tag = tag_value
    print tag,'=============!!==='
    tag_list = tag.split('&')
    left_tag = []
    keep_tag = []
    for i in tag_list:
        user_tag = i.split('_')
        if user_tag[0] == submit_user:
            keep_tag.append(user_tag[1])
        else:
            left_tag.append(i)
    return [keep_tag, left_tag]

def search_related_e_card(item, submit_user, theme_name):
    if theme_name:
        theme_name_pinyin = p.get_pinyin(theme_name)
        event_list_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=theme_name_pinyin,\
                            fields=['event'])
        eid_list = []
        eid_list = event_list_string['fields']['event'][0].split('&')
    else:
        eid_list = []

    query_body = {
        "query":{
            'bool':{
                'should':[
                    {"wildcard":{'keywords':'*'+str(item.encode('utf-8'))+'*'}},            
                    {"wildcard":{'en_name':'*'+str(item.encode('utf-8'))+'*'}},            
                    {"wildcard":{'name':'*'+str(item.encode('utf-8'))+'*'}}         
                ]
            }

        },
        'size':1000
    }
    fields_list = ['en_name','name', 'event_type','real_time', 'real_geo', 'uid_counts', 'weibo_counts', 'keywords', 'work_tag']
    only_eid = []
    event_id_list = []
    u_nodes_list = {}
    e_nodes_list = {}
    event_relation =[]
    try:
        event_result = es_event.search(index=event_analysis_name, doc_type=event_text_type, \
                body=query_body, fields=['en_name'])['hits']['hits']
    except:
        return 'node does not exist'
    # print event_result
    search_eid = []
    result = []
    for i in event_result:
        event = []
        i_fields = i['fields']
        search_eid.append(i_fields['en_name'][0])
    show_id_set = set(search_eid) - set(eid_list)
    show_id = [i for i in show_id_set]
    if not show_id:
        return []
    event_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
                body={'ids':show_id}, fields=fields_list)['docs']
    for i in event_result:
        i_fields = i['fields']
        for j in fields_list:
            if not i_fields.has_key(j):
                event.append('')
                continue
            if j == 'keywords':
                keywords = i_fields[j][0].split('&')
                keywords = keywords[:5]
                event.append(keywords)
            elif j == 'work_tag':
                tag = deal_event_tag(i_fields[j][0], submit_user)[0]
                event.append(tag)
            else:
                event.append(i_fields[j][0])
        result.append(event)
    return result

def create_theme_relation(node_key1, node1_list, node1_index_name, rel, node_key2, node2_id, node2_index_name, submit_user):
    node2_id_pinyin = p.get_pinyin(node2_id)
    event_list_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=node2_id_pinyin,\
                                fields=['event'])
    eid_list = []
    eid_list = event_list_string['fields']['event'][0].split('&')
    eid_list.extend(node1_list)
    eid_list = [i for i in set(eid_list)]
    eid_string = '&'.join(eid_list)
    # print eid_string
    es_event.update(index=special_event_name,doc_type=special_event_type,id=node2_id_pinyin,\
            body={'doc':{'event':eid_string, 'event_count':len(eid_list)}})
    flag = create_rel(node_key1, node1_list, node1_index_name, rel, node_key2, node2_id_pinyin, node2_index_name, submit_user)
    return flag


def create_rel(node_key1, node1_list, node1_index_name, rel, node_key2, node2_id, node2_index_name, submit_user):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node1_index_name)
    group_index = Index.get_index(Node, node2_index_name)
    tx = graph.begin()
    for node1_id in node1_list:
        print node1_id, '----==！！！==----'
        node1 = node_index.get(node_key1, node1_id)
        node1 = node_index.get(node_key1, node1_id)[0]
        node2 = group_index.get(node_key2, node2_id)[0]
        if not (node1 and node2):
            print "node does not exist"
            return 'node does not exist'
        c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" % (
        node1_index_name, node_key1, node1_id, node2_index_name, node_key2, node2_id, rel)
        result = graph.run(c_string)
        rel_list = []
        for item in result:
            rel_list.append(item)
        if rel not in rel_list:
            rel2 = Relationship(node1, rel, node2)
            graph.create(rel2)
            print "create success"
            return 'success'
        # else:
        #     print "The current two nodes already have a relationship"
        #     return '0'
    return 'has relation'


def get_special_labels(node1_list):
    labels = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={'ids':node1_list},\
                                fields=['keywords'], _source=False)['docs']
    result_label = []
    theme_label = []
    keywords_dict = {}
    for i in labels:
        theme_label.extend(i['fields']['keywords'][0].split('&'))
    for i in set(theme_label):
        keywords_dict[i] = theme_label.count(i)
    sorted_keywords = sorted(keywords_dict.iteritems(), key=lambda x:x[1], reverse=True)
    print sorted_keywords
    result_label = [i[0] for i in sorted_keywords[:100]]
    result_label_string = '&'.join(result_label)
    return result_label_string

def create_node_and_rel(node_key1, node1_list, node1_index_name, rel, node_key2, \
                        node2_id, node2_index_name, submit_user, k_label, node2_name):
    Index = ManualIndexManager(graph) # manage index
    theme_index = Index.get_or_create_index(Node, node2_index_name)
    p_node2_id = p.get_pinyin(node2_id)
    c_string = "START end_node=node:%s(%s='%s')  RETURN end_node"\
                 % (node2_index_name, node_key2, p_node2_id)
    print c_string
    try:
        result = graph.run(c_string)
    except:
        result = []
    node_l = []
    for i in result:
        # node1_l
        node_l.append(i[0])
    if len(node_l)>0:#判断对否有该节点存在
        return 'theme already exist'
    else:
        theme_dict = {}
        theme_dict['topic_name'] = node2_name
        theme_dict['event'] = '&'.join(node1_list)
        theme_dict['event_count'] = len(node1_list)
        theme_dict['create_ts'] = int(time.time())
        theme_dict['user'] = submit_user
        theme_dict['k_label'] = k_label
        topic_id = p.get_pinyin(node2_id)
        labels = get_special_labels(node1_list)
        theme_dict['label'] = labels
        es_event.delete(index=special_event_name, doc_type=special_event_type, id='mei-guo-da-xuan-_admin@qq.com')
        es_event.index(index=special_event_name, doc_type=special_event_type, id=topic_id, body=theme_dict)
        new_theme = Node(special_event_node, event=topic_id)
        graph.create(new_theme)
        theme_index.add("event", topic_id, new_theme)
        # return 'succeed'
    info = create_rel(node_key1, node1_list, node1_index_name, rel, node_key2, topic_id, node2_index_name, submit_user)
    return info

def query_detail_theme(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    # topic_id = topic_id + '_' + submit_user
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event'])
    eid_list = eid_string['fields']['event'][0].split('&')
    result = event_detail_search(eid_list, submit_user)
    return result

# # 查找该专题下的包含事件卡片信息，事件卡片
# def event_detail_search(eid_list, submit_user):
#     fields_list = ['en_name','name', 'event_type','real_time', 'real_geo', 'uid_counts', 'weibo_counts', 'keywords', 'work_tag']
#     only_eid = []
#     event_id_list = []
#     u_nodes_list = {}
#     e_nodes_list = {}
#     event_relation =[]
#     # try:
#     event_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
#             body={'ids':eid_list}, fields=fields_list)['docs']
#     # except:
#     #     return 'node does not exist'
#     result = []
#     for i in event_result:
#         event = []
#         i_fields = i['fields']
#         print i_fields
#         for j in fields_list:
#             if not i_fields.has_key(j):
#                 event.append('')
#                 continue
#             if j == 'keywords':
#                 keywords = i_fields[j][0].split('&')
#                 keywords = keywords[:5]
#                 event.append(keywords)
#             elif j == 'work_tag':
#                 tag = deal_event_tag(i_fields[j][0], submit_user)[0]
#                 event.append(tag)
#             else:
#                 event.append(i_fields[j][0])
#         result.append(event)
#     return result

def get_theme_all(submit_user):
    theme_detail = es_event.search(index=special_event_name, doc_type=special_event_type,\
            body={'query':{'term':{'user':submit_user}}})['hits']['hits']
    theme_result = []
    for i in theme_detail:
        topic_id = i['_id']
        theme_name = i['_source']['topic_name']
        contain_event = i['_source']['event_count']
        auto_label = i['_source']['label'].split('&')[:5]
        try:
            work_tag = i['_source']['k_label'].split('&')
        # work_tag = deal_event_tag(work_tag, submit_user)[0]
        except:
            work_tag = []
        submit_ts = ts2date(i['_source']['create_ts'])
        theme_result.append([topic_id, theme_name, contain_event, auto_label, work_tag, submit_ts])
    return theme_result

def del_e_theme_rel(theme_name, event_id):
    en_name = p.get_pinyin(theme_name)
    s_string = 'START s0 = node:special_event_index(event="%s"),s3 = node:event_index(event_id="%s")\
                MATCH (s0)-[r:special_event]-(s3) DELETE r' %(en_name, event_id)
    print s_string
    graph.run(s_string)

    event_list_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=en_name,\
                            fields=['event'])
    eid_list = event_list_string['fields']['event'][0].split('&')
    new_eid_list = set(eid_list) - set([event_id])
    new_eid_list = [i for i in new_eid_list]
    eid_string = '&'.join(new_eid_list)
    if len(new_eid_list) == 0:
        s_string = 'START s0 = node:special_event_index(event="%s") DELETE s0' %(en_name)
        graph.run(s_string)
        es_event.delete(index=special_event_name, doc_type=special_event_type, id=en_name)
    else:
        es_event.update(index=special_event_name,doc_type=special_event_type,id=en_name,\
            body={'doc':{'event':eid_string, 'event_count':len(new_eid_list)}}) 
    return 'true'

def add_theme_k_label(theme_name, k_label,operation):
    new_label = k_label.split('&')
    en_name = p.get_pinyin(theme_name)
    print en_name
    theme_label = es_event.get(index=special_event_name, doc_type=special_event_type, id=en_name,\
            fields=['k_label'])
    print theme_label,'------------'
    # try:
    theme_label_list = theme_label['fields']['k_label'][0].split('&')
    # except:
    #     theme_label_list = []
    if operation == 'add':
        theme_label_list.extend(new_label)
    elif operation == 'del':
        theme_label_list = set(theme_label_list) - set(new_label)
    theme_label_list = [i for i in set(theme_label_list)]
    theme_label_string = '&'.join(theme_label_list)
    es_event.update(index=special_event_name,doc_type=special_event_type,id=en_name,\
            body={'doc':{'k_label':theme_label_string}})
    return True

def compare_theme(theme_name1, theme_name2, submit_user, flag):
    if flag == 'all':
        theme1 = query_detail_theme(theme_name1, submit_user)
        theme2 = query_detail_theme(theme_name2, submit_user)
        return [theme1, theme2]
    else:
        topic_id1 = p.get_pinyin(theme_name1)
        eid_string1 = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id1,  fields=['event'])
        event_list1 = eid_string1['fields']['event'][0].split('&')
        topic_id2 = p.get_pinyin(theme_name2)
        eid_string2 = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id2,  fields=['event'])
        event_list2 = eid_string2['fields']['event'][0].split('&')
        if flag == 'same':
            same_e = set(event_list1)&set(event_list2)
            same_e = [i for i in same_e]
            detail_result1 = event_detail_search(same_e,submit_user)
            detail_result2 = event_detail_search(same_e,submit_user)
        if flag == 'diff':
            diff_e1 = set(event_list1) - (set(event_list1)&set(event_list2))
            diff_e1 = [i for i in diff_e1]
            diff_e2 = set(event_list2) - (set(event_list1)&set(event_list2))
            diff_e2 = [i for i in diff_e2]
            detail_result1 = event_detail_search(diff_e1,submit_user)
            detail_result2 = event_detail_search(diff_e2,submit_user)
        return [detail_result1, detail_result2]

def compare_theme_user(theme_name1, theme_name2, submit_user, flag):
    topic_id1 = p.get_pinyin(theme_name1)
    eid_string1 = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id1,  fields=['event'])
    event_list1 = eid_string1['fields']['event'][0].split('&')
    
    topic_id2 = p.get_pinyin(theme_name2)
    eid_string2 = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id2,  fields=['event'])
    event_list2 = eid_string2['fields']['event'][0].split('&')
    
    event_list_all = [event_list1, event_list2]
    uid_list = []
    for event_result in event_list_all:
        uid_list1 = []
        print event_result
        for event in event_result:
            event_value = event
            # event_list.append(event_value)
            c_string = 'START s0 = node:event_index(event_id="'+str(event_value)+'") '
            c_string += 'MATCH (s0)-[r]-(s1:User) return s1 LIMIT 50'
            print c_string
            result = graph.run(c_string)
            for i in list(result):
                end_id = dict(i['s1'])
                uid_list1.append(end_id['uid'])
        uid_list.append(uid_list1)
    return uid_list
    ##对于实际的人怎么处理？
    if flag == 'all':
        uid_list1 = [i for i in set(uid_list1)]
        uid_list2 = [i for i in set(uid_list2)]
        detail_result1 = related_user_search(uid_list1,submit_user)
        detail_result2 = related_user_search(uid_list2,submit_user)

    if flag == 'same':
        same_u = set(uid_list1)&set(uid_list2)
        same_u = [i for i in same_u]
        detail_result1 = related_user_search(same_u,submit_user)
        detail_result2 = related_user_search(same_u,submit_user)

    if flag == 'diff':
        diff_u1 = set(uid_list1) - (set(uid_list1)&set(uid_list2))
        diff_u1 = [i for i in diff_u1]
        diff_u2 = set(uid_list2) - (set(uid_list1)&set(uid_list2))
        diff_u2 = [i for i in diff_u2]
        detail_result1 = related_user_search(diff_u1,submit_user)
        detail_result2 = related_user_search(diff_u2,submit_user)
    return {'detail_result1':detail_result1,'detail_result2':detail_result2}

def compare_theme_keywords(theme_name1, theme_name2, submit_user, flag):
    topic_id1 = p.get_pinyin(theme_name1)
    eid_string1 = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id1,  fields=['label'])
    label_list1 = eid_string1['fields']['label'][0].split('&')
    
    topic_id2 = p.get_pinyin(theme_name2)
    eid_string2 = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id2,  fields=['label'])
    label_list2 = eid_string2['fields']['label'][0].split('&')
    if flag == 'all':
        new_label_list1 = [i for i in set(label_list1)]
        new_label_list2 = [i for i in set(label_list2)]

    if flag == 'same':
        same_u = set(label_list1)&set(label_list2)
        same_u = [i for i in same_u]
        new_label_list1 = same_u
        new_label_list2 = same_u

    if flag == 'diff':
        diff_u1 = set(label_list1) - (set(label_list1)&set(label_list2))
        new_label_list1 = [i for i in diff_u1]

        diff_u2 = set(label_list2) - (set(label_list1)&set(label_list2))
        new_label_list2 = [i for i in diff_u2]

    return [new_label_list1, new_label_list2]

def compare_theme_k_label(theme_name1, theme_name2, submit_user, flag):
    topic_id1 = p.get_pinyin(theme_name1)
    eid_string1 = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id1,  fields=['k_label'])
    label_list1 = eid_string1['fields']['k_label'][0].split('&')
    
    topic_id2 = p.get_pinyin(theme_name2)
    eid_string2 = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id2,  fields=['k_label'])
    label_list2 = eid_string2['fields']['k_label'][0].split('&')
    if flag == 'all':
        new_label_list1 = [i for i in set(label_list1)]
        new_label_list2 = [i for i in set(label_list2)]

    if flag == 'same':
        same_u = set(label_list1)&set(label_list2)
        same_u = [i for i in same_u]
        new_label_list1 = same_u
        new_label_list2 = same_u

    if flag == 'diff':
        diff_u1 = set(label_list1) - (set(label_list1)&set(label_list2))
        new_label_list1 = [i for i in diff_u1]

        diff_u2 = set(label_list2) - (set(label_list1)&set(label_list2))
        new_label_list2 = [i for i in diff_u2]

    return [new_label_list1, new_label_list2]

def search_related_event(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event'])
    event_list = eid_string['fields']['event'][0].split('&')
    related_list = []
    for en_name in event_list:
        s_string = 'START s0 = node:event_index(event_id="%s") \
                MATCH (s0)-[r]-(s3:Event) return s3' %(en_name)
        print s_string
        result = graph.run(s_string)
        for item in result:
            item_dict = dict(item)
            related_list.append(item_dict['s3']['event_id'])
    related_list = set(related_list) - set(event_list)
    related_list = [i for i in related_list]
    result = event_detail_search(related_list, submit_user)
    return result

# def theme_analysis_basic(theme_name, submit_user):







