# -*- coding=utf-8 -*-

import re
import zmq
import time
import json
import math
import sys
import redis
from datetime import datetime
reload(sys)
sys.path.append('../../')
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1, ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1 
from global_utils import  R_CLUSTER_FLOW1
from global_utils import uname2uid_redis as r_name
from time_utils import ts2date

def get_queue_index(timestamp):
    time_struc = time.gmtime(float(timestamp))
    hour = time_struc.tm_hour
    minute = time_struc.tm_min
    index = hour*4+math.ceil(minute/15.0) #every 15 minutes
    return int(index)

def cal_propage_work(item):
    cluster_redis = R_CLUSTER_FLOW1
    user = str(item['uid'])
    followers_count = item['user_fansnum']
    friends_count = item.get("user_friendsnum", 0)
    cluster_redis.hset(user, 'user_fansnum', followers_count)
    cluster_redis.hset(user, 'user_friendsnum', friends_count)

    retweeted_uid = str(item['root_uid'])
    retweeted_mid = str(item['root_mid'])

    message_type = int(item['message_type'])
    mid = str(item['mid'])
    timestamp = item['timestamp']
    text = item['text']

    if message_type == 1:
        cluster_redis.sadd('user_set', user)
        cluster_redis.sadd(user + '_origin_weibo', mid)
        #cluster_redis.hset(user, mid + '_origin_weibo_retweeted', 0)
        #cluster_redis.hset(user, mid + '_origin_weibo_comment', 0)
        #cluster_redis.hset(user, mid + '_origin_weibo_timestamp', timestamp) # origin weibo mid and timestamp

    elif message_type == 2: # comment weibo
        cluster_redis.sadd('user_set', user)
        if cluster_redis.sismember(user + '_comment_weibo', retweeted_mid):
            return 
        cluster_redis.sadd(user + '_comment_weibo', retweeted_mid)
        RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
        nicknames = RE.findall(text)
        queue_index = get_queue_index(timestamp)
        #cluster_redis.hincrby(user, 'comment_weibo', 1)

        #if 1:
        if len(nicknames) == 0:
            cluster_redis.hincrby(retweeted_uid, retweeted_mid + '_origin_weibo_comment', 1) 
            cluster_redis.hincrby(retweeted_uid, 'origin_weibo_comment_timestamp_%s' % queue_index, 1)
            #cluster_redis.hset(retweeted_uid, retweeted_mid + '_origin_weibo_comment_timestamp', timestamp)

        else:
            nick_id = nicknames[0]
            _id = r_name.hget("weibo_user", nick_id)
            if _id:
                cluster_redis.hincrby(str(_id), retweeted_mid + '_retweeted_weibo_comment', 1) 
                cluster_redis.hincrby(str(_id), 'retweeted_weibo_comment_timestamp_%s' % queue_index, 1)
                #cluster_redis.hset(str(_id), retweeted_mid + '_retweeted_weibo_comment_timestamp', timestamp)

    elif message_type == 3:
        cluster_redis.sadd('user_set', user)
        if cluster_redis.sismember(user + '_retweeted_weibo', retweeted_mid):
            return

        cluster_redis.sadd(user + '_retweeted_weibo', retweeted_mid)
        #cluster_redis.hset(user, retweeted_mid + '_retweeted_weibo_timestamp', timestamp) 
        queue_index = get_queue_index(timestamp)
        cluster_redis.hincrby(retweeted_uid, 'origin_weibo_retweeted_timestamp_%s' % queue_index, 1)
        cluster_redis.hincrby(retweeted_uid, retweeted_mid + '_origin_weibo_retweeted', 1) 
        #cluster_redis.hset(user, retweeted_mid + '_retweeted_weibo_retweeted', 0)
        #cluster_redis.hset(user, retweeted_mid + '_retweeted_weibo_comment', 0)
        RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
        nicknames = RE.findall(text)
        if len(nicknames) != 0:
            for nick_id in nicknames:
                _id = r_name.hget("weibo_user", nick_id)
                if _id:
                    cluster_redis.hincrby(str(_id), retweeted_mid+'_retweeted_weibo_retweeted', 1) 
                    #cluster_redis.hset(str(_id), retweeted_mid+'_retweeted_weibo_retweeted_timestamp', timestamp)
                    cluster_redis.hincrby(str(_id), 'retweeted_weibo_retweeted_timestamp_%s' % queue_index, 1)


if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW1))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1))
    poller = zmq.Poller()
    poller.register(controller, zmq.POLLIN)
    controller.setsockopt(zmq.SUBSCRIBE, "")
    cluster_redis = R_CLUSTER_FLOW1
    f = open("cluster_error.txt", "a")

    count = 0
    tb = time.time()
    ts = tb
    while 1:
        item = receiver.recv_json()

        if not item:
            continue 
        if int(item['sp_type']) == 1:
            cal_propage_work(item)


            count += 1
            if count % 10000 == 0:
                te = time.time()
                print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000)
                ts = te


            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
                ts = te


