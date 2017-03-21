# -*- coding: UTF-8 -*-
from elasticsearch import Elasticsearch
from knowledge.global_utils import es_wiki
from knowledge.global_config  import wiki_type_name,wiki_index_name



def getUrlByKeyWord(key_words):
    if len(key_words) == 0:
        print '****没有*****'
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
        url_list = []
        if n > 0:
            for item in search_results:
                url = item['_id'].encode('utf-8')
                name = item["_source"]['name'].encode('utf-8')
                print name
                print url
                url_list.append(name)
                url_list.append(url)
        else:
            url_list = []  #  查询结果小于等于0时返回空
    return url_list

if __name__ == '__main__':
    key = "特朗普"
    wiki_list = getUrlByKeyWord(key)
    print wiki_list

