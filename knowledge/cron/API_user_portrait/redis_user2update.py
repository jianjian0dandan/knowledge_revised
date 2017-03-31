# -*- coding: utf-8 -*-
'''
use to update by add task from user
'''
import sys
import time
import json
from weibo_api import read_flow_text, read_flow_text_sentiment
from cron_text_attribute import test_cron_text_attribute_v2
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import r_user_update_long_hash_name as r_user_update_hash_name
from global_config import ALL_PERSON_RELATION_LIST, ALL_VERIFIED_RELATION_LIST
from parameter import WEIBO_API_INPUT_TYPE

def scan_compute_redis_v2():
    task_type = 'user'
    bulk_action = []
    count = 0
    iter_user_list = []
    verified_mark_dict = dict()
    relation_mark_dict = dict()
    submit_user_dict = dict()
    submit_ts_dict = dict()
    while True:
        r_user_item = r.rpop(r_user_update_hash_name)
        #print 'r_user_item:', r_user_item
        if r_user_item:
            #print 'r_user_item:', r_user_item
            r_user_item = json.loads(r_user_item)
            uid = r_user_item[0]
            relation_mark = r_user_item[1]
            iter_user_list.append(uid)
            relation_mark_dict[uid] = relation_mark
            count += 1
        else:
            break

        if count % 100==0 and count != 0:
            if WEIBO_API_INPUT_TYPE == 0:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(iter_user_list)
            else:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(iter_user_list)
            compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts, relation_mark_dict, task_type, submit_user_dict, submit_ts_dict)

            iter_user_list = []
            relation_mark_dict = dict()

    if iter_user_list != []:
        if WEIBO_API_INPUT_TYPE == 0:
            user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(iter_user_list)
        else:
            user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(iter_user_list)
        compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts, relation_mark_dict, task_type, submit_user_dict, submit_ts_dict)


'''
def scan_compute_redis():
    hash_name = r_user_hash_name
    results = r.hgetall(hash_name)
    iter_user_list = []
    mapping_dict = dict()
    verify_mark_dict = dict()
    count = 0
    for uid in results:
        user_list = json.loads(results[uid])
        in_date = user_list[0]
        status = user_list[1]
        if status == '1': #imme
            #test
            count += 1
            iter_user_list.append(uid)
            mapping_dict[uid] = json.dumps([in_date, '3']) # mark status:3 computing
        if len(iter_user_list) % 100 == 0 and len(iter_user_list) != 0:
            r.hmset(r_user_hash_name, mapping_dict)
            #acquire bulk user weibo data
            if WEIBO_API_INPUT_TYPE == 0:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text_sentiment(iter_user_list)
            else:
                user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts = read_flow_text(iter_user_list)
            #compute text attribute
            compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts)
            
            if compute_status==True:
                change_status_computed(mapping_dict)
            else:
                change_status_compute_fail(mapping_dict)
            
            #when uid user no weibo at latest week to change compute status to 1
            if len(user_keywords_dict) != len(iter_user_list):
                change_mapping_dict = dict()
                change_user_list = set(iter_user_list) - set(user_keywords_dict.keys())
                for change_user in change_user_list:
                    change_mapping_dict[change_user] = json.dumps([in_date, '1'])
                r.hmset(r_user_hash_name, change_mapping_dict)

            iter_user_list = []
            mapping_dict = {}
            
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
        compute_status = test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts)
        if compute_status==True:
            change_status_computed(mapping_dict)
        else:
            change_status_compute_fail(mapping_dict)
        #when uid user no weibo at latest week to change compute status to 1
        if len(user_keywords_dict) != len(iter_user_list):
            change_mapping_dict = dict()
            change_user_list = set(iter_user_list) - set(user_keywords_dict.keys())
            for change_user in change_user_list:
                change_mapping_dict[change_user] = json.dumps([in_date, '1'])
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
        user_list[1] = '1'
        new_mapping_dict[uid] = json.dumps(user_list)
    r.hmset(hashname, new_mapping_dict)	
'''

if __name__=='__main__':
    log_time_ts = int(time.time())
    print 'cron/API_user_portrait/redis_user2update.py&start&' + str(log_time_ts)
    
    #try:
    scan_compute_redis_v2()
    #except Exception, e:
    #    print e, '&error&', ts2date(time.time())

    log_time_ts = int(time.time())
    print 'cron/API_user_portrait/redis_user2update.py&end&' + str(log_time_ts)
