# -*- coding: UTF-8 -*-

import os
import time
import scws
import csv
import sys
import json
from elasticsearch import Elasticsearch
from config import *

def event_input(event_words,event_id):
    '''
        输入数据：
        event_words 事件关键词列表
        event_id 事件id

        输出数据：
        event_list 相关联事件列表（id）
    '''
    if len(event_words) == 0:
        return []
    elif len(event_words) > 0 and len(event_words) <= 2:
        n = 1
    else:
        n = float(len(event_words))*event_sta
        if n < 2:
            n = 2
    
    w_list = []
    for w in event_words:
        w_list.append({"term":{"keywords":w}})
            
    query_body = {
        "query":{
            "bool":{
                "should":w_list,
                "minimum_should_match": n
            }
        },
        "size":2000
    }
    search_results = es_event.search(index=event_analysis_name, doc_type=event_type, body=query_body)['hits']['hits']
    n = len(search_results)
    event_list = []
    if n > 0:
        for item in search_results:
            uid = item['_id'].encode('utf-8')
            if uid != event_id:
                event_list.append(uid)

    return event_list

if __name__ == '__main__':
    event_words = ['香港','澳门']
    event_list = event_input(event_words,'111')

    print event_list    
