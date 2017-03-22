# -*- coding: UTF-8 -*-
from elasticsearch import Elasticsearch
from knowledge.global_utils import es_wiki
from knowledge.global_config  import wiki_type_name,wiki_index_name



def getUrlByKeyWord(key_words):
    if len(key_words) == 0:
        print '***keywords is null***'
        return 0
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
                name = item["_source"]['name'].encode('utf-8')
                url = item['_id'].encode('utf-8')
                print name.decode('utf-8')
                item_list.append([name, url])
        else:
            item_list = 0  #  查询结果小于等于0时返回空
    return item_list

if __name__ == '__main__':
    key = "特朗普"
    wiki_list = getUrlByKeyWord(key)
    print wiki_list

