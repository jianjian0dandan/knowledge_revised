# -*-coding:utf-8-*-

import time
import json
import redis
import sys
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property
from py2neo.packages.httpstream import http
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
http.socket_timeout = 9999

reload(sys)
sys.path.append("../../")
from global_config import location_index_name, node_index_name, domain_list, topic_list, special_event_index_name, event_index_name, event_special
from global_utils import graph


class User(GraphObject):
    __primarykey__ = "uid"
    uid = Property()

class Domain(GraphObject):
    __primarykey__ = "domain"
    domain = Property()

class Topic(GraphObject):
    __primarykey__ = 'topic'
    topic = Property()

class Location(GraphObject):
    __primarykey__ = 'location'
    location = Property()

class SpecialEvent(GraphObject):
    __primarykey__ = 'event'
    event = Property()

def create_node_location():
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    location_index = Index.get_or_create_index(Node, location_index_name)

    f = open("user_portrait.txt", "rb")
    count = 0
    update_node = []
    index_list = []
    in_set = set()
    tx = graph.begin()
    for item in f:
        user_dict = json.loads(item)
        each_location = user_dict["location"]
        exist = location_index.get("location", each_location)
        if not exist and each_location not in in_set:
            node = Node("Location", location=each_location)
            tx.create(node)
            index_list.append([each_location,node])
            count += 1
            in_set.add(each_location)
            if count % 10 == 0:
                print count
                tx.commit()
                tx = graph.begin()
                for item in index_list:
                    location_index.add("location", item[0], item[1])
                index_list = []
    tx.commit()
    if index_list:
        for item in index_list:
            location_index.add("location", item[0], item[1])
    print "all done"

    f.close()

def put_in_special_event(event_name):
    Index = ManualIndexManager(graph)
    special_event_index = Index.get_or_create_index(Node, special_event_index_name)

    exist = special_event_index.get("event", event_name)
    if not exist:
        node = Node("SpecialEvent", event=event_name)
        tx = graph.begin()
        tx.create(node)
        tx.commit()
        special_event_index.add("event", event_name, node)
        return 1
    return 0

def put_in_node():
    Index = ManualIndexManager(graph) # manage index
    tx = graph.begin()
    count = 0
    index_list = [] # temporal put in
    filter_set = set()
    ts = time.time()
    #domain_name = "domain_index"
    domain_name = "topic_index"
    domain_index = Index.get_or_create_index(Node, domain_name)
    Batch_index = ManualIndexWriteBatch(graph)

    #for item in domain_list:
    for item in topic_list:
        #st_node = Index.get_or_create_indexed_node(node_name, "uid", start_node, {"uid":start_node})
        #ed_node = Index.get_or_create_indexed_node(node_name, "uid", end_node, {"uid":end_node})
        #exist = Index.get_indexed_node(domain_name, "domain", item)
        exist = Index.get_indexed_node(domain_name, "topic", item)
        if not exist:
            #node = Node("Domain", domain=item)
            node = Node("Topic", topic=item)
            tx.create(node)
            index_list.append([item, node])
    tx.commit()
    for item in index_list:
        #domain_index.add('domain', item[0], item[1])
        domain_index.add('topic', item[0], item[1])
    print domain_index
    print domain_index.get("topic", '科技类')



def put_in_user_portrait():
    Index = ManualIndexManager(graph) # manage index
    node_name = "node_index"
    node_index = Index.get_index(Node, node_name)

    f = open("user_portrait.txt", "rb")
    count = 0
    update_node = []
    for item in f:
        user_dict = json.loads(item)
        uid = user_dict["uid"]
        exist = node_index.get("uid", uid)
        if not exist:
            Index.get_or_create_indexed_node(node_name, "uid", uid, user_dict)
        else:
            user_node = exist[0]
            for k,v in user_dict.iteritems():
                user_node[k] = v
            graph.push(user_node)
        count += 1
        print count


    f.close()


def create_rel_from_uid2_domain():
    Index = ManualIndexManager(graph) # manage index
    domain_name = "domain_index"
    node_index = Index.get_index(Node, "node_index")
    domain_index = Index.get_index(Node, domain_name)
    domain_node = domain_index.get("domain", "媒体")

    tx = graph.begin()
    count = 0
    ts = time.time()
    f = open("user_portrait.txt", "rb")
    for line in f:
        user_dict = json.loads(line)
        uid = user_dict["uid"]
        print uid
        print count
        domain = user_dict["domain"]
        user_node = node_index.get("uid", uid)[0]
        domain_node = domain_index.get("domain", domain)[0]
        rel = Relationship(user_node, "domain", domain_node)
        tx.create(rel)
        count += 1
        if count % 1000 == 0:
            tx.commit()
            print count
            te = time.time()
            print te - ts
            ts = te
            tx = graph.begin()
    tx.commit()




def create_rel_from_uid2_topic():
    Index = ManualIndexManager(graph) # manage index
    topic_name = "topic_index"
    node_index = Index.get_index(Node, "node_index")
    topic_index = Index.get_index(Node, topic_name)

    tx = graph.begin()
    count = 0
    ts = time.time()
    f = open("user_portrait.txt", "rb")
    for line in f:
        user_dict = json.loads(line)
        uid = user_dict["uid"]
        topic_string = user_dict["topic_string"]
        user_node = node_index.get("uid", uid)[0]
        topic_list = topic_string.split("&")
        for iter_topic in topic_list:
            topic_node = topic_index.get("topic", iter_topic)[0]
            rel = Relationship(user_node, "topic", topic_node)
            tx.create(rel)
            count += 1
            if count % 1000 == 0:
                tx.commit()
                print count
                te = time.time()
                print te - ts
                ts = te
                tx = graph.begin()
    tx.commit()


def create_rel_from_event_special(event, special_event):
    Index = ManualIndexManager(graph) # manage index
    event_index = Index.get_index(Node, event_index_name)
    special_event_index = Index.get_index(Node, special_event_index_name)

    node1 = event_index.get("event", event)[0]
    node2 = special_event_index.get("event", special_event)[0]

    rel = Relationship(node1, event_special, node2)
    tx = graph.begin()
    tx.create(rel)
    tx.commit()




def create_rel_from_uid2_location():
    Index = ManualIndexManager(graph) # manage index
    node_index = Index.get_index(Node, node_index_name)
    location_index = Index.get_index(Node, location_index_name)

    tx = graph.begin()
    count = 0
    ts = time.time()
    f = open("user_portrait.txt", "rb")
    for line in f:
        user_dict = json.loads(line)
        uid = user_dict["uid"]
        location = user_dict["location"]
        if not location:
            continue
        user_node = node_index.get("uid", uid)[0]
        location_node = location_index.get("location", location)[0]
        rel = Relationship(user_node, "location", location_node)
        tx.create(rel)
        count += 1
        if count % 1000 == 0:
            tx.commit()
            print count
            te = time.time()
            print te - ts
            ts = te
            tx = graph.begin()
    tx.commit()

if __name__ == "__main__":
    #put_in_node()
    #create_rel_from_uid2_domain()
    #create_rel_from_uid2_topic()
    #put_in_user_portrait()
    #create_node_location()
    #create_rel_from_uid2_location()
    #put_in_special_event("电信诈骗")
    #create_rel_from_event_special("ma-lai-xi-ya-zhua-huo-dian-xin-qi-zha-an-fan-1482126431", "电信诈骗")
    create_rel_from_event_special("ao-men-xuan-ju-fa-xin-zeng-jia-ai-guo-tiao-li-1482126431", "港澳台")

