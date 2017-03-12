# -*- coding: UTF-8 -*-
import sys
import csv
import json
import time
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_DICT, es_retweet, retweet_index_name_pre, retweet_index_type
from time_utils import datetime2ts, ts2datetime
from parameter import DAY
from parameter import RUN_TYPE, RUN_TEST_TIME
from parameter import RECOMMEND_IN_ACTIVITY_THRESHOLD as activity_threshold
from parameter import RECOMMEND_IN_IP_THRESHOLD as  ip_threshold
from parameter import RECOMMEND_IN_RETWEET_THRESHOLD as  retweet_threshold
from parameter import RECOMMEND_IN_MENTION_THRESHOLD as mention_threshold
from cron.detect.cron_detect import get_db_num


csvfile = open('/home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/cron/recommentation_in/filter_uid_list.csv', 'wb')
writer = csv.writer(csvfile)



def filter_activity(user_set):
    results = []
    #run_type
    if RUN_TYPE == 1:
        now_date = ts2datetime(time.time())
    else:
        now_date = RUN_TEST_TIME
    ts = datetime2ts(now_date) - DAY
    date = ts2datetime(ts)
    timestamp = datetime2ts(date)
    for user in user_set:
        over_count = 0
        for i in range(0,7):
            ts = timestamp - DAY*i
            result = r_cluster.hget('activity_'+str(ts), str(user))
            if result:
                items_dict = json.loads(result)
                for item in items_dict:
                    weibo_count = items_dict[item]
                    if weibo_count > activity_threshold:
                        over_count += 1
        if over_count == 0:
            results.append(user)
        else:
            writer.writerow([user, 'activity'])
            
    return results

def filter_ip(user_set):
    results = []
    #run_type
    if RUN_TYPE == 1:
        now_date = ts2datetime(time.time())
    else:
        now_date = RUN_TEST_TIME
    ts = datetime2ts(now_date) - DAY
    for user in user_set:
        ip_set = set()
        for i in range(0,7):
            timestamp = ts - DAY*i
            ip_result = r_cluster.hget('ip_'+str(ts), str(user))
            if ip_result:
                result_dict = json.loads(ip_result)
            else:
                result_dict = {}
            for ip in result_dict:
                ip_set.add(ip)
        if len(ip_set) < ip_threshold:
            results.append(user)
        else:
            writer.writerow([user, 'ip'])
    return results

def filter_retweet_count(user_set):
    FILTER_ITER_COUNT = 100;
    results = []
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    retweet_index_name = retweet_index_name_pre + str(db_number)
    # test
    search_user_count = len(user_set);
    iter_search_count = 0
    while iter_search_count < search_user_count:
        iter_search_user_list = user_set[iter_search_count:iter_search_count + FILTER_ITER_COUNT]
        try:
            retweet_result = es_retweet.mget(index = retweet_index_name, doc_type = retweet_index_type,\
                    body = {'ids':iter_search_user_list}, _source=True)['docs']
        except:
            retweet_result = []
        for retweet_item in retweet_result:
            if retweet_item['found']:
                retweet_set = set()
                user = retweet_item['_id']
                per_retweet_result = json.loads(retweet_item['_source']['uid_retweet'])
                for retweet_user in per_retweet_result:
                    retweet_set.add(retweet_user)
                if len(retweet_set) < retweet_threshold:
                    results.append(user)
                else:
                    writer.writerow([user, 'retweet'])
            else:
                user = retweet_item['_id']
                results.append(user)

        iter_search_count += FILTER_ITER_COUNT
    return results

def filter_mention(user_set):
    results = []
    #run_type
    if RUN_TYPE == 1:
        now_date = ts2datetime(time.time())
    else:
        now_date = RUN_TEST_TIME
    timestamp = datetime2ts(now_date) - DAY
    date = ts2datetime(timestamp)
    for user in user_set:
        mention_set = set()
        for i in range(0,7):
            ts = timestamp - DAY*i
            result = r_cluster.hget('at_'+str(ts), str(user))
            if result:
                item_dict = json.loads(result)
                for at_user in item_dict:
                    mention_set.add(at_user)
        at_count = len(mention_set)
        if at_count < mention_threshold:
            results.append(user)
        else:
            writer.writerow([user, 'mention'])
    return results
