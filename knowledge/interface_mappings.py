# -*- coding: utf-8 -*-

import json
from elasticsearch import Elasticsearch
from global_utils import es_user_portrait as es

index_info = {
    "settings":{
        "number_of_replicas":0
    },

    "mappings":{
        "user":{
            "properties":{
                "task_name":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "task_time":{
                    "type": "long"
                },
                "in_portrait_list":{
                    "type": "string",
                    "index": "no"
                },
                "new_in_list":{
                    "type": "string",
                    "index": "no"
                },
                "not_in_list":{
                    "type": "string",
                    "index": "no"
                }
            }
        }
    }
}

es.indices.create(index="user_portrait_task_results", body=index_info, ignore=400)


