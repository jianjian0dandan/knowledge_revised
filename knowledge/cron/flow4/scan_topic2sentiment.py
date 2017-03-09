# -*- coding: UTF-8 -*-
'''
use to save user topic to redis hash for compute sentiment
update: one week
'''
import sys
import time
import json
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import R_TOPIC, r_topic_name
from parameter import topic_ch2en_dict
from time_utils import ts2datetime, datetime2ts


def del_topic_redis():
    R_TOPIC.delete(r_topic_name)


#use to scan user topic to redis which save as english
def scan_topic2redis():
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all': {}}, 'size':1000}, index=portrait_index_name, doc_type=portrait_index_type)
    start_ts = time.time()
    hmset_dict = {}
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            topic_ch_string = scan_re['topic_string']
            topic_ch_list = topic_ch_string.split('&')
            topic_en_string = [topic_ch2en_dict[item] for item in topic_ch_list]
            hmset_dict[uid] = json.dumps(topic_en_string)
            if count % 1000 == 0 and count != 0:
                R_TOPIC.hmset(r_topic_name, hmset_dict)
                end_ts = time.time()
                #print '%s sec count 1000' % (end_ts - start_ts)
        except StopIteration:
            if hmset_dict:
                R_TOPIC.hmset(r_topic_name, hmset_dict)
                hmset_dict = {}
            break
        except Exception as e:
            raise e
            break
    if hmset_dict:
        R_TOPIC.hmset(r_topic_name, hmset_dict)
    #print 'all count:', count


if __name__=='__main__':
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/flow4/scan_topic2senitment.py&start&' + log_time_date
   
    del_topic_redis()
    scan_topic2redis()
    
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/flow4/scan_topic2senitment.py&end&' + log_time_date
    #topic_string = R_TOPIC.hget(r_topic_name, '2010832710')
    #print 'topic_string:', topic_string, type(topic_string)
