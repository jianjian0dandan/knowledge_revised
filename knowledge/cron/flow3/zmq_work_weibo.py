# -*- coding=utf-8 -*-

import re
import sys
import zmq
import time
import json
import math
from datetime import datetime
from test_save_attribute import save_ruid

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW3, ZMQ_CTRL_VENT_PORT_FLOW3,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1


def extract_uname(text):
    at_uname_list = []
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    text = text.split('//@')[0]
    RE = re.compile(u'@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+) ', re.UNICODE)
    repost_chains = RE.findall(text)

    return repost_chains

def cal_propage_work(item):
    uid = item['uid']
    timestamp = item['timestamp']
    #r_uid = item['retweeted_uid']
    r_uid = item['root_uid']
    #save_ruid(uid, r_uid, timestamp)


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
        try:
            item = receiver.recv_json()
        except Exception, e:
            print Exception, ":", e 
        if not item:
            continue 
        
        if item['sp_type'] == 1:
            try:
                if item and item['message_type']==3:
                    cal_propage_work(item)
            except:
                pass
        
        count += 1
        if count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
