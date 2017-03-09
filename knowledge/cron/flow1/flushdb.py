# -*-coding:utf-8-*-
"""
放弃原先设想的采用redis cluster方案，而使用单台redis形式
"""

import sys
import redis
from redis import StrictRedis
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW1 as r

if __name__ == '__main__':

    """
    startup_nodes = [{"host": '219.224.135.91', "port": "6379"}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    startup_nodes = [{"host": '219.224.135.91', "port": "6380"}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    startup_nodes = [{"host": '219.224.135.93', "port": "6380"}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    print "finish flushing!"
    """
    r.flushdb()
