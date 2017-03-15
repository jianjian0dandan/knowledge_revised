# -*-coding:utf-8-*-
import json
import sys
from py2neo.ext.batman import ManualIndexManager
from py2neo import Node, Relationship
from py2neo.packages.httpstream import http
from py2neo.ogm import GraphObject
from myutil import get_type_key
sys.path.append('../../')
from global_utils import graph,es_event as es
from global_config import *

http.socket_timeout = 9999

# 多对多创建节点关系([node1_type,node1_id],rel,[node2_type,node2_id])
def nodes_rels(list):
    result = ''
    count = 0
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    event_index = Index.get_index(Node, event_index_name)
    org_index = Index.get_index(Node, org_index_name)
    tx = graph.begin()
    if not (node_index and event_index):
        return 'Relation Wrong'
    
    for item in list:
        node1_key = get_type_key(item[0][0])
        node2_key = get_type_key(item[2][0])
        node1_uid = item[0][1]
        node2_uid = item[2][1]
        rel = item[1]
        if node1_key == '' or node2_key == '' or node1_uid == '' or node2_uid == '' or rel == '':
            continue
        flag = 0
        if node1_key == "uid":
            if node2_key == 'uid':
                node1 = node_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                node1 = node1[0]
                node2 = node_index.get(node2_key, node2_uid)
                if (node2 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                node2 = node2[0]
                print 'Person-Person'

            elif node2_key == 'event':
                node1 = node_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                else:
                    node1 = node1[0]
                node2 = event_index.get(node2_key, node2_uid)
                if (node1 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                else:
                    node2 = node2[0]
                print 'Person-Event'
            else:
                node1 = node_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                else:
                    node1 = node1[0]
                node2 = org_index.get(node2_key, node2_uid)
                if (node1 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                else:
                    node2 = node2[0]
                print 'Person-Org'

        elif node1_key == 'event':
            if node2_key == 'uid':
                node1 = event_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                else:
                    node1 = node1[0]
                node2 = node_index.get(node2_key, node2_uid)
                if (node1 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                else:
                    node2 = node2[0]
                print 'Event-Person'
            elif node2_key == 'event':
                node1 = event_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                else:
                    node1 = node1[0]
                node2 = event_index.get(node2_key, node2_uid)
                if (node1 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                else:
                    node2 = node2[0]
                print 'Event-Event'
            else:
                node1 = event_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                else:
                    node1 = node1[0]
                node2 = org_index.get(node2_key, node2_uid)
                if (node1 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                else:
                    node2 = node2[0]
                print 'Event-Org'
        else:
            if node2_key == 'uid':
                node1 = org_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                else:
                    node1 = node1[0]
                node2 = node_index.get(node2_key, node2_uid)
                if (node1 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                else:
                    node2 = node2[0]
                print 'Org-Person'
            elif node2_key == 'event':
                node1 = org_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                else:
                    node1 = node1[0]
                node2 = event_index.get(node2_key, node2_uid)
                if (node1 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                else:
                    node2 = node2[0]
                print 'Org-Event'
            else:
                node1 = org_index.get(node1_key, node1_uid)
                if (node1 == []):
                    result =result + ",%d" % node1_uid
                    flag=1
                else:
                    node1 = node1[0]
                node2 = org_index.get(node2_key, node2_uid)
                if (node1 == []):
                    result = result +",%d" % node2_uid
                    flag=1
                else:
                    node2 = node2[0]
                print 'Org-Org'
            
        if flag == 0:
            rel = Relationship(node1, rel, node2)
            tx.create(rel)
            count += 1
        if count % 100 == 0:
            tx.commit()
            tx = graph.begin()
    tx.commit()
    return 'Relation Success'

# 对数据进行存放
def create_person(node_type, node_key, node_id, node_name_index):
    Index = ManualIndexManager(graph)
    node_name = Index.get_or_create_index(Node, node_name_index)
    if node_name:
        exist = node_name.get(node_key, node_id)
        if exist:
            return 'Node Exist'#节点已存在
        else:
            person_node = Node(node_type, uid=node_id)
            graph.create(person_node)
            node_name.add(node_key, node_id, person_node)
            return 'Node Success'#创建节点成功
    else:
        return 'Node Wrong'#创建节点失败

# 返回需要的查询结果
def select_rels_all(c_string):
    list = []
    result = graph.run(c_string)
    for item in result:
        list.append(item)
    return list
