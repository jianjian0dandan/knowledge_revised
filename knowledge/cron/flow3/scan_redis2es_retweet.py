# -*- coding=utf-8 -*-
'''
use to scan redis(retweet/be_retweet) to insert es
'''
import sys
import time
import json
import redis

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es
from global_utils import retweet_redis_dict, comment_redis_dict, redis_host_list
from global_config import R_BEGIN_TIME
from parameter import DAY, RUN_TYPE, RUN_TEST_TIME
from time_utils import ts2datetime, datetime2ts
from retweet_mappings import retweet_es_mappings, be_retweet_es_mappings


begin_ts = datetime2ts(R_BEGIN_TIME)


#use to get db_number which is needed to es
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = 2 - (((date_ts - begin_ts) / (DAY * 7))) % 2
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number


#use to get db retweet/be_retweet redis to es
def scan_retweet():
    count = 0
    scan_cursor = 0
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #get redis db number
    db_number = get_db_num(now_date_ts)
    #get redis db
    retweet_redis = retweet_redis_dict[str(db_number)]

    """
    # 1. 判断即将切换的db中是否有数据
    while 1:
        redis_host_list.pop(str(db_number))
        other_db_number = retweet_redis_dict[redis_host_list[0]] # 获得对应的redis
        current_dbsize = other_db_number.dbsize()
        if current_dbsize:
            break # 已经开始写入新的db，说明前一天的数据已经写完
        else:
            time.sleep(60)
    """
    # 2. 删除之前的es
    retweet_es_mappings(str(db_number))
    be_retweet_es_mappings(str(db_number))

    # 3. scan
    retweet_bulk_action = []
    be_retweet_bulk_action = []
    start_ts = time.time()
    #retweet count/be_retweet count
    retweet_count = 0
    be_retweet_count = 0
    while True:
        re_scan = retweet_redis.scan(scan_cursor, count=100)
        re_scan_cursor = re_scan[0]
        for item in re_scan[1]:
            count += 1
            item_list = item.split('_')
            save_dict = {}
            if len(item_list)==2:
                retweet_count += 1
                uid = item_list[1]
                item_result = retweet_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_retweet'] = json.dumps(item_result)
                retweet_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
            elif len(item_list)==3:
                be_retweet_count += 1
                uid = item_list[2]
                item_result = retweet_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_be_retweet'] = json.dumps(item_result)
                be_retweet_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
        
        if retweet_bulk_action:
            es.bulk(retweet_bulk_action, index='1225_retweet_'+str(db_number), doc_type='user')
        if be_retweet_bulk_action:
            es.bulk(be_retweet_bulk_action, index='1225_be_retweet_'+str(db_number), doc_type='user')
        retweet_bulk_action = []
        be_retweet_bulk_action = []
        end_ts = time.time()
        #run_type
        if RUN_TYPE == 0:
            print '%s sec scan %s count user:' %(end_ts - start_ts, count)
        start_ts = end_ts
        scan_cursor = re_scan[0]
        if scan_cursor==0:
            break

    # 4. flush redis
    #retweet_redis.flushdb()


def split_bulk_action(bulk_action, index_name):
    new_bulk_action = []
    for i in range(0, len(bulk_action)):
        if i % 2 == 0:
            new_bulk_action = [bulk_action[i], bulk_action[i+1]]
            try:
                es.bulk(new_bulk_action, index=index_name, doc_type='user')
            except:
                print 'cron/flow3/scan_redis2es_retweet.py&error-1&'




if __name__=='__main__':
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)

    scan_retweet()
    print 'cron/flow3/scan_redis2es_retweet.py&start&' + log_time_date

    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/flow3/scan_redis2es_comment.py&end&' + log_time_date
