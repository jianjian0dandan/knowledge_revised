# -*-coding:utf-8-*-
import json
import sys
from py2neo.ext.batman import ManualIndexManager
from py2neo import Node, Relationship
from py2neo.packages.httpstream import http
from py2neo.ogm import GraphObject
from knowledge.global_utils import graph
from knowledge.global_config import *
from myutil import get_type_key
from knowledge.global_utils import es_event as es

http.socket_timeout = 9999


# 对es进行读取数据
def get_es_node():
    query_search = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match_all": {}
                    }
                ],
                "must_not": [],
                "should": []
            }
        },
        "from": 0,
        "size": 100,
        "sort": [],
        "facets": {}
    }
    print "ss"
    result = es.search(index="user_portrait", doc_type="user",
                       body=query_search)['hits']['hits']
    return result


def get_es_status(index_name):
    query_search = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match_all": {}
                    }
                ],
                "must_not": [],
                "should": []
            }
        },
        "from": 0,
        "size": 3,
        "sort": [],
        "aggs": {}
    }
    print "ss"
    result = es.search(index=index_name, doc_type="text",
                       body=query_search)['hits']['hits']
    return result


# 返回需要的查询结果
def select_rels_all(c_string):
    list = []
    result = graph.run(c_string)
    for item in result:
        list.append(item)
    return list


# 查询一个节点的所有rel
def select_rels(node_key, node_id, node_name_index):
    list = []
    Index = ManualIndexManager(graph)
    node_name = Index.get_index(Node, node_name_index)
    if not node_name:
        print "node_index does not exist "
        return None
    node = node_name.get(node_key, node_id)[0]
    if not node:
        print "node does not exist"
        return None
    c_string = "START start_node=node:%s(%s='%s') MATCH (start_node)-[r]-() return r" % (
        node_name_index, node_key, node_id)
    print c_string
    result = graph.run(c_string)
    for item in result:
        list.append(item)
    return list


# 对数据进行存放
def create_person(node_type, node_key, node_id, node_name_index, attribute_dict=dict()):
    Index = ManualIndexManager(graph)
    node_name = Index.get_or_create_index(Node, node_name_index)
    print node_name
    if node_name:
        exist = node_name.get(node_key, node_id)
        print exist
        if exist:
            person_node = exist[0]
            for k, v in attribute_dict.iteritems():
                person_node[k] = v
            graph.push(person_node)
        else:
            person_node = Node(node_type, uid=node_id)
            for k, v in attribute_dict.iteritems():
                person_node[k] = v
            graph.create(person_node)
            node_name.add(node_key, node_id, person_node)
            print "create person success"
            return True


# 对多个节点和类建立关系
def create_rel_from_uid2group(node_key, uid_list, node_index_name, group_rel, group_key, group_id, group_index_name):
    count = 0
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    group_index = Index.get_index(Node, group_index_name)
    tx = graph.begin()
    if not (node_index and group_index):
        print "node or group does not exist"
        return None
    for uid in uid_list:
        node = node_index.get(node_key, uid)[0]
        group_node = group_index.get(group_key, group_id)[0]
        rel = Relationship(node, group_rel, group_node)
        tx.create(rel)
        count += 1
        if count % 100 == 0:
            tx.commit()
            print count
            tx = graph.begin()
    tx.commit()


# 多对多创建节点关系([node1_type,node1_id],rel,[node2_type,node2_id])
def nodes_rels(list):
    result = ''
    count = 0
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    event_index = Index.get_index(Node, event_index_name)
    tx = graph.begin()
    if not (node_index and event_index):
        print "node or group does not exist"
        return "0"
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
                print 11

            else:
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
                print 12
        else:
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
                print 21
            else:
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
                print 22
        if flag == 0:
            rel = Relationship(node1, rel, node2)
            tx.create(rel)
            count += 1
        if count % 100 == 0:
            tx.commit()
            tx = graph.begin()
    tx.commit()
    return 'success'



# 对单节点和单节点建立关系
def create_node_or_node_rel(node_key1, node1_id, node1_index_name, rel, node_key2, node2_id, node2_index_name):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node1_index_name)
    group_index = Index.get_index(Node, node2_index_name)
    print node_index
    print group_index
    tx = graph.begin()
    if len(node_index.get(node_key1, node1_id)) == 0:
        print "node1 does not exist"
        return 'node1 does not exist'
    print node2_id, '======='
    print group_index.get(node_key2, node2_id)
    print 'node_key2', node_key2
    if len(group_index.get(node_key2, node2_id)) == 0:
        print "node2 does not exist"
        return "node2 does not exist"
    node1 = node_index.get(node_key1, node1_id)[0]
    node2 = group_index.get(node_key2, node2_id)[0]
    if not (node1 and node2):
        print "node does not exist"
        return None
    c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" \
               % (node1_index_name, node_key1, node1_id, node2_index_name, node_key2, node2_id, rel)
    print c_string
    result = graph.run(c_string)
    # print result
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
    return True


# 对节点进行更新
def update_node(key_id, uid, node_index_name, attribute_dict):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    node = node_index.get(key_id, uid)[0]
    print node
    if not node:
        print "no such node"
        sys.exit(0)

    for k, v in attribute_dict.iteritems():
        node[k] = v

    graph.push(node)
    print "update success"
    return True


# 对节点间的rel进行更新
def update_node_or_node_rel(node_key1, node1_id, node1_index_name, old_rel, new_rel, node_key2, node2_id,
                            node2_index_name):
    # 需要对节点的关系进行删除以后在进行添加。
    delete_rel(node_key1, node1_id, node1_index_name, old_rel, node_key2, node2_id, node2_index_name)
    create_node_or_node_rel(node_key1, node1_id, node1_index_name, old_rel, node_key2, node2_id, node2_index_name)
    print "update rel success"
    return True


# 删除一个rel
def delete_rel(node_key1, node1_id, node1_index_name, rel, node_key2, node2_id, node2_index_name):
    list = []
    Index = ManualIndexManager(graph)
    node1_index = Index.get_index(Node, node1_index_name)
    node2_index = Index.get_index(Node, node2_index_name)
    if not (node1_index or node2_index):
        print "node_index does not exist"
        return None
    node1 = node1_index.get(node_key1, node1_id)[0]
    node2 = node2_index.get(node_key2, node2_id)[0]
    if not (node1 or node2):
        print ("node does not exist")
    c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]-(end_node) RETURN r" % (
        node1_index_name, node_key1, node1_id, node2_index_name, node_key2, node2_id, rel)
    result = graph.run(c_string)
    for item in result:
        list.append(item)
    if not list:
        print "Deleted rel does not exist"
        return None
    c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]-(end_node) DELETE r" % (
        node1_index_name, node_key1, node1_id, node2_index_name, node_key2, node2_id, rel)
    print c_string
    graph.run(c_string)
    print "delete success"
    return True


def delete_node(node_key, node_id, node_index_name):
    Index = ManualIndexManager(graph)
    node_index = Index.get_index(Node, node_index_name)
    if not node_index:
        print "node_index does not exist"
        return None
    node = node_index.get(node_key, node_id)[0]
    if not node:
        print "The node does not exist"
        return None
    c_string = "START start_node=node:%s(%s='%s') MATCH (start_node)-[r]-()  DELETE r" % (
        node_index_name, node_key, node_id)
    graph.run(c_string)
    print "delete rel success"
    c_string = "START start_node=node:%s(%s='%s') delete start_node" % (node_index_name, node_key, node_id)
    graph.run(c_string)
    print "delete node success"
    return True

def select_event_es(result):
    print "111"
    list = []
    for ls in result:
        event_dict= {}
        uid = dict(ls)["n"]["event_id"]
        item=es.get(index=event_analysis_name,doc_type=event_type,id=uid)
        event_dict["id"]=item["_id"]
        item = item["_source"]
        event_dict["name"]=item["name"]
        event_dict["weibo_counts"]=item["weibo_counts"]
        event_dict["uid_counts"]=item["uid_counts"]
        event_dict["start_ts"]=item["start_ts"]
        event_dict["location"]=item["location"]
        event_dict["tag"]=item["tag"]
        event_dict["description"]=item["description"]
        event_dict["submit_ts"]=item["submit_ts"]
        event_dict["end_ts"]=item["end_ts"]
        print event_dict
        list.append(event_dict)
    return list

def select_people_es(result):
    list = []
    for ls in result:
        uid = dict(ls)["n.uid"]
        item=es.get(index=portrait_name,doc_type=portrait_type,id=uid)
        people_dict["id"]=result["_id"]
        item = item["_source"]
        people_dict["domain"]=item["domain"]
        people_dict["influence"]=item["influence"]
        people_dict["uname"]=item["uname"]
        people_dict["sensitive_string"]=item["sensitive_string"]
        people_dict["activity_geo_aggs"]=item["activity_geo_aggs"]
        people_dict["importnace"]=item["importnace"]
        people_dict["activeness"]=item["activeness"]
        people_dict["location"]=item["location"]
        people_dict["importance"]=item["importance"]
        people_dict["hashtag"]=item["hashtag"]
        people_dict["photo_url"]=item["photo_url"]
        people_dict["topic_string"]=item["topic_string"]
        people_dict["friendsnum"]=item["friendsnum"]
        people_dict["create_time"]=item["create_time"]
        people_dict["description"]=item["description"]
        people_dict["create_user"]=item["create_user"]
        people_dict["tag"]=item["tag"]
        list.append(people_dict)
    return list

