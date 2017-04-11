# -*-coding:utf-8-*-
import sys
import time
import json
from knowledge.global_utils import es_prediction, sensing_compute_interval, es_user_profile,\
        profile_index_name,profile_index_type, es_flow_text,flow_text_index_name_pre, flow_text_index_type
from knowledge.parameter import DAY, WEEK, RUN_TYPE
from knowledge.time_utils import ts2datetime

def get_time_series():
    if RUN_TYPE == 0:
        ts = 1479571200
    else:
        ts = time.time()
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
        else:
            tmp = dict()
            tmp["photo_url"] = ""
            tmp["nick_name"] = tmp_profile["_id"]
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


def current_status(mid):
    es_results = es_prediction.get(index="social_sensing_text",doc_type="text", id=mid)["_source"]
    uid = es_results["uid"]
    ts = es_results["timestamp"]
    print "mid result: ", es_results
    query_body = {
        "query": {
            "bool":{
                "must":[
                    {"term":{"root_mid": mid}},
                    {"term": {"message_type": 3}}
                ]
            }
        },
        "aggs":{
            "hot_uid":{
                "terms":{"field": "directed_uid", "size":11}
            }
        }
    }
    index_list = []
    for i in range(2):
        index_name = flow_text_index_name_pre + ts2datetime(ts)
        if es_flow_text.indices.exists(index=index_name):
            index_list.append(index_name)
        ts = ts+3600*24

    results = es_flow_text.search(index=index_list, doc_type=flow_text_index_type, body=query_body)["aggregations"]["hot_uid"]["buckets"]
    retweet_dict = dict()
    for item in results:
        iter_uid = item["key"]
        if str(iter_uid) == str(uid):
            continue
        else:
            retweet_dict[str(iter_uid)] = item["doc_count"]
        
    print "retweet_dict: ", retweet_dict

    query_body = {
        "query": {
            "bool":{
                "must":[
                    {"term":{"root_mid": mid}},
                    {"term": {"message_type": 2}}
                ]
            }
        },
        "aggs":{
            "hot_uid":{
                "terms":{"field": "directed_uid", "size":11}
            }
        }
    }

    index_name = flow_text_index_name_pre + ts2datetime(ts)
    results = es_flow_text.search(index=index_list, doc_type=flow_text_index_type, body=query_body)["aggregations"]["hot_uid"]["buckets"]
    comment_dict = dict()
    for item in results:
        iter_uid = str(item["key"])
        if iter_uid == str(uid):
            continue
        else:
            comment_dict[iter_uid] = item["doc_count"]
        
    print "comment_dict: ", comment_dict

    # user_profile
    uid_list = list(set(comment_dict.keys())|set(retweet_dict.keys()))
    profile_results = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list})["docs"]
    profile_dict = dict()
    for item in profile_results:
        if item["found"]:
            item = item["_source"]
            iter_uid = str(item["uid"])
            tmp = dict()
            tmp["nick_name"] = item["nick_name"]
            if not tmp["nick_name"]:
                tmp["nick_name"] = iter_uid
            tmp["photo_url"] = item["photo_url"]
            profile_dict[iter_uid] = tmp
        else:
            tmp = dict()
            tmp["nick_name"] = item["_id"]
            tmp["photo_url"] = ""
            profile_dict[iter_uid] = tmp




    hot_retweet_list = []
    retweet_uid_list = retweet_dict.keys()
    retweet_list = es_flow_text.search(index=index_list, doc_type="text", body={"query":{"bool":{"must":[{"terms":{"uid":retweet_uid_list}}, {"term":{"root_mid":mid}}]}},"size":100})["hits"]["hits"]
    in_set = set()
    for item in retweet_list:
        item = item["_source"]
        iter_uid = str(item["uid"])
        if iter_uid in in_set:
            continue
        else:
            in_set.add(iter_uid)
        item["retweeted"] = retweet_dict[iter_uid]
        item["comment"] = query_retweeted(iter_uid, mid, ts, 2)# 获取转发微博的评论量
        item.update(profile_dict[iter_uid])
        hot_retweet_list.append(item)

    hot_retweet_list = sorted(hot_retweet_list, key=lambda x:x["retweeted"], reverse=True)

    hot_comment_list = []
    comment_uid_list = comment_dict.keys()
    comment_list = es_flow_text.search(index=index_list, doc_type="text", body={"query":{"bool":{"must":[{"terms":{"uid":comment_uid_list}}, {"term":{"root_mid":mid}}]}},"size":100})["hits"]["hits"]
    in_set = set()
    for item in comment_list:
        item = item["_source"]
        iter_uid = str(item["uid"])
        if iter_uid in in_set:
            continue
        else:
            in_set.add(iter_uid)
        item["comment"] = comment_dict[iter_uid]
        item["retweeted"] = query_retweeted(iter_uid, mid, ts, 3)# 获取转发微博的评论量
        item.update(profile_dict[iter_uid])
        hot_comment_list.append(item)

    hot_comment_list = sorted(hot_comment_list, key=lambda x:x["comment"], reverse=True)

    results = dict()
    results["hot_retweeted"] = hot_retweet_list
    results["hot_comment"] = hot_comment_list

    return results


def query_retweeted(uid, mid, ts, ttype=3):
    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"term":{"root_mid": mid}},
                    {"term": {"directed_uid": uid}},
                    {"term": {"message_type": ttype}}
                ]
            }
        }
    }

    index_list = []
    for i in range(2):
        index_name = flow_text_index_name_pre + ts2datetime(ts)
        if es_flow_text.indices.exists(index=index_name):
            index_list.append(index_name)
        ts = ts+3600*24

    count = es_flow_text.count(index=index_list, doc_type=flow_text_index_type, body=query_body)["count"]

    return count





if __name__ == "__main__":
    print get_time_series()

