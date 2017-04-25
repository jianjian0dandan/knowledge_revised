#-*-coding:utf-8-*-
import sys,json
sys.path.append('./knowledge')
sys.path.append('./knowledge/cron')
sys.path.append('../../')

import datetime
import time
import os
import redis
import xlrd
from xpinyin import Pinyin
from elasticsearch import Elasticsearch
from time_utils import date2ts
from global_utils import es_event
from global_config import event_task_name, event_task_type, event_analysis_name, event_text_type

# from knowledge.construction.utils import submit_event
p = Pinyin()

def excel_read():
    data = xlrd.open_workbook('events.xlsx') 
    table = data.sheets()[0] # 打开第一张表
    nrows = table.nrows # 获取表的行数

    for i in range(nrows): 

        if i == 0: # 跳过第一行
            continue

        now_ts=int(time.time())
        keywords_list = table.row_values(i)[1].split(' ')
        keywords = '&'.join(keywords_list)
        event_type=table.row_values(i)[2]
        print event_type
        condition=[]
        for w in keywords_list:
            condition.append({'term':{'keywords':w}})
            print w

        condition.append({'term':{'compute_status':1}})
        es_query = {
            'query':{
                'bool':{
                    'must':condition
                     }
                }
            }

        res = es_event.search(index=event_task_name, doc_type=event_task_type, \
            body=es_query, request_timeout=999999,params={"search_type":"query_and_fetch"}) 
        print res['hits']['hits']

        if len(res['hits']['hits'])==1:
            en_id = res['hits']['hits'][0]['_id']
            es_event.update(index=event_task_name, doc_type=event_task_type, id=en_id, body={'doc':{'event_type':event_type}})
            es_event.update(index=event_analysis_name, doc_type='text', id=en_id, body={'doc':{'event_type':event_type}})
        elif len(res['hits']['hits'])>=1:
            en_id = res['hits']['hits'][0]['_id']
            es_event.update(index=event_task_name, doc_type=event_task_type, id=en_id,  \
                body={'doc':{'event_type':event_type}})
            try:
                task_exist = es_event.get(index=event_analysis_name,doc_type='text',id=task_id)['_source']
            except:
                task_exist={}
            if task_exist:
                es_event.update(index=event_analysis_name, doc_type='text', id=en_id, body={'doc':{'event_type':event_type}})
            else:
                print 'event_result not exist'+en_id 
            print "查询到多个结果！",i

    print 'END'

def input_one(en_name,event_type):

    es_event.update(index=event_task_name, doc_type=event_task_type, id=en_name, body={'doc':{'event_type':event_type}})
    es_event.update(index=event_analysis_name, doc_type='text', id=en_name, body={'doc':{'event_type':event_type}})

def excel_read_v2():
    data = xlrd.open_workbook('event1.xlsx') 
    table = data.sheets()[0] # 打开第一张表
    nrows = table.nrows # 获取表的行数

    for i in range(nrows): 
        if i == 0:
            continue
        en_name = table.row_values(i)[0]
        event_type=table.row_values(i)[1]
        print en_name,event_type
        print 
        es_event.update(index=event_task_name, doc_type=event_task_type, id=en_name, body={'doc':{'event_type':event_type}})

        # es_event.update(index=event_analysis_name, doc_type='text', id=en_name, body={'doc':{'event_type':event_type}})

    print 'END'

if __name__ == '__main__':
    # excel_read()
    input_one('te-lang-pu-qi-hou-he-zuo-1492166854','diplomacy')
    # excel_read_v2()


