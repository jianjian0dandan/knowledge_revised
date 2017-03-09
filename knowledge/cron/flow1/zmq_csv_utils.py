# -*- coding:utf-8 -*-

import os
import sys
import zmq
import time
import json
import struct
from datetime import datetime
from csv2json import itemLine2Dict, csv2bin

reload(sys)
sys.path.append('../../')
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, BIN_FILE_PATH, FIRST_FILE_PART

def load_items_from_bin(bin_path):
    return open(bin_path, 'rb')

def ordered_file_list(file_list):
    rank_list = []
    for item in file_list:
        if FIRST_FILE_PART in item and '.csv' in item:
            rank_list.append(int((item.split('.')[0]).split('NODE')[1]))
    new_list = []
    for i in sorted(rank_list):
        new_list.append(FIRST_FILE_PART + str(i) + '.csv')

    return new_list


def send_filter(filter_set, weibo_send, count_send, sender):
    for item in weibo_send:
        if item['mid'] not in filter_set:
            sender.send_json(item)
            count_send += 1
    return count_send

def send_all(f, sender):
    count = 0
    count_send = 0
    tb = time.time()
    ts = tb
    weibo_list = []
    weibo_send = []

    try:
        for line in f:
            weibo_item = itemLine2Dict(line)
            if weibo_item:
                weibo_item_bin = csv2bin(weibo_item)
                if int(weibo_item_bin['sp_type']) != 1:
                    continue
                sender.send_json(weibo_item_bin)
                count += 1

            if count % 10000 == 0:
                te = time.time()
                print '[%s] read csv speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000)
                ts = te
                time.sleep(1)
    except:
        print "pass"
    total_cost = time.time() - tb
    return count, total_cost


def send_weibo(sender, poller, controller, total_count=0, total_cost=0):
    """
    send weibo data to zmq_work
    """

    file_list = set(os.listdir(BIN_FILE_PATH))
    print "total file is ", len(file_list)
    file_list = ordered_file_list(file_list)
    for each in file_list:
        event = poller.poll(0)
        if event:
            socks = dict(poller.poll(0))
        else:
            socks = None
        if socks and socks.get(controller) == zmq.POLLIN:
            item = controller.recv()
            if str(item) == "PAUSE":
                print item
                break
        else:
            pass
        if 'data' in each:
            filename = each.split('.')[0]
            if '%s.csv' % filename in file_list and '%s_yes1.txt' % filename not in file_list:
                bin_input = load_items_from_bin(os.path.join(BIN_FILE_PATH, each))
                load_origin_data_func = bin_input
                tmp_count, tmp_cost = send_all(load_origin_data_func, sender)
                total_count += tmp_count
                total_cost += tmp_cost

                with open(os.path.join(BIN_FILE_PATH, '%s_yes1.txt' % filename), 'w') as fw:
                    fw.write('finish reading' + '\n')

    print 'this scan total deliver %s, cost %s sec' % (total_count, total_cost)

    return total_count, total_cost
