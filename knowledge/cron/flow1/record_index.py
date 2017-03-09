# -*- coding: utf-8 -*-

"""
record the activity of user

"""

import logging
import sys
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_uitls import ES_CLUSTER_FOLW1

es = ES_CLUSTER_FLOW1
index_date = "20130902"

def expand_index_action(data):
    _id = data['uid']
    action = {'index': {'_id': _id}}
    return action, data

def compare_activity(new_item, old_item):
    update_item={}
    average_index = (old_item['max_index'] + old_item['min_index'])/2.0
    if new_item['user_index'] < average_index:
        update_item['lower_than_average_number'] = old_item['lower_than_average_number'] + 1
    else:
        update_item['lower_than_average_number'] = old_item['lower_than_average_number']
    if update_item['lower_than_average_number'] > 4:
        update_item['remove'] = 1 # remove
    else:
        update_item['remove'] = 0

    update_item['uid'] = old_item['uid']
    update_item['max_index'] = max(new_item['user_index'], old_item['max_index'])
    update_item['min_index'] = min(new_item['user_index'], old_item['min_index'])
    update_item['index_number'] = old_item['index_number'] + 1

    return update_item



if __name__ == "__main__":

    tb = time.time()

    es_logger = logging.getLogger("elasticsearch")
    es_logger.setLevel(logging.ERROR)
    FileHandler = logging.FileHandler("es.log")
    formatter = logging.Formatter("%(asctime)s_%(name)s_%(levelname)s_%(message)s")
    FileHandler.setFormatter(formatter)
    es_logger.addHandler(FileHandler)

    try:
        index_exist = es.indices.exists(index="activity")
        if not index_exist:
            es.indices.create(index="activity", ignore=400)
    except Exception,r:
        print Exception,":",r

    s_re = scan(es, query={"query":{"match_all":{}},"size":1000}, index=index_date, doc_type='bci')
    bulk_action = [] # new uid record to es
    count_index = 0
    count_n = 0
    count_uid = 0 # bulk get uids
    exist_uid_list = []
    while 1:
        user_list = []
        while 1:
            try:
                scan_re = s_re.next()['_source']
            except:
                print "no user left"
                break
            user_list.append(scan_re)
            count_n += 1
            if count_n % 1000 == 0:
                break

        for item in user_list:
            user_id = item['user']
            doc_exist = es.exists(index="activity", id=user_id)
            if not doc_exist:
                activity_info = {}
                activity_info['uid'] = user_id
                activity_info['max_index'] = item['user_index']
                activity_info['min_index'] = item['user_index']
                activity_info['index_number'] = 1
                activity_info['lower_than_average_number'] = 0
                activity_info['remove'] = 0 # 0 denotes not remove
                xdata = expand_index_action(activity_info)
                bulk_action.extend([xdata[0], xdata[1]])
                count_index += 1
                if count_index % 2000 == 0:
                    while True:
                        try:
                            es.bulk(bulk_action, index="activity", doc_type="manage", timeout=30)
                            bulk_action=[]
                            break
                        except Exception, r:
                            print Exception,":",r
                            es = Elasticsearch("219.224.135.93")
                            print "retry"
                    print count_index

                if count_index % 10000 == 0:
                    ts = time.time()
                    print "%s  per  %s  second"  %(count_index, ts-tb)
                    tb = ts

            else:
                exist_uid_list.append(user_id)
                count_uid += 1
                if count_uid % 1000 == 0:
                    multi_items = es.mget(index="activity", doc_type="manage", body={"ids": exist_uid_list}, _source=True)['docs']
                    exist_uid_list = []
                    for m_item in multi_items:
                        m_item = m_item['_source']
                        update_item = compare_activity(item, m_item)
                        xdata = expand_index_action(update_item)
                        bulk_action.extend([xdata[0], xdata[1]])
                        count_index += 1

                        if count_index % 2000 == 0:
                            while True:
                                try:
                                    es.bulk(bulk_action, index="activity", doc_type="manage", timeout=30)
                                    bulk_action=[]
                                    break
                                except Exception, r:
                                    print Exception,":",r
                                    es = Elasticsearch("219.224.135.93")
                                    print "retry"
                            print count_index

                        if count_index % 10000 == 0:
                            ts = time.time()
                            print "%s  per  %s  second"  %(count_index, ts-tb)
                            tb = ts

    es.bulk(bulk_action, index="activity", doc_type="manage", timeout=30)










