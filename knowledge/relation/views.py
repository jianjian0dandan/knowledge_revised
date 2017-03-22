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
from utils import recommentation_in, recommentation_in_auto,submit_task,search_data
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
@login_required
def relation_search():#图谱搜索

    return render_template('relation/search.html')

@mod.route('/search_result/')
@login_required
def relation_search_result():#图谱搜索结果

    return render_template('relation/search_result.html')

@mod.route('/similarity/')
@login_required
def relation_similarity():#相似计算

    return render_template('relation/similarity.html')

@mod.route('/similarity_result/')
@login_required
def relation_similarity_result():#相似计算

    return render_template('relation/similarity_result.html')

@mod.route('/submit_task/',methods=['GET', 'POST'])
def ajax_submit_task():
    input_data = dict()
    # input_data = request.get_json()
    input_data = {
        'start_nodes':[
            {
                'node_type':'User',
                'ids':[533,522],
                'conditions':[
                    {'must':{'keywords':'kkk'}},
                    {'should':{'hashtag':'ddd'}}
                ]
            },
            {
                'node_type':'User',
                'ids':[],
                'conditions':[
                    {'must':{'keywords':'kkk'}},
                    {'should':{'hashtag':'ddd'}}
                ]
            }
        ],
        'end_nodes':[
            {
                'node_type':'User',
                'ids':[],
                'conditions':[
                    {'must':{'keywords':'kkk'}},
                    {'should':{'hashtag':'ddd'}}
                ]
            },
            {
                'node_type':'User',
                'ids':[],
                'conditions':[
                    {'must':{'keywords':'kkk'}},
                    {'should':{'hashtag':'ddd'}}
                ]
            }
        ],
        'relation':['join','discuss'],
        'step':'5',
        'limit':'100',
        'short_path':True
    }
    result = search_data(input_data)
    return result


#start d=node(533),e=node(522) match p=allShortestPaths( d-[r:discuss|:join*0..15]-e ) return p limit 10