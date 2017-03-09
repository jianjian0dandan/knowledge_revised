# -*- coding: UTF-8 -*-

# 知识图谱人物属性计算入口：
# 需要的用户列表存储在redis的uid_list的队列中；
# 如果人物画像中已有，则将人物属性导入到71的es中
# 如果没有，则需要调用人物属性计算程序，再导入es中

import sys
import time
import json
from elasticsearch import Elasticsearch
from weibo_api_v2 import read_flow_text, read_flow_text_sentiment
from km_cron_text_attribute import test_cron_text_attribute_v2
import redis
reload(sys)
sys.path.append('../../')
from global_config import remote_portrait_name, portrait_type
from global_utils import es_user_portrait
from parameter import WEIBO_API_INPUT_TYPE
from time_utils import ts2date
from global_utils import r_user as  r
from global_utils import es_km_user_portrait as es_km

def scan_compute_redis():
    iter_user_list = []
    mapping_dict = dict()
    #test
    count = 0
    while 1:
        uid = r.rpop("uid_list") #用户列表
        print uid
        count += 1
        if not uid:
            break
        iter_user_list.append(uid)
        if len(iter_user_list) % 100 == 0 and len(iter_user_list) != 0:
            #acquire bulk user weibo data
            out_list = es_km_storage(iter_uid_list)
            if out_list:
                iter_uid_list = out_list
                if WEIBO_API_INPUT_TYPE == 0:
                    user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(iter_user_list)
                else:
                    user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(iter_user_list)
                #compute text attribute
                compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts)
            
                if compute_status==True:
                    print "finish iteration"
                else:
                    for uid in iter_user_list:
                        r.lpush("uid_list", uid)
            
                #when uid user no weibo at latest week to change compute status to 1
                if len(user_keywords_dict) != len(iter_user_list):
                    change_mapping_dict = dict()
                    change_user_list = set(iter_user_list) - set(user_keywords_dict.keys())
                    for change_user in change_user_list:
                        r.lpush("uid_list",change_user)

            iter_user_list = []
            mapping_dict = {}
            
    if iter_user_list != []:
        #acquire bulk user weibo date
        print 'iter_user_list:', len(iter_user_list)
        out_list = es_km_storage(iter_user_list)
        iter_user_list = out_list
        if iter_user_list:
            if WEIBO_API_INPUT_TYPE == 0:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(iter_user_list)
            else:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(iter_user_list)
            #compute text attribute
            print 'user_weibo_dict:', len(user_weibo_dict)
            compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts)
            if compute_status==True:
                print "finish iteration"
            else:
                for uid in iter_user_list:
                    r.lpush("uid_list", uid)
            #when uid user no weibo at latest week to change compute status to 1
            if len(user_keywords_dict) != len(iter_user_list):
                change_mapping_dict = dict()
                change_user_list = set(iter_user_list) - set(user_keywords_dict.keys())
                for change_user in change_user_list:
                    r.lpush("uid_list",change_user)


def es_km_storage(uid_list):
    es_results = es_user_portrait.mget(index=remote_portrait_name, doc_type=portrait_type, body={"ids":uid_list})["docs"]
    in_list = []
    out_list = []
    bulk_action = []
    for item in es_results:
        if item["found"]:
            in_list.append(item["_id"])
            bulk_action.append(item["_source"])
        else:
            out_list.append(item["_id"])

    if bulk_action:
        es_km.bulk(bulk_action, index=portrait_name, doc_type=portrait_type, timeout=60) 

    return out_list



if __name__=='__main__':
    log_time_ts = int(time.time())
    print 'cron/text_attribute/scan_compute_redis_imm.py&start&' + str(log_time_ts)
    
    scan_compute_redis()

    log_time_ts = int(time.time())
    print 'cron/text_attribute/scan_compute_redis_imm.py&end&' + str(log_time_ts)
