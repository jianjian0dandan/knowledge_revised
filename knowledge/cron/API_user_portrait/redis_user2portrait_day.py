# -*- coding: utf-8 -*-
import sys
import time
import json
from weibo_api import read_flow_text, read_flow_text_sentiment
from cron_text_attribute import test_cron_text_attribute_v2
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import r_user_hash_name
from time_utils import ts2date, datetime2ts
from parameter import WEIBO_API_INPUT_TYPE

def scan_compute_redis():
    task_mark = 'user'
    hash_name = r_user_hash_name
    results = r.hgetall(hash_name)
    iter_user_list = []
    mapping_dict = dict()
    verify_mark_dict = dict()
    relation_mark_dict = dict()
    submit_user_dict = dict()
    submit_ts_dict = dict()
    count = 0
    for uid in results:
        user_list = json.loads(results[uid])
        in_date = user_list[0]
        status = user_list[1]
        verify_mark = user_list[2]
        relation_list = user_list[3]
        submit_user = user_list[4]
        submit_ts = datetime2ts(in_date)
        verify_mark_dict[uid] = verify_mark
        relation_mark_dict[uid] = relation_list
        submit_user_dict[uid] = submit_user
        submit_ts_dict[uid] = submit_ts
        if status == '2': #imme
            #test
            count += 1
            iter_user_list.append(uid)
            mapping_dict[uid] = json.dumps([in_date, '3', verify_mark, relation_list, submit_user]) # mark status:3 computing
        if len(iter_user_list) % 100 == 0 and len(iter_user_list) != 0:
            r.hmset(r_user_hash_name, mapping_dict)
            #acquire bulk user weibo data
            if WEIBO_API_INPUT_TYPE == 0:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(iter_user_list)
            else:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(iter_user_list)
            #compute text attribute
            compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts, relation_mark_dict, task_mark, submit_user_dict, submit_ts_dict)
            
            if compute_status==True:
                change_status_computed(mapping_dict)
            else:
                change_status_compute_fail(mapping_dict)
            
            #when uid user no weibo at latest week to change compute status to 1
            if len(user_keywords_dict) != len(iter_user_list):
                change_mapping_dict = dict()
                change_user_list = set(iter_user_list) - set(user_keywords_dict.keys())
                for change_user in change_user_list:
                    change_mapping_dict[change_user] = json.dumps([in_date, '2', verify_mark_dict[change_user], relation_mark_dict[change_user], submit_user_dict[change_user], submit_ts_dict[change_user]])
                r.hmset(r_user_hash_name, change_mapping_dict)

            iter_user_list = []
            mapping_dict = {}
            verify_mark_dict = dict()
            relation_mark_dict = dict()
            submit_user_dict = dict()
            submit_ts_dict = dict()
            
    if iter_user_list != [] and mapping_dict != {}:
        r.hmset(r_user_hash_name, mapping_dict)
        #acquire bulk user weibo date
        print 'iter_user_list:', len(iter_user_list)
        if WEIBO_API_INPUT_TYPE == 0:
            user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(iter_user_list)
        else:
            user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(iter_user_list)
        #compute text attribute
        print 'user_weibo_dict:', len(user_weibo_dict)
        compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts, relation_mark_dict, task_mark,submit_user_dict, submit_ts_dict)
        if compute_status==True:
            change_status_computed(mapping_dict)
        else:
            change_status_compute_fail(mapping_dict)
        #when uid user no weibo at latest week to change compute status to 1
        if len(user_keywords_dict) != len(iter_user_list):
            change_mapping_dict = dict()
            change_user_list = set(iter_user_list) - set(user_keywords_dict.keys())
            for change_user in change_user_list:
                change_mapping_dict[change_user] = json.dumps([in_date, '2', verify_mark_dict[change_user], relation_mark_dict[change_user], submit_user_dict[change_user], submit_ts_dict[change_user]])
            r.hmset(r_user_hash_name, change_mapping_dict)


def change_status_computed(mapping_dict):
    hash_name = r_user_hash_name
    status = 4
    new_mapping_dict = {}
    for uid in mapping_dict:
        user_list = json.loads(mapping_dict[uid])
        user_list[1] = '4'
        new_mapping_dict[uid] = json.dumps(user_list)
    r.hmset(hash_name, new_mapping_dict)

#use to deal compute fail situation
def change_status_compute_fail(mapping_dict):
    hash_name = r_user_hash_name
    status = 1
    new_mapping_dict = {}
    for uid in mapping_dict:
        user_list = json.loads(mapping_dict[uid])
        user_list[1] = '2'
        new_mapping_dict[uid] = json.dumps(user_list)
    r.hmset(hashname, new_mapping_dict)	


if __name__=='__main__':
    log_time_ts = int(time.time())
    print 'cron/API_user_portrait/redis_user2portrait_day.py&start&' + str(log_time_ts)
    
    #try:
    scan_compute_redis()
    #except Exception, e:
    #    print e, '&error&', ts2date(time.time())

    log_time_ts = int(time.time())
    print 'cron/API_user_portrait/redis_user2portrait_day.py&end&' + str(log_time_ts)
