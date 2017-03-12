# -*- coding:utf-8 -*-
# version 3


import sys
import time
import json
import math
import numpy as np
from elasticsearch import Elasticsearch
from  mappings_social_sensing import mappings_sensing_task
from clustering import freq_word, tfidf, kmeans, text_classify, cluster_evaluation
from get_group_keywords import count_trend, detect_burst
reload(sys)
sys.path.append("../../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait
from global_utils import R_SOCIAL_SENSING as r
from time_utils import ts2datetime, datetime2ts, ts2date
from global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type
from parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
from parameter import SOCIAL_SENSOR_FORWARD_RANGE as forward_time_range
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_social_task
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import FORWARD_N as forward_n
from parameter import INITIAL_EXIST_COUNT as initial_count
from parameter import IMPORTANT_USER_NUMBER, IMPORTANT_USER_THRESHOULD, signal_brust, signal_track,\
                       signal_count_varition, signal_sentiment_varition, signal_nothing,signal_nothing_variation, \
                       unfinish_signal, finish_signal, signal_sensitive_variation, WARNING_SENSITIVE_COUNT, DAY

AVERAGE_COUNT = 4000
MEAN_COUNT = 100

# 获得前12个小时内 各个时间段内社会传感器发布微博的原创微博/转发微博/评论微博，计算均值和方差

def get_forward_numerical_info(task_name, ts, create_by):
    results = []
    ts_series = []
    for i in range(1, forward_n+1):
        ts_series.append(ts-i*time_interval)

    # check if detail es of task exists
    doctype = create_by + "-" + task_name
    index_exist = es_user_portrait.indices.exists_type(index_sensing_task, doctype)
    if not index_exist:
        print "new create task detail index"
        mappings_sensing_task(doctype)

    if ts_series:
        search_results = es_user_portrait.mget(index=index_sensing_task, doc_type=doctype, body={"ids":ts_series})['docs']
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
        """
        "aggs":{
            "all_count":{
                "terms":{"field":"root_uid", "size":1000}
            }
        }
        """
        "sort":{"user_fansnum":{"order":"desc"}},
        "size": 1000
    }

    datetime = ts2datetime(ts - time_segment)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    results = []
    if origin_mid_list and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_all_body, _source=False)["hits"]["hits"]
        if search_results:
            for item in search_results:
                results.append(item['_id'])

    return results



def social_sensing(task_detail):
    # 任务名 传感器 终止时间 之前状态 创建者 时间
    task_name = task_detail[0]
    social_sensors = task_detail[1]
    stop_time = task_detail[2]
    forward_warning_status = task_detail[3]
    create_by = task_detail[4]
    ts = int(task_detail[5])
    new = int(task_detail[6])

    print ts2date(ts)
    # PART 1
    
    forward_result = get_forward_numerical_info(task_name, ts, create_by)
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
    all_retweeted_list = []
    all_retweeted_list.extend(current_retweeted_mid_list)
    all_retweeted_list.extend(forward_retweeted_weibo_list)#被转发微博的mid/root-mid
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


    # PART 2
    # 聚合当前时间内积极、中性、悲伤、愤怒情绪分布
    # sentiment_dict = {"0": "neutral", "1":"positive", "2":"sad", "3": "anger"}
    sentiment_count = {"0": 0, "1": 0, "2": 0, "3": 0}
    search_results = aggregation_sentiment_related_weibo(ts, all_mid_list, time_interval)
    sentiment_count = search_results
    print "sentiment_count: ", sentiment_count
    negetive_key = ["2", "3", "4", "5", "6"]
    negetive_count = 0
    for key in negetive_key:
        negetive_count += sentiment_count[key]


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


    #判断感知
    burst_reason = signal_nothing_variation
    warning_status = signal_nothing
    finish = unfinish_signal # "0"
    process_status = "1"

    if forward_result[0]:
        # 根据移动平均判断是否有时间发生
        mean_count = forward_result[1]
        std_count = forward_result[2]
        mean_sentiment = forward_result[3]
        std_sentiment = forward_result[4]
        if mean_count >= MEAN_COUNT and current_total_count > mean_count+1.96*std_count or current_total_count >= len(all_mid_list)*AVERAGE_COUNT: # 异常点发生
            if forward_warning_status == signal_brust: # 已有事件发生，改为事件追踪
                warning_status = signal_track
            else:
                warning_status = signal_brust
            burst_reason += signal_count_varition # 数量异常

        if negetive_count > mean_sentiment+1.96*std_sentiment and mean_sentiment >= MEAN_COUNT or negetive_count >= len(all_mid_list)*AVERAGE_COUNT:
            warning_status = signal_brust
            burst_reason += signal_sentiment_varition # 负面情感异常, "12"表示两者均异常
            if forward_warning_status == signal_brust: # 已有事件发生，改为事件追踪
                warning_status = signal_track

    if int(stop_time) <= ts: # 检查任务是否已经完成
        finish = finish_signal
        process_status = "0"

    # 感知到的事, all_mid_list
    tmp_burst_reason = burst_reason
    topic_list = []
    sensitive_text_list = []

    # 有事件发生时开始
    #if warning_status:
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
                "size": 2000
            }
            search_results = es_text.search(index=index_list, doc_type="text", body=query_body)['hits']['hits']
            text_list = []
            tmp_sensitive_warning = ""
            sensitive_words_dict = dict()
            if search_results:
                for item in search_results:
                    iter_mid = item['_source']['mid']
                    iter_text = item['_source']['text']
                    iter_sensitive = item['_source'].get('sensitive', 0)
                    if iter_sensitive:
                        tmp_sensitive_warning = signal_sensitive_variation #涉及到敏感词的微博
                        sensitive_words_dict[iter_mid] = iter_sensitive
                    temp_dict = dict()
                    temp_dict["mid"] = iter_mid
                    temp_dict["text"] = iter_text
                    text_list.append(temp_dict)
            if tmp_sensitive_warning:
                warning_status = signal_brust
                burst_reason += signal_sensitive_variation
            sensitive_weibo_detail = {}
            if sensitive_words_dict:
                sensitive_mid_list = sensitive_words_dict.keys()
                sensitivie_weibo_detail = query_hot_weibo(ts, sensitive_mid_list, time_interval)

            """
            if len(text_list) == 1:
                top_word = freq_word(text_list[0])
                topic_list = [top_word.keys()]
            elif len(text_list) == 0:
                topic_list = []
                tmp_burst_reason = "" #没有相关微博，归零
                print "no relate weibo text"
            else:
                feature_words, input_word_dict = tfidf(text_list) #生成特征词和输入数据
                word_label, evaluation_results = kmeans(feature_words, text_list) #聚类
                inputs = text_classify(text_list, word_label, feature_words)
                clustering_topic = cluster_evaluation(inputs)
                print "clustering weibo topic"
                sorted_dict = sorted(clustering_topic.items(), key=lambda x:x[1], reverse=True)
                topic_list = []
                if sorted_dict:
                    for item in sorted_dict:
                        if item[0] != "other":
                            topic_list.append(word_label[item[0]])
                print "topic list: ", len(topic_list)
            """

    results = dict()
    if sensitive_weibo_detail:
        print "sensitive_weibo_detail: ", sensitive_weibo_detail
    results['sensitive_words_dict'] = json.dumps(sensitive_words_dict)
    results['sensitive_weibo_detail'] = json.dumps(sensitive_weibo_detail)
    results['origin_weibo_number'] = len(all_origin_list)
    results['retweeted_weibo_number'] = len(all_retweeted_list)
    results['origin_weibo_detail'] = json.dumps(origin_weibo_detail)
    results['retweeted_weibo_detail'] = json.dumps(retweeted_weibo_detail)
    results['retweeted_weibo_count'] = current_retweeted_count
    results['comment_weibo_count'] = current_comment_count
    results['weibo_total_number'] = current_total_count
    results['sentiment_distribution'] = json.dumps(sentiment_count)
    results['important_users'] = json.dumps(filter_important_list)
    results['unfilter_users'] = json.dumps(important_uid_list)
    results['burst_reason'] = tmp_burst_reason
    results['timestamp'] = ts
    #results['clustering_topic'] = json.dumps(topic_list)
    # es存储当前时段的信息
    doctype = create_by + '-' + task_name
    es_user_portrait.index(index=index_sensing_task, doc_type=doctype, id=ts, body=results)

    # 更新manage social sensing的es信息
    if not new:
        temporal_result = es_user_portrait.get(index=index_manage_social_task, doc_type=task_doc_type, id=doctype)['_source']
        temporal_result['warning_status'] = warning_status
        temporal_result['burst_reason'] = tmp_burst_reason
        temporal_result['finish'] = finish
        temporal_result['processing_status'] = process_status
        history_status = json.loads(temporal_result['history_status'])
        history_status.append([ts, task_name, warning_status])
        temporal_result['history_status'] = json.dumps(history_status)
        es_user_portrait.index(index=index_manage_social_task, doc_type=task_doc_type, id=doctype, body=temporal_result)
    else:
        print "test"
    return "1"

