# -*- coding: utf-8 -*-

import zmq
import time
import redis
import os
import sys

reload(sys)
sys.path.append('../../')
from global_config import ZMQ_CTRL_VENT_PORT_FLOW1, ZMQ_CTRL_HOST_FLOW1
from time_utils import ts2datetime

if __name__ == "__main__":

    context = zmq.Context()

    controller = context.socket(zmq.PUB)
    controller.bind("tcp://%s:%s" %(ZMQ_CTRL_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1))

    """
    for node in REDIS_CLUSTER_HOST_FLOW1_LIST:
        for port in REDIS_CLUSTER_PORT_FLOW1_LIST:
            startup_nodes = [{"host": node, "port": port}]
            weibo_redis = RedisCluster(startup_nodes = startup_nodes)
            weibo_redis.flushall()
    print "finish flushing"
    """

    for i in range(5):
        time.sleep(0.1)
        controller.send("RESTART")
    ts = ts2datetime(time.time())
    print "restart_zmq&start&%s" %ts
