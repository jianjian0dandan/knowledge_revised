# -*- coding: UTF-8 -*-
'''
save some about event
'''
from elasticsearch import Elasticsearch
from global_utils import es_event as es
from global_config import group_name,group_type,special_event_name,special_event_type

def get_mappings(index_name):
    index_info = {
            'settings':{
                "number_of_replicas": 0,
                "number_of_shards":5,
                'analysis':{
                    'analyzer':{
                        'my_analyzer':{
                            'type': 'pattern',
                            'pattern': '&'
                        }
                    }
                }
            },
            'mappings':{
                group_type:{
                    'properties':{
                        'user':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'group_name':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'people':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'people_count':{
                            'type': 'long'
                            },
                        'create_ts':{
                            'type': 'long'
                            },
                        'modify_ts':{
                            'type': 'long'
                            },
                        'label':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'k_label':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)

if __name__=='__main__':
    get_mappings(group_name)
    #es.indices.put_mapping(index='flow_text_2013-09-05', doc_type="text", body={"properties":{"comment":{"type": "long"}, "retweeted":{"type":"long"}}})
