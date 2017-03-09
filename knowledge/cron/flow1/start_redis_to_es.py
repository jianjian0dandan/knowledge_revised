# -*- coding: utf-8 -*-

import zmq
import time
import redis
import os
import sys

reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW1, ES_CLUSTER_FLOW1
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1, ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1

if __name__ == "__main__":
    
    """
    cal from redis and store to elasticsearch
    """
    context = zmq.Context()
    cluster_redis = R_CLUSTER_FLOW1

    controller = context.socket(zmq.PUB)
    controller.bind("tcp://%s:%s" %(ZMQ_CTRL_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1))

    es = ES_CLUSTER_FLOW1
    es_former_index = time.strftime("%Y%m%d", time.localtime(time.time()-7*86400))
    index_exist = es.indices.exists(index=es_former_index)
    if index_exist:
        es.indices.delete(index=es_former_index)
#        print "delete the index of %s" % es_former_index

    count = 0
    scan_cursor = 0
    tb = time.time()
    number = cluster_redis.scard("user_set")
#    print number

    while True:
        re_scan = cluster_redis.sscan('user_set',scan_cursor, count=10000)
        if re_scan[0] == 0:
#            print 'finish'
            cluster_redis.lpush("active_user_id", re_scan[1])
            break
        else:
            cluster_redis.lpush("active_user_id", re_scan[1])
            count += 10000
            scan_cursor = re_scan[0]
            if count % 100000 == 0:
                ts = time.time()
 #               print '%s : %s' %(count, ts - tb)
                tb = ts
    ts = ts2datetime(time.time())
    print "send_uid&start&ts"
