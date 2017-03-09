# -*- coding=utf-8 -*-
'''
use to scan redis(retweet/be_retweet) to insert es
'''
import sys
import time
import json
import redis

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es
from global_utils import retweet_redis_dict, comment_redis_dict
from global_config import R_BEGIN_TIME
from parameter import DAY
from time_utils import ts2datetime, datetime2ts
from retweet_mappings import retweet_es_mappings, be_retweet_es_mappings

begin_ts = datetime2ts(R_BEGIN_TIME)

error_f = open('./error_file.txt', 'w')

#use to get db_number which is needed to es
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = 2 - (((date_ts - begin_ts) / (DAY * 7))) % 2
    #test
    db_number = 1
    return db_number


#use to get db retweet/be_retweet redis to es
def scan_retweet():
    count = 0
    scan_cursor = 0
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #get redis db number
    db_number = get_db_num(now_date_ts)
    #retweet/be_retweet es mappings
    '''
    retweet_es_mappings(str(db_number))
    be_retweet_es_mappings(str(db_number))
    '''
    #get redis db
    retweet_redis = retweet_redis_dict[str(db_number)]
    retweet_bulk_action = []
    be_retweet_bulk_action = []
    start_ts = time.time()
    #retweet count/be_retweet count
    retweet_count = 0
    be_retweet_count = 0
    while True:
        re_scan = retweet_redis.scan(scan_cursor, count=100)
        re_scan_cursor = re_scan[0]
        '''
        if re_scan_cursor == 0:
            print 'scan finish'
            if retweet_bulk_action != []:
                es.bulk(retweet_bulk_action, index='retweet_'+str(db_number), doc_type='user')
            if be_retweet_bulk_action != []:
                es.bulk(be_retweet_bulk_action, index='be_retweet_'+str(db_number), doc_type='user')
            break
        '''
        for item in re_scan[1]:
            count += 1
            item_list = item.split('_')
            save_dict = {}
            if len(item_list)==2:
                retweet_count += 1
                uid = item_list[1]
                item_result = retweet_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_retweet'] = json.dumps(item_result)
                retweet_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
            elif len(item_list)==3:
                be_retweet_count += 1
                uid = item_list[2]
                item_result = retweet_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_be_retweet'] = json.dumps(item_result)
                be_retweet_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
        es.bulk(retweet_bulk_action, index='1225_retweet_'+str(db_number), doc_type='user')
        es.bulk(be_retweet_bulk_action, index='1225_be_retweet_'+str(db_number), doc_type='user')
        retweet_bulk_action = []
        be_retweet_bulk_action = []
        end_ts = time.time()
        print '%s sec scan %s count user:', (end_ts - start_ts, count)
        start_ts = end_ts
        scan_cursor = re_scan[0]
        if scan_cursor==0:
            break
    print 'count:', count
    print 'end'

def scan_comment():
    count = 0
    scan_cursor = 0
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #get redis db number
    db_number = get_db_num(now_date_ts)
    #comment/be_comment es mappings
    '''
    comment_es_mappings(str(db_number))
    be_comment_es_mappings(str(db_number))
    '''
    #get redis db
    comment_redis = comment_redis_dict[str(db_number)]
    comment_bulk_action = []
    be_comment_bulk_action = []
    start_ts = time.time()
    #comment count/be_comment count
    comment_count = 0
    be_comment_count = 0
    while True:
        re_scan = comment_redis.scan(scan_cursor, count=100)
        re_scan_cursor = re_scan[0]
        for item in re_scan[1]:
            count += 1
            item_list = item.split('_')
            save_dict = {}
            if len(item_list)==2:
                comment_count += 1
                uid = item_list[1]
                item_result = comment_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_comment'] = json.dumps(item_result)
                comment_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
            '''
            elif len(item_list)==3:
                be_comment_count += 1
                uid = item_list[2]
                item_result = comment_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_be_comment'] = json.dumps(item_result)
                be_comment_bulk_action.extend([{'index':{'_id': uid}}, save_dict])
            '''
        try:
            es.bulk(comment_bulk_action, index='1225_comment_'+str(db_number), doc_type='user')
        except:
            index_name = '1225_comment_'+str(db_number)
            split_bulk_action(comment_bulk_action, index_name)
        '''
        try:
            es.bulk(be_comment_bulk_action, index='1225_be_comment_'+str(db_number), doc_type='user')
        except:
            index_name = '1225_be_comment_'+str(db_number)
            split_bulk_action(be_comment_bulk_action, index_name)
        '''
        comment_bulk_action = []
        #be_comment_bulk_action = []
        end_ts = time.time()
        print '%s sec scan %s count user' % (end_ts - start_ts, count)
        start_ts = end_ts
        scan_cursor = re_scan[0]
        if scan_cursor==0:
            break
    print 'count:', count
    print 'end'


def split_bulk_action(bulk_action, index_name):
    new_bulk_action = []
    for i in range(0, len(bulk_action)):
        if i % 2 == 0:
            new_bulk_action = [bulk_action[i], bulk_action[i+1]]
            #print 'new_bulk_action:', new_bulk_action
            try:
                es.bulk(new_bulk_action, index=index_name, doc_type='user')
            except:
                error_f.writelines([new_bulk_action[0]['index']['_id'], '\n'])




if __name__=='__main__':
    #scan_retweet()
    scan_comment()
    '''
    bulk_action = [{'index':{'_id': '1234567890'}}, {'test':'test'}, {'index':{'_id':'7894561230'}}, {'test2':'test2'}]
    index_name = 'test_portrait_00'
    split_bulk_action(bulk_action, index_name)
    '''
    error_f.close()
