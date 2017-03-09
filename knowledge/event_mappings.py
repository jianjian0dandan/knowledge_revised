# -*- coding: UTF-8 -*-
'''
save some about event
'''
from elasticsearch import Elasticsearch
from global_utils import es_event as es
from global_config import event_name


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
                'text':{
                    'properties':{
                        'compute_status':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'name':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'start_ts':{
                            'type': 'long',
                            },
                        'start_ts':{
                            'type':'long',
                            },
                        'en_name':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'submit_user': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'keywords':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'submit_ts':{
                            'type': 'long'
                            },
                        "first_compute":{
                            "type":"long"
                        },
                        "immediate_compute":{
                            "type":"long"
                        }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)

if __name__=='__main__':
    get_mappings(event_name)
    #es.indices.put_mapping(index='flow_text_2013-09-05', doc_type="text", body={"properties":{"comment":{"type": "long"}, "retweeted":{"type":"long"}}})
