# -*-coding:utf-8-*-
import sys
import time
import json
from knowledge.global_utils import es_prediction, sensing_compute_interval, es_user_profile,\
        profile_index_name,profile_index_type, RUN_TYPE


def get_time_series(ts):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "range":{
                        "detect_ts":{
                            "lt": ts,
                            "gte": ts-3*24*3600
                        }
                    }
                }
            }
        },
        "aggs":{
            "all_count":{
                "terms":{"field": "detect_ts", "size": 100},
                "aggs":{
                    "all_type":{
                        "terms":{"field": "type"}
                    }
                }
            }
        }
    }
    es_results = es_prediction.search(index="social_sensing_text", doc_type="text", body=query_body)["aggregations"]["all_count"]["buckets"]

    results = []
    for item in es_results:
        tmp_ts = item["key"]
        tmp_type = item["all_type"]["buckets"]
        tmp_type_dict = dict()
        tmp_type_dict["ts"] = tmp_ts
        for iter_item in tmp_type:
            if int(iter_item["key"]) == 1:
                tmp_type_dict["origin"] = iter_item["doc_count"]
            else:
                tmp_type_dict["retweet"] = iter_item["doc_count"]
        results.append(tmp_type_dict)

    sorted_results = sorted(results, key=lambda x:x["ts"], reverse=False)

    return sorted_results


def show_weibo_list(message_type,ts,sort_item):
    query_body = {
        "query": {
            "bool":{
                "must":[
                    {"term":{"type": int(message_type)}},
                    {"term": {"detect_ts": int(ts)}}
                ]
            }
        },
        "size": 100,
        "sort":{sort_item:{"order": "desc"}}
    }

    text_results = []
    uid_list = []
    text_keys = ["text", "retweeted","keywords_string","mid", "comment", "user_fansnum", "timestamp", "geo", "uid"]
    es_results = es_prediction.search(index="social_sensing_text",doc_type="text", body=query_body)["hits"]["hits"]
    if not es_results:
        return []

    for item in es_results:
        item = item["_source"]
        tmp = dict()
        for key in text_keys:
            tmp[key] = item[key]
        text_results.append(tmp)
        uid_list.append(item["uid"])

    profile_results = es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type, body={"ids":uid_list})["docs"]
    for i in range(len(uid_list)):
        tmp_profile = profile_results[i]
        if tmp_profile["found"]:
            tmp = dict()
            tmp["photo_url"] = tmp_profile["_source"]["photo_url"]
            tmp["nick_name"] = tmp_profile["_source"]["nick_name"]
            if not tmp["nick_name"]:
                tmp["nick_name"] = uid_list[i]
            text_results[i].update(tmp)

    return text_results



def get_weibo_bursting(mid):
    es_results = es_prediction.get(index="social_sensing_text",doc_type="text", id=mid)["_source"]
    es_results["trendline"] = json.loads(es_results["trendline"])
    uid = es_results["uid"]
    try:
        profile_result = es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=uid)["_source"]
        es_results["photo_url"] = profile_result["photo_url"]
        es_results["nick_name"] = profile_result["nick_name"]
        es_results["statusnum"] = profile_result["statusnum"]
        es_results["friendsnum"] = profile_result["friendsnum"]
    except:
        es_results["photo_url"] = ""
        es_results["nick_name"] = uid
        es_results["statusnum"] = ""
        es_results["friendsnum"] = ""

    return es_results


if __name__ == "__main__":
    print get_time_series()

