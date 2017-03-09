# -*- coding:utf-8 -*-

import math
import json
import os

def influence_weibo_cal(total_number, average_number, top_number,brust):
    influence_weibo = 0.5*math.log(int(total_number)+1) + 0.2*math.log(int(average_number)+1) +0.1*math.log(int(top_number)+1) + 0.1*math.log(10*brust[0]+1) +0.1*math.log(10*brust[1]+1)
    return influence_weibo

def user_index_cal(origin_weibo_list, retweeted_weibo_list, user_fansnum, influence_origin_weibo_retweeted, influence_origin_weibo_comment, influence_retweeted_weibo_retweeted, influence_retweeted_weibo_comment):
    user_index = 300*(0.15*(0.6*math.log(len(origin_weibo_list)+1)+0.3*math.log(len(retweeted_weibo_list)+1)+0.1*math.log(int(user_fansnum)+1))+0.85*(0.3*influence_origin_weibo_retweeted+0.3*influence_origin_weibo_comment+0.2*influence_retweeted_weibo_retweeted+0.2*influence_retweeted_weibo_comment))
    return user_index

def deliver_weibo_brust(time_list, division=900, percent=0.5):

    time_list = [int(value) for value in time_list]
    max_value = max(time_list)
    if max_value <= 5:
        return 0, 0
    else:
        list_brust = [value for value in time_list if value >= percent*max_value]
        brust_time = len(list_brust)
        brust_velosity = sum(list_brust)/float(brust_time)
    return brust_time, brust_velosity


def activity_weibo(weibo_timestamp, user_info, timestamp_type):

    user_weibo_timestamp = [0]*96
    if weibo_timestamp != []:
        for i in weibo_timestamp:
            count = user_info[timestamp_type+'_%s' %i]
            user_weibo_timestamp[int(i)-1] = count
    weibo_brust = deliver_weibo_brust(user_weibo_timestamp)
    return weibo_brust


def statistic_weibo(origin_weibo_retweeted_count, origin_weibo_set, user_info,weibo_type, total_number=0, average_number=0):

    origin_weibo_retweeted_detail = {}
    top_retweeted = [("0", 0)]
    origin_weibo_top_retweeted_id = 0
    average_number = 0
    if len(origin_weibo_retweeted_count) != 0 and len(origin_weibo_set) != 0:
        for origin_weibo_id in origin_weibo_retweeted_count: # mid set
            if origin_weibo_id not in origin_weibo_set:
                continue
            origin_weibo_id = str(origin_weibo_id)
            origin_weibo_retweeted_detail[origin_weibo_id] = int(user_info[origin_weibo_id+weibo_type])
            total_number += int(origin_weibo_retweeted_detail[origin_weibo_id])
        average_number = total_number * 1.0/ len(origin_weibo_set)
        if origin_weibo_retweeted_detail:
            order = sorted(origin_weibo_retweeted_detail.iteritems(), key=lambda x:x[1], reverse=True)
            top_retweeted = order[0:3] # list of top 3 weibo

    return origin_weibo_retweeted_detail, total_number, top_retweeted, average_number


def expand_index_action(data):

    _id = data['user']
    action = {'index': {"_id": _id}}
    return action, data

