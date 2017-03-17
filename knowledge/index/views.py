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
mod = Blueprint('index', __name__, url_prefix='/index')

@mod.route('/')
@login_required
def index():#首页

    user_name = g.user.email

    peo_infors = get_people(user_name,2)

    peo_string = 'START start_node=node:'+node_index_name+'("'+people_primary+':*") return count(start_node)'
    peo_object = graph.run(peo_string)

    for item in peo_object:
        peo_count = item['count(start_node)']

    org_string = 'START start_node=node:'+org_index_name+'("'+org_primary+':*") return count(start_node)'
    org_object = graph.run(org_string)
    for item in org_object:
        org_count = item['count(start_node)']

    event_string = 'START start_node=node:'+event_index_name+'("'+event_primary+':*") return count(start_node)'
    event_object = graph.run(event_string)
    for item in event_object:
        event_count = item['count(start_node)']

    special_event_string = 'START start_node=node:'+special_event_index_name+'(\"'+special_event_primary+':*") return count(start_node)'
    special_event_object = graph.run(special_event_string)
    for item in special_event_object:
        special_event_count = item['count(start_node)']

    group_string = 'START start_node=node:'+group_index_name+'("'+group_primary+':*") return count(start_node)'
    group_object = graph.run(group_string)
    for item in group_object:
        group_count = item['count(start_node)']

    neo_count = {'people':peo_count, 'org':org_count, 'event':event_count, 'special_event':special_event_count, 'group':group_count}
    
    weibo_list = get_hot_weibo()

    people_list = get_hot_people()

    map_count = get_map_count()

    print len(people_list)
    return render_template('index/knowledge_home.html', peo_infors = peo_infors, neo_count = neo_count, weibo_list = weibo_list,\
                           people_list = people_list, map_count = map_count)

@mod.route('/graph/')
@login_required
def get_graph():#图谱页面

    p_string = 'START n=node:%s("%s:*") MATCH (n)-[r]-(m) return n.event_id,r,m LIMIT 100' % (event_index_name,event_primary)

    r_relation = dict()
    p_result = graph.run(p_string)
    uid_list = []
    for item in p_result:
        uid_list.append(item[0])
        r_relation[item[0]] = [item[1].type(),dict(item[2]).values()[0]]

    if len(uid_list) > 0:
        result = eventid_name(uid_list)
        relation = []
        for k,v in r_relation.iteritems():
            relation.append([result[k],v[1],v[0]])
    else:
        relation = []

    return render_template('index/knowledgeGraph.html', relation = relation)

@mod.route('/map/')
@login_required
def get_map():#地图页面

    event_result,people_result,org_relation = get_geo()

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

    return render_template('index/card_display.html')

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


