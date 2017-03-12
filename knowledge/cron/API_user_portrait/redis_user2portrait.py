# -*- coding: utf-8 -*-
import sys
import time
import json
#from wei_api import read_flow_text

def scan_compute_redis():
    print 'mark'	


if __name__=='__main__':
    log_time_ts = int(time.time())
    print 'cron/API_user_portrait/redis_user2portrait.py&start&' + str(log_time_ts)
    
    try:
        scan_compute_redis()
    except Exception, e:
        print e, '&error&', ts2date(time.time())

    log_time_ts = int(time.time())
    print 'cron/API_user_portrait/redis_user2portrait.py&end&' + str(log_time_ts)
