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
from search_protrait import *
from knowledge.global_utils import graph,es_related_docs, user_docs_name, user_docs_type, event_docs_name, event_docs_type
from GetUrl import getUrlByKeyWord,getUrlByKeyWordList
mod = Blueprint('index', __name__, url_prefix='/index')

@mod.route('/')
@login_required
def index():#首页

    user_name = g.user.email

    peo_infors = get_people(user_name,2)

    try:
        peo_string = 'MATCH(n:%s) return count(n)' % people_node#'START start_node=node:'+node_index_name+'("'+people_primary+':*") return count(start_node)'
        peo_object = graph.run(peo_string)

        for item in peo_object:
            peo_count = item['count(n)']
    except:
        peo_count = 0

    try:
        org_string = 'MATCH(n:%s) return count(n)' % org_node#'START start_node=node:'+org_index_name+'("'+org_primary+':*") return count(start_node)'
        org_object = graph.run(org_string)
        for item in org_object:
            org_count = item['count(n)']
    except:
        org_count = 0

    try:
        event_string = 'MATCH(n:%s) return count(n)' % event_node#'START start_node=node:'+event_index_name+'("'+event_primary+':*") return count(start_node)'
        event_object = graph.run(event_string)
        for item in event_object:
            event_count = item['count(n)']
    except:
        event_count = 0

    try:
        special_event_string = 'MATCH(n:%s) return count(n)' % special_event_node#'START start_node=node:'+special_event_index_name+'(\"'+special_event_primary+':*") return count(start_node)'
        special_event_object = graph.run(special_event_string)
        for item in special_event_object:
            special_event_count = item['count(n)']
    except:
        special_event_count = 0

    try:
        group_string = 'MATCH(n:%s) return count(n)' % group_node#'START start_node=node:'+group_index_name+'("'+group_primary+':*") return count(start_node)'
        group_object = graph.run(group_string)
        for item in group_object:
            group_count = item['count(n)']
    except:
        group_count = 0

    try:
        wiki_string = 'MATCH(n:%s) return count(n)' % wiki_node#'START start_node=node:'+wiki_url_index_name+'("'+wiki_primary+':*") return count(start_node)'
        wiki_object = graph.run(wiki_string)
        for item in wiki_object:
            wiki_count = item['count(n)']
    except:
        wiki_count = 0

    neo_count = {'people':peo_count, 'org':org_count, 'event':event_count, 'special_event':special_event_count, 'group':group_count, 'wiki':wiki_count}
    
    weibo_list = get_hot_weibo()

    people_list = get_hot_people()    
    
    return render_template('index/knowledge_home.html', peo_infors = peo_infors, neo_count = neo_count, weibo_list = weibo_list,\
                           people_list = people_list)

@mod.route('/get_index_map/')
def get_index_map():#地图

    map_count = get_map_count(5000)

    return json.dumps(map_count)

@mod.route('/graph/', methods=['GET','POST'])
@login_required
def get_graph():#图谱页面

    user_id = request.args.get('user_id', '')
    node_type = request.args.get('node_type', '')
    #result_na = request.args.get('result_na', '')

    if node_type == 'people':#人物节点图谱
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
    elif node_type == 'wiki':#维基节点图谱
        relation = get_wiki_graph(user_id)
        flag = 'Success'
    else:
        relation = []
        flag = 'Wrong Type'
    
    return render_template('index/knowledgeGraph.html', relation = relation, flag = flag)

@mod.route('/graph_index/')
@login_required
def get_graph_index():#首页图谱页面

    result_na = request.args.get('flag_type', '')
    if result_na:
        relation = []
        flag = 'Wrong Type'        
    else:
        relation = get_all_graph()
        flag = 'Success'
    
    return render_template('index/knowledgeGraph_home.html', relation = relation, flag = flag)

@mod.route('/map/', methods=['GET','POST'])
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

    data_dict = {'event':event_result,'people':people_result,'org':org_relation}

    return render_template('index/baidu_map.html', data_dict = data_dict, flag = flag)

@mod.route('/person/', methods=['GET','POST'])
@login_required
def get_person_atr():#人物属性页面

    user_id = request.args.get('user_id', '')
    user_name = g.user.email
    ### 人物属性查询函数
    if user_id:
        result_att = search_person_by_id(user_id,user_name)#查找人物属性
        doc_list = search_related_docs(user_id,es_related_docs,user_docs_name,user_docs_type)#查找关联文档
        inter_list = get_interaction(user_id)#查找人物交互情况
        friends_dict = search_bci(user_id)#查找人物的影响力信息
        text_list = get_people_weibo(user_id)#查找人物的微博文本
    else:
        result_att = {}
        doc_list = []
        inter_list = {'retweet':[],'beretweet':[],'comment':[],'becomment':[]}
        friends_dict = {'fansnum':'', 'statusnum':'', 'friendnum':''}
        text_list = []

    ### 获取相关wiki
    try:
        if result_att['uname']:#name不为空
            wiki_list = getUrlByKeyWord(result_att['uname'])
        else:
            wiki_list = []
    except KeyError:
        wiki_list = []

    ### 获取关联实体
    if user_id:
        relation_dict = search_neo4j_by_uid(user_id,node_index_name,people_primary)
    else:
        relation_dict = {'people':[],'org':[],'event':[]}
    
    relation_dict['wiki'] = wiki_list[0:10]
    relation_dict['doc'] = doc_list[0:10]

    return render_template('index/person.html',result_att = result_att,inter_list = inter_list,friends_dict = friends_dict,text_list = text_list,relation_dict = relation_dict)

@mod.route('/event/', methods=['GET','POST'])
@login_required
def get_event_atr():#事件属性页面

    user_id = request.args.get('user_id', '')
    user_name = g.user.email
    ### 事件属性查询函数
    if user_id:
        result_att = search_event_by_id(user_id,user_name)
        doc_list = search_related_docs(user_id,es_related_docs,event_docs_name,event_docs_type)#查找关联文档
        all_weibo,media_weibo,people_weibo = get_event_weibo(user_id)
    else:
        result_att = {}
        doc_list = []
        all_weibo,media_weibo,people_weibo = [],[],[]

    ### 获取相关wiki
    try:
        if result_att['name']:#name不为空
            key_words = result_att['name'].split('&') 
            wiki_list = getUrlByKeyWordList(key_words)
        else:
            wiki_list = []
    except KeyError:
        wiki_list = []
    
    ### 获取关联实体
    if user_id:
        relation_dict = search_neo4j_by_uid(user_id,event_index_name,event_primary)
    else:
        relation_dict = {'people':[],'org':[],'event':[]}
    
    relation_dict['wiki'] = wiki_list[0:10]
    relation_dict['doc'] = doc_list[0:10]
    
    text_list = {'all':all_weibo,'media':media_weibo,'people':people_weibo}

    return render_template('index/event.html',result_att = result_att,text_list = text_list,relation_dict = relation_dict)

@mod.route('/organization/', methods=['GET','POST'])
@login_required
def get_organization():#机构属性页面

    user_id = request.args.get('user_id', '')
    user_name = g.user.email
    ### 机构属性查询函数
    if user_id:
        result_att = search_org_by_id(user_id,user_name)
        doc_list = search_related_docs(user_id,es_related_docs,user_docs_name,user_docs_type)#查找关联文档
        inter_list = get_interaction(user_id)#查找人物交互情况
        friends_dict = search_bci(user_id)#查找人物的影响力信息
        text_list = get_people_weibo(user_id)#查找人物的微博文本
    else:
        result_att = {}
        doc_list = []
        inter_list = {'retweet':[],'beretweet':[],'comment':[],'becomment':[]}
        friends_dict = {'fansnum':'', 'statusnum':'', 'friendnum':''}
        text_list = []

    ### 获取相关wiki
    try:
        if result_att['uname']:#name不为空
            wiki_list = getUrlByKeyWord(result_att['uname'])
        else:
            wiki_list = []
    except KeyError:
        wiki_list = []

    ### 获取关联实体
    if user_id:
        relation_dict = search_neo4j_by_uid(user_id,org_index_name,org_primary)
    else:
        relation_dict = {'people':[],'org':[],'event':[]}
    
    relation_dict['wiki'] = wiki_list[0:10]
    relation_dict['doc'] = doc_list[0:10]

    return render_template('index/organization.html',result_att = result_att,inter_list = inter_list,friends_dict = friends_dict,text_list = text_list,relation_dict = relation_dict)

@mod.route('/cards/', methods=['GET','POST'])
@login_required
def get_card():#卡片罗列页面

    user_id = request.args.get('user_id', '')
    node_type = request.args.get('node_type', 'Not Found')
    card_type = request.args.get('card_type', 'Not Found')
    user_name = g.user.email
    
    if user_id:
        if node_type == '3':#专题关联
            if card_type == '1':#人物
                uid_list = user_id.split(',')
                result = get_detail_person(uid_list,user_name)
                flag = 1
            elif card_type == '2':#事件
                uid_list = user_id.split(',')
                result = get_detail_event(uid_list,user_name)
                flag = 2
            elif card_type == '0':#机构
                uid_list = user_id.split(',')
                result = get_detail_org(uid_list,user_name)
                flag = 0
            else:#有错误
                result = {}
                flag = -1
        elif node_type == '4':#群体关联
            if card_type == '1':#人物
                uid_list = user_id.split(',')
                result = get_detail_person(uid_list,user_name)
                flag = 1
            elif card_type == '2':#事件
                uid_list = user_id.split(',')
                result = get_detail_event(uid_list,user_name)
                flag = 2
            elif card_type == '0':#机构
                uid_list = user_id.split(',')
                result = get_detail_org(uid_list,user_name)
                flag = 0
            else:#有错误
                result = {}
                flag = -1
        else:#其他关联
            result,flag = get_relation_node(user_id,node_type,card_type,user_name)#获取关联节点
    else:
        result = {}
        flag = -1

    return render_template('index/card_display.html', result = result, flag = flag)

@mod.route('/card_rank/', methods=['GET','POST'])
def card_rank():#卡片罗列页面排序

    rank_data = request.form['r_data']
    node_type = request.form['node_type']
    rank_type = request.form['rank_type']

    if rank_data:
        if node_type == '1':#人物节点
            result = rank_people_card_data(eval(rank_data),rank_type)
            flag = 1
        elif node_type == '2':#事件节点
            result = rank_event_card_data(eval(rank_data),rank_type)
            flag = 2
        elif node_type == '0':#事件节点
            result = rank_org_card_data(eval(rank_data),rank_type)
            flag = 0
        else:#其他关联
            result = {}
            flag = -1
    else:
        result = {}
        flag = -1

    return json.dumps(result)

@mod.route('/show_attention/', methods=['GET','POST'])
def show_attention():

    user_name = request.form['user_name']
    s_type = request.form['s_type']

    if s_type == 'people':
        infors = get_people(user_name,2)
    elif s_type == 'event':
        infors = get_event(user_name,2)
    else:
        infors = get_org(user_name,2)

    return json.dumps(infors)

@mod.route('/get_media_weibo/', methods=['GET','POST'])
def get_media_weibo():#获取媒体发布的weibo

    #event_id = request.args.get('event_id', '')
    event_id = request.form['event_id']
    if event_id:
        result = get_event_weibo_by_type(event_id,['3'])
    else:
        result = []

    return json.dumps(result)

@mod.route('/get_user_weibo/', methods=['GET','POST'])
def get_user_weibo():#获取网民发布的weibo

    #event_id = request.args.get('event_id', '')
    event_id = request.form['event_id']
    if event_id:
        result = get_event_weibo_by_type(event_id,['-1','0','200','220'])
    else:
        result = []

    return json.dumps(result)    

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

    
