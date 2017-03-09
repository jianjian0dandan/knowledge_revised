# -*- coding: UTF-8 -*-
'''
use to compute ip
'''
import IP
import json
import time
import redis
from test_save_attribute import save_city

# ip to city
def ip2city(ip):
    try:
        city = IP.find(str(ip))
        if city:
            city = city.encode('utf-8')
        else:
            return None
    except Exception,e:
        return None
    return city

#main function
# ip to city and accumulate the distribution
def accumulate_ip(item2dict):
    weibo = item2dict
    #print weibo
    ip = weibo['geo']
    uid = weibo['user']
    timestamp = weibo['timestamp']
    if ip:
        save_city(uid, ip, timestamp)
