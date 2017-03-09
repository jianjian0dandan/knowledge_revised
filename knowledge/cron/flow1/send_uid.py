# -*- coding = utf-8 -*-

import redis
import sys
import json
import time
#from rediscluster import RedisCluster

reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW1

#weibo_redis = redis.StrictRedis(host='219.224.135.47', port='6379')

weibo_redis = R_CLUSTER_FLOW1

def send_uid():
    count = 0
    scan_cursor = 0
    tb = time.time()
    number = weibo_redis.scard("user_set")
    print number

    while 1:
        re_scan = weibo_redis.sscan('user_set',scan_cursor, count=10000)
        if int(re_scan[0]) == 0:
            weibo_redis.lpush("active_user_id", json.dumps(re_scan[1]))
            count += len(re_scan[1])
            print count
            print 'finish'
            break
        else:
            weibo_redis.lpush("active_user_id", json.dumps(re_scan[1]))
            count += 10000
            scan_cursor = re_scan[0]
            if count % 100000 == 0:
                ts = time.time()
                print '%s : %s' %(count, ts - tb)
                tb = ts

if __name__ == "__main__":
    send_uid()


