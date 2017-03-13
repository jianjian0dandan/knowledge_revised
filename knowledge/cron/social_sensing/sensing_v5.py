# -*- coding:utf-8 -*-
# version 3


import sys
import time
import json
import math
import numpy as np
from elasticsearch import Elasticsearch
from  mappings_social_sensing import mappings_sensing_task
from text_classify.test_topic import topic_classfiy
from duplicate import duplicate
from extract_feature_0312 import organize_feature, trendline_list
import pickle
reload(sys)
sys.path.append("../../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_profile as es_profile
from global_utils import R_SOCIAL_SENSING as r
from global_utils import es_prediction
from time_utils import ts2datetime, datetime2ts, ts2date

from global_config import topic_value_dict
AVERAGE_COUNT = 4000
MEAN_COUNT = 100


time_interval = 3600
forward_time_range = 12*3600
DAY = 24*3600
index_sensing_task = "social_sensing_task"
type_sensing_task = "social_sensing"
index_manage_social_task = "manage_sensing_task"
task_doc_type = "task"
forward_n = 24
initial_count = 12
flow_text_index_name_pre = "flow_text_"
flow_text_index_type = "text"
profile_index_name = "weibo_user"
profile_index_type = "user"

# 获得前12个小时内 各个时间段内社会传感器发布微博的原创微博/转发微博/评论微博，计算均值和方差

def get_forward_numerical_info(task_name, ts):
    results = []
    ts_series = []
    for i in range(1, forward_n+1):
        ts_series.append(ts-i*time_interval)

    # check if detail es of task exists
    doctype = task_name
    index_exist = es_prediction.indices.exists_type(index_sensing_task, doctype)
    if not index_exist:
        print "new create task detail index"
        mappings_sensing_task(doctype)

    if ts_series:
        search_results = es_prediction.mget(index=index_sensing_task, doc_type=doctype, body={"ids":ts_series})['docs']
        found_count = 0
        average_origin = []
        average_retweeted = []
        average_commet = []
        average_total = []
        average_negetive = []
        for item in search_results:
            if item['found']:
                temp = item['_source']
                sentiment_dict = json.loads(temp['sentiment_distribution'])
                average_total.append(int(temp['weibo_total_number']))
                average_negetive.append(int(sentiment_dict["2"])+int(sentiment_dict['3'])+int(sentiment_dict['4'])+int(sentiment_dict['5'])+int(sentiment_dict['6']))
                found_count += 1

        if found_count > initial_count:
            number_mean = np.mean(average_total)
            number_std = np.std(average_total)
            sentiment_mean = np.mean(average_negetive)
            sentiment_std = np.mean(average_negetive)
            results = [1, number_mean, number_std, sentiment_mean, sentiment_std]
        else:
            results = [0]

    return results

# 给定社会传感器，查找原创微博列表
def query_mid_list(ts, social_sensors, time_segment, message_type=1):
    query_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must":[
                            {"range": {
                                "timestamp": {
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"uid": social_sensors}},
                            {"term":{"message_type": message_type}}
                        ]
                    }
                }
            }
        },
        "sort": {"sentiment": {"order": "desc"}},
        "size": 10000
    }

    datetime_1 = ts2datetime(ts)
    datetime_2 = ts2datetime(ts-24*3600)
    index_name_1 = flow_text_index_name_pre + datetime_1
    index_name_2 = flow_text_index_name_pre + datetime_2
    index_list = []
    exist_es_1 = es_text.indices.exists(index_name_1)
    exist_es_2 = es_text.indices.exists(index_name_2)
    if exist_es_1:
        index_list.append(index_name_1)
    if exist_es_2:
        index_list.append(index_name_2)
    if index_list:
        search_results = es_text.search(index=index_list, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    else:
        search_results = []
    origin_mid_list = set()
    if search_results:
        for item in search_results:
            if message_type == 1:
                origin_mid_list.add(item["_id"])
            else:
                origin_mid_list.add(item['_source']['root_mid'])

    return list(origin_mid_list)


# 给定原创微博list，搜索之前time_segment时间段内的微博总数，即转发和评论总数
def query_related_weibo(ts, origin_mid_list, time_segment):
    query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"root_mid":origin_mid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_count":{
                "terms":{"field": "message_type"}
            }
        }
    }

    return_results = {"origin": 0, "retweeted": 0, "comment": 0}
    datetime_1 = ts2datetime(ts)
    datetime_2 = ts2datetime(ts-24*3600)
    index_name_1 = flow_text_index_name_pre + datetime_1
    index_name_2 = flow_text_index_name_pre + datetime_2
    index_list = []
    exist_es_1 = es_text.indices.exists(index_name_1)
    exist_es_2 = es_text.indices.exists(index_name_2)
    if exist_es_1:
        index_list.append(index_name_1)
    if exist_es_2:
        index_list.append(index_name_2)
    if index_list:
        results = es_text.search(index=index_list, doc_type=flow_text_index_type,body=query_all_body)['aggregations']['all_count']['buckets']
        if results:
            for item in results:
                if int(item['key']) == 1:
                    return_results['origin'] = item['doc_count']
                elif int(item['key']) == 3:
                    return_results['retweeted'] = item['doc_count']
                elif int(item['key']) == 2:
                    return_results['comment'] = item['doc_count']
                else:
                    pass

    return_results['total_count'] = sum(return_results.values())
    return return_results



# 给定原创微博list， 聚合热门微博的转发量和评论量
def query_hot_weibo(ts, origin_mid_list, time_segment):
    query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"root_mid":origin_mid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_mid":{
                "terms":{"field": "root_mid", "size":400},
                "aggs":{
                    "message_type":{
                        "terms":{
                            "field":"message_type"
                        }
                    }
                }
            }
        }
    }

    return_results = dict()
    datetime_1 = ts2datetime(ts)
    datetime_2 = ts2datetime(ts-24*3600)
    index_name_1 = flow_text_index_name_pre + datetime_1
    index_name_2 = flow_text_index_name_pre + datetime_2
    index_list = []
    exist_es_1 = es_text.indices.exists(index_name_1)
    exist_es_2 = es_text.indices.exists(index_name_2)
    if exist_es_1:
        index_list.append(index_name_1)
    if exist_es_2:
        index_list.append(index_name_2)
    if index_list:
        results = es_text.search(index=index_list, doc_type=flow_text_index_type,body=query_all_body)['aggregations']['all_mid']['buckets']
        if results:
            for item in results:
                temp_dict = dict()
                temp_dict[item['key']] = item['doc_count']
                detail = item['message_type']['buckets']
                detail_dict = dict()
                for iter_item in detail:
                    detail_dict[iter_item['key']] = iter_item['doc_count']
                temp_dict['retweeted'] = detail_dict.get(3, 0)
                temp_dict['comment'] = detail_dict.get(2, 0)
                return_results[item['key']] = temp_dict
        else:
            for item in origin_mid_list:
                temp_dict = dict()
                temp_dict[item] = 0
                temp_dict['retweeted'] = 0
                temp_dict['comment'] = 0
                return_results[item] = temp_dict

    return return_results

# 给定原创微博list，搜索之前time_segment时间段内的微博情绪
def aggregation_sentiment_related_weibo(ts, origin_mid_list, time_segment, message_type=1, uid_list=[]):
    if message_type == 1:
        query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"root_mid":origin_mid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_sentiments":{
                "terms":{ "field": "sentiment"}
            }
        }
        }
    else:
        query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"root_mid":origin_mid_list}},
                            {"terms":{"directed_uid": uid_list}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_sentiments":{
                "terms":{ "field": "sentiment"}
            }
        }
    }

    results = {"0": 0, "1": 0, "2":0, "3": 0, "4": 0, "5": 0, "6": 0}
    datetime_1 = ts2datetime(ts)
    datetime_2 = ts2datetime(ts-24*3600)
    index_name_1 = flow_text_index_name_pre + datetime_1
    index_name_2 = flow_text_index_name_pre + datetime_2
    index_list = []
    exist_es_1 = es_text.indices.exists(index_name_1)
    exist_es_2 = es_text.indices.exists(index_name_2)
    if exist_es_1:
        index_list.append(index_name_1)
    if exist_es_2:
        index_list.append(index_name_2)
    if index_list:
        search_results = es_text.search(index=index_list, doc_type=flow_text_index_type,body=query_all_body)['aggregations']['all_sentiments']['buckets']
        if search_results:
            for item in search_results:
                key = item['key']
                count = item['doc_count']
                results[key] = count
    print "results: ", results, sum(results.values())
    return results

# 给定所有原创微博list，搜索在time-time-interval时间内的热门微博root-uid
def get_important_user(ts, origin_mid_list, time_segment):
    query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }}],
                        "should": [
                            {"terms":{"root_mid":origin_mid_list}},
                            {"terms":{"mid":origin_mid_list}}
                        ]
                    }
                }
            }
        },
        "sort":{"user_fansnum":{"order":"desc"}},
        "size": 1000
    }

    datetime = ts2datetime(ts - time_segment)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    results = []
    if origin_mid_list and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_all_body,fields=["uid"], _source=False)["hits"]["hits"]
        if search_results:
            for item in search_results:
                results.append(item['fields']['uid'][0])

    return results



def social_sensing(task_detail):

    with open("prediction_uid.pkl", "r") as f:
        uid_model = pickle.load(f)
    with open("prediction_weibo.pkl", "r") as f:
        weibo_model = pickle.load(f)

    # 任务名 传感器 终止时间 之前状态 创建者 时间
    task_name = task_detail[0]
    social_sensors = task_detail[1]
    ts = int(task_detail[2])

    print ts2date(ts)
    # PART 1
    
    #forward_result = get_forward_numerical_info(task_name, ts, create_by)
    # 之前时间阶段内的原创微博list/retweeted
    forward_origin_weibo_list = query_mid_list(ts-time_interval, social_sensors, forward_time_range)
    forward_retweeted_weibo_list = query_mid_list(ts-time_interval, social_sensors, forward_time_range, 3)
    # 当前阶段内原创微博list
    current_mid_list = query_mid_list(ts, social_sensors, time_interval)
    current_retweeted_mid_list = query_mid_list(ts, social_sensors, time_interval, 3)
    all_mid_list = []
    all_mid_list.extend(current_mid_list)
    all_mid_list.extend(current_retweeted_mid_list)
    all_mid_list.extend(forward_origin_weibo_list)
    all_mid_list.extend(forward_retweeted_weibo_list)
    all_origin_list = []
    all_origin_list.extend(current_mid_list)
    all_origin_list.extend(forward_origin_weibo_list)
    all_origin_list = list(set(all_origin_list))
    all_retweeted_list = []
    all_retweeted_list.extend(current_retweeted_mid_list)
    all_retweeted_list.extend(forward_retweeted_weibo_list)#被转发微博的mid/root-mid
    all_retweeted_list = list(set(all_retweeted_list))
    print "all mid list: ", len(all_mid_list)
    #print "all_origin_list", all_origin_list
    #print "all_retweeted_list", all_retweeted_list

    # 查询微博在当前时间内的转发和评论数, 聚合按照message_type
    statistics_count = query_related_weibo(ts, all_mid_list, time_interval)
    if all_origin_list:
        origin_weibo_detail = query_hot_weibo(ts, all_origin_list, time_interval) # 原创微博详情
    else:
        origin_weibo_detail = {}
    if all_retweeted_list:
        retweeted_weibo_detail = query_hot_weibo(ts, all_retweeted_list, time_interval) # 转发微博详情
    else:
        retweeted_weibo_detail = {}
    current_total_count = statistics_count['total_count']

    # 当前阶段内所有微博总数
    current_retweeted_count = statistics_count['retweeted']
    current_comment_count = statistics_count['comment']


    """
    # 聚合当前时间内重要的人
    important_uid_list = []
    datetime = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        search_results = get_important_user(ts, all_mid_list, time_interval)
        important_uid_list = search_results
    # 根据获得uid_list，从人物库中匹配重要人物
    if important_uid_list:
        important_results = es_user_portrait.mget(index=portrait_index_name,doc_type=portrait_index_type, body={"ids": important_uid_list})['docs']
    else:
        important_results = []
    filter_important_list = [] # uid_list
    if important_results:
        for item in important_results:
            if item['found']:
                #if item['_source']['importance'] > IMPORTANT_USER_THRESHOULD:
                filter_important_list.append(item['_id'])

    print "filter_important_list", filter_important_list
    print "important_results", important_uid_list
    """

    #判断感知



    # 感知到的事, all_mid_list
    sensitive_text_list = []
    tmp_sensitive_warning = ""
    text_dict = dict() # 文本信息
    mid_value = dict() # 文本赋值
    duplicate_dict = dict() # 重合字典
    portrait_dict = dict() # 背景信息
    classify_text_dict = dict() # 分类文本
    classify_uid_list = []
    duplicate_text_list = []
    sensitive_words_dict = dict()
    sensitive_weibo_detail = {}
    trendline_dict = dict()

    # 有事件发生时开始
    if 1:
        index_list = []
        important_words = []
        datetime_1 = ts2datetime(ts)
        index_name_1 = flow_text_index_name_pre + datetime_1
        exist_es = es_text.indices.exists(index=index_name_1)
        if exist_es:
            index_list.append(index_name_1)
        datetime_2 = ts2datetime(ts-DAY)
        index_name_2 = flow_text_index_name_pre + datetime_2
        exist_es = es_text.indices.exists(index=index_name_2)
        if exist_es:
            index_list.append(index_name_2)
        if index_list and all_mid_list:
            query_body = {
                "query":{
                    "filtered":{
                        "filter":{
                            "terms":{"mid": all_mid_list}
                        }
                    }
                },
                "size": 5000
            }
            search_results = es_text.search(index=index_list, doc_type="text", body=query_body)['hits']['hits']
            tmp_sensitive_warning = ""
            text_dict = dict() # 文本信息
            mid_value = dict() # 文本赋值
            duplicate_dict = dict() # 重合字典
            portrait_dict = dict() # 背景信息
            classify_text_dict = dict() # 分类文本
            classify_uid_list = []
            duplicate_text_list = []
            sensitive_words_dict = dict()
            uid_prediction_dict = dict()
            weibo_prediction_dict = dict()
            trendline_dict = dict()
            if search_results:
                for item in search_results:
                    iter_uid = item['_source']['uid']
                    iter_mid = item['_source']['mid']
                    iter_text = item['_source']['text'].encode('utf-8', 'ignore')
                    iter_sensitive = item['_source'].get('sensitive', 0)

                    duplicate_text_list.append({"_id":iter_mid, "title": "", "content":iter_text.decode("utf-8",'ignore')})

                    if iter_sensitive:
                        tmp_sensitive_warning = signal_sensitive_variation #涉及到敏感词的微博
                        sensitive_words_dict[iter_mid] = iter_sensitive

                    keywords_dict = json.loads(item['_source']['keywords_dict'])
                    personal_keywords_dict = dict()
                    for k, v in keywords_dict.iteritems():
                        k = k.encode('utf-8', 'ignore')
                        personal_keywords_dict[k] = v
                    classify_text_dict[iter_mid] = personal_keywords_dict
                    classify_uid_list.append(iter_uid)

                # 去重
                if duplicate_text_list:
                    dup_results = duplicate(duplicate_text_list)
                    for item in dup_results:
                        if item['duplicate']:
                            duplicate_dict[item['_id']] = item['same_from']

                # 分类
                mid_value = dict()
                if classify_text_dict:
                    classify_results = topic_classfiy(classify_uid_list, classify_text_dict)
                    #print "classify_results: ", classify_results
                    for k,v in classify_results.iteritems(): # mid:value
                        mid_value[k] = topic_value_dict[v[0]]
                        feature_list = organize_feature(k, v[0])
                        uid_prediction = uid_model.predict(feature_list)
                        for iiii in uid_prediction:
                            uid_prediction_value = iiii
                        uid_prediction_dict[k] = uid_prediction_value
                        weibo_prediction = weibo_model.predict(feature_list)
                        for iii in weibo_prediction:
                            weibo_prediction_value = iii
                        weibo_prediction_dict[k] = weibo_prediction_value
                        tmp_trendline = trendline_list(k, weibo_prediction_value)
                        trendline_dict[k] = tmp_trendline

            if sensitive_words_dict:
                sensitive_mid_list = sensitive_words_dict.keys()
                sensitivie_weibo_detail = query_hot_weibo(ts, sensitive_mid_list, time_interval)


    results = dict()
    results["trendline_dict"] = json.dumps(tmp_trendline)
    results['mid_topic_value'] = json.dumps(mid_value)
    results['duplicate_dict'] = json.dumps(duplicate_dict)
    results["uid_prediction_dict"] = json.dumps(uid_prediction_dict)
    results["weibo_prediction_dict"] = json.dumps(weibo_prediction_dict)
    results['sensitive_words_dict'] = json.dumps(sensitive_words_dict)
    results['sensitive_weibo_detail'] = json.dumps(sensitive_weibo_detail)
    results['origin_weibo_number'] = len(all_origin_list)
    results['retweeted_weibo_number'] = len(all_retweeted_list)
    results['origin_weibo_detail'] = json.dumps(origin_weibo_detail)
    results['retweeted_weibo_detail'] = json.dumps(retweeted_weibo_detail)
    results['retweeted_weibo_count'] = current_retweeted_count
    results['comment_weibo_count'] = current_comment_count
    results['weibo_total_number'] = current_total_count
    results['timestamp'] = ts
    # es存储当前时段的信息
    es_prediction.index(index=index_sensing_task, doc_type=type_sensing_task, id=ts, body=results)

    return "1"

