# -*- coding=utf-8 -*-

import re
import sys
import zmq
import time
import json
import math
from datetime import datetime
from test_save_attribute import save_retweet, save_comment

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW3, ZMQ_CTRL_VENT_PORT_FLOW3,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_config import UNAME2UID_HASH as uname2uid_hash
from global_utils import uname2uid_redis
from parameter import RUN_TYPE, RUN_TEST_TIME

#uname2uid from redis
def uname2uid(uname):
    uid = uname2uid_redis.hget(uname2uid_hash, uname)
    if not uid:
        uid = ''
    return uid

#use to extract retweet weibo direct uname
#write in version:15-12-08
def retweet_uname2uid(item):
    direct_uid = None
    uid = item['uid']
    root_uid = item['root_uid']
    timestamp = item['timestamp']
    text = item['text']
    direct_uid = ''
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
    repost_chains = RE.findall(text)
    if repost_chains != []:
        direct_uname = repost_chains[0]
        direct_uid = uname2uid(direct_uname)

    if direct_uid == '':
        direct_uid = root_uid

    save_retweet(uid, direct_uid, timestamp)

#use to extract comment weibo direct uname
#write in version:15-12-08
def comment_uname2uid(item):
    direct_uid = None
    uid = item['uid']
    root_uid = item['root_uid']
    timestamp = item['timestamp']
    text = item['text']
    direct_uid = ''
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    RE = re.compile(u'回复@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
    comment_chains = RE.findall(text)
    if comment_chains != []:
        direct_uname = comment_chains[0]
        direct_uid = uname2uid(direct_uname)
    if direct_uid == '':
        direct_uid = root_uid
    
    save_comment(uid, direct_uid, timestamp)


if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW3))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW3))

    count = 0
    tb = time.time()
    ts = tb
    while 1:
        item = receiver.recv_json()
        if not item:
            continue 
        
        if int(item['sp_type']) == 1:
            message_type = item['message_type']
            
            if int(message_type)==3:
                retweet_uname2uid(item)
            elif int(message_type)==2:
                comment_uname2uid(item)

        count += 1
        if count % 10000 == 0 and RUN_TYPE == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
