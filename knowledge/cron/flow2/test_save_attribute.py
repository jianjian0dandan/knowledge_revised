# -*- coding: UTF-8 -*-
'''
test save in a redis not in the cluster_redis
'''
import sys
import csv
import json
import time
import redis
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_utils import R_CLUSTER_FLOW2 as r_cluster



# save redis as Date:{uid1:'{str(at_uid1):count1,... }', uid2:'str(at_uid2):count2,...'}
def save_at(uid, at_uid, timestamp):
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    key = str(uid)
    try:
        ruid_count_string = r_cluster.hget('at_'+str(ts), str(uid))
        ruid_count_dict = json.loads(ruid_count_string)
        try:
            ruid_count_dict[str(at_uid)] += 1
        except:
            ruid_count_dict[str(at_uid)] = 1
        r_cluster.hset('at_'+str(ts), str(uid), json.dumps(ruid_count_dict))
    except:
        r_cluster.hset('at_'+str(ts), str(uid), json.dumps({str(at_uid):1}))


#abandon in version-15-12-08
'''
# save redis as Date:{uid1:'{ip:count...}', uid2:'{ip:count....}'}
def save_city(uid, ip, timestamp):
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    key = str(uid)
    try:
        ip_count_string = r_cluster.hget('ip_'+str(ts), str(uid))
        ip_count_dict = json.loads(ip_count_string)
        try:
            ip_count_dict[str(ip)] += 1
        except:
            ip_count_dict[str(ip)] = 1
        r_cluster.hset('ip_'+str(ts), str(uid), json.dumps(ip_count_dict))
    except:
        r_cluster.hset('ip_'+str(ts), str(uid), json.dumps({str(ip):1}))
'''

#save redis as {date:{uid:'{ip:'timestamp1&timestamp2'}'}}
def save_city_timestamp(uid, ip, timestamp):
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    try:
        ip_timestamp_string = r_cluster.hget('new_ip_'+str(ts), str(uid))
        ip_timestamp_string_dict = json.loads(ip_timestamp_string)
        try:
            add_string = '&'+str(timestamp)
            ip_timestamp_string_dict[str(ip)] += add_string
        except:
            ip_timestamp_string_dict[str(ip)] = str(timestamp)
        r_cluster.hset('new_ip_'+str(ts), str(uid), json.dumps(ip_timestamp_string_dict))

    except:
        r_cluster.hset('new_ip_'+str(ts), str(uid), json.dumps({str(ip): str(timestamp)}))
        

# save redis as 'activity_' + Date:{uid1:'{}', uid2:'{}'}        
def save_activity(uid, ts, time_segment):
    key = str(ts)
    try:
        activity_count_dict = r_cluster.hget('activity_' + key, str(uid))
        activity_count_dict = json.loads(activity_count_dict)
        try:
            activity_count_dict[str(time_segment)] += 1
        except:
            activity_count_dict[str(time_segment)] = 1
        r_cluster.hset('activity_' + key, str(uid), json.dumps(activity_count_dict))
    except:
        r_cluster.hset('activity_' + key, str(uid), json.dumps({str(time_segment): 1}))

