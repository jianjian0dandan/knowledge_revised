# -*- coding:utf-8 -*-

import sys
import json
import pinyin
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
reload(sys)
sys.path.append('../../')
from global_utils import es_prediction as es
from global_config import type_manage_event_analysis, index_manage_event_analysis
    

def mappings_event_analysis_task():

    index_info = {
        'settings':{
            'number_of_replicas': 0,
            'number_of_shards': 5
        },
        "mappings":{
            type_manage_event_analysis:{
                "properties":{
                    "task_name":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "pinyin_task_name":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "must_keywords":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "should_keywords":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "start_ts":{      #event start time
                        "type": "long"
                    },
                    "end_ts":{          #event end time
                        "type": "long"
                    },
                    "submit_user":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "stop_time":{ # task end time
                        "type": "long"
                    },
                    "submit_time":{ # task start time
                        "type": "long"
                    },
                    "scan_text_finish":{ #事件文本是否从流文本扫描完 0 未扫描 1 正在扫描 2 扫描完成
                        "type":"long"  
                    },
                    "event_value_finish":{
                        "type":"long",     
                        "index":"not_analyzed"
                    },
                    "weibo_counts":{
                        "type":"long"
                    },
                    "uid_counts":{
                        "type":"long"
                    }
                }
            }
        }
    }
#event_value_finish
#事件是否计算完 0 未计算且未提交队列  1 已提交队列尚未计算  2 开始计算  3 计算完成
# finish: -1 weibo_counts\uid_counts -2 time -3 geo -4 network -5 sentiment 
    #index_name = "event_analysis_task_"+task_name

    if not es.indices.exists(index=index_manage_event_analysis):

        es.indices.create(index=index_manage_event_analysis, body=index_info, ignore=400)

    return 1

if __name__ == "__main__":

    mappings_event_analysis_task()


