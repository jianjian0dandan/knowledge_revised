# -*- coding: UTF-8 -*-
'''
save some about event
'''
from elasticsearch import Elasticsearch
from global_utils import es_event as es
from global_config import sim_name,sim_type

def get_mappings(index_name):
    index_info = {
            'settings':{
                'number_of_replicas': 0,
                'number_of_shards':5,
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
                sim_type:{
                    'properties':{
                        'name':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'node_type':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'submit_ts':{
                            'type': 'long'
                            },
                        'compute_status':{
                            'type': 'long'
                            },
                        'submit_user':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'node_id':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'related_id':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        print es.indices.create(index=index_name, body=index_info, ignore=400)

if __name__=='__main__':
    print get_mappings(sim_name)
    #es.indices.put_mapping(index='flow_text_2013-09-05', doc_type='text', body={'properties':{'comment':{'type': 'long'}, 'retweeted':{'type':'long'}}})
