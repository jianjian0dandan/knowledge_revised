# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
from config import _default_single_redis, REDIS_NICK_UID_HOST, REDIS_NICK_UID_PORT, NICK_UID_FILE_PATH, NICK_UID_NAMESPACE

redis = _default_single_redis(REDIS_NICK_UID_HOST, REDIS_NICK_UID_PORT)

f = open(NICK_UID_FILE_PATH, 'r')

count = 0
tb = time.time()
ts = tb

for line in f:
    if count == 0:
        count += 1
        continue
    try:
        line = line.strip().decode('utf-8').split(',')
        id = int(line[0])
        nickname = line[1][2:]
        redis.hset(NICK_UID_NAMESPACE, nickname, id)
    except Exception, e:
        print e

    count += 1
    if count % 10000 == 0:
        te = time.time()
        print '[%s] deliver speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
        if count % 100000 == 0:
	    print '[%s] total deliver %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
        ts = te

f.close()
