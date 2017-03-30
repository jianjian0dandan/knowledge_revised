# -*- coding: UTF-8 -*-
'''
use to scan the user_portrait uid, activeness_history and influence_history to redis
for 
'''
import sys
import time
import json
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import R_RECOMMENTATION as r
from global_utils import r_user_update_long_hash_name
from global_config import ALL_PERSON_RELATION_LIST, ALL_VERIFIED_RELATION_LIST

#scan es to redis as a queue for update long term
#write in version: 15-12-08
#order time task for every day
#data in redis: [[uid, relation_list],[uid, relation_list],....]
def scan_es2redis():
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}, 'size':1000}, index=portrait_index_name, doc_type=portrait_index_type)
    start_ts = time.time()
    user_list = []
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            verified = scan_re['verified']
            if verified:
                relation_list = ALL_VERIFIED_RELATION_LIST
            else:
                relation_list = ALL_PERSON_RELATION_LIST
            r.lpush(r_user_update_long_hash_name, json.dumps([uid, relation_list]))
            if count % 1000==0 and count!=0:
                end_ts = time.time()
                print '%s sec count 1000' % (end_ts - start_ts)
                start_ts = end_ts
        except StopIteration:
            print 'all done'
            break
        except Exception, e:
            raise e
            break

    print 'count:', count


if __name__ == '__main__':
    log_time_ts = int(time.time())
    print 'cron/API_user_portrait/scan_es2redis_update.py&start&' + str(log_time_ts)
    
    #try:
    scan_es2redis()
    #except Exception, e:
    #print e, '&error&', ts2date(time.time())

    log_time_ts = int(time.time())
    print 'cron/API_user_portrait/scan_es2redis_update.py&end&' + str(log_time_ts)
