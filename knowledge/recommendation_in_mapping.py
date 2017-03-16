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
                'task_name':{
                    'type':'string',
                    'index': 'not_analyzed'
                    },
                'status':{
                    'type':'long'
                    },
                'cal_style':{
                    'type':'long'
                    },
                'submit_date':{
                    'type': 'long'
                    },
                'submit_user':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'uid_list':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'relation_list':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'recommend_style':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'count':{
                    'type': 'long'
                    },
                'task_id':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    }
                }
            }
        }
    }

es.indices.create(index='recommendation_in_user', body=index_info, ignore=400)