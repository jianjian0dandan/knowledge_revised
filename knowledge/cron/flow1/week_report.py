# -*- coding: utf-8 -*-
import time
import math
from timeit import Timer
import sys
import json
from index_cal import influence_weibo_cal
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('../../')
from global_utils import _default_es_cluster_flow1

es = _default_es_cluster_flow1
#index_name = time.strftime("%Y%m%d",time.localtime(time.time()-86400))
#index_name = time.strftime("%Y%m%d",time.localtime(1377964800))
index_type = "bci"

def search_top_k(k, index_name, index_type="bci"):
    query_body = {
        "query": {
            "match_all": {}
        },
        "sort": [{"user_index": {"order": "desc"}}],
        "size": k
    }
    
    result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    
    return result


def average_weibo(weibo_number, total_number):
    if weibo_number == 0:
        return 0
    else:
        aver_number = float(total_number)/weibo_number
        return aver_number

def top_number(number_1, number_2):
    return max(number_1, number_2)

def average_number(number_1, number_2):
    return (int(number_1) + int(number_2))/2

def brust_degree(brust_1, brust_2):
    time_scale = average_number(brust_1[0], brust_2[0])
    if time_scale == 0:
        return (0,0)
    else:
        time_number = (brust_1[0]*brust_1[1]+brust_2[0]*brust_2[1])/time_scale
        return (time_scale, time_number)

def user_index_cal(origin_weibo_number, retweeted_weibo_number, user_fansnum, influence_origin_weibo_retweeted, influence_origin_weibo_comment, influence_retweeted_weibo_retweeted, influence_retweeted_weibo_comment):
    user_index = 300*(0.2*(0.6*math.log(origin_weibo_number+1)+0.3*math.log(retweeted_weibo_number+1)+0.1*math.log(int(user_fansnum)+1))+0.8*(0.3*influence_origin_weibo_retweeted+\
    0.3*influence_origin_weibo_comment+0.2*influence_retweeted_weibo_retweeted+0.2*influence_retweeted_weibo_comment))
    return user_index



def list_merge(list_1, list_2):
    result_set = []
    common_user = []
    accumulate_keys = ["origin_weibo_number", "retweeted_weibo_number", "origin_weibo_retweeted_total_number", "origin_weibo_comment_total_number",\
            "retweeted_weibo_comment_total_number", "retweeted_weibo_retweeted_total_number"]
    top_keys = ['origin_weibo_retweeted_top_number', 'origin_weibo_comment_top_number', 'retweeted_weibo_retweeted_top_number', 'retweeted_weibo_comment_top_number']
    average_keys = ["user_fansnum"]
    brust_keys = [('origin_weibo_retweeted_brust_n','origin_weibo_retweeted_brust_average'), ('origin_weibo_comment_brust_n','origin_weibo_comment_brust_average'),\
            ('retweeted_weibo_retweeted_brust_n','retweeted_weibo_retweeted_brust_average'), ('retweeted_weibo_comment_brust_n','retweeted_weibo_comment_brust_average')]
    for item_1 in list_1:
        for item_2 in list_2:
            if item_1["_id"] == item_2["_id"]:
                common_user.append(item_2["_id"])
                source_1 = item_1['_source']
                source_2 = item_2['_source']
                for iter_key in accumulate_keys:
                    source_2[iter_key] += source_1[iter_key]

                for iter_key in top_keys:
                    source_2[iter_key] = top_number(source_1[iter_key], source_2[iter_key])

                for iter_key in average_keys:
                    source_2[iter_key] = average_number(source_1[iter_key], source_2[iter_key])

                for key_1, key_2 in brust_keys:
                    brust_result = brust_degree((source_1[key_1],source_1[key_2]), (source_2[key_1],source_2[key_2]))
                    source_2[key_1] = brust_result[0]
                    source_2[key_2] = brust_result[1]

                source_2['origin_weibo_retweeted_average_number'] = average_weibo(source_2['origin_weibo_number'],source_2["origin_weibo_retweeted_total_number"])
                source_2['origin_weibo_comment_average_number'] = average_weibo(source_2['origin_weibo_number'],source_2["origin_weibo_comment_total_number"])
                source_2['retweeted_weibo_retweeted_average_number'] = average_weibo(source_2['retweeted_weibo_number'],source_2["retweeted_weibo_retweeted_total_number"])
                source_2['retweeted_weibo_comment_average_number'] = average_weibo(source_2['retweeted_weibo_number'],source_2["retweeted_weibo_comment_total_number"])

                influence_origin_weibo_retweeted = influence_weibo_cal(source_2['origin_weibo_retweeted_total_number'],source_2['origin_weibo_retweeted_average_number'],\
                        source_2['origin_weibo_retweeted_top_number'],(source_2['origin_weibo_retweeted_brust_n'],source_2['origin_weibo_retweeted_brust_average']))
                influence_origin_weibo_comment = influence_weibo_cal(source_2['origin_weibo_comment_total_number'], source_2['origin_weibo_comment_average_number'], \
                        source_2['origin_weibo_comment_top_number'], (source_2['origin_weibo_comment_brust_n'],source_2['origin_weibo_comment_brust_average']))
                influence_retweeted_weibo_retweeted = influence_weibo_cal(source_2['retweeted_weibo_retweeted_total_number'], source_2['retweeted_weibo_retweeted_average_number'],\
                        source_2['retweeted_weibo_retweeted_top_number'], (source_2['retweeted_weibo_retweeted_brust_n'],source_2['retweeted_weibo_retweeted_brust_average']))
                influence_retweeted_weibo_comment = influence_weibo_cal(source_2['retweeted_weibo_comment_total_number'], source_2['retweeted_weibo_comment_average_number'], \
                        source_2['retweeted_weibo_comment_top_number'], (source_2['retweeted_weibo_retweeted_brust_n'],source_2['retweeted_weibo_retweeted_brust_average']))
                source_2['user_index'] = user_index_cal(source_2['origin_weibo_number'], source_2['retweeted_weibo_number'], source_2['user_fansnum'], influence_origin_weibo_retweeted,\
                        influence_origin_weibo_comment, influence_retweeted_weibo_retweeted, influence_retweeted_weibo_comment)

                item_2['_source'] = source_2
                result_set.append(item_2)

                list_1.remove(item_1)
                list_2.remove(item_2)
    [result_set.append(item) for item in list_1]
    [result_set.append(item) for item in list_2]
    return result_set

def write_to_json(result, index_name):
    f = open("%s_sort.jl" %index_name, "wb")
    for item in result:
        user_item = {}
        user_item["_id"] = item['_id']
        user_item["_time"] = item['_index']
        user_item["user_info"] = item['_source']
        line = json.dumps(user_item) + "\n"
        f.write(line)

def store_to_elasticsearch(es,result,index_name):
    es.indices.create(index=index_name, ignore=400)
    bulk_actions = []
    count = 0
    for everyone in result:
        user_info = everyone['_source']
        x = expand_index_action(everyone)
        bulk_actions.extend([x[0], x[1]])
        count += 1
        if count % 1000 == 0:
            print count
            while 1:
                try:
                    es.bulk(bulk_actions, index=index_name, doc_type="bci", timeout=30)
                    bulk_actions = []
                    break
                except Exception,r:
                    print Exception,':',r
                    es = _default_es_cluster_flow1
                    continue
    es.bulk(bulk_actions, index=index_name, doc_type="bci", timeout=30)

def expand_index_action(data):
    _id = data['_id']
    action = {'index': {"_id": _id} }
    return action, data


if __name__ == "__main__":

    """
    a week report of weibo from elasticsearch

    """

    #index_time = 1377964800
    start_index = time.strftime("%Y%m%d",time.localtime(time.time() - 86400))
    start_list = search_top_k(20000, start_index)
    for i in range(1,7):
        index_time = index_time - 86400
        next_index = time.strftime("%Y%m%d",time.localtime(index_time))
        next_list = search_top_k(20000, next_index)
        start_list = list_merge(start_list, next_list)
    store_to_elasticsearch(es, start_list, start_index+"_7days")





