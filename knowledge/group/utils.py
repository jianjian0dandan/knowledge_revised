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
from knowledge.global_utils import es_user_portrait as es, es_group
from knowledge.global_utils import es_recommendation_result, recommendation_index_name, recommendation_index_type
from knowledge.global_utils import es_user_profile, portrait_index_name, portrait_index_type, profile_index_name, profile_index_type
from knowledge.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from knowledge.global_utils import es_bci_history, sensitive_index_name, sensitive_index_type
from knowledge.time_utils import ts2datetime, datetime2ts, ts2date
from knowledge.global_utils import event_detail_search, user_name_search, user_detail_search
from knowledge.global_config import event_task_name, event_task_type, event_analysis_name, event_text_type
from knowledge.global_config import special_event_name, special_event_type
from knowledge.global_config import event_index_name, special_event_node, group_node, people_primary,\
                            event_node, event_primary, event_index_name, org_primary, people_node, org_node, event_node,\
                            group_name, group_type, group_index_name, group_primary, node_index_name, people_primary,\
                            group_rel, relation_dict,org_list, org_index_name
from knowledge.parameter import DAY, WEEK, RUN_TYPE, RUN_TEST_TIME,MAX_VALUE,sensitive_score_dict
# from knowledge.cron.event_analysis.event_compute import immediate_compute
p = Pinyin()
WEEK = 7


def search_user_type(uid_list):
    type_list = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, \
                body={'ids': uid_list},_source=False, fields=['id', 'verified_type'])['docs']
    user_list1 = []
    org_list1 = []
    for i in type_list:
        if i['found'] == False:
            user_list1.append(i['_id'])
        else:
            if not i['fields'].has_key('verified_type'):
                user_list1.append(i['_id'])
                continue
            verified_type = i['fields']['verified_type'][0]
            if int(verified_type) in org_list:
                org_list1.append(i['_id'])
            else:
                user_list1.append(i['_id'])
    return user_list1,org_list1

def deal_user_tag(tag ,submit_user):
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

def get_evaluate_max():
    max_result = {}
    evaluate_index = ['importance', 'influence', 'activeness', 'sensitive']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size': 1,
            'sort': [{evaluate: {'order': 'desc'}}]
            }
        try:
            result = es.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result

def search_related_u_auto(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id, fields=['people'])
    uid_list = uid_string['fields']['people'][0].split('&')
    related_list = []
    for en_name in uid_list:
        s_string = 'START s0 = node:node_index(uid="%s") \
                MATCH (s0)-[r]-(s3:User) return s3' %(en_name)
        print s_string
        result = graph.run(s_string)
        for item in result:
            item_dict = dict(item)
            related_list.append(item_dict['s3']['uid'])
    # print related_list, '---------'
    # print uid_list, '---------'
    related_list = set(related_list) - set(uid_list)
    related_list = [i for i in related_list]
    result = user_detail_search(related_list, submit_user)
    return result

def search_related_u_card(item, submit_user, g_name):
    evaluate_max = get_evaluate_max()
    if g_name:
        g_name = g_name + '_' + submit_user
        g_name_pinyin = p.get_pinyin(g_name)
        g_name_pinyin = g_name_pinyin.lower()
        user_list_string = es_group.get(index=group_name, doc_type=group_type, id=g_name_pinyin,\
                            fields=['people'])
        uid_list = []
        uid_list = user_list_string['fields']['people'][0].split('&')
        # print uid_list,'==========='
    else:
        uid_list = []

    query_body = {
        "query":{
            'bool':{
                'should':[
                    {"wildcard":{'keywords':'*'+str(item.encode('utf-8'))+'*'}},            
                    {"wildcard":{'uid':'*'+str(item.encode('utf-8'))+'*'}},            
                    {"wildcard":{'uname':'*'+str(item.encode('utf-8'))+'*'}}         
                ]
            }

        },
        'size':1000
    }
    try:
        user_result = es.search(index=portrait_index_name, doc_type=portrait_index_type, \
                body=query_body, fields=['uid'])['hits']['hits']
    except:
        return 'node does not exist'
    # print user_result
    search_uid = []
    result = []
    for i in user_result:
        i_fields = i['fields']
        search_uid.append(i_fields['uid'][0])
    show_id_set = set(search_uid) - set(uid_list)
    show_id = [i for i in show_id_set]
    if not show_id:
        return []
    fields_list = ['uid','uname', 'location','influence', 'sensitive', 'activeness', 'keywords_string', 'function_mark']
    user_result = es.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body={'ids':show_id}, fields=fields_list)['docs']
    for i in user_result:
        user = []
        i_fields = i['fields']
        for j in fields_list:
            if not i_fields.has_key(j):
                user.append('')
                continue
            if j == 'keywords':
                keywords = i_fields[j][0].split('&')
                keywords = keywords[:5]
                user.append(keywords)
            elif j == 'function_mark':
                tag = deal_user_tag(i_fields[j][0], submit_user)[0]
                user.append(tag)
            elif j in ['influence', 'sensitive', 'activeness']:
                user.append(math.log(i_fields[j][0] / (evaluate_max[j] * 9+1) + 1, 10) * 100)
            else:
                user.append(i_fields[j][0])
        result.append(user)
    return result

def get_special_labels(node1_list):
    labels = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':node1_list},\
                                fields=['keywords_string'], _source=False)['docs']
    result_label = []
    group_label = []
    keywords_dict = {}
    for i in labels:
        group_label.extend(i['fields']['keywords_string'][0].split('&'))
    for i in set(group_label):
        keywords_dict[i] = group_label.count(i)
    sorted_keywords = sorted(keywords_dict.iteritems(), key=lambda x:x[1], reverse=True)
    # print sorted_keywords
    result_label = [i[0] for i in sorted_keywords[:100]]
    result_label_string = '&'.join(result_label)
    return result_label_string

def create_node_and_rel(node_key1, node1_list, node1_index_name, rel, node_key2, \
                        node2_id, node2_index_name, submit_user, k_label, node2_name):
    Index = ManualIndexManager(graph) # manage index
    group_index = Index.get_or_create_index(Node, node2_index_name)
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
        node_l.append(i[0])
    if len(node_l)>0:#判断对否有该节点存在
        return 'group already exist'
    else:
        group_dict = {}
        group_dict['group_name'] = node2_name
        group_dict['people'] = '&'.join(node1_list)
        group_dict['people_count'] = len(node1_list)
        group_dict['create_ts'] = int(time.time())
        group_dict['user'] = submit_user
        group_dict['k_label'] = '&'.join(k_label.split(','))
        group_id = p.get_pinyin(node2_id)
        group_id = group_id.lower()
        labels = get_special_labels(node1_list)
        group_dict['label'] = labels
        wiki_link = getUrlByKeyWordList(labels)
        group_dict['wiki_link'] = json.dumps(wiki_link)
        # es_group.delete(index=group_name, doc_type=group_type, id='mei-xuan-qun-ti-_admin@qq.com')
        es_group.index(index=group_name, doc_type=group_type, id=group_id, body=group_dict)
        new_group = Node(group_node, group=group_id)
        graph.create(new_group)
        group_index.add("group", group_id, new_group)
        # return 'succeed'
    user_org = search_user_type(node1_list)
    user_id = user_org[0]
    org_id = user_org[1]
    flag = create_rel(node_key1, user_id, node1_index_name, rel, node_key2, group_id, node2_index_name, submit_user)
    node_key11 = org_primary
    node11_index_name = org_index_name
    info = create_rel(node_key1, org_id, node1_index_name, rel, node_key2, group_id, node2_index_name, submit_user)
    return info

def create_rel(node_key1, node1_list, node1_index_name, rel, node_key2, node2_id, node2_index_name, submit_user):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node1_index_name)
    group_index = Index.get_index(Node, node2_index_name)
    tx = graph.begin()
    for node1_id in node1_list:
        # print node2_id
        # print node1_id,'-----'
        # node1 = node_index.get(node_key1, node1_id)
        try:
            node1 = node_index.get(node_key1, node1_id)[0]
            # print node1, node1_id,'node1 hey2222!!'

        except:
            continue
            # print node1, node1_id,'node1 hey!!'
            return 'uid1 not exist'
        node2 = group_index.get(node_key2, node2_id)[0]
        if not (node1 and node2):
            print "node does not exist"
            return 'node does not exist'
        c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" % (
        node1_index_name, node_key1, node1_id, node2_index_name, node_key2, node2_id, rel)
        result = graph.run(c_string)
        rel_list = []
        for item in result:
            print item,'00000000000'
            rel_list.append(item)
        if rel not in rel_list:
            rel2 = Relationship(node1, rel, node2)
            graph.create(rel2)
            print "create success"
        else:
            return 'has relation'
    return '1'

def create_group_relation(node_key1, node1_list, node1_index_name, rel, node_key2, node2_id, node2_index_name, submit_user):
    node2_id_pinyin = p.get_pinyin(node2_id)
    node2_id_pinyin = node2_id_pinyin.lower()
    user_list_string = es_group.get(index=group_name, doc_type=group_type, id=node2_id_pinyin,\
                                fields=['people'])
    uid_list = []
    uid_list = user_list_string['fields']['people'][0].split('&')
    uid_list.extend(node1_list)
    uid_list = [i for i in set(uid_list)]
    eid_string = '&'.join(uid_list)
    # print eid_string
    es_group.update(index=group_name, doc_type=group_type, id=node2_id_pinyin,\
            body={'doc':{'people':eid_string, 'people_count':len(uid_list)}})
    user_org = search_user_type(uid_list)
    user_id = user_org[0]
    org_id = user_org[1]
    flag = create_rel(node_key1, user_id, node1_index_name, rel, node_key2, node2_id_pinyin, node2_index_name, submit_user)
    node_key11 = org_primary
    node11_index_name = org_index_name
    flag = create_rel(node_key11, org_id, node11_index_name, rel, node_key2, node2_id_pinyin, node2_index_name, submit_user)
    
    return flag

def del_u_group_rel(g_name, uid):
    en_name = p.get_pinyin(g_name)
    en_name = en_name.lower()
    s_string = 'START s0 = node:'+group_index_name+'('+group_primary+'="'+en_name+'"),'\
               +'s3 = node:'+node_index_name+'('+people_primary+'="'+uid+'") MATCH (s0)-[r:'+group_rel+']-(s3) DELETE r' 
    
    print s_string
    graph.run(s_string)

    user_list_string = es_group.get(index=group_name, doc_type=group_type, id=en_name, fields=['people'])
    uid_list = user_list_string['fields']['people'][0].split('&')
    new_uid_list = set(uid_list) - set([uid])
    new_uid_list = [i for i in new_uid_list]
    uid_string = '&'.join(new_uid_list)
    if len(new_uid_list) == 0:
        s_string = 'START s0 = node:'+group_index_name+'('+group_primary+'="'+en_name+'") DELETE s0' 
        graph.run(s_string)
        es_group.delete(index=group_name, doc_type=group_type, id=en_name)
    else:
        es_group.update(index=group_name,doc_type=group_type,id=en_name,\
            body={'doc':{'people':uid_string, 'people_count':len(new_uid_list)}}) 
    return '1'

def add_group_k_label(g_name, k_label,operation):
    new_label = k_label.split('&')
    en_name = p.get_pinyin(g_name)
    en_name = en_name.lower()
    print en_name
    group_label = es_group.get(index=group_name, doc_type=group_type, id=en_name,\
            fields=['k_label'])
    print group_label,'------------'
    try:
        group_label_list = group_label['fields']['k_label'][0].split('&')
    except:
        group_label_list = []
    if operation == 'add':
        group_label_list.extend(new_label)
    elif operation == 'del':
        group_label_list = set(group_label_list) - set(new_label)
    group_label_list = [i for i in set(group_label_list)]
    group_label_string = '&'.join(group_label_list)
    es_group.update(index=group_name,doc_type=group_type, id=en_name,\
            body={'doc':{'k_label':group_label_string}})
    return 1

def add_group_file_link(g_name, file_name,operation):
    new_label = file_name.split('+')
    en_name = p.get_pinyin(g_name)
    en_name = en_name.lower()
    print en_name
    group_label = es_group.get(index=group_name, doc_type=group_type, id=en_name,\
            fields=['file_link'])
    print group_label,'------------'
    try:
        group_label_list = group_label['fields']['file_link'][0].split('+')
    except:
        group_label_list = []
    if operation == 'add':
        group_label_list.extend(new_label)
    elif operation == 'del':
        group_label_list = set(group_label_list) - set(new_label)
    group_label_list = [i for i in set(group_label_list)]
    group_label_string = '+'.join(group_label_list)
    es_group.update(index=group_name,doc_type=group_type, id=en_name,\
            body={'doc':{'file_link':group_label_string}})
    return 1

def query_detail_group(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    try:
        uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people'])
    except:
        return 0
    uid_list = uid_string['fields']['people'][0].split('&')
    # result = uid_list
    result = user_detail_search(uid_list, submit_user) #后面加！！
    return result

def compare_group_user(g_name1, g_name2, submit_user, flag):
    if flag == 'all':
        detail_result1 = query_detail_group(g_name1, submit_user)
        detail_result2 = query_detail_group(g_name2, submit_user)
        return {'detail_result1':detail_result1,'detail_result2':detail_result2}
    else:
        topic_id1 = p.get_pinyin(g_name1)
        topic_id1 = topic_id1.lower()
        eid_string1 = es_group.get(index=group_name, doc_type=group_type, id=topic_id1,  fields=['people'])
        event_list1 = eid_string1['fields']['people'][0].split('&')
        topic_id2 = p.get_pinyin(g_name2)
        topic_id2 = topic_id2.lower()
        eid_string2 = es_group.get(index=group_name, doc_type=group_type, id=topic_id2,  fields=['people'])
        event_list2 = eid_string2['fields']['people'][0].split('&')
        if flag == 'same':
            same_e = set(event_list1)&set(event_list2)
            same_e = [i for i in same_e]
            detail_result1 = user_detail_search(same_e,submit_user)
            detail_result2 = user_detail_search(same_e,submit_user)
        if flag == 'diff':
            diff_e1 = set(event_list1) - (set(event_list1)&set(event_list2))
            diff_e1 = [i for i in diff_e1]
            diff_e2 = set(event_list2) - (set(event_list1)&set(event_list2))
            diff_e2 = [i for i in diff_e2]
            detail_result1 = user_detail_search(diff_e1,submit_user)
            detail_result2 = user_detail_search(diff_e2,submit_user)
        return {'detail_result1':detail_result1,'detail_result2':detail_result2}

def compare_group_event(g_name1, g_name2, submit_user, flag):
    group_id1 = p.get_pinyin(g_name1)
    group_id1 = group_id1.lower()
    uid_string1 = es_group.get(index=group_name, doc_type=group_type, id=group_id1,  fields=['people'])
    uid_list1 = uid_string1['fields']['people'][0].split('&')

    group_id2 = p.get_pinyin(g_name2)
    group_id2 = group_id2.lower()
    uid_string2 = es_group.get(index=group_name, doc_type=group_type, id=group_id2,  fields=['people'])
    uid_list2 = uid_string2['fields']['people'][0].split('&')
    
    uid_list_all = [uid_list1, uid_list2]
    event_list = []
    for user_result in uid_list_all:
        event_list1 = []
        print user_result
        for user in user_result:
            user_value = user
            c_string = 'START s0 = node:node_index(uid="'+str(user_value)+'") '
            c_string += 'MATCH (s0)-[r]-(s1:Event) return s1 LIMIT 50'
            print c_string
            result = graph.run(c_string)
            for i in list(result):
                end_id = dict(i['s1'])
                event_list1.append(end_id['event_id'])
        event_list.append(event_list1)
    if flag == 'all':
        event_list1 = [i for i in set(event_list[0])]
        event_list2 = [i for i in set(event_list[1])]
        detail_result1 = event_detail_search(event_list1,submit_user)
        detail_result2 = event_detail_search(event_list2,submit_user)

    if flag == 'same':
        same_u = set(event_list[0])&set(event_list[1])
        same_u = [i for i in same_u]
        detail_result1 = event_detail_search(same_u,submit_user)
        detail_result2 = event_detail_search(same_u,submit_user)

    if flag == 'diff':
        diff_u1 = set(event_list[0]) - (set(event_list[0])&set(event_list[1]))
        diff_u1 = [i for i in diff_u1]
        diff_u2 = set(event_list[1]) - (set(event_list[0])&set(event_list[1]))
        diff_u2 = [i for i in diff_u2]
        detail_result1 = event_detail_search(diff_u1,submit_user)
        detail_result2 = event_detail_search(diff_u2,submit_user)
    return {'detail_result1':detail_result1,'detail_result2':detail_result2}

def compare_group_keywords(g_name1, g_name2, submit_user, flag):
    topic_id1 = p.get_pinyin(g_name1)
    topic_id1 = topic_id1.lower()
    eid_string1 = es_group.get(index=group_name, doc_type=group_type, id=topic_id1,  fields=['label'])
    label_list1 = eid_string1['fields']['label'][0].split('&')
    
    topic_id2 = p.get_pinyin(g_name2)
    topic_id2 = topic_id2.lower()
    eid_string2 = es_group.get(index=group_name, doc_type=group_type, id=topic_id2,  fields=['label'])
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

    return {'detail_result1':new_label_list1,'detail_result2':new_label_list2}

def compare_group_k_label(g_name1, g_name2, submit_user, flag):
    topic_id1 = p.get_pinyin(g_name1)
    topic_id1 = topic_id1.lower()
    eid_string1 = es_group.get(index=group_name, doc_type=group_type, id=topic_id1,  fields=['k_label'])
    label_list1 = eid_string1['fields']['k_label'][0].split('&')
    
    topic_id2 = p.get_pinyin(g_name2)
    topic_id2 = topic_id2.lower()
    eid_string2 = es_group.get(index=group_name, doc_type=group_type, id=topic_id2,  fields=['k_label'])
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
    return {'detail_result1':new_label_list1,'detail_result2':new_label_list2}

def union_dict_list(objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])

    return _total

def get_vary_detail_info(vary_detail_dict, uid_list):
    results = {}
    #get uname
    try:
        user_portrait_result = es.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                            body={'ids':uid_list})['docs']
    except:
        user_portrait_result = []
    uname_dict = {}
    for portrait_item in user_portrait_result:
        uid = portrait_item['_id']
        if portrait_item['found']==True:
            uname = portrait_item['_source']['uname']
            uname_dict[uid] = uname
        else:
            uname_dict[uid] = uid

    #get new vary detail information
    for vary_pattern in vary_detail_dict:
        user_info_list = vary_detail_dict[vary_pattern]
        new_pattern_list = []
        for user_item in user_info_list:
            uid = user_item[0]
            uname= uname_dict[uid]
            start_date = ts2datetime(int(user_item[1]))
            end_date = ts2datetime(int(user_item[2]))
            new_pattern_list.append([uid, uname, start_date, end_date])
        results[vary_pattern] = new_pattern_list

    return results

def get_group_location(city, direction, g_name, submit_user):
    basic_info = group_map(g_name, submit_user)
    need_info = basic_info['activity_geo_vary']
    # if need_info:
    long_city = city
    short_city = city.split('\t')[-1]
    geolist = []
    line_list = []
    geolist.append(short_city)
    for k,v in need_info.iteritems():
        start_city = k.split('&')[0].split('\t')[-1]
        end_city = k.split('&')[1].split('\t')[-1]
        if direction == 'out':
            if short_city == start_city:
                geolist.append(end_city.split('\t')[-1])
                line_list.append([short_city, end_city.split('\t')[-1], v])
            else:
                continue
        elif direction == 'in':
            if short_city == end_city:
                geolist.append(start_city.split('\t')[-1])
                line_list.append([short_city, start_city.split('\t')[-1], v])
            else:
                continue
    return {'city':geolist, 'line':line_list}

def group_map(g_name, submit_user):
    result = {}
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people'])
    uid_list = uid_string['fields']['people'][0].split('&')
    source = group_geo_vary(g_name, submit_user)
    result['activity_geo_distribution_date'] = source['activity_geo_distribution_date']
    result['activity_geo_vary'] = source['activity_geo_vary']
    result['main_activity_geo'] = source['main_activity_geo']
    try:
        vary_detail_geo_dict = source['vary_detail_geo']
    except:
        vary_detail_geo_dict = {}
    if vary_detail_geo_dict != {}:
        result['vary_detail_geo'] = get_vary_detail_info(vary_detail_geo_dict, uid_list)
    else:
        result['vary_detail_geo'] = {}

    try:
        main_start_geo_dict = source['main_start_geo']
    except:
        main_start_geo_dict = {}
    result['main_start_geo'] = sorted(main_start_geo_dict.items(), key=lambda x:x[1], reverse=True)

    try:
        main_end_geo_dict = source['main_end_geo']
    except:
        main_end_geo_dict = {}
    result['main_end_geo'] = sorted(main_end_geo_dict.items(), key=lambda x:x[1], reverse=True)
    return result

def group_geo_vary(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people'])
    uid_list = uid_string['fields']['people'][0].split('&')
    activity_geo_vary={}
    main_start_geo = {}
    main_end_geo = {}
    vary_detail_geo  = {}
    activity_geo_distribution_date = {}
    if RUN_TYPE == 1:
        now_ts = int(time.time())
    else:
        now_ts = datetime2ts(RUN_TEST_TIME)
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    try: 
        iter_user_dict_list = es.mget(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'ids':uid_list})['docs']
    except:
        iter_user_dict_list = []
    for user_dict in iter_user_dict_list:
        uid = user_dict['_id']
        source = user_dict['_source']
        #attr8: activity_geo_dict---distribution by date
        user_activity_geo = {}
        activity_geo_dict_list = json.loads(source['activity_geo_dict'])
        activity_geo_date_count = len(activity_geo_dict_list)
        iter_ts = now_date_ts - activity_geo_date_count * DAY
        user_date_main_list = []
        for i in range(0, activity_geo_date_count):
            date_item = activity_geo_dict_list[i]
            if iter_ts in activity_geo_distribution_date:
                activity_geo_distribution_date[iter_ts] = union_dict_list([activity_geo_distribution_date[iter_ts], date_item])
            else:
                activity_geo_distribution_date[iter_ts] = date_item
            #use to get activity_geo vary
            sort_date_item = sorted(date_item.items(), key=lambda x:x[1], reverse=True)
            if date_item != {}:
                main_date_city = sort_date_item[0][0]
                try:
                    last_user_date_main_item = user_date_main_list[-1][0]
                except:
                    last_user_date_main_item = ''
                if main_date_city != last_user_date_main_item:
                    user_date_main_list.append([main_date_city, iter_ts])

            iter_ts += DAY
        #attr8: activity_geo_dict---location vary
        if len(user_date_main_list) > 1:
            for i in range(1, len(user_date_main_list)):
                vary_city = [geo_ts_item[0] for geo_ts_item in user_date_main_list[i-1:i+1]]
                vary_ts = [geo_ts_item[1] for geo_ts_item in user_date_main_list[i-1:i+1]]
                vary_item = '&'.join(vary_city)
                #vary_item = '&'.join(user_date_main_list[i-1:i+1])
                #get activity geo vary for vary table and map
                try:
                    activity_geo_vary[vary_item] += 1
                except:
                    activity_geo_vary[vary_item] = 1
                #get main start geo
                try:
                    main_start_geo[vary_city[0]] += 1
                except:
                    main_start_geo[vary_city[0]] = 1
                #get main end geo
                try:
                    main_end_geo[vary_city[1]] += 1
                except:
                    main_end_geo[vary_city[1]] = 1
                #get vary detail geo
                try:
                    vary_detail_geo[vary_item].append([uid, vary_ts[0], vary_ts[1]])
                except:
                    vary_detail_geo[vary_item] = [[uid, vary_ts[0], vary_ts[1]]]
    all_activity_geo = union_dict_list(activity_geo_distribution_date.values())
    sort_all_activity_geo = sorted(all_activity_geo.items(), key=lambda x:x[1], reverse=True)
    try:
        main_activity_geo = sort_all_activity_geo[0][0]
    except:
        main_activity_geo = ''


    return  {'main_start_geo':main_start_geo, 'main_end_geo': main_end_geo, \
        'vary_detail_geo': vary_detail_geo, 'activity_geo_vary':activity_geo_vary,\
        'main_activity_geo':main_activity_geo, 'activity_geo_distribution_date':activity_geo_distribution_date}

#show group user geo track
#input: uid
#output: results [geo1,geo2,..]
def get_group_user_track(uid):
    results = []
    #step1:get user_portrait activity_geo_dict
    try:
        portrait_result = es.get(index=portrait_index_name, doc_type=portrait_index_type,\
                id=uid, _source=False, fields=['activity_geo_dict'])
    except:
        portrait_result = {}
    if portrait_result == {}:
        return 'uid is not in user_portrait'
    activity_geo_dict = json.loads(portrait_result['fields']['activity_geo_dict'][0])
    now_date_ts = datetime2ts(ts2datetime(int(time.time())))
    start_ts = now_date_ts - DAY * len(activity_geo_dict)
    #step2: iter date to get month track
    for geo_item in activity_geo_dict:
        iter_date = ts2datetime(start_ts)
        sort_day_dict = sorted(geo_item.items(), key=lambda x:x[1], reverse=True)
        if sort_day_dict:
            results.append([iter_date, sort_day_dict[0][0]])
        else:
            results.append([iter_date, ''])
        start_ts = start_ts + DAY
    # results= [['2017-03-31', ''], ['2017-04-01', u'\u4e2d\u56fd\t\u56db\u5ddd\t2\u6210\u90fd'], ['2017-04-02', u'\u4e2d\u56fd\t\u56db\u5ddd\t3\u6210\u90fd'], ['2017-04-03', u'\u4e2d\u56fd\t\u56db\u5ddd\t7\u6210\u90fd'], ['2017-04-04', u'\u4e2d\u56fd\t\u56db\u5ddd\t\u6210\u90fd'], ['2017-04-05', u'\u4e2d\u56fd\t\u56db\u5ddd\t\u6210\u90fd'], ['2017-04-06', u'\u4e2d\u56fd\t\u56db\u5ddd\t\u6210\u90fd']]
    geolist = []
    line_list = []
    index_city = 0
    for i in results:
        if i[1] and i[1].split('\t')[0] == u'中国':
            geolist.append(i[1])
    geolist = [i for i in set(geolist)]
    for x in range(len(results)-1):
        if results[x][1] != '' and results[x+1][1]!='' and results[x][1].split('\t')[0] == u'中国' and results[x+1][1].split('\t')[0] == u'中国':
            if results[x][1] !=  results[x+1][1]:
                line_list.append([results[x][1], results[x+1][1]])
    return {'city':geolist, 'line':line_list}

def group_event_rank(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people'])
    uid_list = uid_string['fields']['people'][0].split('&')
    related_event_list = []
    event_user_dict = {}
    for uid in uid_list:
        c_string = 'start n=node:'+node_index_name+'("'+people_primary+':'+str(uid)+'") match (n)-[r]-(e:Event) return e'
        result = graph.run(c_string)
        for event in result:
            print event,'---------'
            # if event:
            event_dict = dict(event)
            event_id = event_dict['e']['event_id']
            related_event_list.append(event_id)
            try:
                event_user_dict[event_id].append(uid)
            except:
                event_user_dict[event_id] = []
                event_user_dict[event_id].append(uid)
    event_rank_list = []
    for k,v in event_user_dict.iteritems():
        k_dict = {}
        event_result = es_event.get(index=event_analysis_name, doc_type=event_text_type, id=k, fields=['user_results','name'])
        event_rank = event_result['fields']['user_results'][0]
        event_name = event_result['fields']['name'][0]
        user_results = json.loads(event_rank)
        k_dict['event_id'] = k
        k_dict['event_name'] = event_name
        k_dict['user'] = v
        k_dict['influ'] = 0
        print k
        for u in v:
            print u
            # if not user_results.has_key(u):
            #     continue
            try:
                influ_val = user_results[u]['influ']
            except:
                print u,'00000'
                influ_val = 10.0
            k_dict['influ'] += influ_val
        event_rank_list.append(k_dict)
    print event_rank_list,'event_rank_list'
    sorted_event = sorted(event_rank_list, key=lambda x:x['influ'], reverse=True)
    try:
        max_value = sorted_event[0]['influ']
    except:
        return []
    final_event_rank = []
    for ii in sorted_event:
        ii['influ'] = float(ii['influ'])/max_value
        final_event_rank.append(ii)
    return final_event_rank


def group_user_tag(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people'])
    uid_list = uid_string['fields']['people'][0].split('&')
    event_list = ['te-lang-pu-1480176000']
    event_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, \
                body={'ids':event_list}, fields=['keywords_list', 'work_tag'])['docs']
    keywords_dict = {}
    mark_dict = {}
    print len(event_result)
    for i in event_result:
        i_keywords = json.loads(i['fields']['keywords_list'][0])
        try:
            i_mark = i['fields']['work_tag'][0]
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

def group_user_keyowrds(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people'])
    uid_list = uid_string['fields']['people'][0].split('&')

    tag_result = es.mget(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'ids':uid_list}, fields=['hashtag_dict', 'keywords'])['docs']
    keywords_dict = {}
    hashtag_dict = {}
    print len(tag_result)
    for i in tag_result:
        i_keywords = json.loads(i['fields']['keywords'][0])
        i_hashtag = json.loads(i['fields']['hashtag_dict'][0])
        for hashtag, value in i_hashtag.iteritems():
            try:
                hashtag_dict[hashtag] += value
            except:
                hashtag_dict[hashtag] = value
        for key in i_keywords:
            try:
                keywords_dict[key[0]] += key[1]
            except:
                keywords_dict[key[0]] = key[1]
    sorted_keywords_dict = sorted(keywords_dict.iteritems(), key=lambda x:x[1], reverse=True)[:100]
    sorted_mark_dict = sorted(hashtag_dict.iteritems(), key=lambda x:x[1], reverse=True)[:100]
    
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


def group_user_rank(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    print group_id
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people'])
    uid_list = uid_string['fields']['people'][0].split('&')

    indx_id_list = []
    for i in uid_list:
        a = graph.run('start n=node:'+node_index_name+'("'+people_primary+':'+str(i)+'") return id(n)')
        for j in a:
            indx_id_list.append(str(dict(j)['id(n)']))
    event_id_string = ','.join(indx_id_list)
    query = 'start d=node('+event_id_string+'),e=node('+event_id_string+') match (d)-[r]->(e) return d,type(r),e'
    result = graph.run(query)
    exist_relation = []
    exist_relation_string = []
    for i in result:
        # print i
        dict_i = dict(i)
        start_id = dict_i['d']['uid']
        start_name = user_name_search(start_id)
        end_id = dict_i['e']['uid']
        end_name = user_name_search(end_id)
        exist_relation.append([start_id, start_name, relation_dict[dict_i['type(r)']], \
                    end_id, end_name])
        # print exist_relation
        relation_string = start_id+'-'+end_id
        exist_relation_string.append(relation_string)
    set_exist_relation = set(exist_relation_string)
    relation_set_count = len(list(set_exist_relation))
    node_count = len(uid_list)
    total_count = node_count*(node_count-1)/2
    try:
        relation_degree = float(relation_set_count)/total_count
    except:
        relation_degree = 0
    if relation_degree == 0:
        conclusion = u'无关联'
    elif relation_degree <0.33 and relation_degree >0:
        conclusion = u'关联度较低'
    elif relation_degree >= 0.33 and relation_degree <0.66:
        conclusion = u'关联度适中'
    elif relation_degree >= 0.66:
        conclusion = u'联系紧密'##未定义！！
    return {'relation_table':exist_relation, 'relation_count':relation_set_count,\
        'conclusion':conclusion, 'relation_degree':relation_degree}

def show_file_link(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people', 'file_link', 'wiki_link'])
    uid_list = uid_string['fields']['people'][0].split('&')
    origin_list = []
    try:
        file_link = uid_string['fields']['file_link'][0].split('+')
    except:
        file_link = []
    final_file = []
    for i in file_link:
        final_file.append(i.split(','))
    return final_file

def group_related(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
    group_id = group_id.lower()
    uid_string = es_group.get(index=group_name, doc_type=group_type, id=group_id,  fields=['people', 'file_link', 'wiki_link'])
    origin_list = uid_string['fields']['people'][0].split('&')
    # origin_list = []

    try:
        file_link = uid_string['fields']['file_link'][0].split('+')
    except:
        file_link = []
    final_file = []
    for i in file_link:
        final_file.append(i.split(','))
    try:
        final_wiki = json.loads(uid_string['fields']['wiki_link'][0])
    except:
        final_wiki = []
    event_graph_id = []
    for i in origin_list:
        a = graph.run('start n=node:'+node_index_name+'("'+people_primary+':'+str(i)+'") return id(n)')
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
        org_list_ = [i for i in set(node_dict['org'])]
        org_result = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':org_list_}, fields=['uname', 'uid'])['docs']
    except:
        org_result = []
    try:
        event_list = [i for i in set(node_dict['event'])]
        event_result = es_event.mget(index=event_analysis_name,doc_type=event_text_type, body={'ids':event_list}, fields=['en_name', 'name'])['docs']
    except:
        event_result = []
    final_user = []
    for i in user_result:
        if i['_id'] in origin_list:
            continue
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
        if i['_id'] in origin_list:
            continue
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
        if i['found'] == True:
            final_event.append([i['fields']['en_name'][0], i['fields']['name'][0]])
        else:
            final_event.append([i['_id'],i['_id']])
    return {'final_user':final_user, 'final_org':final_org, 'final_event':final_event, \
            'final_file':final_file, 'final_wiki':final_wiki}