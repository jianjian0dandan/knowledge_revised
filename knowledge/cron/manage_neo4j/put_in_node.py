# -*-coding:utf-8-*-

import time
import json
import redis
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property
from py2neo.packages.httpstream import http
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
http.socket_timeout = 9999

graph = Graph('http://219.224.134.213:7474/db/data', user="neo4j", password="database")
#graph = Graph()
#r = redis.StrictRedis(host="219.224.134.211", port="7381", db=15)

class User(GraphObject):
    __primarykey__ = "uid"
    uid = Property()


def put_in():
    Index = ManualIndexManager(graph) # manage index
    tx = graph.begin()
    count = 0
    index_list = [] # temporal put in
    filter_set = set()
    ts = time.time()
    node_name = "node_index"
    #rel_name = "rel_index"
    node_index = Index.get_or_create_index(Node, node_name)
    #rel_index = Index.get_or_create_index(Relationship, rel_name)
    Batch_index = ManualIndexWriteBatch(graph)
    user_list = json.loads(r.get("user_set"))
    for user in user_list:
        #st_node = Index.get_or_create_indexed_node(node_name, "uid", start_node, {"uid":start_node})
        #ed_node = Index.get_or_create_indexed_node(node_name, "uid", end_node, {"uid":end_node})
        exist = Index.get_indexed_node(node_name, "uid", user)
        if not exist and user not in filter_set:
            node = Node("User", uid=user)
            tx.create(node)
            index_list.append([user, node])
            filter_set.add(node)

        count += 1
        if count % 1000 == 0:
            print count
            te = time.time()
            print "cost time: %s" %(te-ts)
            ts = te
            tx.commit()
            tx = graph.begin()
            for item in index_list:
                Batch_index.add_to_index(Node, node_name, "uid", item[0], item[1])
            index_list = []
            filter_set = set()
    tx.commit()


def put_in_user_portrait():
    Index = ManualIndexManager(graph) # manage index
    Batch_index = ManualIndexWriteBatch(graph)
    tx = graph.begin()
    index_list = [] # temporal put in
    node_name = "node_index"
    node_index = Index.get_index(Node, node_name)

    f = open("user_portrait.txt", "rb")
    count = 0
    filter_set = set()
    for item in f:
        user_dict = json.loads(item)
        user = user_dict["uid"]
        exist = node_index.get("uid", user)
        if not exist and user not in filter_set:
            node = Node("User", uid=user)
            tx.create(node)
            index_list.append([user, node])
            filter_set.add(node)

            count += 1
            if count % 1000 == 0:
                print count
                tx.commit()
                tx = graph.begin()
                for item in index_list:
                    node_index.add("uid", item[0], item[1])
                    #Batch_index.add_to_index(Node, node_name, "uid", item[0], item[1])
                index_list = []
                filter_set = set()
    tx.commit()
    if index_list:
        for item in index_list:
            node_index.add("uid", item[0], item[1])
            #Batch_index.add_to_index(Node, node_name, "uid", item[0], item[1])
    print count


    f.close()

if __name__ == "__main__":
    #put_in()
    put_in_user_portrait()

