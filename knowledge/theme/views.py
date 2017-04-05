    # -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from xpinyin import Pinyin
from datetime import date
from datetime import datetime
from utils import search_related_e_card,  create_node_and_rel, create_rel,query_detail_theme, create_theme_relation,\
                  del_e_theme_rel, add_theme_k_label, add_theme_file_link, compare_theme, compare_theme_user, compare_theme_keywords,\
                  compare_theme_k_label, search_related_event, get_theme_flow, get_theme_geo, get_theme_net,\
                  get_theme_keywords, get_theme_user_rank, get_theme_user_tag, get_theme_related
from knowledge.global_utils import get_theme
p = Pinyin()

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
    theme_name = request.args.get('theme_name','')
    return render_template('theme/theme_modify.html',theme_name=theme_name)

@mod.route('/compare/')
@login_required
def theme_compare():#专题对比
    theme_name1 = request.args.get('theme_name1','')
    theme_name2 = request.args.get('theme_name2','')
    return render_template('theme/theme_compare.html',theme_name1=theme_name1,theme_name2=theme_name2)

@mod.route('/result/')
@login_required
def theme_result():#专题查看
    theme_name = request.args.get('theme_name','')
    return render_template('theme/theme_result.html',theme_name=theme_name)

@mod.route('/theme_overview/')
def ajax_event_overview():  #专题总览
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    result = get_theme('',submit_user)
    return json.dumps(result)

@mod.route('/search_related_event_item/')
def search_related_event_item():  #专题编辑-增加前先搜索事件,如果为已有专题添加，需加上专题名称，新建为空
    theme_name = request.args.get('theme_name', u'')
    search_item = request.args.get('item', u'北京')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    event_card = search_related_e_card(search_item, submit_user, theme_name)
    return json.dumps(event_card)

@mod.route('/search_related_event/')
def ajax_search_related_event():  #专题编辑，推荐与之相关的一跳事件
    theme_name = request.args.get('theme_name', u'房价')
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    event_card = search_related_event(theme_name, submit_user)
    return json.dumps(event_card)

@mod.route('/theme_detail/')
def detail_theme():  #专题包含事件
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    detail_t = query_detail_theme(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/del_event_in_theme/')
def del_event_in_theme():  #专题编辑-删除事件
    theme_name = request.args.get('theme_name', u'房价')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    event_id = request.args.get('event_id', u'te-lang-pu-1480176000')
    flag = del_e_theme_rel(theme_name, event_id)
    return json.dumps(flag)

@mod.route('/theme_add_tag/')
def theme_add_tag():  #专题编辑-添加标签,删除标签
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    k_label = request.args.get('k_label', u'11月8号')
    operation = request.args.get('operation', 'del') #add del
    flag = add_theme_k_label(theme_name, k_label, operation)
    return json.dumps(flag)

@mod.route('/theme_edit_file/')
def theme_edit_file():  #专题编辑-添加资源文档链接
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    file_name = request.args.get('file_name', u'档案,testurl+希拉里新闻,www.baidu.com')  #name,url+name2,url2
    operation = request.args.get('operation', 'add') #add del
    flag = add_theme_file_link(theme_name, file_name, operation)
    return json.dumps(flag)

@mod.route('/create_new_relation/')#添加到新专题
def create_new_relation():
    node_key1 = request.args.get('node_key1', 'event_id')  # uid,event_id
    node1_id = request.args.get('node1_id', 'te-lang-pu-1480176000,lu-han-1480176000')
    if node1_id == '':
    	return 'must add event'
    node1_list = node1_id.split(',')
    node1_index_name = request.args.get('node1_index_name', 'event_index')  # node_index event_index
    rel = request.args.get('rel', 'special_event')
    node_key2 = request.args.get('node_key2', 'event')  # event,uid
    node2_name = request.args.get('node2_id', u'政治专题5')
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    node2_id = node2_name + '_' + submit_user
    node2_index_name = request.args.get('node2_index_name', 'special_event_index')
    k_label = request.args.get('k_label', 'test') #split &
    flag = create_node_and_rel(node_key1, node1_list, node1_index_name, rel, \
                                   node_key2, node2_id, node2_index_name, submit_user, k_label, node2_name)
    return json.dumps(flag)

@mod.route('/create_relation/')#添加到已有专题
def create_relation():
    node_key1 = request.args.get('node_key1', 'event_id')  # uid,event_id
    # node1_id11 = 'lao-tai-ao-ye-mai-cai-wei-er-zi-mai-fang-1482126431,受骗后自杀'
    node1_id = request.args.get('node1_id', 'lu-han-1480176000')
    node1_list = node1_id.split(',')
    node1_index_name = request.args.get('node1_index_name', 'event_index')  # node_index event_index
    rel = request.args.get('rel', 'special_event')
    node_key2 = request.args.get('node_key2', 'event')  
    node2_id = request.args.get('node2_id', u'美国大选')
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    node2_index_name = request.args.get('node2_index_name', 'special_event_index')
    node2_id = node2_id + '_' + submit_user
    flag = create_theme_relation(node_key1, node1_list, node1_index_name, rel, \
                                   node_key2, node2_id, node2_index_name, submit_user)
    return json.dumps(flag)

@mod.route('/get_difference_event/')  #对比,包含事件
def ajax_get_difference():
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    theme_name1 = request.args.get('theme_name1', u'政治专题')  # uid,event_id
    theme_name1 = theme_name1 + '_' + submit_user
    theme_name2 = request.args.get('theme_name2', u'美国大选')  # uid,event_id
    theme_name2 = theme_name2 + '_' + submit_user
    flag = request.args.get('flag', 'all')   #all, diff same
    result = compare_theme(theme_name1, theme_name2, submit_user, flag)
    return json.dumps(result)

@mod.route('/get_difference_user/')  #对比,关联人物
def ajax_get_difference_user():
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    theme_name1 = request.args.get('theme_name1', u'政治专题')  # uid,event_id
    theme_name1 = theme_name1 + '_' + submit_user
    theme_name2 = request.args.get('theme_name2', u'美国大选')  # uid,event_id
    theme_name2 = theme_name2 + '_' + submit_user
    flag = request.args.get('flag', 'same')   #all, diff same
    result = compare_theme_user(theme_name1, theme_name2, submit_user, flag)
    return json.dumps(result)

@mod.route('/get_difference_keywords/')  #对比,自动标签
def ajax_get_difference_keywords():
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    theme_name1 = request.args.get('theme_name1', u'政治专题')  # uid,event_id
    theme_name1 = theme_name1 + '_' + submit_user
    theme_name2 = request.args.get('theme_name2', u'美国大选')  # uid,event_id
    theme_name2 = theme_name2 + '_' + submit_user
    flag = request.args.get('flag', 'same')   #all, diff same
    result = compare_theme_keywords(theme_name1, theme_name2, submit_user, flag)
    return json.dumps(result)

@mod.route('/get_difference_k_label/')  #对比,业务标签
def ajax_get_difference_k_label():
    submit_user = request.args.get('submit_user', 'admin@qq.com')
    theme_name1 = request.args.get('theme_name1', u'政治专题')  # uid,event_id
    theme_name1 = theme_name1 + '_' + submit_user
    theme_name2 = request.args.get('theme_name2', u'美国大选')  # uid,event_id
    theme_name2 = theme_name2 + '_' + submit_user
    flag = request.args.get('flag', 'same')   #all, diff same
    result = compare_theme_k_label(theme_name1, theme_name2, submit_user, flag)
    return json.dumps(result)

#专题分析
@mod.route('/theme_analysis_basic/')
def ajax_theme_analysis():  #专题基本信息
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    detail_t = get_theme(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/theme_analysis_flow/')
def ajax_theme_flow():  #专题鱼骨图
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    detail_t = get_theme_flow(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/theme_analysis_geo/')
def ajax_theme_geo():  #专题地域分析
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    detail_t = get_theme_geo(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/theme_analysis_net/')
def ajax_theme_net():  #专题网络分析
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    detail_t = get_theme_net(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/theme_analysis_keywords/')
def ajax_theme_keywords():  #专题包含事件的自动标签、关键词
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    detail_t = get_theme_keywords(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/theme_analysis_user_rank/')
def ajax_theme_user_rank():  #专题包含事件的用户排名
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    detail_t = get_theme_user_rank(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/theme_analysis_user_tag/')
def ajax_theme_user_tag():  #专题包含事件的用户自动标签页业务标签
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    detail_t = get_theme_user_tag(theme_name, submit_user)
    return json.dumps(detail_t)

@mod.route('/theme_analysis_related/')
def ajax_theme_related():  #专题的关联信息
    theme_name = request.args.get('theme_name', u'美国大选')
    submit_user = request.args.get('submit_user', u'admin@qq.com')
    theme_name = theme_name + '_' + submit_user
    detail_t = get_theme_related(theme_name, submit_user)
    return json.dumps(detail_t)  #[人，机构，事，资源, wiki]