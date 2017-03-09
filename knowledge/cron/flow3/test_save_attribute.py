# -*- coding: UTF-8 -*-
'''
test save in a redis not in the cluster_redis
'''
import re
import sys
import csv
import json
import time
import redis
from config import Day
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import R_BEGIN_TIME
from global_utils import retweet_redis_dict, comment_redis_dict
from global_utils import R_DICT
from parameter import RUN_TYPE, RUN_TEST_TIME

r_begin_ts = datetime2ts(R_BEGIN_TIME)

# two weeks retweet relation write to one db
# need add delete module
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = (((date_ts - r_begin_ts) / Day) / 7) % 2 + 1
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number

#use to save retweet and be_retweet
#write in version: 15-12-08
#input: uid, direct_uid, timestamp
#output: {'retweet_'+date_ts:{uid:{direct_uid:count, ...}}}   {'be_retweet_'+date_ts:{direct_uid:{uid:count, ...}}}
def save_retweet(uid, direct_uid, timestamp):
    db_number = get_db_num(timestamp)
    r = retweet_redis_dict[str(db_number)]
    r.hincrby('retweet_'+str(uid), str(direct_uid), 1)
    r.hincrby('be_retweet_'+str(direct_uid), str(uid), 1)

#use to save comment and be_comment
#write in version: 15-12-08
#input: uid, direct_uid, timestamp
#output: {'comment_'+date_ts:{uid:{direct_uid:count, ...}}}  {'be_comment_'+date_ts:{direct_uid:{uid:count, ...}}}
def save_comment(uid,direct_uid, timestamp):
    db_number = get_db_num(timestamp)
    r = comment_redis_dict[str(db_number)]
    r.hincrby('comment_'+str(uid), str(direct_uid), 1)
    r.hincrby('be_comment_'+str(direct_uid), str(uid), 1)


if __name__=='__main__':
    # test
    date1 = '2013-09-08'
    ts1 = datetime2ts(date1)
    date2 = '2013-09-15'
    ts2 = datetime2ts(date2)
    db_number = get_db_num(ts2)
