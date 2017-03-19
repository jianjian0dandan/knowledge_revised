# -*-coding:utf-8-*-
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect,make_response,request
from neo4j_event import select_rels_all, select_rels, create_person, create_rel_from_uid2group, create_node_or_node_rel, \
    update_node, update_node_or_node_rel, delete_rel, delete_node,nodes_rels,get_es_status,select_event_es,\
    select_people_es
from knowledge.global_config import *
from knowledge.global_utils import *
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from utils import recommentation_in, recommentation_in_auto, submit_task
from knowledge.time_utils import ts2datetime, datetime2ts
from knowledge.parameter import RUN_TYPE, RUN_TEST_TIME, DAY
test_time = datetime2ts(RUN_TEST_TIME)
# from draw_redis import *

# from knowledge.global_utils import event_name_search

mod = Blueprint('search', __name__, url_prefix='/search')

@mod.route('/submit_task/',methods=['GET', 'POST'])
def ajax_submit_task():
    input_data = dict()
    input_data = request.get_json()
    input_data = {'u_type':'user/organization', 'submit_date':'x', 'uid_list':json.dumps(['3036528532','5825134863']), 'relation_list':json.dumps(['friend']), 'cal_style':0, 'recommend_style':'', 'submit_user':'submit_user'}
    try:
        submit_user = input_data['submit_user']
    except:
        return 'no submit_user information'
    try:
    	task_name = input_data['task_name']
    except:
    	task_name = submit_user + '_' + str(int(time.time()))
        input_data['task_name'] = task_name
    task_id = submit_user + '_' + str(int(time.time()))
    input_data['task_id'] = task_id
    now_ts = int(time.time())
    input_data['submit_date'] = now_ts
    status = submit_task(input_data)
    return json.dumps(status)



    start_id = get_node_id(start_node)
    end_id = get_node_id(end_node)
    relation = relation.split('&')
    step = step
    limit = 'limit 10'
    query = 'start n=node('+','.join(start_id)+'),e=node('+','.join(end_id)+') match (n)-[r:'+'|:'.join(relation)+'*0..'+step+'-(e) return n,x,e'+limit
    graph.run(query)

	# start n=node(123,208),x=node(161) match (n)-[r:discuss|:join*1..2]-(x) return n,r,x


def get_node_id(start_node):
    input_id = []
    for node in start_node:
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
    	if id_list:  #输入或者上传id
    		id_list
    	else:#属性搜索
    		condition={'must/should/must_not':{'key1':'value1','key2':'value2'}}
    		if node_type == people_node or node_type == org_node:#人，机构
    			if node_type == people_node:
	    			condition['must']['terms']={'verified_type':peo_list}
    			else:
    				condition['must']['terms']={'verified_type':org_list}
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
				}
			}
			result = es_user_portrait.search(index=portrait_index_name,type=portrait_index_type,body=query_body)['hits']['hits']
			id_list = [i['_id'] for i in result]
    	'node:node_type(primary=id_list)'
    	for i in id_list：
	    	input_id.append(graph.run('start n=node:'+neo_index+'("'+primary+':'+i+'") return id(n)')) 
	return input_id    	
