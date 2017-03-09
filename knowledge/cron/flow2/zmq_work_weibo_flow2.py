# -*- coding=utf-8 -*-

import re
import sys
import zmq
import time
import json
import math
from datetime import datetime
from test_save_attribute import save_city_timestamp
from test_save_attribute import save_activity
from test_save_attribute import save_at

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW2, ZMQ_CTRL_VENT_PORT_FLOW2,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from parameter import RUN_TYPE, RUN_TEST_TIME
Fifteenminutes = 15*60
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
    ip = item['send_ip']
    # attribute location
    if ip:
        save_city_timestamp(uid, ip, timestamp)
    
    # attribute activity
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    time_segment = (timestamp - ts) / Fifteenminutes
    save_activity(uid, ts, time_segment)
    
    # attribute mention
    
    text = item['text']
    at_uname_list = extract_uname(text)
    try:
        at_uname = at_uname_list[0]
        if at_uname != '':
            save_at(uid, at_uname, timestamp)
    except:
        pass
    


if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW2))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW2))

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
        #run_type
        if count % 10000 == 0 and RUN_TYPE == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
