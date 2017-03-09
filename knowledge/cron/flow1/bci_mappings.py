# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch

index_info = {
    "mappings":{
        "bci":{
            "properties":{
                "origin_weibo_retweeted_detail": {
                    "type": "string",
                    "index": "no"
                },
                "origin_weibo_retweeted_top": {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_comment_detail': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_comment_top': {
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_retweeted_detail':{
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_retweeted_top':{
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_comment_detail': {
                    "type": "string",
                    "index": "no"
                }, 
                'retweeted_weibo_comment_top': {
                    "type": "string",
                    "index": "no"
                }, 
                'origin_weibo_retweeted_brust_n': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_retweeted_average_number': {
                    "type": "long",
                },
                'retweeted_weibo_comment_brust_n': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_comment_top_number': {
                    "type": "long",
                },
                'origin_weibo_comment_brust_average': {
                    "type": "long",
                },
                'retweeted_weibo_retweeted_brust_average': {
                    "type": "long",
                },
                'retweeted_weibo_top_retweeted_id': {
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_number': {
                    "type": "long",
                },
                'total_number': {
                    "type": "long",
                },
                'retweeted_weibo_comment_top_number': {
                    "type": "long",
                },
                'user_friendsnum': {
                    "type": "long",
                },
                'origin_weibo_top_comment_id': {
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_retweeted_total_number': {
                    "type": "long",
                },
                'retweeted_weibo_retweeted_average_number': {
                    "type": "long",
                },
                'origin_weibo_retweeted_total_number': {
                    "type": "long",
                },
                'retweeted_weibo_top_comment_id': {
                    "type": "string",
                    "index": "no"
                },
                'user_fansnum': {
                    "type": "long",
                },
                'origin_weibo_comment_brust_n': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_top_retweeted_id': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_comment_average_number': {
                    "type": "long",
                },
                'origin_weibo_retweeted_brust_average': {
                    "type": "long",
                },
                'origin_weibo_retweeted_top_number': {
                    "type": "long",
                },
                'comment_weibo_number': {
                    "type": "long",
                },
                'retweeted_weibo_retweeted_brust_n': {
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_retweeted_top_number': {
                    "type": "long",
                },
                'origin_weibo_number': {
                    "type": "long",
                },
                'retweeted_weibo_comment_total_number': {
                    "type": "long",
                },
                'retweeted_weibo_comment_brust_average': {
                    "type": "long",
                },
                'origin_weibo_comment_total_number': {
                    "type": "long",
                },
                'retweeted_weibo_comment_average_number': {
                    "type": "long",
                } 

            }
        }
    }
}


def mappings(es, index_name):
    es.indices.create(index=index_name, body=index_info, ignore=400)
    return 1


if __name__ == "__main__":
    es = Elasticsearch("10.128.55.70:9200")
    print mappings(es, "bci_20160402")





