# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from get_result import *
from knowledge.global_utils import graph
from GetUrl import getUrlByKeyWord
mod = Blueprint('index', __name__, url_prefix='/index')

@mod.route('/')
@login_required
def index():#首页

    user_name = g.user.email

    peo_infors = get_people(user_name,2)

    try:
        peo_string = 'START start_node=node:'+node_index_name+'("'+people_primary+':*") return count(start_node)'
        peo_object = graph.run(peo_string)

        for item in peo_object:
            peo_count = item['count(start_node)']
    except:
        peo_count = 0

    try:
        org_string = 'START start_node=node:'+org_index_name+'("'+org_primary+':*") return count(start_node)'
        org_object = graph.run(org_string)
        for item in org_object:
            org_count = item['count(start_node)']
    except:
        org_count = 0

    try:
        event_string = 'START start_node=node:'+event_index_name+'("'+event_primary+':*") return count(start_node)'
        event_object = graph.run(event_string)
        for item in event_object:
            event_count = item['count(start_node)']
    except:
        event_count = 0

    try:
        special_event_string = 'START start_node=node:'+special_event_index_name+'(\"'+special_event_primary+':*") return count(start_node)'
        special_event_object = graph.run(special_event_string)
        for item in special_event_object:
            special_event_count = item['count(start_node)']
    except:
        special_event_count = 0

    try:
        group_string = 'START start_node=node:'+group_index_name+'("'+group_primary+':*") return count(start_node)'
        group_object = graph.run(group_string)
        for item in group_object:
            group_count = item['count(start_node)']
    except:
        group_count = 0

    neo_count = {'people':peo_count, 'org':org_count, 'event':event_count, 'special_event':special_event_count, 'group':group_count}
    
    weibo_list = get_hot_weibo()

    people_list = get_hot_people()

    map_count = get_map_count()

    return render_template('index/knowledge_home.html', peo_infors = peo_infors, neo_count = neo_count, weibo_list = weibo_list,\
                           people_list = people_list, map_count = map_count)

@mod.route('/graph/')
@login_required
def get_graph():#图谱页面

    user_id = request.args.get('user_id', '')
    node_type = request.args.get('node_type', '')

    if node_type == 'ALL':#首页跳转
        relation = get_all_graph()
        flag = 'Success'
    elif node_type == 'people':#人物节点图谱
        relation = get_people_graph(user_id)
        flag = 'Success'
    elif node_type == 'event':#事件节点图谱
        relation = get_event_graph(user_id)
        flag = 'Success'
    elif node_type == 'org':#机构节点图谱
        relation = get_org_graph(user_id)
        flag = 'Success'
    elif node_type == 'topic':#专题节点图谱
        relation = get_special_event_graph(user_id)
        flag = 'Success'
    elif node_type == 'group':#群体节点图谱
        relation = get_group_graph(user_id)
        flag = 'Success'
    else:
        relation = []
        flag = 'Wrong Type'

    return render_template('index/knowledgeGraph.html', relation = relation, flag = flag)

@mod.route('/map/')
@login_required
def get_map():#地图页面

    user_id = request.args.get('user_id', '')
    node_type = request.args.get('node_type', '')

    if node_type == 'ALL':#首页跳转
        event_result,people_result,org_relation = get_all_geo()
        flag = 'Success'
    elif node_type == 'people':#人物节点图谱
        event_result,people_result,org_relation = get_people_geo(user_id)
        flag = 'Success'
    elif node_type == 'event':#事件节点图谱
        event_result,people_result,org_relation = get_event_geo(user_id)
        flag = 'Success'
    elif node_type == 'org':#机构节点图谱
        event_result,people_result,org_relation = get_org_geo(user_id)
        flag = 'Success'
    elif node_type == 'topic':#专题节点图谱
        event_result,people_result,org_relation = get_topic_geo(user_id)
        flag = 'Success'
    elif node_type == 'group':#群体节点图谱
        event_result,people_result,org_relation = get_group_geo(user_id)
        flag = 'Success'
    else:
        event_result = []
        people_result = []
        org_relation = []
        flag = 'Wrong Type'

    return render_template('index/baidu_map.html', event_result = event_result, people_result = people_result, org_relation = org_relation)

@mod.route('/person/')
@login_required
def get_person():#人物属性页面

    return render_template('index/person.html')

@mod.route('/event/')
@login_required
def get_event():#事件属性页面

    return render_template('index/event.html')

@mod.route('/organization/')
@login_required
def get_organization():#机构属性页面

    return render_template('index/organization.html')

@mod.route('/cards/')
@login_required
def get_card():#卡片罗列页面

    user_id = request.args.get('user_id', '')
    node_type = request.args.get('node_type', '')
    card_type = request.args.get('card_type', '')
    user_name = g.user.email

    result,flag = get_relation_node(user_id,node_type,card_type,user_name)#获取关联节点

    return render_template('index/card_display.html', result = result, flag = flag)

@mod.route('/show_attention/', methods=['GET','POST'])
def show_attention():

    user_name = request.args.get('user_name', '')
    s_type = request.args.get('s_type', '')

    if not user_name or not s_type:
        return json.dumps('Wrong')
    
    if s_type == 'people':
        infors = get_people(user_name,2)
    elif s_type == 'event':
        infors = get_event(user_name,2)
    else:
        infors = get_org(user_name,2)

    return json.dumps(infors)

### for neo4j test
@mod.route('/test/')
def neo4j_test():

    p_string = 'START n=node:event_index(event_id="bei-jing-fang-jia-zheng-ce-1480176000") return labels(n)'
    p_result = graph.run(p_string)
    for item in p_result:
        print item

    return 'sss'

@mod.route('/wiki/')
def wikitest():
    key = "特朗普"
    wiki_list = getUrlByKeyWord(key)
    return json.dumps(wiki_list)

    
