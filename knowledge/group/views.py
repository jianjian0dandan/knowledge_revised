# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
import csv
from  knowledge.global_utils import get_group
from utils import search_related_u_card, create_node_and_rel, create_group_relation, del_u_group_rel,\
     add_group_k_label, add_group_file_link, query_detail_group, compare_group_user,compare_group_event,\
     compare_group_keywords, compare_group_k_label, group_geo_vary

mod = Blueprint('group', __name__, url_prefix='/group')

@mod.route('/')
@login_required
def group_analysis():#群体概览

    return render_template('group/group_main.html')

@mod.route('/add/')
@login_required
def group_add():#新建群体

    return render_template('group/group_add.html')

@mod.route('/modify/')
@login_required
def group_modify():#编辑群体

    return render_template('group/group_modify.html')

@mod.route('/compare/')
@login_required
def group_compare():#群体对比

    return render_template('group/group_compare.html')

@mod.route('/result/')
@login_required
def group_result():#群体查看

    return render_template('group/group_result.html')

@mod.route('/group_overview/')
def ajax_group_overview():  #群体总览
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    result = get_group('',submit_user)
    return json.dumps(result)

@mod.route('/search_related_people_item/')
def search_related_event_item():  #群体编辑-增加前先搜索人物,如果为已有群体添加，需加上群体名称，新建为空
    g_name = request.args.get('g_name', u'美选群体')
    search_item = request.args.get('item', u'1799')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    user_card = search_related_u_card(search_item, submit_user, g_name)
    return json.dumps(user_card)

@mod.route('/create_new_relation/')#添加到新群体
def create_new_relation():
    node_key1 = request.args.get('node_key1', 'uid')  # uid,event_id
    node1_id = request.args.get('node1_id', '5848882336,1799791715')
    if node1_id == '':
    	return 'must add user'
    node1_list = node1_id.split(',')
    node1_index_name = request.args.get('node1_index_name', 'node_index')  # node_index event_index
    rel = request.args.get('rel', 'group')
    node_key2 = request.args.get('node_key2', 'group')  # event,uid
    node2_name = request.args.get('node2_id', u'美选群体')
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    node2_id = node2_name + '_' + submit_user
    node2_index_name = request.args.get('node2_index_name', 'group_index')
    k_label = request.args.get('k_label', 'test') #split ,
    flag = create_node_and_rel(node_key1, node1_list, node1_index_name, rel, \
                                   node_key2, node2_id, node2_index_name, submit_user, k_label, node2_name)
    return json.dumps(flag)

@mod.route('/create_relation/')#添加到已有群体
def create_relation():
    node_key1 = request.args.get('node_key1', 'uid')  # uid,event_id
    node1_id = request.args.get('node1_id', '1974576991,1895431523')
    node1_list = node1_id.split(',')
    node1_index_name = request.args.get('node1_index_name', 'node_index')  # node_index event_index
    rel = request.args.get('rel', 'group')
    node_key2 = request.args.get('node_key2', 'group')  
    node2_id = request.args.get('node2_id', u'美选群体')
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    node2_index_name = request.args.get('node2_index_name', 'group_index')
    node2_id = node2_id + '_' + submit_user
    flag = create_group_relation(node_key1, node1_list, node1_index_name, rel, \
                                node_key2, node2_id, node2_index_name, submit_user)
    return json.dumps(flag)

@mod.route('/group_detail/')
def detail_group():  #群体包含人物
    g_name = request.args.get('g_name', u'美选群体')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    g_name = g_name + '_' + submit_user
    detail_t = query_detail_group(g_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/del_user_in_group/')
def del_user_in_group():  #群体编辑-删除用户
    g_name = request.args.get('g_name', u'美选群体')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    g_name = g_name + '_' + submit_user
    uid = request.args.get('uid', u'1895431523')
    flag = del_u_group_rel(g_name, uid)
    return json.dumps(flag)

@mod.route('/group_add_tag/')
def group_add_tag():  #群体编辑-添加标签,删除标签
    g_name = request.args.get('g_name', u'美选群体')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    g_name = g_name + '_' + submit_user
    k_label = request.args.get('k_label', u'11月9号')
    operation = request.args.get('operation', 'del') #add del
    flag = add_group_k_label(g_name, k_label, operation)
    return json.dumps(flag)

@mod.route('/group_edit_file/')
def group_edit_file():  #群体编辑-添加资源文档链接
    g_name = request.args.get('g_name', u'美选群体')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    g_name = g_name + '_' + submit_user
    file_name = request.args.get('file_name', u'希拉里新闻,www.baidu.com')  #name,url+name2,url2
    operation = request.args.get('operation', 'add') #add del
    flag = add_group_file_link(g_name, file_name, operation)
    return json.dumps(flag)

@mod.route('/get_difference_user/')  #对比,包含人物
def ajax_get_difference_user():
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    g_name1 = request.args.get('g_name1', u'美选群体')  # uid,event_id
    g_name1 = g_name1 + '_' + submit_user
    g_name2 = request.args.get('g_name2', u'政治群体')  # uid,event_id
    g_name2 = g_name2 + '_' + submit_user
    flag = request.args.get('flag', 'same')   #all, diff same
    result = compare_group_user(g_name1, g_name2, submit_user, flag)
    return json.dumps(result)

@mod.route('/get_difference_event/')  #对比,关联事件
def ajax_get_difference():
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    g_name1 = request.args.get('g_name1', u'美选群体')  # uid,event_id
    g_name1 = g_name1 + '_' + submit_user
    g_name2 = request.args.get('g_name2', u'政治群体')  # uid,event_id
    g_name2 = g_name2 + '_' + submit_user
    flag = request.args.get('flag', 'all')   #all, diff same
    result = compare_group_event(g_name1, g_name2, submit_user, flag)
    return json.dumps(result)

@mod.route('/get_difference_keywords/')  #对比,自动标签
def ajax_get_difference_keywords():
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    g_name1 = request.args.get('g_name1', u'美选群体')  # uid,event_id
    g_name1 = g_name1 + '_' + submit_user
    g_name2 = request.args.get('g_name2', u'政治群体')  # uid,event_id
    g_name2 = g_name2 + '_' + submit_user
    flag = request.args.get('flag', 'all')   #all, diff same
    result = compare_group_keywords(g_name1, g_name2, submit_user, flag)
    return json.dumps(result)

@mod.route('/get_difference_k_label/')  #对比,业务标签
def ajax_get_difference_k_label():
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    g_name1 = request.args.get('g_name1', u'美选群体')  # uid,event_id
    g_name1 = g_name1 + '_' + submit_user
    g_name2 = request.args.get('g_name2', u'政治群体')  # uid,event_id
    g_name2 = g_name2 + '_' + submit_user
    flag = request.args.get('flag', 'diff')   #all, diff same
    result = compare_group_k_label(g_name1, g_name2, submit_user, flag)
    return json.dumps(result)

@mod.route('/group_basic/')
def detail_group_basic():  #群体基本信息
    g_name = request.args.get('g_name', u'美选群体')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    detail_t = get_group(g_name, submit_user)
    return json.dumps(detail_t)

# @mod.route('/group_basic/')
# def detail_group_basic():  #群体基本信息
#     g_name = request.args.get('g_name', u'美选群体')
#     submit_user = request.args.get('submit_user', u'admin@qq.com')
#     detail_t = group_geo_vary(g_name, submit_user)
#     return json.dumps(detail_t)