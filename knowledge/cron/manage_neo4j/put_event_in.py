# -*-coding:utf-8-*-

import time
import json
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property
from py2neo.packages.httpstream import http
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
http.socket_timeout = 9999

import sys
sys.path.append("../../")
from global_utils import graph
from global_config import event_index_name, group_index_name

class Event(GraphObject):
    __primarykey__ = "event_id"

    event_id = Property()

class Tag(GraphObject):
    __primarykey__ = "tag"

    tag = Property()

class Group(GraphObject):
    __primarykey__ = "group"

    group = Property()

# create a group with Group class
def create_group(group_id, attribute_dict=dict()):
    Index = ManualIndexManager(graph) # manage index
    group_index = Index.get_or_create_index(Node, group_index_name)
    exist = group_index.get("group", group_id)

    if exist:
        group_node = exist[0]
        for k,v in attribute_dict.iteritems():
            group_node[k] = v
        graph.push(group_node)
    else:
        group_node = Node("Group", group=group_id) # create event node with only one event_id
        for k,v in attribute_dict.iteritems():
            group_node[k] = v
        graph.create(group_node)
        group_index.add("group", group_id, group_node)

    return True


# create a event with Event class
def create_event(event, attribute_dict=dict()):
    Index = ManualIndexManager(graph) # manage index
    event_index = Index.get_or_create_index(Node, event_index_name)
    exist = event_index.get("event", event)

    if exist:
        event_node = exist[0]
        for k,v in attribute_dict.iteritems():
            event_node[k] = v
        graph.push(event_node)
    else:
        event_node = Node("Event", event_id=event) # create event node with only one event_id
        for k,v in attribute_dict.iteritems():
            event_node[k] = v
        graph.create(event_node)
        event_index.add("event", event, event_node)

    return True

# create a tag with Service_label class
def create_tag(tag_id, attribute_dict=dict()):
    Index = ManualIndexManager(graph) # manage index
    index_name = "tag_index"
    tag_index = Index.get_or_create_index(Node, index_name)
    exist = tag_index.get("tag", tag_id)

    if exist:
        tag_node = exist[0]
        for k,v in attribute_dict.iteritems():
            tag_node[k] = v
        graph.push(tag_node)
    else:
        tag_node = Node("Tag", tag=tag_id) # create event node with only one event_id
        for k,v in attribute_dict.iteritems():
            tag_node[k] = v
        graph.create(tag_node)
        tag_index.add("tag", tag_id, tag_node)

    return True



# uid is index of node in neo4j
# attribute_dict: {update_attribute: update_value}

def update_attribute(uid, attribute_dict):
    ts = time.time()
    Index = ManualIndexManager(graph) # manage index
    ts = time.time()
    node_name = "node_index"
    node_index = Index.get_index(Node, node_name)
    user_node = node_index.get("uid", uid)[0] # return with a list
    print user_node

    # update attribute-value
    for k,v in attribute_dict.iteritems():
        user_node[k] = v


    # push to neo4j-db
    graph.push(user_node)

    te = time.time()
    print te-ts

# delete user node with uid
# 删除用户节点时，需要把对应的所有节点的关系全部删除
def delete_user(uid): 
    Index = ManualIndexManager(graph) # manage index
    node_name = "node_index"
    node_index = Index.get_index(Node, node_name)
    user_node = node_index.get("uid", uid)
    print user_node
    if not user_node:
        print "no user exists"
        return None
    #c_string = "MATCH (n {uid: '%s'})-[rel]->(fof) DELETE n,rel" %uid
    c_string = "START start_node=node:node_index(uid='%s') MATCH (start_node)-[rel]->(fof) DELETE start_node, rel" %uid
    result = graph.run(c_string)
    print result


# get user info in neo4j with uid_index
def get_user_attribute_by_index(uid):
    ts = time.time()
    Index = ManualIndexManager(graph) # manage index
    node_name = "node_index"
    node_index = Index.get_index(Node, node_name)
    user_node = node_index.get("uid", uid)
    print user_node
    te = time.time()
    print te-ts

    return user_node


def get_user_attribute_by_cypher(uid):
    ts = time.time()
    c_string = "MATCH (n {uid: '%s'}) RETURN n" %uid
    result = graph.run(c_string)
    for item in result:
        print item
    te = time.time()
    print te - ts


#############################################
# test relationship

# get_rel_by_index
# st_node: start node
# end_node: end node
# rel_type: 
# 返回cursor，字典组合的列表形式，for循环后取value值即为relationship或者是node
def create_relationship(st_node, ed_node, rel_type):
    Index = ManualIndexManager(graph) # manage index
    node_name = "node_index"
    node_index = Index.get_index(Node, node_name)
    start_node = node_index.get("uid", st_node)
    end_node = node_index.get("uid", ed_node)
    c_string = "START start_node=node:node_index(uid='%s'),end_node=node:node_index(uid='%s') MATCH (start_node)-[r:'%s']->(end_node) RETURN r" %(st_node, ed_node, rel_type)
    result = graph.run(c_string)
    for item in result:
        print item



def get_rel_by_cypher(st_node, rel_type=None):
    ts = time.time()
    node_list = []
    rel_list = []

    if rel_type:
        c_string = "START start_node=node:node_index(uid='%s') MATCH (start_node)-[r:%s]->(end) RETURN r,end" %(st_node, rel_type)
    else:
        c_string = "START start_node=node:node_index(uid='%s') MATCH (start_node)-[r]->(end) RETURN r,end" %st_node

    result = graph.run(c_string)
    for item in result:
        k = item.values()
        rel_list.append(dict(k[0]))
        node_list.append(dict(k[1]))

    print node_list
    print rel_list
    te = time.time()
    print te - ts

# update one rel
def update_rel_by_cypher(st_node, end_node, rel_type, attribute_dict):
    c_string = "START start_node=node:node_index(uid='%s'),end_node=node:node_index(uid='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" %(st_node, end_node, rel_type)
    result = graph.run(c_string)
    for item in result:
        rel = item[0]
    print type(rel)
    c_delete_string = "START start_node=node:node_index(uid='%s'),end_node=node:node_index(uid='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" %(st_node, end_node, rel_type)
    graph.run(c_delete_string)
    for k,v in attribute_dict.iteritems():
        rel[k] = v
    graph.create(rel)

# delete rel between st_node and end_node
def delete_rel_by_cypher(st_node, end_node, rel_type):
    c_string = "START start_node=node:node_index(uid='%s'),end_node=node:node_index(uid='%s') MATCH (start_node)-[r:%s]->(end_node) DELETE r" %(st_node,end_node,rel_type)
    graph.run(c_string)



if __name__ == "__main__":
    #update_attribute("1768871224", {"times":"20", "age":4})
    #delete_user("2264700665")
    #get_user_attribute_by_index("1768871224")
    #create_event("电信诈骗", {"event_id":"电信诈骗"})
    #create_tag("法律人士", {"tag":"法律人士"})
    create_group("法律人士")
    #get_user_attribute_by_cypher("1768871224")
    #get_rel_by_cypher("2582763431", "retweet")
    #update_rel_by_cypher("3293303045", "3272538233", "retweet", {"times": "10", "age":55})


    """
    event_name = ["yun-chao-che-ji-bi-nan-zi-huo-pei-chang-1482126431", "min-jin-dang-yi-yuan-cheng-yao-qing-da-lai-dui-kang-da-lu-1482126431", "xiang-gang-qian-zong-du-qian-ze-liang-you-er-ren-1482126431", \
            "huai-yun-nv-jiao-shi-bei-jia-chang-ou-da-1482079340", "lao-tai-ao-ye-mai-cai-wei-er-zi-mai-fang-1482126431", "xi-an-hu-shi-huai-yun-er-tai-bei-po-ci-zhi-1482126431", \
            "gong-an-bu-gua-pai-du-ban-shi-da-dian-xin-qi-zha-an-jian-1482127322", "ao-men-xuan-ju-fa-xin-zeng-jia-ai-guo-tiao-li-1482126431", \
            "ma-lai-xi-ya-zhua-huo-dian-xin-qi-zha-an-fan-1482126431", "zhong-guo-zhi-shi-chan-quan-shen-qing-liang-shi-jie-di-yi-1482079340"]

    for each in event_name:
        create_event(each)
    """


