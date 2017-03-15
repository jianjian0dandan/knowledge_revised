# -*-coding:utf-8-*-
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect,make_response,request
from neo4j_event import select_rels_all, select_rels, create_person, create_rel_from_uid2group, create_node_or_node_rel, \
    update_node, update_node_or_node_rel, delete_rel, delete_node,nodes_rels,get_es_status,select_event_es,\
    select_people_es
from knowledge.global_config import *
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from draw_redis import *

# from knowledge.global_utils import event_name_search

mod = Blueprint('construction', __name__, url_prefix='/construction')


@mod.route('/node/')
def add_node():
    return render_template('construction/addmap.html')


@mod.route('/relation/')
def add_relation():
    return render_template('construction/compile.html')


@mod.route('/read_file/', methods=['GET', 'POST'])
def read_node():
    f_name = request.form['new_words']

    uid_list = []
    line = f_name.split('\n')
    if len(line) == 0:
        return json.dumps('No Content!')

    for li in line:
        uid_list.append(li)

    return json.dumps(uid_list)

@mod.route('/read_relation/', methods=['GET', 'POST'])
def read_relation():
    f_name = request.form['new_words']

    uid_list = []
    line = f_name.split('\n')
    if len(line) == 0:
        return json.dumps('No Content!')

    for li in line:
        n1,t1,r,n2,t2 = li.split(',')
        uid_list.append([[t1,n1],r,[t2,n2]])

    return json.dumps(uid_list)


@mod.route('/select_relation/')
def select_relation():
    result_dict = {}
    list = []
    list1 = []
    result = select_rels_all("MATCH (n:Person)-[r]->(m) return n.uid,r,m.uid")
    for item in result:
        id = item[0]
        friend = item[1].type()
        print friend
        id2 = item[2]
        a = (id, friend, id2)
        list.append(a)
        list1.append(id)
        list1.append(id2)
    list1_set = [i for i in set(list1)]
    result_dict["relation"] = list
    result_dict["node"] = list1_set
    return json.dumps(result_dict)


# select node
@mod.route('/select_node/')
def select_node():
    list = []
    list_set = []
    result = select_rels_all("MATCH (n:Person)-[r]-() return n")
    for item in result:
        list.append(item)
    list_set = [i for i in set(list)]
    return json.dumps(list_set)


@mod.route('/select_event/')
def select_event_relation():
    result_dict = {}
    list = []
    list1 = []
    result = select_rels_all("MATCH (n:Person)-[r:admin]->(m) return n.uid,r,m.event_id")
    for item in result:
        id = item[0]
        friend = item[1].type()
        print friend
        id2 = item[2]
        a = (id, friend, id2)
        list.append(a)
        list1.append(id)
        list1.append(id2)
    list1_set = [i for i in set(list1)]
    result_dict["relation"] = list
    result_dict["node"] = list1_set
    return json.dumps(result_dict)


@mod.route('/select_event_node/')
def select_event_node():
    list = []
    list_set = []
    result = select_rels_all("MATCH (n:Person)-[r:admin]-(m) return n,m")
    for item in result:
        list.append(item[1])
        # list.append(item[2])
    list_set = [i for i in set(list)]
    return json.dumps(list_set)


@mod.route('/create_relation/')
def create_relation():
    node_key1 = request.args.get('node_key1', 'uid')  # uid,event
    node1_id = request.args.get('node1_id', '1581366400')
    node1_index_name = request.args.get('node1_index_name', 'node_index')  # node_index event_index
    rel = request.args.get('rel', 'join')
    node_key2 = request.args.get('node_key2', 'event')  # event,uid
    node2_id = request.args.get('node2_id', 'min-jin-dang-yi-yuan-cheng-yao-qing-da-lai-dui-kang-da-lu-1482126431')
    node2_index_name = request.args.get('node2_index_name', 'event_index')
    flag = create_node_or_node_rel(node_key1, node1_id, node1_index_name, rel, \
                                   node_key2, node2_id, node2_index_name)
    return json.dumps(flag)


@mod.route('/event_node_create/')
def add_node_event():
    event_name = request.args.get('event_name', '')
    event_type = request.args.get('event_type', '')
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    upload_time = request.args.get('upload_time', '')
    if event_name == '' or event_type == '' or start_time == '' or end_time == '' or upload_time == '':
        print ("event is null")
        return '0'
    event_push_redis(event_name, event_type, start_time, end_time, upload_time)
    return '1'


@mod.route('/user_upload_file/')
def upload_file():
    uid_list = request.args.get('uid_list', '')
    upload_time = request.args.get('upload_time', '')
    if uid_list == '' or upload_time == '':
        print ("null")
        return '0'
    print uid_list
    task_name = "user" + "-" + len(uid_list) + str(upload_time)
    user_push_redis(uid_list, task_name, upload_time)
    return '1'


# 对进来的数据进行模糊查询
@mod.route('/fuzzy_query/')
def fuzzy_query():
    node_type = request.args.get('node_type', '')
    uid = request.args.get('uid', '')
    if node_type == '' or uid == '':
        print "incoming there null"
        return '0'
    if node_type == '1':  # user query
        c_string = "start n = node:%s('uid:*%s*') match (n) return n.uid order by n.id limit 50" % (node_index_name, uid)
        print c_string
        result = select_rels_all(c_string)
        result = select_people_es(result)
        return json.dumps(result)
    elif node_type == '2':  # event query
        c_string = "start n = node:%s('event:*%s*') match (n) return n order by n.id limit 50" % (event_index_name, uid)
        result = select_rels_all(c_string)
        result = select_event_es(result)
        return json.dumps(result)
    else:
        print "node_type is error"
        return '0'


# 对节点进行更新
@mod.route('/update_node/')
def update_nodes():
    node_type = request.args.get('node_type', '')
    uid = request.args.get('uid', '')
    attribute_dict = request.args.get('attribute_dict', '')
    if node_type == '' or uid == '' or attribute_dict == '':
        print "incoming there null"
        return '0'
    if node_type == '1':  # user update
        result = update_node("uid", uid, node_index_name, attribute_dict)
        if result:
            return "1"
        else:
            return "0"
    elif node_type == '2':  # event update
        result = update_node("event", uid, event_index_name, attribute_dict)
        if result:
            return "1"
        else:
            return "0"
    else:
        print "node_type is error"
        return "0"


# 删除节点   其中node_type代表传进来是对象，来判断是user还是event
@mod.route('/delete_node/')
def delete_nodes():
    node_type = request.args.get('node_type', '')
    uid = request.args.get('uid', '')
    if node_type == '' or uid == '':
        print "incoming there null"
        return '0'
    if node_type == '1':  # user update
        result = delete_node("uid", uid, node_index_name)
        if result:
            return "1"
        else:
            return "0"
    elif node_type == '2':  # event update
        result = delete_node("event", uid, event_index_name)
        if result:
            return "1"
        else:
            return "0"
    else:
        print "node_type is error"
        return "0"

#少一个添加！！一会写上。


# 对2个节点的关系进行模糊查询
@mod.route('/node_or_node_query/')
def node_or_node_query():
    node1_uid = request.args.get('node1_uid', '')
    node1_type = request.args.get('node1_type','')
    node2_uid = request.args.get('node2_uid', '')
    node2_type = request.args.get('node2_type','')
    if node1_type== '2':
        node1_index_name=event_index_name
    else:
        node1_index_name=node_index_name
    if node2_type== '2':
        node2_index_name=event_index_name
    else:
        node2_index_name=node_index_name
    if node1_uid == '' or node2_uid == '':
        print ("incoming there null")
        return '0'
    c_string = "start start_node= node:%s('uid:*%s*'),end_node=node:%s('uid:*%s*') match (start_node)-[r]->(end_node) return start_node.uid,start_node.uname,r,end_node.uid,end_node.uname order by start_node.id limit 10" \
                % (node1_index_name, node1_uid, node2_index_name, node2_uid)
    print c_string
    result = select_rels_all(c_string)
    list = []
    for item in result:
        uid1 = item[0]
        uname1 = item[1]
        rel = item[2].type()
        uid2 = item[3]
        uname2 = item[4]

        result={}
        result["uid1"]=uid1
        result["uname1"]=uname1
        result["rel"]=rel
        result["uid2"]=uid2
        result["uname2"]=uname2
        list.append(result)
    return json.dumps(list)


# 对模糊查询的节点关系进行删除。
@mod.route('/node_or_node_delete/')
def node_or_node_delete():
    node1_uid = request.args.get('node1_uid', '')
    node2_uid = request.args.get('node2_uid', '')
    rel = request.args.get('rel', '')
    if node1_uid == '' or node2_uid == '':
        print "incoming there null"
    result = delete_rel('uid', node1_uid, node_index_name, rel, 'uid', node2_uid, node_index_name)
    if result:
        return '1'
    else:
        return '0'


# 对模糊查询的节点关系进行修改。
@mod.route('/node_or_node_update/')
def node_or_node_update():
    node1_uid = request.args.get('node1_uid', '')
    node2_uid = request.args.get('node2_uid', '')
    old_rel = request.args.get('old_rel', '')
    new_rel = request.args.get('new_rel', '')
    result =update_node_or_node_rel('uid',node1_uid,node_index_name,old_rel,new_rel,'uid',node2_uid,node_index_name)
    if result:
        return '1'
    else:
        return '0'

@mod.route('/nodes_or_nodes_rel/', methods=['GET', 'POST'])
def nodes_create_rels():
    result = request.args.get("list",'')
    result = result.split("|")
    list = []
    if len(result)==1:
        print "1"
        result =eval(result[0])
        list  = [[[result[0],result[1]],result[2],[result[3],result[4]]],]
    else :
        for item in result:
            item = eval(item)
            list.append([[item[0],item[1]],item[2],[item[3],item[4]]])
    result = nodes_rels(list)
    return json.dumps(result)



################################
@mod.route('/select_event_status/')
def select_event_status():
    list =[]
    results =get_es_status("event_status")
    for item in results:
        result= item["_source"]
        result["id"] =item["_id"]
        list.append(result)
    return json.dumps(list)


@mod.route('/select_user_status/')
def select_user_status():
    list =[]
    results =get_es_status("user_status")
    for item in results:
        result= item["_source"]
        result["id"] =item["_id"]
        list.append(result)
    return json.dumps(list)



@mod.route('/set_session/')
def set_session():
    response = make_response("hellow")
    response.set_cookie("Name","zhaishujie")
    return response

@mod.route('/get_session/')
def get_session():
    return request.cookies.get("Name")
