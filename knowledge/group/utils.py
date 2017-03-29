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
from knowledge.global_config import node_index_name, event_index_name, special_event_node, group_node, people_primary,\
                            event_node, event_primary, event_index_name, org_primary, people_node, org_node, event_node,\
                            group_name, group_type, group_index_name, group_primary, node_index_name, people_primary,\
                            group_rel
from knowledge.parameter import DAY, WEEK, RUN_TYPE, RUN_TEST_TIME,MAX_VALUE,sensitive_score_dict
# from knowledge.cron.event_analysis.event_compute import immediate_compute
p = Pinyin()
WEEK = 7

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

def search_related_u_card(item, submit_user, g_name):
    if g_name:
        g_name = g_name + '_' + submit_user
        g_name_pinyin = p.get_pinyin(g_name)
        user_list_string = es_group.get(index=group_name, doc_type=group_type, id=g_name_pinyin,\
                            fields=['people'])
        uid_list = []
        uid_list = user_list_string['fields']['people'][0].split('&')
        print uid_list,'==========='
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
    info = create_rel(node_key1, node1_list, node1_index_name, rel, node_key2, group_id, node2_index_name, submit_user)
    return info

def create_rel(node_key1, node1_list, node1_index_name, rel, node_key2, node2_id, node2_index_name, submit_user):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node1_index_name)
    group_index = Index.get_index(Node, node2_index_name)
    tx = graph.begin()
    for node1_id in node1_list:
        print node2_id
        print node1_id,'-----'
        # node1 = node_index.get(node_key1, node1_id)
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
    flag = create_rel(node_key1, node1_list, node1_index_name, rel, node_key2, node2_id_pinyin, node2_index_name, submit_user)
    return flag

def del_u_group_rel(g_name, uid):
    en_name = p.get_pinyin(g_name)
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
        s_string = 'START s0 = node:'+group_index_name+'('+group_primary+'='+en_name+') DELETE s0' 
        graph.run(s_string)
        es_group.delete(index=group_name, doc_type=group_type, id=en_name)
    else:
        es_group.update(index=group_name,doc_type=group_type,id=en_name,\
            body={'doc':{'people':uid_string, 'people_count':len(new_uid_list)}}) 
    return '1'

def add_group_k_label(g_name, k_label,operation):
    new_label = k_label.split('&')
    en_name = p.get_pinyin(g_name)
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
        eid_string1 = es_group.get(index=group_name, doc_type=group_type, id=topic_id1,  fields=['people'])
        event_list1 = eid_string1['fields']['people'][0].split('&')
        topic_id2 = p.get_pinyin(g_name2)
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
    uid_string1 = es_group.get(index=group_name, doc_type=group_type, id=group_id1,  fields=['people'])
    uid_list1 = uid_string1['fields']['people'][0].split('&')

    group_id2 = p.get_pinyin(g_name2)
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
    eid_string1 = es_group.get(index=group_name, doc_type=group_type, id=topic_id1,  fields=['label'])
    label_list1 = eid_string1['fields']['label'][0].split('&')
    
    topic_id2 = p.get_pinyin(g_name2)
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
    eid_string1 = es_group.get(index=group_name, doc_type=group_type, id=topic_id1,  fields=['k_label'])
    label_list1 = eid_string1['fields']['k_label'][0].split('&')
    
    topic_id2 = p.get_pinyin(g_name2)
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

def group_geo_vary(g_name, submit_user):
    group_id = p.get_pinyin(g_name)
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
    main_activity_geo = sort_all_activity_geo[0][0]


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

    return results