# -*- coding: UTF-8 -*-
from global_config import *
from global_utils import *
from py2neo.ext.batman import ManualIndexManager
from py2neo.ext.batman import ManualIndexWriteBatch
from py2neo.ogm import GraphObject, Property
from py2neo import Node, Relationship
import re
from elasticsearch import Elasticsearch

def getUrlByKeyWord(key_words):
    if len(key_words) == 0:
        return []
    else:
        #  链接ES执行查询语句
        query_body = {
            "query":
                {"bool":
                     {"should":
                          [{"query_string": {"default_field": "wiki_result.name", "query": key_words}}]
                     }
                },
            "size": 10
        }
        search_results = es_wiki.search(index=wiki_index_name, doc_type=wiki_type_name, body=query_body)["hits"]["hits"]
        n = len(search_results)
        item_list = []
        if n > 0:
            for item in search_results:
                name = item["_source"]['name']#.encode('utf-8')
                url = item['_id']#.encode('utf-8')
                item_list.append([name, url])
        else:
            item_list = []  #  查询结果小于等于0时返回空
    return item_list

def getUrlByKeyWordList(key_words):
    if len(key_words) == 0:
        return []
    else:
        #  链接ES执行查询语句
        query_list = []
        for key in key_words:
            query_list.append({"query_string": {"default_field": "wiki_result.name", "query": key}})
        query_body = {
            "query":
                {"bool":
                     {"should":query_list}
                },
            "size": 10
        }
        search_results = es_wiki.search(index=wiki_index_name, doc_type=wiki_type_name, body=query_body)["hits"]["hits"]
        n = len(search_results)
        item_list = []
        if n > 0:
            for item in search_results:
                name = item["_source"]['name'].encode('utf-8')
                url = item['_id'].encode('utf-8')
                item_list.append([name, url])
        else:
            item_list = []  #  查询结果小于等于0时返回空
    return item_list


# create a user with User class
def create_user(user, attribute_dict=dict()):
    Index = ManualIndexManager(graph) # manage index
    node_name = wiki_url_index_name
    node_index = Index.get_index(Node, node_name)
    exist = node_index.get("url", user)
    # print exist
    if exist:
        user_node = exist[0]
        for k,v in attribute_dict.iteritems():
            user_node[k] = v
        graph.push(user_node)
    else:
        user_node = Node("Wiki", url=user)
        for k,v in attribute_dict.iteritems():
            user_node[k] = v
        graph.create(user_node)
        node_index.add("url", user, user_node)

    return True

def create_wiki_node():
    wiki_result = es_wiki.search(index=wiki_index_name, doc_type=wiki_type_name,body={'query':{'match_all':{}}, 'size':1000000})['hits']['hits']
    # Index = ManualIndexManager(graph) # manage index
    # wiki_index = Index.get_or_create_index(Node, wiki_url_index_name)
    count = 0
    for i in wiki_result:
        if count%1000 == 0:
            print count
        count += 1
        # print i['_id']
        create_user(i['_id'])

def create_relation_wiki_u():
    pattern = re.compile(r'[1-9]([0-9]{9})')
    user_string = 'match (n:User) return n'
    uid_list = []
    result = graph.run(user_string)
    for i in result:
        uid_list.append(dict(i)['n']['uid'])
    print len(uid_list)

    Index = ManualIndexManager(graph)
    tx = graph.begin()

    en_name = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'ids':uid_list}, fields=['uname', 'uid'])['docs']
    rel_count = 0
    for i in en_name:
        key_words = ''
        if i['found'] == False:
            match = pattern.match(i['_id'])
            if not match :
                key_words = i['_id']
                # print key_words,'=============='
        else:
            if i['fields']['uname'][0] not in ['', 'NULL', 'unknown']:
                key_words = i['fields']['uname'][0]

        if key_words != '':
            # print key_words,'=============='
            try:
                wiki_list = getUrlByKeyWord(key_words)
            except:
                wiki_list = []
        else:
            continue

        wikii_index = Index.get_index(Node, wiki_url_index_name)
        node_index = Index.get_index(Node, 'node_index')

        node1 = node_index.get('uid', i['_id'])[0]
        # print wiki_list,'----------'
        for ij in wiki_list:
            # print ij
            node2 = wikii_index.get('url', ij[1])[0]
            rel2 = Relationship(node1, 'wiki_link', node2)
            # print key_words, ij[0]
            rel_count += 1
            if rel_count%1000 == 0:
                print rel_count
            graph.create(rel2)
            # print i[0], i[1]



def create_relation_wiki_o():
    pattern = re.compile(r'[1-9]([0-9]{9})')
    user_string = 'match (n:Org) return n'
    uid_list = []
    result = graph.run(user_string)
    for i in result:
        uid_list.append(dict(i)['n']['org_id'])
    print len(uid_list)

    Index = ManualIndexManager(graph)
    tx = graph.begin()

    en_name = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'ids':uid_list}, fields=['uname', 'uid'])['docs']
    rel_count = 0
    for i in en_name:
        key_words = ''
        if i['found'] == False:
            match = pattern.match(i['_id'])
            if not match :
                key_words = i['_id']
                # print key_words,'=============='
        else:
            if i['fields']['uname'][0] not in ['', 'NULL', 'unknown']:
                key_words = i['fields']['uname'][0]

        if key_words != '':
            # print key_words,'=============='
            try:
                wiki_list = getUrlByKeyWord(key_words)
            except:
                wiki_list = []
        else:
            continue

        wikii_index = Index.get_index(Node, wiki_url_index_name)
        node_index = Index.get_index(Node, 'org_index')

        node1 = node_index.get('org_id', i['_id'])[0]
        # print wiki_list,'----------'
        for ij in wiki_list:
            # print ij
            node2 = wikii_index.get('url', ij[1])[0]
            rel2 = Relationship(node1, 'wiki_link', node2)
            # print key_words, ij[0]
            rel_count += 1
            if rel_count%1000 == 0:
                print rel_count
            rel_count += 1
            graph.create(rel2)
    print rel_count



def create_relation_wiki_e():
    pattern = re.compile(r'[1-9]([0-9]{9})')
    user_string = 'match (n:Event) return n'
    uid_list = []
    result = graph.run(user_string)
    for i in result:
        uid_list.append(dict(i)['n']['event_id'])
    print len(uid_list)

    Index = ManualIndexManager(graph)
    tx = graph.begin()

    en_name = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={'ids':uid_list},\
                    fields=['name'], _source=False)['docs']
    rel_count = 0
    for i in en_name:
        key_words = ''
        if i['found'] == False:
            continue
        else:
            if i['fields']['name'][0] not in ['', 'NULL', 'unknown']:
                key_words = i['fields']['name'][0]

        if key_words != '':
            # print key_words,'=============='
            key_words_list = key_words.split('&')
            try:
                wiki_list = getUrlByKeyWordList(key_words_list)
            except:
                wiki_list = []
        else:
            continue

        wikii_index = Index.get_index(Node, wiki_url_index_name)
        node_index = Index.get_index(Node, 'event_index')

        node1 = node_index.get('event_id', i['_id'])[0]
        # print wiki_list,'----------'
        for ij in wiki_list:
            # print ij
            node2 = wikii_index.get('url', ij[1])[0]
            rel2 = Relationship(node1, 'wiki_link', node2)
            # print key_words, ij[0]
            rel_count += 1
            if rel_count %1000 ==0:
                print rel_count
            rel_count+= 1
            graph.create(rel2)
            # print i[0], i[1]


if __name__ == '__main__':
    # create_wiki_node()
    # create_relation_wiki_u()
    create_relation_wiki_e()
    # create_relation_wiki_o()