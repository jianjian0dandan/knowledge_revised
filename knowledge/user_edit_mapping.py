# -*- coding:UTF-8 -*-
import json
from elasticsearch import Elasticsearch
from global_utils import es_user_portrait as es

index_info = {
    'settings':{
        'number_of_shards':5,
        'number_of_replicas':0,
        },
    'mappings':{
        'group':{
            'properties':{
                'uid':{
                    'type':'string',
                    'index': 'not_analyzed'
                    },
                'related_docs':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    }
                }
            }
        }
    }

es.indices.create(index='user_docs', body=index_info, ignore=400)