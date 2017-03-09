# -*- coding:utf-8 -*-
'''
use to scan user domain to redis hash for compute sentiment
update: one month
'''
import sys
import time
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import R_DOMAIN, r_domain_name
from parameter import domain_ch2en_dict
from time_utils import ts2datetime, datetime2ts

def del_domain_redis():
    R_DOMAIN.delete(r_domain_name)


#use to scan user domain to redis which save as english
def scan_domain2redis():
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}, 'size':1000}, index=portrait_index_name, doc_type=portrait_index_type)
    start_ts = time.time()
    hmset_dict = {}
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            domain_en = domain_ch2en_dict[scan_re['domain']]
            hmset_dict[uid] = domain_en
            if count % 1000 == 0 and count != 0:
                R_DOMAIN.hmset(r_domain_name, hmset_dict)
                end_ts = time.time()
                print '%s sec count 1000' % (end_ts -start_ts)
                start_ts = end_ts
                hmset_dict = {}
        except StopIteration:
            if hmset_dict:
                R_DOMAIN.hmset(r_domain_name, hmset_dict)
                hmset_dict = {}
            break
        except Exception as e:
            raise e
            break

    if hmset_dict:
        R_DOMAIN.hmset(r_domain_name, hmset_dict)
    print 'all count:', count


if __name__=='__main__':
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/flow4/scan_domain2sentiment.py&start&' + log_time_date

    del_domain_redis()
    scan_domain2redis()

    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/flow4/scan_domain2sentiment&end&' + log_time_date
