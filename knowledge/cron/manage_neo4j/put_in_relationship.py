# -*-coding:utf-8-*-

import time
import json
import sys
import random
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property
from py2neo.packages.httpstream import http
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
http.socket_timeout = 9999

reload(sys)
sys.path.append('../../')
from global_config import node_index_name, friend, interaction, relative, colleague, leader_member, user_tag, group_index_name,\
                        group_rel, event_index_name
from global_utils import graph, es_user_portrait

class User(GraphObject):
    __primarykey__ = "uid"
    uid = Property()

def create_user2user_rel(uid_list,rel_type):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    tx = graph.begin()
    count = 0

    """
    f = open("user_portrait.txt", "rb")
    uid_list = []
    for line in f:
        user_dict = json.loads(line)
        uid = user_dict["uid"]
        uid_list.append(uid)
    """

    for i in range(len(uid_list)-1):
        for j in range(i+1,len(uid_list)):
            user1 = uid_list[i]
            user2 = uid_list[j]
            user_node1 = node_index.get("uid", user1)[0]
            user_node2 = node_index.get("uid", user2)[0]
            prob = random.random()
            if prob <= 0.03:
                rel = Relationship(user_node1, rel_type, user_node2)
                tx.create(rel)
                count += 1
                if count % 100 == 0:
                    tx.commit()
                    print count
                    tx = graph.begin()
    tx.commit()
    print "finish"


def create_rel_from_uid2group(uid_list, group_id):
    count = 0
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    group_index = Index.get_index(Node, group_index_name)

    tx = graph.begin()
    for user in uid_list:
        exist = node_index.get("uid", user)
        if exist:
            node = exist[0]
        else:
            node = Node("User", uid=user)
            graph.create(node)
            node_index.add("uid", user, node)
        group_node = group_index.get("group", group_id)[0]
        rel = Relationship(node, group_rel, group_node)
        tx.create(rel)
        count += 1
        if count % 100 == 0:
            tx.commit()
            print count
            tx = graph.begin()
    tx.commit()


def create_rel_uid2event(uid_list, event_id, rel_type):
    count = 0
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    event_index = Index.get_index(Node, event_index_name)

    tx = graph.begin()
    for user in uid_list:
        exist = node_index.get("uid", user)
        if exist:
            node = exist[0]
        else:
            node = Node("User", uid=user)
            graph.create(node)
            node_index.add("uid", user, node)
        event_node = event_index.get("event", event_id)[0]
        rel = Relationship(node, rel_type, event_node)
        tx.create(rel)
        count += 1
        if count % 100 == 0:
            tx.commit()
            print count
            tx = graph.begin()
    tx.commit()


def query_db():
    Index = ManualIndexManager(graph) # manage index
    #node_1 = Index.get_indexed_node("uid_index", "uid", "3293303045")
    node_1 = Index.get_indexed_node("uid_index", "uid", "2139111593")
    c_string = "MATCH (node_1)-[:retweet]->(fof) RETURN fof.uid"
    result = graph.run(c_string)
    uid_set = []
    count = 0
    for item in graph.run(c_string):
        uid_set.append(item['fof.uid'])
        count += 1
    print count
    print len(uid_set)
    print sorted(uid_set)[:20]



if __name__ == "__main__":
    user_set = set()
    with open("event_user_list.txt", "r") as f:
        for line in f:
            user_set.add(line.strip())
    for each in [interaction, relative, colleague, leader_member]:
        create_user2user_rel(list(user_set),each)
    """
    results = es_user_portrait.search(index="user_portrait", doc_type="user", body={"query":{"term":{"domain":"媒体"}}, "size":150})["hits"]["hits"]
    uid_list = []
    for item in results:
        uid_list.append(item["_id"])
    print uid_list
    create_rel_from_uid2group(uid_list, "媒体")
    """


