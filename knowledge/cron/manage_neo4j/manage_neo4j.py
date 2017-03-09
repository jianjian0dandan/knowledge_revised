# -*-coding:utf-8-*-

import time
import sys
import json
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo.ogm import GraphObject, Property
from py2neo.packages.httpstream import http
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
http.socket_timeout = 9999

graph = Graph('http://219.224.134.213:7474/db/data', user="neo4j", password="database")
#graph = Graph()

class User(GraphObject):
    __primarykey__ = "uid"

    uid = Property()

# create a user with User class
def create_user(user, attribute_dict=dict()):
    Index = ManualIndexManager(graph) # manage index
    node_name = "node_index"
    node_index = Index.get_index(Node, node_name)
    exist = node_index.get("uid", user)
    if exist:
        user_node = exist[0]
        for k,v in attribute_dict.iteritems():
            user_node[k] = v
        graph.push(user_node)
    else:
        user_node = Node("User", uid=user)
        for k,v in attribute_dict.iteritems():
            user_node[k] = v
        graph.create(user_node)
        node_index.add("uid", user, user_node)

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
def create_relationship(st_node, ed_node, rel_type, st_type="node_index", ed_type="node_index", st_index="uid", ed_index="uid"):
    Index = ManualIndexManager(graph) # manage index
    start_index = Index.get_index(Node, st_type)
    start_node = start_index.get(st_index, st_node)
    if start_node:
        start_node = start_node[0]
    else:
        print "start_node no exists"
        sys.exit(0)
    end_index = Index.get_index(Node, ed_type)
    end_node = end_index.get(ed_index, ed_node)
    if end_node:
        end_node = end_node[0]
    else:
        print "end_node no exists"
        sys.exit(0)
    c_string = "START start_node=node:%s(%s='%s'),end_node=node:%s(%s='%s') MATCH (start_node)-[r:%s]->(end_node) RETURN r" %(st_type, st_index, st_node, ed_type, ed_index, ed_node, rel_type)
    result = graph.run(c_string)
    rel_list = []
    for item in result:
        rel_list.append(item)
    if not rel_list:
        rel = Relationship(start_node, rel_type, end_node)
        graph.create(rel)
        print "create"



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
    #create_relationship("1283493053","1264080891","retweet","node_index","node_index","uid", "uid")
    #create_relationship("1707314224","2154144855","retweet","node_index","node_index","uid", "uid")
    #create_relationship("1264080891","1283493053","retweet","node_index","node_index","uid", "uid")
    #create_relationship("2154144855","徐玉玉事件","event","node_index","event_index","uid", "event")
    #create_relationship("1264080891","大学生失联","event","node_index","event_index","uid", "event")
    #create_relationship("1510017057","律师","group","node_index","group_index","uid", "group")
    #update_attribute("2154144855", {"name":"潘强"})
    #delete_user("2264700665")
    #get_user_attribute_by_index("1768871224")
    create_user("5144595165")
    #create_user("1283493053", {"name":"梅春来律师"})
    #create_user("1707314224", {"name":"郑在索律师"})
    #create_user("1264080891", {"name":"朱明勇律师"})
    #create_user("1936027780", {"name":"律师郑海峰"})
    #create_user("1510017057", {"name":"徐利平律师"})
    #get_user_attribute_by_cypher("1768871224")
    #get_rel_by_cypher("2582763431", "retweet")
    #update_rel_by_cypher("3293303045", "3272538233", "retweet", {"times": "10", "age":55})



