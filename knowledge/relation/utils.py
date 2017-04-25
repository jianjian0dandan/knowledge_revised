# -*- coding: UTF-8 -*-
'''
recommentation
save uid list should be in
'''
import IP
import sys
import time
import datetime
import math,re
import json
import redis
import math,os
from xpinyin import Pinyin
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
from py2neo.ogm import GraphObject, Property
from py2neo import Node, Relationship,Path,walk
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
# from knowledge.global_utils import es_bci_history, bci_history_index_name, bci_history_index_type, ES_SENSITIVE_INDEX, DOCTYPE_SENSITIVE_INDEX
# from knowledge.filter_uid import all_delete_uid
from knowledge.time_utils import ts2datetime, datetime2ts
from knowledge.global_config import event_task_name, event_task_type, event_analysis_name, event_text_type
from knowledge.global_config import node_index_name, event_index_name, special_event_node, group_node, people_primary
from knowledge.parameter import DAY, WEEK, RUN_TYPE, RUN_TEST_TIME,MAX_VALUE,sensitive_score_dict
from knowledge.global_config import *
from knowledge.global_utils import *
p = Pinyin()
WEEK = 7



#get user detail
#output: uid, uname, location, fansnum, statusnum, influence
def get_user_detail(date, input_result, status, user_type="influence", auth=""):
    bci_date = ts2datetime(datetime2ts(date) - DAY)
    results = []
    if status=='show_in':
        uid_list = input_result
    if status=='show_compute':
        uid_list = input_result.keys()
    if status=='show_in_history':
        uid_list = input_result.keys()
    if date!='all':
        index_name = 'bci_' + ''.join(bci_date.split('-'))
    else:
        now_ts = time.time()
        now_date = ts2datetime(now_ts)
        index_name = 'bci_' + ''.join(now_date.split('-'))
    tmp_ts = str(datetime2ts(date) - DAY)
    sensitive_string = "sensitive_score_" + tmp_ts
    query_sensitive_body = {
        "query":{
            "match_all":{}
        },
        "size":1,
        "sort":{sensitive_string:{"order":"desc"}}
    }
    try:
        top_sensitive_result = es_bci_history.search(index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX, body=query_sensitive_body, _source=False, fields=[sensitive_string])['hits']['hits']
        top_sensitive = top_sensitive_result[0]['fields'][sensitive_string][0]
    except Exception, reason:
        print Exception, reason
        top_sensitive = 400
    index_type = 'bci'
    user_bci_result = es_cluster.mget(index=index_name, doc_type=index_type, body={'ids':uid_list}, _source=True)['docs']  #INFLUENCE,fans,status
    user_profile_result = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list}, _source=True)['docs'] #个人姓名，注册地
    # bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={"ids":uid_list}, fields=['user_fansnum', 'weibo_month_sum'])['docs']
    # sensitive_history_result = es_bci_history.mget(index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX, body={'ids':uid_list}, fields=[sensitive_string], _source=False)['docs']
    max_evaluate_influ = get_evaluate_max(index_name)
    for i in range(0, len(uid_list)):
        uid = uid_list[i]
        bci_dict = user_bci_result[i]
        profile_dict = user_profile_result[i]
        # bci_history_dict = bci_history_result[i]
        # sensitive_history_dict = sensitive_history_result[i]
        #print sensitive_history_dict
        try:
            bci_source = bci_dict['_source']
        except:
            bci_source = None
        if bci_source:
            influence = bci_source['user_index']
            influence = math.log(influence/float(max_evaluate_influ['user_index']) * 9 + 1 ,10)
            influence = influence * 100
        else:
            influence = ''
        try:
            profile_source = profile_dict['_source']
        except:
            profile_source = None
        if profile_source:
            uname = profile_source['nick_name'] 
            location = profile_source['user_location']
            try:
                fansnum = bci_dict['fields']['user_fansnum'][0]
            except:
                fansnum = 0
            try:
                statusnum = bci_dict['fields']['weibo_month_sum'][0]
            except:
                statusnum = 0
        else:
            uname = uid
            location = ''
            try:
                fansnum = bci_dict['fields']['user_fansnum'][0]
            except:
                fansnum = 0
            try:
                statusnum = bci_dict['fields']['weibo_month_sum'][0]
            except:
                statusnum = 0
        if status == 'show_in':
            if user_type == "sensitive":
                tmp_ts = datetime2ts(date) - DAY
                tmp_data = r_cluster.hget("sensitive_"+str(tmp_ts), uid)
                if tmp_data:
                    sensitive_dict = json.loads(tmp_data)
                    sensitive_words = sensitive_dict.keys()
                else:
                    sensitive_words = []
                if sensitive_history_dict.get('fields',0):
                    #print sensitive_history_dict['fields'][sensitive_string][0]
                    #print top_sensitive
                    sensitive_value = math.log(sensitive_history_dict['fields'][sensitive_string][0]/float(top_sensitive)*9+1, 10)*100
                    #print "sensitive_value", sensitive_value
                else:
                    sensitive_value = 0
                results.append([uid, uname, location, fansnum, statusnum, influence, sensitive_words, sensitive_value])
            else:
                results.append([uid, uname, location, fansnum, statusnum, influence])
            if auth:
                hashname_submit = "submit_recomment_" + date
                tmp_data = json.loads(r.hget(hashname_submit, uid))
                recommend_list = (tmp_data['operation']).split('&')
                admin_list = []
                admin_list.append(tmp_data['system'])
                admin_list.append(list(set(recommend_list)))
                admin_list.append(len(recommend_list))
                results[-1].extend(admin_list)
        if status == 'show_compute':
            in_date = json.loads(input_result[uid])[0]
            compute_status = json.loads(input_result[uid])[1]
            if compute_status == '1':
                compute_status = '3'
            results.append([uid, uname, location, fansnum, statusnum, influence, in_date, compute_status])
        if status == 'show_in_history':
            in_status = input_result[uid]
            if user_type == "sensitive":
                tmp_ts = datetime2ts(date) - DAY
                tmp_data = r_cluster.hget("sensitive_"+str(tmp_ts), uid)
                if tmp_data:
                    sensitive_dict = json.loads(tmp_data)
                    sensitive_words = sensitive_dict.keys()
                if sensitive_history_dict.get('fields', 0):
                    sensitive_value = math.log(sensitive_history_dict['fields'][sensitive_string][0]/float(top_sensitive)*9+1, 10)*100
                else:
                    sensitive_value = 0
                results.append([uid, uname, location, fansnum, statusnum, influence, in_status, sensitive_words, sensitive_value])
            else:
                results.append([uid, uname, location, fansnum, statusnum, influence, in_status])

    return results

def get_evaluate_max(index_name):
    max_result = {}
    index_type = 'bci'
    evaluate_index = ['user_index']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size':1,
            'sort':[{evaluate: {'order': 'desc'}}]
            }
        # try:
        result = es_cluster.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        # except Exception, e:
        # raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result


def submit_event(input_data):
    if not input_data.has_key('name'):
        input_data['name'] = input_data['keywords']

    if input_data.has_key('mid'):
        # event_id = mid
        input_data['en_name'] = input_data['mid']
        del input_data['mid']
    else:
        e_name = input_data['name']
        e_name_string = ''.join(e_name.split('&'))
        event_id = p.get_pinyin(e_name_string)+'-'+str(input_data['event_ts'])  #+str(int(time.time()))
        input_data['en_name'] = event_id

    if not input_data.has_key('start_ts'):
        start_ts = input_data['event_ts'] - 2*DAY
        input_data['start_ts'] = start_ts
    if not input_data.has_key('end_ts'):
        end_ts = input_data['event_ts'] + 5*DAY
        input_data['end_ts'] = end_ts
    input_data['submit_ts'] = int(time.time())
    del input_data['event_ts']
    try:
        result = es_event.get(index=event_task_name, doc_type=event_task_type, id=input_data['en_name'])['_source']
        return 'already in'
    except:
        es_event.index(index=event_task_name, doc_type=event_task_type, id=input_data['en_name'], body=input_data)
    return True

def submit_event_file(input_data):
    submit_ts = input_data['submit_ts']
    relation_compute = input_data['relation_compute']
    immediate_compute = input_data['immediate_compute']
    submit_user = input_data['submit_user']
    recommend_style = input_data['recommend_style']
    compute_status = input_data['compute_status']
    file_data = input_data['upload_data']
    result_flag = False
    valid_event = 0
    total_event = len(file_data)
    for event in file_data:
        if not event.has_key('event_ts'):
            event['event_ts'] = int(time.time())
        event['submit_ts'] = submit_ts
        event['relation_compute'] = relation_compute
        event['immediate_compute'] = immediate_compute
        event['submit_user'] = submit_user
        event['recommend_style'] = recommend_style
        event['compute_status'] = compute_status
        result = submit_event(event)
        if result == True:
            valid_event += 1
    if valid_event == total_event:
        result_flag = True
    return result_flag, valid_event

def relation_add(input_data):
    result_detail = [False]
    rel_num = 0
    for i in input_data:
        rel_num += 1
        node_key1 = i[0]
        node1_id = i[1]
        node1_index_name = i[2]
        rel = i[3]
        node_key2 = i[4]
        node2_id = i[5]
        node2_index_name = i[6]
        result = create_node_or_node_rel(node_key1, node1_id, node1_index_name, rel, node_key2, node2_id, node2_index_name)
        # return result
        if result == 'have relation':
            result_detail.append(rel_num)
            return result_detail
    result_detail[0] = True
    return result_detail

def show_relation(node_key1, node1_id, node1_index_name, rel, node_key2, node2_id, node2_index_name):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node1_index_name)
    group_index = Index.get_index(Node, node2_index_name)
    #print node_index
    #print group_index
    tx = graph.begin()
    node1 = node_index.get(node_key1, node1_id)[0]
    node2 = group_index.get(node_key2, node2_id)[0]
    if not (node1 and node2):
        print "node does not exist"
        return 'does not exist'
    c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" % (
    node1_index_name,node_key1, node1_id, node2_index_name, node_key2, node2_id, rel)
    # return c_string

    result = graph.run(c_string)
    # print result
    # rel_list = []
    for item in result:
        rel_list.append(item)
    return rel_list

def create_node_or_node_rel(node_key1, node1_id, node1_index_name, rel, node_key2, node2_id, node2_index_name):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node1_index_name)
    group_index = Index.get_index(Node, node2_index_name)
    #print node_index
    #print group_index
    tx = graph.begin()
    node1 = node_index.get(node_key1, node1_id)[0]
    node2 = group_index.get(node_key2, node2_id)[0]
    if not (node1 and node2):
        print "node does not exist"
        return 'does not exist'
    c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" % (
    node1_index_name,node_key1, node1_id, node2_index_name, node_key2, node2_id, rel)
    # return c_string

    result = graph.run(c_string)
    # print result
    # rel_list = []
    for item in result:
        rel_list.append(item)
    # print rel_list
    if rel in rel_list:
        return 'has relation already'
    rel = Relationship(node1, rel, node2)
    graph.create(rel)
    print "create success"
    return True

def search_event(item, field):
    query_body = {
        "query":{
            'bool':{
                'should':[
                    {"wildcard":{'keywords':'*'+str(item.encode('utf-8'))+'*'}},            
                    {"wildcard":{'en_name':'*'+str(item.encode('utf-8'))+'*'}},            
                    # {"wildcard":{'name':'*'+str(item.encode('utf-8'))+'*'}}         
                ]
            }

        },
        'size':10
    }
    only_eid = []
    event_id_list = []
    u_nodes_list = {}
    e_nodes_list = {}
    event_relation =[]
    try:
        name_results = es_event.search(index=event_analysis_name, doc_type=event_text_type, \
                body=query_body, fields=field)['hits']['hits']  #fields=['name','en_name']
    except:
        return 'does not exist'
    for i in name_results:
        field_list = []
        for key in field:
            try:
                key1 = i['fields'][key][0]
            except:
                key1 = ''
            field_list.append(key1)

        event_id_list.append(field_list)
    return event_id_list

def search_event_time_limit(item, field, start_ts, end_ts):
    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"range":{
                        "submit_ts":{
                            "gte": start_ts,
                            "lte": end_ts
                        }
                    }}
                ]
            }
        }
    }
    only_eid = []
    event_id_list = []
    u_nodes_list = {}
    e_nodes_list = {}
    event_relation =[]
    try:
        name_results = es_event.search(index=event_analysis_name, doc_type=event_text_type, \
                body=query_body, fields=field)['hits']['hits']  #fields=['name','en_name']
    except:
        return 'does not exist'
    for i in name_results:
        field_list = []
        for key in field:
            try:
                key1 = i['fields'][key][0]
            except:
                key1 = ''
            field_list.append(key1)

        event_id_list.append(field_list)
    return event_id_list

def search_user(item,field):
    query_body = {
        "query":{
            'bool':{
                'should':[
                    {"wildcard":{'uid':'*'+str(item.encode('utf-8'))+'*'}},            
                    {"wildcard":{'uname':'*'+str(item.encode('utf-8'))+'*'}}
                ]
            }

        },
        'size':10
    }
    only_uid = []
    user_uid_list = []
    u_nodes_list = {}

    try:
        name_results = es.search(index=portrait_index_name, doc_type=portrait_index_type, \
                body=query_body, fields= field)['hits']['hits']
    except:
        return 'does not exist'

    for i in name_results:
        field_list = []
        for key in field:
            try:
                key1 = i['fields'][key][0]
            except:
                key1 = ''
            field_list.append(key1)
        user_uid_list.append(field_list)
    return user_uid_list

def search_user_time_limit(item, field, start_ts, end_ts):
    query_body = {
        "query":{
            # "uid":uid_list #-------------------!!!!!
            "bool":{
                "must":[
                    {"range":{
                        "create_time":{
                            "gte": former_ts,
                            "lte": current_ts
                        }
                    }}
                ]
            }
        }
    }
    only_uid = []
    user_uid_list = []
    u_nodes_list = {}

    try:
        name_results = es.search(index=portrait_index_name, doc_type=portrait_index_type, \
                body=query_body, fields= field)['hits']['hits']
    except:
        return 'does not exist'

    for i in name_results:
        field_list = []
        for key in field:
            try:
                key1 = i['fields'][key][0]
            except:
                key1 = ''
            field_list.append(key1)
        user_uid_list.append(field_list)
    return user_uid_list

def search_node_time_limit(node_type, item, start_ts, end_ts, editor):
    if node_type == 'User' or node_type == 'Org':
        field = ['uid', 'uname','location', 'influence', 'activeness', 'sensitive','keywords_string']
        # field = ['uid', 'uname','location', 'influence', 'activeness', 'sensitive','keywords_string', 'user_tag']
        node_result = search_user_time_limit(item, field, start_ts, end_ts, editor)
    if node_type == 'Event':
        # field = ['en_name', 'submit_ts',  'uid_counts', 'weibo_counts']
        field = ['en_name','name', 'category', 'submit_ts', 'real_geo', 'uid_counts',\
         'weibo_counts', 'keywords', 'work_tag','compute_status']
        node_result = search_event_time_limit(item, field, start_ts, end_ts, editor)
    return node_result

def show_node_detail(node_type, item, submit_user):
    if node_type == 'User' or node_type == 'Org':
        field = ['uid', 'uname', 'topic_string', 'domain', 'function_description']
        # field = ['uid', 'uname','location', 'influence', 'activeness', 'sensitive','keywords_string', 'user_tag']
        index_n = node_index_name
        index_key = people_primary
        node_key = group_node
        node_result = search_user(item, field)[0]
        tag = deal_user_tag(item, submit_user)[0]
        node_result.append(tag)

    if node_type == 'Event':
        field = ['en_name', 'name', 'real_geo', 'real_time',  'category', 'real_person', 'real_auth', \
              'start_ts', 'end_ts','description', 'related_docs']
        node_result = search_event(item, field)[0]
        tag = deal_event_tag(item, submit_user)[0]
        node_result.append(tag)
        index_n = event_index_name
        index_key = 'event'
        node_key = special_event_node

    s_string = 'START s3 = node:%s(%s="%s") MATCH (s0:%s)-[r]-(s3) return s0' \
               %(index_n, index_key, item, node_key)
    event_result = graph.run(s_string)
    events = []
    for special_event in event_result:
        events.append(special_event[0][index_key])
    # result = node_result[0]
    node_result.append(events)
    return node_result

def deal_user_tag(item ,submit_user):
    tag = es.get(index=portrait_index_name,doc_type=portrait_index_type, id=item)['_source']['function_mark']
    # return result
    # tag = tag_value
    #print tag,'======!!=========='
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

# def deal_event_tag(item ,submit_user):
#     tag = es_event.get(index=event_analysis_name,doc_type=event_text_type, id=item)['_source']['work_tag'][0]
#     # return result
#     # tag = tag_value
#     print tag,'=============!!==='
#     tag_list = tag.split('&')
#     left_tag = []
#     keep_tag = []
#     for i in tag_list:
#         user_tag = i.split('_')
#         if user_tag[0] == submit_user:
#             keep_tag.append(user_tag[1])
#         else:
#             left_tag.append(i)
#     return [keep_tag, left_tag]


def search_data(input_data):
    start_id = get_node_id(input_data['start_nodes'])
    print 'start_id',start_id
    if len(start_id) == 0:
    	return 'no start id'
    end_id = get_node_id(input_data['end_nodes'])
    print 'end_id:',end_id
    relation = input_data['relation']
    submit_user = input_data['submit_user']
    step = str(input_data['step'])
    if len(step) == 0:
        step = '1'
    if input_data['limit']:
        limit = 'limit '+input_data['limit']
    else:
        limit = 'limit 200'
    if len(start_id) == 0:
        start_id = '*'
    else:
        start_id = ','.join(start_id)
    if len(end_id) == 0:
        end_id = '*'
    else:
        end_id = ','.join(end_id)
    if len(relation) == 0:
        relation = 'r'
    else:
        relation = 'r:'+'|:'.join(relation)

    if input_data['short_path']=='True':
    	if end_id == '*':
    		return 'short_path no end id'
        query = 'start d=node('+start_id+'),e=node('+end_id+') match p=allShortestPaths( d-['+relation+'*0..'+step+']-e ) return p '+limit
        print query
        return get_info_by_query(query,submit_user)
        # compute_short_path(start_id,end_id,relation,step,limit)
    else:
        if end_id == '*':
            query = 'start n=node('+start_id+') match (n)-['+relation+'*0..'+step+']-(e) return n,r,e '+limit
        else:
            query = 'start n=node('+start_id+'),e=node('+end_id+') match (n)-['+relation+'*0..'+step+']-(e) return n,r,e '+limit
        print query
        return get_info_by_query(query,submit_user)


def get_info_by_query(query,submit_user):
    node_list = []
    result = list(graph.run(query))
    graph_result = []
    print result
    for i in result:
        i = dict(i)
        try:
            print i['n'],i['r'],i['e']
        except:
            print i['p']
        # print list(i['n'].labels()),dict(i['n']).keys()[0],dict(i['n']).values()[0]
        try: 
            i_type = i['r']
        except:
            i_type = i['p']
        for j in i_type:
            # print '???????????/'
            print '602',j.start_node(),j.type(),j.end_node()
            # print dict(j.start_node())
            start_node = dict(j.start_node())
            relation = j.type()
            end_node = dict(j.end_node())
            if relation == 'wiki_link' or relation == 'wiki_link2':
            	continue
            #节点信息，名字
            info,start_node['name'] = get_es_by_id(start_node.keys()[0],start_node.values()[0],submit_user)
            if info == 0:
            	continue
            if info and info not in node_list :
                node_list.append(info)
            info,end_node['name'] = get_es_by_id(end_node.keys()[0],end_node.values()[0],submit_user)
            if info == 0:
            	continue
            if info and info not in node_list :
                node_list.append(info)

            this_relation = [start_node,relation,end_node]
            if this_relation not in graph_result:
                graph_result.append(this_relation)
        # print list(i['e'].labels()),dict(i['e']).keys()[0],dict(i['e']).values()[0]
    # max_influence_peo =  get_max_index_peo('influence')
    # max_activeness_peo = get_max_index_peo('activeness')
    # max_sensitive_peo = get_max_index_peo('sensitive')
    # max_influence_org =  get_max_index_org('influence')
    # max_activeness_org = get_max_index_org('activeness')
    # max_sensitive_org = get_max_index_org('sensitive')
    # print max_influence,max_activeness,max_sensitive
    table_result = {'p_nodes':[],'o_nodes':[],'e_nodes':[],'s_nodes':[],'g_nodes':[]}
    for i in node_list:
        if i[0] == people_primary:
            table_result['p_nodes'].append(i[1])
        elif i[0] == org_primary:
            table_result['o_nodes'].append(i[1])
        elif i[0] == event_primary:
            table_result['e_nodes'].append(i[1])
        elif i[0] == special_event_primary:
            table_result['s_nodes'].append(i[1])
        else:
            table_result['g_nodes'].append(i[1])
    # print {'graph_result':graph_result,'table_result':table_result}
    return {'graph_result':graph_result,'table_result':table_result}



def simple_get_info_by_query(query,submit_user):
    node_list = []
    result = list(graph.run(query))
    graph_result = []
    for i in result:
        i = dict(i)
        #print i['n'],i['r'],i['e']
        # print list(i['n'].labels()),dict(i['n']).keys()[0],dict(i['n']).values()[0]
        try: 
            i_type = i['r']
        except:
            i_type = i['p']

        start_node = dict(i_type.start_node())
        relation = i_type.type()
        end_node = dict(i_type.end_node())
        if relation == 'wiki_link' or relation == 'wiki_link2':
            continue
        #节点信息，名字
        info,start_node['name'] = get_es_by_id(start_node.keys()[0],start_node.values()[0],submit_user)
        if info == 0:
        	continue
        if info and info not in node_list :
            node_list.append(info)
        info,end_node['name'] = get_es_by_id(end_node.keys()[0],end_node.values()[0],submit_user)
        if info == 0:
        	continue
        if info and info not in node_list :
            node_list.append(info)

        this_relation = [start_node,relation,end_node]
        if this_relation not in graph_result:
            graph_result.append(this_relation)

    return graph_result


def get_sim_status(node_type,node_id):
    results = es_sim.search(index=sim_name,doc_type=sim_type,body={'query':{'term':{'node_type':node_type},'term':{'node_id':node_id}}})['hits']['hits']
    if results:
        return results[0]['_source']['compute_status']
    else:
        return 'not exist'


def get_es_by_id(primary_key,node_id,submit_user):
    if primary_key == people_primary:
        es = es_user_portrait
        es_index = portrait_index_name
        es_type = portrait_index_type
        column = p_column
        name = 'uname'
        tag = 'function_mark'
        max_influence =  get_max_index_peo('influence')
        max_activeness = get_max_index_peo('activeness')
        max_sensitive = get_max_index_peo('sensitive')
        node_type = people_node
    elif primary_key == org_primary:
        es = es_user_portrait
        es_index = portrait_index_name
        es_type = portrait_index_type
        column = o_column
        name = 'uname'
        tag = 'function_mark'
        max_influence =  get_max_index_org('influence')
        max_activeness = get_max_index_org('activeness')
        max_sensitive = get_max_index_org('sensitive')
        node_type = org_node
    elif primary_key == event_primary:
        es = es_event
        es_index = event_analysis_name
        es_type = event_type
        column = e_column
        name = 'name'
        tag = 'work_tag'
        node_type = event_node
    elif primary_key == special_event_primary:
        es = es_special_event
        es_index = special_event_name
        es_type = special_event_type
        column = s_column
        name = 'topic_name'
        tag = 'k_label'
        node_type = special_event_node
    else:
        es = es_group
        es_index = group_name
        es_type = group_type
        column = g_column
        name = 'group_name'
        tag = 'k_label'
        node_type = group_node
    try:
        result = es.get(index=es_index,doc_type=es_type,fields=column,id=node_id)
        f_result = {}
        f_result['id']=node_id
        for k,v in result['fields'].iteritems():
            f_result[k] = v[0]
        if primary_key == people_primary or primary_key == org_primary:
            f_result['influence'] = normal_index(f_result['influence'],max_influence)
            f_result['activeness'] = normal_index(f_result['activeness'],max_activeness)
            f_result['sensitive'] = normal_index(f_result['sensitive'],max_sensitive)
        try: 
            f_result[tag] = deal_event_tag(f_result[tag],submit_user)[0]
        except:
            f_result[tag] = ''
        f_result['sim'] = get_sim_status(node_type,node_id)
        return [[primary_key,f_result],result['fields'][name][0]]
    except Exception,e:#人造节点
    	print e
        return [0,node_id]


def get_node_id(start_node):
    input_id = []
    for node in start_node:
        #print node
        node_type = node['node_type']
        if node_type == people_node:
            primary = people_primary
            neo_index = node_index_name
        elif node_type == org_node:
            primary = org_primary
            neo_index = org_index_name
        elif node_type == event_node:
            primary = event_primary
            neo_index = event_index_name
        elif node_type == special_event_node:
            primary = special_event_primary
            neo_index = special_event_index_name
        elif node_type == group_node:
            primary = group_primary
            neo_index = group_index_name
        try:
            id_list = node['ids'][0].split(',')
        except:#属性搜索
            # condition={'must/should/must_not':{'key1':'value1','key2':'value2'}}
            condition = node['conditions']
            if node_type == people_node or node_type == org_node:#人，机构
                if node_type == people_node:
                    try:
                        condition['must'].append({'terms':{'verify_type':peo_list}})
                    except:
                        condition['must'] = [{'terms':{'verify_type':peo_list}}]
                else:
                    try:
                        condition['must'].append({'terms':{'verify_type':org_list}})
                    except:
                        condition['must'] = [{'terms':{'verify_type':org_list}}]
                es = es_user_portrait
                es_index = portrait_index_name
                es_type = portrait_index_type
            if node_type == event_node:#事
                es = es_event
                es_index = event_analysis_name
                es_type = event_type
            if node_type == group_node:#群体
                es = es_group
                es_index = group_name
                es_type = group_type
            if node_type == special_event_node:#专题          
                es = es_special_event
                es_index = special_event_name
                es_type = special_event_type

            query_body = {
                'query':{
                    'bool':condition
                },
                'size':1000
            }
            result = es.search(index=es_index,doc_type=es_type,body=query_body)['hits']['hits']
            id_list = [i['_id'] for i in result]
        #'node:node_type(primary=id_list)'
        #print id_list
        for i in id_list:
            try:
                a = graph.run('start n=node:'+neo_index+'("'+primary+':'+str(i)+'") return id(n)')
                for j in a:
                    #print j
                    input_id.append(str(dict(j)['id(n)']))
            except:
                continue
            # input_id.append(graph.run('start n=node:'+neo_index+'("'+primary+':'+str(i)+'") return id(n)')) 
    return input_id     

def compute_short_path(start_id,end_id,relation,step,limit):
    query = 'start d=node('+start_id+'),e=node('+end_id+') match p=allShortestPaths( d-['+relation+'*0..'+step+']-e ) return p '+limit
    #print query
    result = graph.run(query)
    for i in result:
        i = dict(i)


def simple_search(keywords_list,submit_user):
    chinese = re.compile(u"[\u4e00-\u9fa5]+")
    table_result = {'p_nodes':[],'o_nodes':[],'e_nodes':[],'s_nodes':[],'g_nodes':[]}
    nodes_list = ['p_nodes','o_nodes','e_nodes','s_nodes','g_nodes']

    index_list = [node_index_name,org_index_name,event_index_name,special_event_index_name,group_index_name]
    primary_list = [people_primary,org_primary,event_primary,special_event_primary,group_primary]
    
    node_type_list = [people_node,org_node,event_node,special_event_node,group_node]
    max_influence_peo =  get_max_index_peo('influence')
    max_activeness_peo = get_max_index_peo('activeness')
    max_sensitive_peo = get_max_index_peo('sensitive')
    max_influence_org =  get_max_index_org('influence')
    max_activeness_org = get_max_index_org('activeness')
    max_sensitive_org = get_max_index_org('sensitive')
    id_list = []
    graph_result = []
    for key in keywords_list:
        #print key

        for i in range(len(es_list)):
            query_body = {
                'query':{
                    'bool':{
                        'should':[
                            {'query_string':{
                                'fields':['uid','en_name','group_name','topic_name','uname','description','function_mark','keywords','hashtag','location','name','work_tag','k_label','label','event'],
                                'query':'*'+key+'*'
                                }
                            }
                        ],
                        'minimum_should_match':1
                    }
                },
                'size':99999
            }
            if i == 0:
                query_body['query']['bool']['must'] = [{'terms':{'verify_type':peo_list}}]
            elif i == 1:
                query_body['query']['bool']['must'] = [{'terms':{'verify_type':org_list}}]
            else:
                pass
            #print query_body
            #print es_list[i],es_index_list[i],es_type_list[i]
            result = es_list[i].search(index=es_index_list[i],doc_type=es_type_list[i],body=query_body,fields=column_list[i])['hits']['hits']
            #print 'len:',len(result)
            if result:
                for j in result:
                    f_result = {}
                    f_result['id']=j['_id']
                    # id_list.append(j['_id'])
                    for k,v in j['fields'].iteritems():
                        f_result[k] = v[0]
                    try:
                        f_result[tag_list[i]] = deal_event_tag(f_result[tag_list[i]],submit_user)[0]
                    except KeyError:
                        pass
                    if i == 0:
                        f_result['influence'] = normal_index(f_result['influence'],max_influence_peo)
                        f_result['activeness'] = normal_index(f_result['activeness'],max_activeness_peo)
                        f_result['sensitive'] = normal_index(f_result['sensitive'],max_sensitive_peo)
                    elif i == 1:
                        f_result['influence'] = normal_index(f_result['influence'],max_influence_org)
                        f_result['activeness'] = normal_index(f_result['activeness'],max_activeness_org)
                        f_result['sensitive'] = normal_index(f_result['sensitive'],max_sensitive_org)
                    else:
                        pass
                    f_result['sim'] = get_sim_status(node_type_list[i],j['_id'])
                    table_result[nodes_list[i]].append(f_result)

                    try:
                        a = graph.run('start n=node:'+index_list[i]+'("'+primary_list[i]+':'+str(j['_id'])+'") return id(n)')
                        for k in a:
                            #print k
                            id_list.append(str(dict(k)['id(n)']))
                            query = 'start n=node('+str(dict(k)['id(n)'])+') match (n)-[r]-(e) where (type(r) <> "wiki_link") return n,r,e limit 10'
                            #print query
                            graph_result.extend(simple_get_info_by_query(query,submit_user)) 
                    except:
                        pass
            else:
                continue
    '''
    # print 'dddddddddddddddddddddddddd',id_list,len(id_list)
    if len(id_list) == 0:
        pass
    else:
        #'start n=node(583,2061),e=node(*) match (n)-[r*0..2]-(e) return n,r,e limit 200'
        query = 'start n=node('+','.join(id_list)+') match (n)-[r]-(e) where (type(r) <> "wiki_link") return n,r,e'
        #print query
        graph_result.extend(simple_get_info_by_query(query,submit_user)) 
    '''
    graph_result = list(graph_result)
    # print graph_result

    return {'table_result':table_result,'graph_result':graph_result}

    '''
    if len(chinese.findall(key)) == 0: #可能是id
        for i in range(len(es_list)):
            if column_list[i] == p_column:
                query_body = {
                    'query':{
                        'bool':{
                            'must':[
                                {'term':{'uid':key}},
                                {'terms':{'verify_type':peo_list}}
                            ]
                        }
                    }
                }
                result = es_list[i].search(index=es_index_list[i],doc_type=es_type_list[i],body=query_body,fields=column_list[i])['hits']['hits']
                if result:
                    f_result = {}
                    print result
                    for k,v in result[0]['fields'].iteritems():
                        f_result[k] = v[0]
                    try:
                        f_result[tag_list[i]] = deal_event_tag(f_result[tag_list[i]],submit_user)[0]
                    except KeyError:
                        pass
                    table_result['p_nodes'].append(f_result)
            elif column_list[i] == o_column:
                query_body = {
                    'query':{
                        'bool':{
                            'must':[
                                {'term':{'uid':key}},
                                {'terms':{'verify_type':org_list}}
                            ]
                        }
                    }
                }
                result = es_list[i].search(index=es_index_list[i],doc_type=es_type_list[i],body=query_body,fields=column_list[i])['hits']['hits']
                if result:
                    f_result = {}
                    for k,v in result[0]['fields'].iteritems():
                        f_result[k] = v[0]
                    try:
                        f_result[tag_list[i]] = deal_event_tag(f_result[tag_list[i]],submit_user)[0]
                    except KeyError:
                        pass
                    table_result['o_nodes'].append(f_result)
            else:
                try:
                    result = es_list[i].get(index=es_index_list[i],doc_type=es_type_list[i],id=key,fields=column_list[i])
                    f_result = {}
                    for k,v in result['fields'].iteritems():
                        f_result[k] = v[0]
                    f_result[tag_list[i]] = deal_event_tag(f_result[tag_list[i]],submit_user)[0]
                    table_result[node_list[i]].append(f_result)
                except :
                    continue
    '''

    # query_body = {
    #     'query':{
    #         'bool':{
    #             'should':[
    #                 {'term':{'uid':key}},
    #                 {'term':{'en_name':key}},
    #                 {'term':{'group_name':key}},
    #                 {'term':{'topic_name':key}},
    #                 {'wildcard':{'uname':'*'+key+'*'}},
    #                 {'wildcard':{'description':'*'+key+'*'}},
    #                 {'wildcard':{'function_mark':'*'+key+'*'}},
    #                 {'wildcard':{'keywords':'*'+key+'*'}},
    #                 {'wildcard':{'hashtag':'*'+key+'*'}},
    #                 {'wildcard':{'location':'*'+key+'*'}},
    #                 {'wildcard':{'name':'*'+key+'*'}},
    #                 {'wildcard':{'work_tag':'*'+key+'*'}},
    #                 {'wildcard':{'topic_name':'*'+key+'*'}},
    #                 {'wildcard':{'k_label':'*'+key+'*'}},
    #                 {'wildcard':{'label':'*'+key+'*'}},
    #                 {'wildcard':{'event':'*'+key+'*'}},
    #                 {'wildcard':{'group_name':'*'+key+'*'}},
    #             ],
    #             'minimum_should_match':1
    #         }
    #     }
    # }

def compute_fun(submit_user,submit_ts,node_name,node_type,node_id):
    info = {'submit_user':submit_user,'submit_ts':int(submit_ts),'node_name':node_name,\
            'node_type':node_type,'node_id':node_id,'compute_status':0
            }
    #print info
    result = es_sim.index(index=sim_name,doc_type=sim_type,id=node_id,body=info)
    # os.system('nohup python -u ./knowledge/cron/get_relationship/compute_sim.py '+node_type+' '+node_id+' >> sim.log&')
    #print result
    if result['created']==True:
        os.system('nohup python -u ./knowledge/cron/get_relationship/compute_sim.py '+node_type+' '+node_id+' >> sim.log&')
        print 'yes'
        return 'yes'
    else:
        return 'no'

def get_sim():
    results = es_sim.search(index=sim_name,doc_type=sim_type,body={'query':{'match_all':{}},'size':1000000})['hits']['hits']
    result = []
    if results:
        for i in results:
            result.append(i['_source'])
        return result
    else:
        return ''

def get_sim_by_id(node_type,node_id,submit_user):
    try:
        result = es_sim.get(index=sim_name,doc_type=sim_type,id=node_id)['_source']
        #人-人    事-事    专题-事   群体-
        related_ids = result['related_id'].split('&')
        table = []

        if node_type == people_node or node_type == org_node or node_type == event_node:
            for node_id in related_ids:
                info,name = get_es_by_id(key_type_dict[node_type],node_id,submit_user)
                if info and info not in table:
                    table.append(info)
            return {node_type:table}
        elif node_type == special_event_node:#专题里面的是相似事件
            for node_id in related_ids:
                info,name = get_es_by_id(event_primary,node_id,submit_user)
                if info and info not in table:
                    table.append(info)
            return {event_node:table}
        else:#群体，里面可能有人或者机构
            results = {people_node:[],org_node:[]}
            for i in [people_node,org_node]:
                if i == people_node:
                    node_list = peo_list
                    column = p_column
                    tag = 'function_mark'
                    max_influence =  get_max_index_peo('influence')
                    max_activeness = get_max_index_peo('activeness')
                    max_sensitive = get_max_index_peo('sensitive')
                else:
                    node_list = org_list
                    column = o_column
                    tag = 'function_mark'
                    max_influence_org =  get_max_index_org('influence')
                    max_activeness_org = get_max_index_org('activeness')
                    max_sensitive_org = get_max_index_org('sensitive')
                query_body = {
                    'query':{
                        'bool':{
                            'must':[
                                {'terms':{'uid':related_ids}},  #一个话题，不同情绪下给定时间里按关键词聚合
                                {'terms':{'verify_type':node_list}}
                            ]
                        }
                    }
                }
                nodes = es_user_portrait.search(index=portrait_name,doc_type=portrait_type,body=query_body,fields=column)['hits']['hits']
                for node in nodes:
                    f_result = {}
                    for k,v in node['fields'].iteritems():
                        f_result[k] = v[0]
                    f_result['influence'] = normal_index(f_result['influence'],max_influence)
                    f_result['activeness'] = normal_index(f_result['activeness'],max_activeness)
                    f_result['sensitive'] = normal_index(f_result['sensitive'],max_sensitive)
                    try: 
                        f_result[tag] = deal_event_tag(f_result[tag],submit_user)[0]
                    except:
                        f_result[tag] = ''
                    f_result['sim'] = get_sim_status(i,node['_id'])
                    results[i].append(f_result)
            return results


    except:
        return 'not exist'
