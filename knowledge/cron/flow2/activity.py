# -*- coding: UTF-8 -*-
'''
compute attribute of activity
'''
import sys
import json
import time
from test_save_attribute import save_activity

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts

Fifteenminutes = 60 * 15

def accumulate_activity(itemdict):
    weibo = itemdict
    timestamp = weibo['timestamp']
    uid = weibo['user']
    date  = ts2datetime(timestamp)
    ts = datetime2ts(date)
    time_segment = (timestamp - ts) / Fifteenminutes
    save_activity(uid, ts, time_segment)
    

