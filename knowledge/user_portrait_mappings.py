# -*- coding: utf-8 -*-

import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_user_portrait as es

index_info = {
    "settings":{
        "analysis":{
            "analyzer":{
                "my_analyzer":{
                    "type": "pattern",
                    "pattern": "&"
                }
            }
        },
        "number_of_replicas":0
    },

    "mappings":{
        "user":{
            "properties":{
                "domain":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                'domain_v3':{
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                "uname":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "uid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "activity_geo_dict":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "hashtag":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                'hashtag_dict':{
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                "keywords":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "psycho_status":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "topic":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                'topic_string':{
                    'type': 'string',
                    'analyzer': 'my_analyzer'
                },

                "activity_geo":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "keywords_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "topic_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },

                "importance": {
                    "type": "double"
                },
                "influence": {
                    "type": "double"
                },
                "activeness": {
                    "type": "double"
                },
                "online_pattern":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "fansnum": {
                    "type": "long"
                },
                "photo_url": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "verified": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "statusnum": {
                    "type": "long"
                },
                "gender": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "location": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "friendsnum": {
                    "type": "long"
                }, 
                'group':{
                    'type': 'string',
                    'analyzer': 'my_analyzer'
                },
                'remark':{
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'character_text':{
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'character_sentiment':{
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'activity_geo_aggs':{
                    'type': 'string',
                    'analyzer': 'my_analyzer'
                },
                'online_pattern_aggs':{
                    'type': 'string',
                    'analyzer': 'my_analyzer'
                },
                'sensitive':{
                    'type': 'double',
                },
                'sensitive_dict':{
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'sensitive_string':{
                    'type': 'string',
                    'analyzer': 'my_analyzer'
                },
                'is_school':{
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'school_string':{
                    'type': 'string',
                    'analyzer': 'my_analyzer'
                },
                'school_dict':{
                    'type': 'string',
                    'index': 'not_analyzed'
                }
            }
        }
    }
}


#es.indices.create(index="user_portrait", body=index_info, ignore=400)

es.indices.put_mapping(index='user_portrait', doc_type='user', \
        body={'properties':{'create_time':{'type':'long'}}}, ignore=400)
