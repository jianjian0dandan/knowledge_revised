# -*- coding: utf-8 -*-
import sys
import zmq
import time
import redis
import os
reload(sys)
sys.path.append('../../')
from global_config import ZMQ_VENT_PORT_FLOW4, ZMQ_CTRL_VENT_PORT_FLOW4,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, BIN_FILE_PATH

if __name__ == "__main__":

    context = zmq.Context()
    #cluster_redis = _default_cluster_redis(REDIS_VENT_HOST, REDIS_VENT_PORT)

    controller = context.socket(zmq.PUB)
    controller.bind("tcp://%s:%s" %(ZMQ_CTRL_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW4))
    '''
    for node in range(91,96):
        for port in [6379, 6380]:
            startup_nodes = [{"host": '219.224.135.%s'%i, "port": '%s'%j}]
            weibo_redis = RedisCluster(startup_nodes = startup_nodes)
            weibo_redis.flushall()
    print "finish flushing"
    '''
    for i in range(5):
        time.sleep(0.1)
        controller.send("RESTART")


