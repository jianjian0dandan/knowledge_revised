# -*-coding:utf-8-*-

import time
import json
from knowledge.global_config import portrait_name, portrait_type, event_name, event_analysis_name, \
        neo4j_name, event_type, event_special, special_event_index_name, group_index_name, \
        group_rel, node_index_name,user_tag,relation_list
from knowledge.global_utils import es_user_portrait, es_event, graph,\
        user_name_search,event_name_search
from knowledge.time_utils import ts2datetime, datetime2ts
from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property
from py2neo.packages.httpstream import http
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
http.socket_timeout = 9999


def create_node_or_node_rel(node_key1, node1_id, node1_index_name, rel, node_key2, node2_id, node2_index_name):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node1_index_name)
    group_index = Index.get_index(Node, node2_index_name)
    print node_index
    print group_index
    tx = graph.begin()
    node1 = node_index.get(node_key1, node1_id)[0]
    node2 = group_index.get(node_key2, node2_id)[0]
    if not (node1 and node2):
        print "node does not exist"
        return '1'
    c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" % (
    node1_index_name, 'pname', node1_id, node2_index_name, 'pname', node2_id, rel)
    print c_string
    result = graph.run(c_string)
    print result
    rel_list = []
    for item in result:
        rel_list.append(item)
    print rel_list
    if not rel_list:
        rel = Relationship(node1, rel, node2)
        graph.create(rel)
        print "create success"
    else:
        print "The current two nodes already have a relationship"
    	return '0'
    return '2'
