# -*-coding:utf-8-*-

import sys
import json
import pinyin
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
reload(sys)
sys.path.append('../../')
from global_utils import es_event as es


def mappings_wiki_results():
    index_info = {
        'settings': {
            'number_of_replicas': 0,
            'number_of_shards': 5,
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "type": "pattern",
                        "pattern": "&"
                    }
                }
            }
        },
        'mappings': {
            "wiki_result": {
                'properties': {
                    "name": {
                        "type": "string",
                    },
                    "url": {
                        "type": "string",
                        "index": "no"
                    },
                    "html": {
                        "index": "no",
                        "type": "string"
                    },
                    "keywords": {
                        "analyzer": "my_analyzer",
                        "type": "string"
                    },
                    "first_in": {
                        "type": "long"
                    },
                    "last_modify": {
                        "type": "long"
                    },
                }
            }
        }
    }


    if not es.indices.exists(index="wiki_analysis_name"):
        print es.indices.create(index="wiki_analysis_name", body=index_info, ignore=400)

    return '1'


if __name__ == "__main__":
     mappings_wiki_results()
