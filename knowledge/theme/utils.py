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
from knowledge.index.GetUrl import getUrlByKeyWordList
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
from knowledge.global_utils import event_detail_search, user_name_search, user_detail_search
from knowledge.global_config import event_task_name, event_task_type, event_analysis_name, event_text_type
from knowledge.global_config import special_event_name, special_event_type
from knowledge.global_config import node_index_name, event_index_name, special_event_node, group_node, people_primary,\
                            event_node, event_primary, event_index_name, org_primary, people_node, org_node, event_node,\
                            relation_dict
from knowledge.parameter import DAY, WEEK, RUN_TYPE, RUN_TEST_TIME,MAX_VALUE,sensitive_score_dict
# from knowledge.cron.event_analysis.event_compute import immediate_compute
p = Pinyin()
WEEK = 7

def deal_user_tag(tag):
    # tag = es.get(index=portrait_index_name,doc_type=portrait_index_type, id=item)['_source']['function_mark']
    # print tag,'======!!=========='
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

def deal_event_tag(tag ,submit_user):
    # tag = es_event.get(index=event_analysis_name,doc_type=event_text_type, id=item)['_source']['work_tag'][0]
    # return result
    # tag = tag_value
    # print tag,'=============!!==='
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
        theme_name = theme_name + '_' + submit_user
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
        i_fields = i['fields']
        search_eid.append(i_fields['en_name'][0])
    show_id_set = set(search_eid) - set(eid_list)
    show_id = [i for i in show_id_set]
    if not show_id:
        return []
    event_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
                body={'ids':show_id}, fields=fields_list)['docs']
    for i in event_result:
        event = []
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
    print node1_list,'00990909000000000000'
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
    # print sorted_keywords
    result_label = [i[0] for i in sorted_keywords[:100]]
    result_label_string = '&'.join(result_label)
    return result_label_string

def create_node_and_rel(node_key1, node1_list, node1_index_name, rel, node_key2, \
                        node2_id, node2_index_name, submit_user, k_label, node2_name):
    Index = ManualIndexManager(graph) # manage index
    theme_index = Index.get_or_create_index(Node, node2_index_name)
    p_node2_id = p.get_pinyin(node2_id)
    p_node2_id = p_node2_id.lower()
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
        if k_label:
            k_label = '&'.join(k_label.split(','))
            theme_dict['k_label'] = k_label
        topic_id = p.get_pinyin(node2_id)
        labels = get_special_labels(node1_list)
        theme_dict['label'] = labels
        wiki_link = getUrlByKeyWordList(labels)
        theme_dict['wiki_link'] = json.dumps(wiki_link)
        # es_event.delete(index=special_event_name, doc_type=special_event_type, id='mei-guo-da-xuan-_admin@qq.com')
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

# def get_theme_all(submit_user):
#     theme_detail = es_event.search(index=special_event_name, doc_type=special_event_type,\
#             body={'query':{'term':{'user':submit_user}}})['hits']['hits']
#     theme_result = []
#     for i in theme_detail:
#         topic_id = i['_id']
#         theme_name = i['_source']['topic_name']
#         contain_event = i['_source']['event_count']
#         auto_label = i['_source']['label'].split('&')[:5]
#         try:
#             work_tag = i['_source']['k_label'].split('&')
#         # work_tag = deal_event_tag(work_tag, submit_user)[0]
#         except:
#             work_tag = []
#         submit_ts = ts2date(i['_source']['create_ts'])
#         theme_result.append([topic_id, theme_name, contain_event, auto_label, work_tag, submit_ts])
#     return theme_result

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
    try:
        theme_label_list = theme_label['fields']['k_label'][0].split('&')
    except:
        theme_label_list = []
    if operation == 'add':
        theme_label_list.extend(new_label)
    elif operation == 'del':
        theme_label_list = set(theme_label_list) - set(new_label)
    theme_label_list = [i for i in set(theme_label_list)]
    theme_label_string = '&'.join(theme_label_list)
    es_event.update(index=special_event_name,doc_type=special_event_type,id=en_name,\
            body={'doc':{'k_label':theme_label_string}})
    return True

def add_theme_file_link(theme_name, file_name,operation):
    new_label = file_name.split('+')
    en_name = p.get_pinyin(theme_name)
    print en_name
    theme_label = es_event.get(index=special_event_name, doc_type=special_event_type, id=en_name,\
            fields=['file_link'])
    print theme_label,'------------'
    try:
        theme_label_list = theme_label['fields']['file_link'][0].split('+')
    except:
        theme_label_list = []
    if operation == 'add':
        theme_label_list.extend(new_label)
    elif operation == 'del':
        theme_label_list = set(theme_label_list) - set(new_label)
    theme_label_list = [i for i in set(theme_label_list)]
    theme_label_string = '+'.join(theme_label_list)
    es_event.update(index=special_event_name,doc_type=special_event_type,id=en_name,\
            body={'doc':{'file_link':theme_label_string}})
    return True

def compare_theme(theme_name1, theme_name2, submit_user, flag):
    if flag == 'all':
        detail_result1 = query_detail_theme(theme_name1, submit_user)
        detail_result2 = query_detail_theme(theme_name2, submit_user)
        return {'detail_result1':detail_result1,'detail_result2':detail_result2}
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
        return {'detail_result1':detail_result1,'detail_result2':detail_result2}

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
    # return uid_list
    ##对于实际的人怎么处理？
    if flag == 'all':
        uid_list1 = [i for i in set(uid_list[0])]
        uid_list2 = [i for i in set(uid_list[1])]
        detail_result1 = user_detail_search(uid_list1,submit_user)
        detail_result2 = user_detail_search(uid_list2,submit_user)

    if flag == 'same':
        same_u = set(uid_list[0])&set(uid_list[1])
        same_u = [i for i in same_u]
        detail_result1 = user_detail_search(same_u,submit_user)
        detail_result2 = user_detail_search(same_u,submit_user)

    if flag == 'diff':
        diff_u1 = set(uid_list[0]) - (set(uid_list[0])&set(uid_list[1]))
        diff_u1 = [i for i in diff_u1]
        diff_u2 = set(uid_list[1]) - (set(uid_list[0])&set(uid_list[1]))
        diff_u2 = [i for i in diff_u2]
        detail_result1 = user_detail_search(diff_u1,submit_user)
        detail_result2 = user_detail_search(diff_u2,submit_user)
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
def get_theme_flow(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event'])
    event_list = eid_string['fields']['event'][0].split('&')
    query_body = {
        'query':{
            'terms':{'en_name':event_list}
            },
        "sort": [{'start_ts':'asc'}]
    }
    name_list = es_event.search(index=event_analysis_name, doc_type=event_text_type, \
                body=query_body,  fields=['name', 'en_name'])['hits']['hits']
    query_body2 = {
        'query':{"match_all":{}},
        "sort": [{'retweeted':'desc'}],
        'size':1
    }
    event_name_list = []
    for i in name_list:
        event_name_list.append(i['fields']['en_name'][0])
    print event_name_list
    result_list = []
    for i in event_name_list:
        max_retweet = es_event.search(index=i, doc_type='text', body=query_body2, \
            fields=['text', 'timestamp'])['hits']['hits']
        print max_retweet,'00000000000'
        text = max_retweet[0]['fields']['text'][0]
        t_datetime = ts2date(max_retweet[0]['fields']['timestamp'][0])
        result_list.append([i, text, t_datetime])
    return result_list


def get_theme_geo(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event'])
    event_list = eid_string['fields']['event'][0].split('&')
    event_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
                body={'ids':event_list}, fields=['geo_results', 'name'])['docs']
    city_dict = {}
    event_city = {}
    event_name_list = []
    for i in event_result:
        event_name = i['fields']['name'][0]
        event_city[event_name] = {}
        event_name_list.append(event_name)
        geo_event = json.loads(i['fields']['geo_results'][0])
        print geo_event
        for k,v in geo_event.iteritems():
            for province_k, city_v in v.iteritems():
                for city_name, city_count in city_v.iteritems():
                    if city_name == 'total' or city_name == 'unknown':
                        continue
                    try:
                        city_dict[city_name] += city_count
                    except:
                        city_dict[city_name] = city_count
                    try:
                        event_city[event_name][city_name] += city_count
                    except:
                        event_city[event_name][city_name] = city_count

    sorted_city_dict = sorted(city_dict.iteritems(), key=lambda x:x[1], reverse=True)[:10]
    top_city = [i[0] for i in sorted_city_dict]
    final_city_count = {}
    for city in event_name_list:
        final_city_count[city] = []
        for i in top_city:
            final_city_count[city].append(event_city[event_name][i])
    return {'top_city': top_city, 'event_city':final_city_count}

def get_theme_net(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event'])
    event_list = eid_string['fields']['event'][0].split('&')
    event_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
                body={'ids':event_list}, fields=['en_name', 'name'])['docs']
    event_name_dict = {}
    for i in event_result:
        event_en_name = i['fields']['en_name'][0]
        event_name = i['fields']['name'][0]
        event_name_dict[event_en_name] = event_name
    event_graph_id = []
    for i in event_list:
        a = graph.run('start n=node:'+event_index_name+'("'+event_primary+':'+str(i)+'") return id(n)')
        for j in a:
            event_graph_id.append(str(dict(j)['id(n)']))
    # print event_graph_id
    event_id_string = ','.join(event_graph_id)
    query = 'start d=node('+event_id_string+'),e=node('+event_id_string+') match (d)-[r]->(e) return d,type(r),e'
    result = graph.run(query)
    exist_relation = []
    exist_relation_string = []
    for i in result:
        # print i
        dict_i = dict(i)
        start_id = dict_i['d']['event_id']
        end_id = dict_i['e']['event_id']
        exist_relation.append([event_name_dict[start_id], relation_dict[dict_i['type(r)']], \
                    event_name_dict[end_id]])
        # print exist_relation
        relation_string = start_id+'-'+end_id
        exist_relation_string.append(relation_string)
    set_exist_relation = set(exist_relation_string)
    relation_set_count = len(list(set_exist_relation))
    node_count = len(event_list)
    total_count = node_count*(node_count-1)/2
    try:
        relation_degree = float(relation_set_count)/total_count
    except:
        relation_degree = 0
    if relation_degree <0.33:
        conclusion = u'关联度较低'
    elif relation_degree >= 0.33 and relation_degree <0.66:
        conclusion = u'关联度适中'
    elif relation_degree >= 0.66:
        conclusion = u'联系紧密'##未定义！！
    return {'relation_table':exist_relation, 'relation_count':relation_set_count,\
        'conclusion':conclusion, 'relation_degree':relation_degree}

def get_theme_keywords(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event'])
    event_list = eid_string['fields']['event'][0].split('&')
    event_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
                body={'ids':event_list}, fields=['keywords_list', 'hashtag_dict'])['docs']
    keywords_dict = {}
    hash_dict = {}
    for i in event_result:
        i_keywords = json.loads(i['fields']['keywords_list'][0])
        i_hashtag = json.loads(i['fields']['hashtag_dict'][0])
        for key in i_keywords:
            # print key,'====='
            try:
                keywords_dict[key[0]] += key[1]
            except:
                keywords_dict[key[0]] = key[1]
        for k,v in i_hashtag.iteritems():
            try:
                hash_dict[k] += v
            except:
                hash_dict[k] = v
    sorted_keywords_dict = sorted(keywords_dict.iteritems(), key=lambda x:x[1], reverse=True)[:100]
    try:
        max_keywords_value = sorted_keywords_dict[0][1]
    except:
        max_keywords_value = 1.0
    normal_keywords_list = []
    for words in sorted_keywords_dict:
        normal_keywords_list.append([words[0], float(words[1])/max_keywords_value])
    
    sorted_hash_dict = sorted(hash_dict.iteritems(), key=lambda x:x[1], reverse=True)[:100]
    try:
        max_hash_value = sorted_hash_dict[0][1]
    except:
        max_hash_value = 1.0
    normal_hash_list = []
    for words in sorted_hash_dict:
        normal_hash_list.append([words[0], float(words[1])/max_hash_value])
    return {'keywords':normal_keywords_list, 'hashtag':normal_hash_list}

def get_theme_user_rank(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event'])
    event_list = eid_string['fields']['event'][0].split('&')
    user_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
                body={'ids':event_list}, fields=['user_results','name'])['docs']
    user_influence ={}
    for i in user_result:
        event_name = i['fields']['name'][0]
        user_dict = json.loads(i['fields']['user_results'][0])
        for k,v in user_dict.iteritems():
            if user_influence.has_key(k):
                continue
            user_influence[k] = {}
            user_influence[k]['id']= k
            user_influence[k]['name']= user_name_search(k)

    for i in user_result:
        event_name = i['fields']['name'][0]
        user_dict = json.loads(i['fields']['user_results'][0])
        for k,v in user_dict.iteritems():
            try:
                user_influence[k]['related_event'].append(event_name)
            except:
                user_influence[k]['related_event'] = []
                user_influence[k]['related_event'].append(event_name)
            try:
                user_influence[k]['influ'] += v['influ']
            except:
                user_influence[k]['influ'] = v['influ']
    user_influence_list= []
    for k,v in user_influence.iteritems():
        user_influence_list.append(v)
    sorted_user_influ = sorted(user_influence_list, key=lambda x:x['influ'], reverse=True) 
    max_importance = sorted_user_influ[0]['influ']
    for i in sorted_user_influ:
        i['influ'] = float(i['influ'])/max_importance
    return sorted_user_influ

def get_theme_user_tag(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event'])
    event_list = eid_string['fields']['event'][0].split('&')
    user_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
                body={'ids':event_list}, fields=['user_results','name'])['docs']
    user_list =[]
    for i in user_result:
        event_name = i['fields']['name'][0]
        user_dict = json.loads(i['fields']['user_results'][0])
        for k,v in user_dict.iteritems():
            user_list.append(k)
    user_list_set = [i for i in set(user_list)]

    tag_result = es.mget(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'ids':user_list_set}, fields=['function_mark', 'keywords'])['docs']
    keywords_dict = {}
    mark_dict = {}
    print len(tag_result)
    for i in tag_result:
        i_keywords = json.loads(i['fields']['keywords'][0])
        try:
            i_mark = i['fields']['function_mark'][0]
        except:
            i_mark = ''
        for key in i_keywords:
            try:
                keywords_dict[key[0]] += key[1]
            except:
                keywords_dict[key[0]] = key[1]
        if i_mark:
            user_mark = deal_user_tag(i_mark)[0]
            for mark in user_mark:
                try:
                    mark_dict[mark] += 1
                except:
                    mark_dict[mark] = 1
    sorted_keywords_dict = sorted(keywords_dict.iteritems(), key=lambda x:x[1], reverse=True)[:100]
    sorted_mark_dict = sorted(mark_dict.iteritems(), key=lambda x:x[1], reverse=True)[:100]
    
    try:
        max_keywords_value = sorted_keywords_dict[0][1]
    except:
        max_keywords_value = 1.0
    normal_keywords_list = []
    for words in sorted_keywords_dict:
        normal_keywords_list.append([words[0], float(words[1])/max_keywords_value])

    try:
        max_mark_value = sorted_mark_dict[0][1]
    except:
        max_mark_value = 1.0
    normal_mark_list = []
    for words in sorted_mark_dict:
        normal_mark_list.append([words[0], float(words[1])/max_mark_value])

    return {'keywords':normal_keywords_list, 'mark':normal_mark_list}

def show_theme_file_link(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event','wiki_link', 'file_link'])
    event_list = eid_string['fields']['event'][0].split('&')
    origin_event = event_list
    try:
        file_link = eid_string['fields']['file_link'][0].split('+')
    except:
        file_link = []
    final_file = []
    for i in file_link:
        final_file.append(i.split(','))
    return final_file
        
def get_theme_related(theme_name, submit_user):
    topic_id = p.get_pinyin(theme_name)
    eid_string = es_event.get(index=special_event_name, doc_type=special_event_type, id=topic_id,  fields=['event','wiki_link', 'file_link'])
    event_list = eid_string['fields']['event'][0].split('&')
    origin_event = event_list
    try:
        file_link = eid_string['fields']['file_link'][0].split('+')
    except:
        file_link = []
    final_file = []
    for i in file_link:
        final_file.append(i.split(','))
    try:
        final_wiki = json.loads(eid_string['fields']['wiki_link'][0])
    except:
        final_wiki = []
    event_graph_id = []
    for i in event_list:
        a = graph.run('start n=node:'+event_index_name+'("'+event_primary+':'+str(i)+'") return id(n)')
        for j in a:
            event_graph_id.append(str(dict(j)['id(n)']))
    print event_graph_id
    event_id_string = ','.join(event_graph_id)
    query = 'start d=node('+event_id_string+') match (d)-[r]-(e) return labels(e), e'
    result = graph.run(query)
    node_dict = {}
    for i in result:
        dict_i = dict(i)
        node_type = dict_i['labels(e)'][0]

        if node_type == people_node:
            node_id = dict_i['e']['uid']
            try:
                node_dict['user'].append(node_id)
            except:
                node_dict['user'] = []
                node_dict['user'].append(node_id)
        elif node_type == org_node:
            node_id = dict_i['e']['org_id']
            try:
                node_dict['org'].append(node_id)
            except:
                node_dict['org'] = []
                node_dict['org'].append(node_id)

        elif node_type == event_node:
            node_id = dict_i['e']['event_id']
            if node_id in event_graph_id:
                continue
            try:
                node_dict['event'].append(node_id)
            except:
                node_dict['event'] = []
                node_dict['event'].append(node_id)
    try:
        uid_list = [i for i in set(node_dict['user'])]
        user_result = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list}, fields=['uname', 'uid'])['docs']
    except:
        user_result = []
    try:
        org_list = [i for i in set(node_dict['org'])]
        org_result = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':org_list}, fields=['uname', 'uid'])['docs']
    except:
        org_result = []
    try:
        event_list = [i for i in set(node_dict['event'])]
        event_result = es_event.mget(index=event_analysis_name,doc_type=event_text_type, body={'ids':event_list}, fields=['en_name', 'name'])['docs']
    except:
        event_result = []
    final_user = []
    for i in user_result:
        if i['found'] == True:
            if i['fields']['uname'][0] == '':
                uname_s = i['fields']['uid'][0]
            else:
                uname_s = i['fields']['uname'][0]
            final_user.append([i['fields']['uid'][0], uname_s])
        else:
            final_user.append([i['_id'],i['_id']])

    final_org = []
    for i in org_result:
        if i['found'] == True:
            if i['fields']['uname'][0] == '':
                uname_s = i['fields']['uid'][0]
            else:
                uname_s = i['fields']['uname'][0]
            final_org.append([i['fields']['uid'][0], uname_s])
        else:
            final_org.append([i['_id'],i['_id']])

    final_event = []
    for i in event_result:
        if i['_id'] in origin_event:
            continue
        if i['found'] == True:
            final_event.append([i['fields']['en_name'][0], i['fields']['name'][0]])
        else:
            final_event.append([i['_id'],i['_id']])
    # final_event2 = set(final_event) - set(origin_event)
    # final_event = [i for i in final_event2]
    return {'final_user':final_user, 'final_org':final_org, 'final_event':final_event, \
            'final_file':final_file, 'final_wiki':final_wiki}




