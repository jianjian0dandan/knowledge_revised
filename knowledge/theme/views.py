# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from utils import search_related_e_card,  create_node_and_rel, create_rel,query_detail_theme, create_theme_relation,\
                  get_theme_all, del_e_theme_rel, edit_theme_k_label
from knowledge.global_utils import get_theme

mod = Blueprint('theme', __name__, url_prefix='/theme')

@mod.route('/')
@login_required
def theme_analysis():#专题概览

    return render_template('theme/theme_main.html')

@mod.route('/add/')
@login_required
def theme_add():#新建专题

    return render_template('theme/theme_add.html')

@mod.route('/modify/')
@login_required
def theme_modify():#编辑专题

    return render_template('theme/theme_modify.html')

@mod.route('/compare/')
@login_required
def theme_compare():#专题对比

    return render_template('theme/theme_compare.html')

@mod.route('/result/')
@login_required
def theme_result():#专题查看

    return render_template('theme/theme_result.html')

@mod.route('/theme_overview/')
def ajax_event_overview():  #专题总览
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    result = get_theme(u'房',submit_user)
    return json.dumps(result)

@mod.route('/search_related_event_card/')
def search_related_event_card():  #专题编辑-增加前先搜索事件,如果为已有专题添加，需加上专题名称，新建为空
    theme_name = request.args.get('theme_name', u'房价')
    search_item = request.args.get('item', u'北京')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    event_card = search_related_e_card(search_item, submit_user, theme_name)
    return json.dumps(event_card)

@mod.route('/theme_detail/')
def detail_theme():  #专题包含事件
    theme_name = request.args.get('theme_name', u'房价')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    # sort_flag = request.args.get('sort_flag', 'start_ts')#weibo_counts #uid_counts
    detail_t = query_detail_theme(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/del_event_in_theme/')
def del_event_in_theme():  #专题编辑-删除事件
    theme_name = request.args.get('theme_name', u'房价')
    event_id = request.args.get('event_id', u'te-lang-pu-1480176000')
    flag = del_e_theme_rel(theme_name, event_id)
    return json.dumps(flag)

@mod.route('/theme_add_tag/')
def theme_add_tag():  #专题编辑-添加标签
    theme_name = request.args.get('theme_name', u'房价')
    k_label = request.args.get('k_label', u'贵')
    flag = edit_theme_k_label(theme_name, k_label)
    return json.dumps(flag)

@mod.route('/create_new_relation/')#添加到新专题
def create_new_relation():
    node_key1 = request.args.get('node_key1', 'event_id')  # uid,event_id
    node1_id = request.args.get('node1_id', 'bei-jing-fang-jia-zheng-ce-1480176000')
    if node1_id == '':
    	return 'must add event'
    node1_list = node1_id.split(',')
    node1_index_name = request.args.get('node1_index_name', 'event_index')  # node_index event_index
    rel = request.args.get('rel', 'special_event')
    node_key2 = request.args.get('node_key2', 'event')  # event,uid
    node2_id = request.args.get('node2_id', u'房价')
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    node2_index_name = request.args.get('node2_index_name', 'special_event_index')
    k_label = request.args.get('k_label', 'test') #split &
    flag = create_node_and_rel(node_key1, node1_list, node1_index_name, rel, \
                                   node_key2, node2_id, node2_index_name, submit_user, k_label)
    return json.dumps(flag)

@mod.route('/create_relation/')#添加到已有专题
def create_relation():
    node_key1 = request.args.get('node_key1', 'event_id')  # uid,event_id
    # node1_id11 = 'lao-tai-ao-ye-mai-cai-wei-er-zi-mai-fang-1482126431,受骗后自杀'
    node1_id = request.args.get('node1_id', 'te-lang-pu-1480176000')
    node1_list = node1_id.split(',')
    node1_index_name = request.args.get('node1_index_name', 'event_index')  # node_index event_index
    rel = request.args.get('rel', 'special_event')
    node_key2 = request.args.get('node_key2', 'event')  
    node2_id = request.args.get('node2_id', u'房价')
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    node2_index_name = request.args.get('node2_index_name', 'special_event_index')

    flag = create_theme_relation(node_key1, node1_list, node1_index_name, rel, \
                                   node_key2, node2_id, node2_index_name, submit_user)
    return json.dumps(flag)


