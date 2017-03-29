# -*-coding:utf-8-*-
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
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
from utils import search_data,simple_search,compute_fun
from knowledge.time_utils import ts2datetime, datetime2ts
from knowledge.parameter import RUN_TYPE, RUN_TEST_TIME, DAY
test_time = datetime2ts(RUN_TEST_TIME)
# from draw_redis import *

# from knowledge.global_utils import event_name_search

mod = Blueprint('search', __name__, url_prefix='/relation')

@mod.route('/')
@login_required
def relation_index():#导航页

    return render_template('relation/relation_index.html')

@mod.route('/search/')
# @login_required
def relation_search():#图谱搜索
    return render_template('relation/search.html')

@mod.route('/search_result/')
@login_required
def relation_search_result():#图谱搜索结果
    result = request.args.get('result', '')
    return render_template('relation/search_result.html',result=result)

@mod.route('/similarity/')
@login_required
def relation_similarity():#相似计算

    return render_template('relation/similarity.html')

@mod.route('/similarity_result/')
@login_required
def relation_similarity_result():#相似计算
    node_id = request.args.get('node_id', '')
    # result = sim_result(node_id)
    return render_template('relation/similarity_result.html',node_id=node_id)

@mod.route('/submit_task/',methods=['GET', 'POST'])
@login_required
def submit_task_function():
    input_data = dict()
    # input_data = request.get_json()
    input_data = {
        'start_nodes':[
            {
                'node_type':'User',
                'ids':[2772291221,1470809487]
                # 'conditions':[
                #     {'must':{'keywords':'kkk'}},
                #     {'should':{'hashtag':'ddd'}}
                # ]
            }#,
            # {
            #     'node_type':'User',
            #     'ids':[],
            #     'conditions':[
            #         {'must':{'keywords':'kkk'}},
            #         {'should':{'hashtag':'ddd'}}
            #     ]
            # }
        ],
        'end_nodes':[
            {
                'node_type':'User',
                'ids':[],
                'conditions':{
                    'must':[{'wildcard':{'keywords':u'*心*'}}],
                    'should':[{'wildcard':{'hashtag':u'*韩庚*'}}]
                }
            }#,
            # {
            #     'node_type':'User',
            #     'ids':[],
            #     'conditions':[
            #         {'must':{'keywords':'kkk'}},
            #         {'should':{'hashtag':'ddd'}}
            #     ]
            # }
        ],
        'relation':['join','discuss'],
        'step':'5',
        'limit':'100',
        'submit_user':'admin',
        'short_path':True#True
    }
    result = json.dumps(search_data(input_data))
    # print type(result)
    return redirect(url_for('.relation_search_result',result=result))
    # return json.dumps(result)


@mod.route('/simple_result/')
def simple_result():
	keywords = request.args.get('keywords', '')
	keywords = keywords.split(',') 
	submit_user = request.args.get('submit_user', '')
	# keywords = ['2635695961','2121667213']
	submit_user = 'admin'
	print keywords
	result = simple_search(keywords,submit_user)
	return json.dumps(result)
	#start d=node(533),e=node(522) match p=allShortestPaths( d-[r:discuss|:join*0..15]-e ) return p limit 10

@mod.route('/compute_sim/')
def compute_sim():
	submit_user = request.args.get('submit_user', '')
	submit_ts = request.args.get('submit_ts', '')
	node_name = request.args.get('node_name', '')
	node_type = request.args.get('node_type', '')
	node_id = request.args.get('node_id', '')
	result = compute_fun(submit_user,submit_ts,node_name,node_type,node_id)
	return result

