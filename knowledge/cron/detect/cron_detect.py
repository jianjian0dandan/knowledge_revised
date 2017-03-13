#-*- coding:utf-8 -*-
import os
import sys
import time
import json

reload(sys)
sys.path.append('../../')
from global_utils import R_GROUP as r_group # save detect and analysis queue
from global_utils import group_detect_queue_name
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from global_utils import es_retweet, retweet_index_name_pre, retweet_index_type,\
                         be_retweet_index_name_pre, be_retweet_index_type
from global_utils import es_comment, comment_index_name_pre, comment_index_type,\
                         be_comment_index_name_pre, be_comment_index_type
from global_utils import es_group_result, group_index_name, group_index_type
from global_config import R_BEGIN_TIME
from parameter import DETECT_QUERY_ATTRIBUTE_MULTI, MAX_DETECT_COUNT, DAY,\
                      DETECT_COUNT_EXPAND, IDENTIFY_ATTRIBUTE_LIST, DETECT_ITER_COUNT, MAX_VALUE
from parameter import RUN_TYPE, RUN_TEST_TIME
from time_utils import ts2datetime, datetime2ts, ts2date


r_beigin_ts = datetime2ts(R_BEGIN_TIME)

#use to identify the task is exist
#input: task_name
#output: status True/False
def identify_task_exist(task_id):
    status = True
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_id)['_source']
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        status = True
    return status

#use to get single user portrait attribute
#input: seed_user_dict
#output: user_portriat_dict
def get_single_user_portrait(seed_user_dict):
    if 'uid' in seed_user_dict:
        uid = seed_user_dict['uid']
        try:
            user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
        except:
            user_portrait_result = {}
    else:
        uname = seed_user_dict['uname']
        query = {'term':{'uname': uname}}
        try:
            user_portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type ,\
                    body={'query':{'bool':{'must': quuery}}})['_source']
        except:
            user_portrait_result = {}

    return user_portrait_result


#use to get retweet/be_retweet/comment/be_comment db_number
#input: timestamp
#output: db_number
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) % 2 + 1
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number


#use to merge dict
#input: dict1, dict2, dict3...
#output: merge dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    
    return _total



#use to get structure user
#input: seed_uid_list
#output: in_portrait_result [uid1, uid2, uid3,...] ranked by iteraction count and meet the filter dict
def get_structure_user(seed_uid_list, structure_dict, filter_dict):
    structure_user_dict = {}
    retweet_mark = int(structure_dict['retweet'])
    comment_mark = int(structure_dict['comment'])
    hop = int(structure_dict['hop'])
    retweet_user_dict = {}
    comment_user_dict = {}
    #get retweet/comment es db_number
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    #iter to find seed uid list retweet/be_retweet/comment/be_comment user set by hop
    iter_hop_user_list = seed_uid_list
    iter_count = 0
    all_union_result = dict()
    while iter_count < hop:   # hop number control
        iter_count += 1
        search_user_count = len(iter_hop_user_list)
        hop_union_result = dict()
        iter_search_count = 0
        while iter_search_count < search_user_count:
            iter_search_user_list = iter_hop_user_list[iter_search_count: iter_search_count + DETECT_ITER_COUNT]
            #step1: mget retweet and be_retweet
            if retweet_mark == 1:
                retweet_index_name = retweet_index_name_pre + str(db_number)
                be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
                #mget retwet
                try:
                    retweet_result = es_retweet.mget(index=retweet_index_name, doc_type=retweet_index_type, \
                                                     body={'ids':iter_search_user_list}, _source=True)['docs']
                except:
                    retweet_result = []
                #mget be_retweet
                try:
                    be_retweet_result = es_retweet.mget(index=be_retweet_index_name, doc_type=be_retweet_type, \
                                                        body={'ids':iter_search_user_list} ,_source=True)['docs']
                except:
                    be_retweet_result = []
            #step2: mget comment and be_comment
            if comment_mark == 1:
                comment_index_name = comment_index_name_pre + str(db_number)
                be_comment_index_name = be_comment_index_name_pre + str(db_number)
                #mget comment
                try:
                    comment_result = es_comment.mget(index=comment_index_name, doc_type=comment_index_type, \
                                                     body={'ids':iter_search_user_list}, _source=True)['docs']
                except:
                    comment_result = []
                #mget be_comment
                try:
                    be_comment_result = es_comment.mget(index=be_comment_index_name, doc_type=be_comment_index_type, \
                                                    body={'ids':iter_search_user_list}, _source=True)['docs']
                except:
                    be_comment_result = []
            #step3: union retweet/be_retweet/comment/be_comment result
            union_count = 0
            
            for iter_search_uid in iter_search_user_list:
                try:
                    uid_retweet_dict = json.loads(retweet_result[union_count]['_source']['uid_retweet'])
                except:
                    uid_retweet_dict = {}
                try:
                    uid_be_retweet_dict = json.loads(be_retweet_result[union_count]['_source']['uid_be_retweet'])
                except:
                    uid_be_retweet_dict = {}
                try:
                    uid_comment_dict = json.loads(comment_result[union_count]['_source']['uid_comment'])
                except:
                    uid_comment_dict = {}
                try:
                    uid_be_comment_dict = json.loads(be_comment_result[union_count]['_source']['uid_be_comment'])
                except:
                    uid_be_comment_dict = {}
                #union four type user set
                union_result = union_dict(uid_retweet_dict, uid_be_retweet_dict, uid_comment_dict, uid_be_comment_dict)
                hop_union_result = union_dict(hop_union_result, union_result)
            #step4: add iter search count
            iter_search_count += DETECT_ITER_COUNT

        #pop seed uid self
        for iter_hop_user_item in iter_hop_user_list:
            try:
                hop_union_result.pop(iter_hop_user_item)
            except:
                pass
        #get new iter_hop_user_list
        iter_hop_user_list = hop_union_result.keys()
        #get all union result
        all_union_result = union_dict(all_union_result, hop_union_result)
    #step5: identify the who is in user_portrait
    sort_all_union_result = sorted(all_union_result.items(), key=lambda x:x[1], reverse=True)
    iter_count = 0
    all_count = len(sort_all_union_result)
    in_portrait_result = []
    filter_importance_from = filter_dict['importance']['gte']
    filter_importance_to = filter_dict['importance']['lt']
    filter_influence_from = filter_dict['influence']['gte']
    filter_influence_to = filter_dict['influence']['lt']
    while iter_count < all_count:
        iter_user_list = [item[0] for item in sort_all_union_result[iter_count:iter_count + DETECT_ITER_COUNT]]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                    body={'ids':iter_user_list}, _source=True)['docs']
        except:
            portrait_result = []
        for portrait_item in portrait_result:
            if portrait_item['found'] == True:
                if portrait_item['_source']['importance'] >= filter_importance_from and portrait_item['_source']['importance'] <= filter_importance_to:
                    if portrait_item['_source']['influence'] >= filter_influence_from and portrait_item['_source']['influence'] <= filter_influence_to:
                        uid = portrait_item['_id']
                        in_portrait_result.append(uid)
        if len(in_portrait_result) > (filter_dict['count'] * DETECT_COUNT_EXPAND):
            break
        iter_count += DETECT_ITER_COUNT

    return in_portrait_result

def get_bidirect_user(union_result, target_uid, db_number):
    result = {}
    be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
    be_comment_index_name = be_comment_index_name_pre + str(db_number)
    try:
        be_retweet_result = es_retweet.get(index=be_retweet_index_name, doc_type=be_retweet_index_type, id=target_uid)['_source']    
    except:
        be_retweet_result = {}
    if be_retweet_result:
        be_retweet_uid_dict = json.loads(be_retweet_result['uid_be_retweet'])
    else:
        be_retweet_uid_dict = {}
    try:
        be_comment_result = es_comment.get(index=be_comment_index_name, doc_type=be_comment_index_type, id=target_uid)['_source']
    except:
        be_comment_result = {}
    if be_comment_result:
        be_comment_uid_dict = json.loads(be_comment_result['uid_be_comment'])
    else:
        be_comment_uid_dict = {}
    union_be_retweet_comment_result = union_dict(be_retweet_uid_dict, be_comment_uid_dict)
    bidirect_user_set = set(union_result.keys()) & set(union_be_retweet_comment_result.keys())
    bidirect_user_list = list(bidirect_user_set)
    for bidirect_user in bidirect_user_list:
        if bidirect_user != target_uid:
            result[bidirect_user] = union_result[bidirect_user] + union_be_retweet_comment_result[bidirect_user]    
    return result

def new_get_structure_user(seed_uid_list, structure_dict, filter_dict):
    structure_user_dict = {}
    retweet_mark = int(structure_dict['retweet'])
    comment_mark = int(structure_dict['comment'])
    bidirect_mark = int(structure_dict['bidirect'])
    hop = int(structure_dict['hop'])
    retweet_user_dict = {}
    comment_user_dict = {}
    bidirect_user_dict = {}
    #get retweet/comment es db_number
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    #iter to find seed uid list retweet/be_retweet/comment/be_comment user set by hop
    iter_hop_user_list = seed_uid_list
    iter_count = 0
    all_union_result = dict()
    while iter_count < hop:
        iter_count += 1
        search_user_count = len(iter_hop_user_list)
        hop_union_result = dict()
        iter_search_count = 0
        while iter_search_count < search_user_count:
            iter_search_user_list = iter_hop_user_list[iter_search_count: iter_search_count + DETECT_ITER_COUNT]
            #step1: mget retweet
            if retweet_mark == 1 or bidirect_mark == 1:
                retweet_index_name = retweet_index_name_pre + str(db_number) 
            try:
                retweet_result = es_retweet.mget(index=retweet_index_name, doc_type=retweet_index_type, body={'ids': iter_search_user_list}, _source=True)['docs']
            except:
                retweet_result = []
            #step2: mget comment
            if comment_mark == 1 or bidirect_mark == 1:
                comment_index_name = comment_index_name_pre + str(db_number)
            try:
                comment_result = es_comment.mget(index=comment_index_name, doc_type=comment_index_type, body={'ids': iter_search_user_list}, _source=True)['docs']
            except:
                comment_result = [] 
            union_count = 0
            #union retweet results
            for iter_search_uid in iter_search_user_list:
                try:
                    uid_retweet_dict = json.loads(retweet_result[union_count]['_source']['uid_retweet'])
                except:
                    uid_retweet_dict = {}
                try:
                    uid_comment_dict = json.loads(comment_result[union_count]['_source']['uid_comment'])
                except:
                    uid_comment_dict = {}
                #filter union_result 
                if bidirect_mark == 1:
                    union_result = union_dict(uid_retweet_dict, uid_comment_dict)
                    bidirect_union_result = get_bidirect_user(union_result, iter_search_uid ,db_number)
                else:
                    bidirect_union_result = {}
                union_result = {}
                
                if retweet_mark == 1:
                    union_result = union_dict(union_result, uid_retweet_dict)
                if comment_mark == 1:
                    union_result = union_dict(union_result, uid_comment_dict)
                
                union_result = union_dict(union_result, bidirect_union_result)
                hop_union_result = union_dict(hop_union_result, union_result)
                union_count += 1
            
            #step5: union retweet/comment/bidirect result
            iter_search_count += DETECT_ITER_COUNT
        #pop seed uid self
        for iter_hop_user_item in iter_hop_user_list:
            try:
                hop_union_result.pop(iter_hop_user_item)
            except:
                pass
        #get new iter hop user list
        iter_hop_user_list = hop_union_result.keys()
        #get all union result
        all_union_result = union_dict(all_union_result, hop_union_result)
    #step6: identify the who is in user_portrait
    sort_all_union_result = sorted(all_union_result.items(), key=lambda x:x[1], reverse=True)
    iter_count = 0
    all_count = len(sort_all_union_result)
    in_portrait_result = []
    filter_importance_from = filter_dict['importance']['gte']
    filter_importance_to = filter_dict['importance']['lt']
    filter_influence_from = filter_dict['influence']['gte']
    filter_influence_to = filter_dict['influence']['lt']
    while iter_count < all_count:
        iter_user_list = [item[0] for item in sort_all_union_result[iter_count: iter_count+DETECT_ITER_COUNT]]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids': iter_user_list}, _source=True)['docs']
        except:
            portrait_result = []
        for portrait_item in portrait_result:
            if portrait_item['found'] == True:
                if portrait_item['_source']['importance'] >= filter_importance_from and portrait_item['_source']['importance'] <= filter_importance_to:
                    if portrait_item['_source']['influence'] >= filter_influence_from and portrait_item['_source']['influence'] <= filter_influence_to:
                        uid = portrait_item['_id']
                        in_portrait_result.append([uid, portrait_item['_source']['importance']])
        iter_count += DETECT_ITER_COUNT
    sort_in_portrait_result = sorted(in_portrait_result, key=lambda x:x[1], reverse=True)[:filter_dict['count'] * DETECT_COUNT_EXPAND]
    new_in_portrait_result = [item[0] for item in sort_in_portrait_result]
    return in_portrait_result
    
             



#use to union attribute result and structure result
#input:attribute_user_reslt [user_dict1, user_dict2,...] ranked by similarity
#input:structure result [uid1, uid2,....] ranked by interaction count
def union_attribute_structure(attribute_user_result, structure_result, attribute_weight, structure_weight):
    union_result = dict()
    #step1:trans structure result list to dict {uid1:rank1, uid2:rank2....}
    structure_user_result = dict()
    for item_rank in range(0, len(structure_result)):
        uid = structure_result[item_rank][0]
        structure_user_result[uid] = item_rank
    #step2:trans attribute result list to dict{uid1:rank1, uid2:rank2, ...}
    attribute_user_dict = dict()
    for attribute_rank in range(0, len(attribute_user_result)):
        uid = attribute_user_result[attribute_rank]['_id']
        attribute_user_dict[uid] = attribute_rank
    #step3: get union user list
    union_user_set = set(structure_user_result.keys()) | set(attribute_user_dict.keys())
    union_user_list = list(union_user_set)
    #step2:use attribute weight and structure weight to score for user
    attribute_rank = 0
    try:
        attribute_normal_index = float(1) / len(attribute_user_result)
    except:
        attribute_normal_index = 0
    try:
        structure_normal_index = float(1) / len(structure_user_result)
    except:
        structure_normal_index = 0
    attribute_count = len(attribute_user_result)
    structure_count = len(structure_user_result)
    for user_item in union_user_list:
        try:
            attribute_rank = attribute_user_dict[user_item]
        except KeyError:
            attribtue_rank = attribute_count
        try:
            structure_rank = structure_user_result[user_item]
        except KeyError:
            structure_rank = structure_count

        new_score = attribute_weight*((attribute_count - attribute_rank)*attribute_normal_index) + \
                    structure_weight*((structure_count - structure_rank)*structure_normal_index)
        
        union_result[user_item] = new_score
    #step3:sort user by new score
    sort_union_result = sorted(union_result.items(), key=lambda x:x[1], reverse=True)
    return sort_union_result

#use to filter event for single or multi detect task
#input: all_union_user, event_condition_dict
#output: user_list (who meet the filter condition)
def filter_event(all_union_user, event_condition_list):
    user_result = []
    new_range_dict_list = []
    #step1: adjust the date condition for date
    new_event_condition_list = []
    for event_condition_item in event_condition_list:
        if 'range' in event_condition_item:
            range_dict = event_condition_item['range']
            from_ts = range_dict['timestamp']['gte']
            to_ts = range_dict['timestamp']['lt']
            from_date_ts = datetime2ts(ts2datetime(from_ts))
            to_date_ts = datetime2ts(ts2datetime(to_ts))
            new_range_dict_list = []
            if from_date_ts != to_date_ts:
                iter_date_ts = from_date_ts
                while iter_date_ts < to_date_ts:
                    iter_next_date_ts = iter_date_ts + DAY
                    new_range_dict_list.append({'range':{'timestamp':{'gte':iter_date_ts, 'lt':iter_next_date_ts}}})
                    iter_date_ts = iter_next_date_ts
                if new_range_dict_list[0]['range']['timestamp']['gte'] < from_ts:
                    new_range_dict_list[0]['range']['timestamp']['gte'] = from_ts
                if new_range_dict_list[-1]['range']['timestamp']['lt'] > to_ts:
                    new_range_dict_list[-1]['range']['timestamp']['lt'] = to_ts
            else:
                new_range_dict_list = [{'range':{'timestamp':{'gte':from_ts, 'lt':to_ts}}}]
        else:
            new_event_condition_list.append(event_condition_item)
    #step2: iter to search user who publish weibo use keywords_string
    #step2.1: split user to bulk action
    #step2.2: iter to search user meet condition weibo for different day
    user_count = len(all_union_user)
    iter_count = 0
    hit_user_set = set()
    while iter_count < user_count:
        iter_user_list = [union_item[0] for union_item in all_union_user[iter_count:iter_count + DETECT_ITER_COUNT / 10]]
        iter_user_event_condition_list = [{'terms':{'uid': iter_user_list}}]
        iter_user_event_condition_list.extend(new_event_condition_list)
        #iter date to search different flow_text es
        for range_item in new_range_dict_list:
            iter_date_event_condition_list = [item for item in iter_user_event_condition_list]
            iter_date_event_condition_list.append(range_item)
            range_from_ts = range_item['range']['timestamp']['gte']
            range_from_date = ts2datetime(range_from_ts)
            flow_index_name = flow_text_index_name_pre + range_from_date
            try:
                flow_text_exist = es_flow_text.search(index=flow_index_name, doc_type=flow_text_index_type, \
                    body={'query':{'bool':{'must':iter_date_event_condition_list}}, 'size':100}, _source=False, fields=['uid'])['hits']['hits']
            except:
                flow_text_exist = []
            #get hit user set
            for flow_text_item in flow_text_exist:
                uid = flow_text_item['fields']['uid'][0]
                hit_user_set.add(uid)

        iter_count += DETECT_ITER_COUNT / 10 
    #identify the hit user list ranked by score
    rank_hit_user = []
    for user_item in all_union_user:
        uid = user_item[0]
        uid_set = set(uid)
        if len(uid_set & hit_user_set) != 0:
            rank_hit_user.append(uid)

    return rank_hit_user


#use to make normal index range to abnormal index
#input: input_filter_from, input_filter_to
#output: abnormal_filter_from, abnormal_filter_to
def modify_evaluate_index(filter_from, filter_to, evaluate_index):
    abnormal_filter_from = 0
    abnormal_filter_to = 0
    #step1: get evaluate_index max value
    query_body = {
        'query':{
            'match_all':{},
            },
        'size': 1,
        'sort': [{evaluate_index: {'order': 'desc'}}]
        }
    try:
        evaluate_index_max = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type ,\
                body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    max_value = evaluate_index_max[0]['_source'][evaluate_index]
    #step2: get abnormal index
    abnormal_filter_from = (10 ** (float(filter_from) / 100) - 1) / 9 * max_value
    abnormal_filter_to = (10 ** (float(filter_to) / 100) - 1)  / 9 * max_value
    return abnormal_filter_from, abnormal_filter_to


#use to detect group by single-person
#input: input_dict
#output: status True/False
def single_detect(input_dict):
    results = {}
    task_information_dict = input_dict['task_information']
    task_name = task_information_dict['task_name']
    submit_user = task_information_dict['submit_user']
    task_id = task_information_dict['task_id']
    
    task_exist_mark = identify_task_exist(task_id)
    if task_exist_mark == False:
        return 'task is not exist'
    
    
    query_condition_dict = input_dict['query_condition']
    seed_user_dict = query_condition_dict['seed_user']
    filter_dict = query_condition_dict['filter']
    structure_dict = query_condition_dict['structure']
    #step1: get seed user portrait result
    user_portrait = get_single_user_portrait(seed_user_dict)
    #step1.1: deal condition---seed user is not in user_portrait
    if user_portrait == {}:
        return []

    seed_uid = user_portrait['uid']
    #step2: search attribute user set
    #step2.1: get attribute query dict
    attribute_item = query_condition_dict['attribute']
    attribute_query_list = []
    #get user tag keys
    tag_query_key = submit_user + '-tag'
    try:
        user_tag_string = user_portrait[tag_query_key]
    except:
        user_tag_string = ''
    user_tag_list = user_tag_string.split('&')
    for query_item in attribute_item:
        #deal tag
        if query_item == 'tag':
            for tag_item in user_tag_list:
                attribute_query_list.append({'term':{tag_query_key: tag_item}})
        else:
            try:
                user_attribute_value = user_portrait[query_item]
            except:
                user_attribute_value = ''
            if user_attribute_value != '':
                if query_item in DETECT_QUERY_ATTRIBUTE_MULTI:
                    nest_body_list = []
                    user_attribute_value_list = user_attribute_value.split('&')
                    for attribute_value_item in user_attribute_value_list:
                        nest_body_list.append({'wildcard': {query_item: '*'+attribute_value_item+'*'}})
                    attribute_query_list.append({'bool':{'should': nest_body_list}})
                else:
                    attribute_query_list.append({'wildcard': {query_item: '*'+user_attribute_value+'*'}})
    

    #step2.2:add filter by evaluate index---filter dict
    
    count = MAX_DETECT_COUNT
    for filter_item in filter_dict:
        if filter_item == 'count':
            count = filter_dict[filter_item] * DETECT_COUNT_EXPAND
        else:
            filter_value_from = filter_dict[filter_item]['gte']
            filter_value_to = filter_dict[filter_item]['lt']
            attribute_query_list.append({'range':{filter_item: {'gte':filter_value_from, 'lt':filter_value_to}}})
    #test
    if attribute_item:
        attribute_user_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'query':{'bool':{'must': attribute_query_list}}, 'size':count})['hits']['hits']
    else:
        attribute_user_result = []
    #print 'attribute_result:', attribute_user_result 
    #step2.3: change process proportion
    
    process_mark = change_process_proportion(task_id, 25)
    if process_mark == 'task is not exist':
        return 'task is not exist'
    elif process_mark == False:
        return process_mark
    
    #step3: search structure user set
    #step3.1: search structure user result
    #structure_user_result = get_structure_user([seed_uid], structure_dict, filter_dict)
    structure_user_result = new_get_structure_user([seed_uid], structure_dict, filter_dict)
    #step3.2: change process proportion
    
    process_mark = change_process_proportion(task_id, 50)
    if process_mark == 'task is not exist':
        return 'task is not exist'
    elif process_mark == False:
        return process_mark
    
    #step4: union attribtue and structure user set
    attribute_weight = query_condition_dict['attribute_weight']
    structure_weight = query_condition_dict['structure_weight']
    all_union_user = union_attribute_structure(attribute_user_result, structure_user_result, attribute_weight, structure_weight)
    #step5: filter user by event
    event_condition_list = query_condition_dict['text']
    #step5.1: filter user list
    if len(event_condition_list) != 0:
        filter_user_list = filter_event(all_union_user, event_condition_list)
    else:
        filter_user_list = [item[0] for item in all_union_user]
    #step5.2: change process proportion
    
    process_mark = change_process_proportion(task_id, 75)
    if process_mark == 'task is not exist':
        return 'task is not exist'
    elif process_mark == False:
        return process_mark
    
    #step6: filter by count
    count = filter_dict['count']
    result = filter_user_list[:count]
    if seed_uid not in result:
        results = [seed_uid]
    else:
        results = []
    results.extend(result)
    return results



#use to get seed user attribute
#input: seed_user_list, attribute_list
#output: results
def get_seed_user_attribute(seed_user_list, attribute_list, submit_user):
    results = {}
    attribute_query_list = []
    #step1: mget user result from user_portrait
    try:
        seed_user_portrait = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body={'ids':seed_user_list}, _source=True)['docs']
    except:
        seed_user_portrait = []
    #init results dict---result={'location':{}, 'domain':{}, ...}
    for attribute_item in attribute_list:
        results[attribute_item] = {}
    #step2: compute attribute result about attribute_list
    for seed_user_item in seed_user_portrait:
        uid = seed_user_item['_id']
        if seed_user_item['found'] == True:
            source = seed_user_item['_source']
            #static the attribute
            #step2.1: location
            if 'location' in attribute_list:
                location_value = source['location']
                try:
                    results['location'][location_value] += 1
                except:
                    results['location'][location_value] = 1
            #step2.2: domain
            if 'domain' in attribute_list:
                domain_value = source['domain']
                try:
                    results['domain'][domain_value] += 1
                except:
                    results['domain'][domain_value] = 1
            #step2.3: topic_string
            if 'topic_string' in attribute_list:
                topic_value_string = source['topic_string']
                topic_value_list = topic_value_string.split('&')
                for topic_item in topic_value_list:
                    try:
                        results['topic_string'][topic_item] += 1
                    except:
                        results['topic_string'][topic_item] = 1
            #step2.4: keywords_string
            if 'keywords_string' in attribute_list:
                keywords_value_string = source['keywords_string']
                keywords_value_list = keywords_value_string.split('&')
                for keywords_item in keywords_value_list:
                    try:
                        results['keywords_string'][keywords_item] += 1
                    except:
                        results['keywords_string'][keywords_item] = 1
            #step2.5: hashtag
            if 'hashtag' in attribute_list:
                hashtag_value_string = source['hashtag']
                hashtag_value_list = hashtag_value_string.split('&')
                for hashtag_item in hashtag_value_list:
                    try:
                        results['hashtag'][hashtag_item] += 1
                    except:
                        results['hashtag'][hashtag_item] = 1
            #step2.6: activity_geo
            if 'activity_geo' in attribute_list:
                activity_geo_dict = json.loads(source['activity_geo_dict'])[-1]
                for activity_geo_item in activity_geo_dict:
                    try:
                        results['activity_geo'][activity_geo_item] += 1
                    except:
                        results['activity_geo'][activity_geo_item] = 1
            #step2.8: tag
            if 'tag' in attribute_list:
                tag_query_key = submit_user + '-tag'
                try:
                    user_tag_string = source[tag_query_key]
                except:
                    user_tag_string = ''
                user_tag_list = user_tag_string.split('&')
                for tag_item in user_tag_list:
                    try:
                        results['tag'][tag_item] += 1
                    except:
                        results['tag'][tag_item] = 1
    #step3: get search attribtue value-- new attribute query condition
    new_attribute_query_condition = []
    for item in results:
        iter_dict = results[item]
        sort_item_dict = sorted(iter_dict.items(), key=lambda x:x[1], reverse=True)
        nest_body_list = []
        for query_item in sort_item_dict[:3]:
            item_value = query_item[0]
            if item =='tag':
                nest_body_list.append({'term':{submit_user+'-tag': item_value}})
            else:
                nest_body_list.append({'wildcard':{item: '*'+item_value+'*'}})
        new_attribute_query_condition.append({'bool':{'should': nest_body_list}})

    return new_attribute_query_condition

#use to detect group by multi-person
#input: detect_task_information
#output: detect user list (contain submit uid list)
def multi_detect(input_dict):
    results = {}
    task_information_dict = input_dict['task_information']
    task_name = task_information_dict['task_name']
    submit_user = task_information_dict['submit_user']
    task_id = task_information_dict['task_id']
    
    task_exist_mark = identify_task_exist(task_id)
    if task_exist_mark == False:
        return 'task is not exist'
    
    query_condition_dict = input_dict['query_condition']
    filter_dict = query_condition_dict['filter']
    structure_dict = query_condition_dict['structure']
    #step1.1: get seed users attribute
    attribute_list = query_condition_dict['attribute']
    seed_user_list = task_information_dict['uid_list']
    attribute_query_condition = get_seed_user_attribute(seed_user_list, attribute_list, submit_user)
    #step1.2: change process proportion
    
    process_mark = change_process_proportion(task_id, 20)
    if process_mark == 'task is not exist':
        return 'task is not exist'
    elif process_mark == False:
        return process_mark
    
    #step2: search attribute user set
    #step2.1: add filter condition
    count = MAX_DETECT_COUNT
    for filter_item in filter_dict:
        if filter_item == 'count':
            count = filter_dict[filter_item] * DETECT_COUNT_EXPAND
        else:
            filter_value_from = filter_dict[filter_item]['gte']
            filter_value_to = filter_dict[filter_item]['lt']
            attribute_query_condition.append({'range':{filter_item: {'gte':filter_value_from, 'lt':filter_value_to}}})
    #step2.2: search user_portriait condition
    if attribute_list:
        attribute_user_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type ,\
            body={'query':{'bool':{'should':attribute_query_condition}}, 'size':count})['hits']['hits']
    else:
        attribute_user_result = []
    #step2.3: change process proportion
    
    process_mark = change_process_proportion(task_id, 40)
    if process_mark == 'task is not exist':
        return 'task is not exist'
    elif process_mark == False:
        return process_mark
    
    #step3: search structure user set
    #step 3.1: structure user
    #structure_user_result = get_structure_user(seed_user_list, structure_dict, filter_dict)
    structure_user_result = new_get_structure_user(seed_user_list, structure_dict, filter_dict)
    #step3.2: change process proportion
    
    process_mark = change_process_proportion(task_id, 60)
    if process_mark == 'task is not exist':
        return 'task is not exist'
    elif process_mark == False:
        return process_mark
    
    #step4: union search and structure user set
    attribute_weight = query_condition_dict['attribute_weight']
    structure_weight = query_condition_dict['structure_weight']
    all_union_user = union_attribute_structure(attribute_user_result, structure_user_result, attribute_weight, structure_weight)
    #step5: filter user by event
    event_condition_list = query_condition_dict['text']
    #test
    event_condition_list = []
    #step5.1: filter user list
    if len(event_condition_list) != 0:
        filter_user_list = filter_event(all_union_user, event_condition_list)
    else:
        filter_user_list = [item[0] for item in all_union_user]
    #step5.2: change process proportion
    
    process_mark = change_process_proportion(task_id, 80)
    if process_mark == 'task is not exist':
        return 'task is not exist'
    elif process_mark == False:
        return process_mark
    
    #step6: filter by count
    count = filter_dict['count']
    result = filter_user_list[:count]
    results = seed_user_list
    results.extend(result)

    return results


#use to deal attribute_pattern detect type1----have attribute condition and filter by pattern
#input: attribute_user_result, pattern_list
#ouput: results --- ranked by attribute similarity score
def attribute_filter_pattern(user_portrait_result, pattern_list):
    results = {}
    #step1: adjust the date condition for date
    new_pattern_list = []
    new_range_dict_list = []
    for pattern_item in pattern_list:
        if 'range' in pattern_item:
            range_dict = pattern_item['range']['timestamp']
            from_ts = range_dict['gte']
            to_ts = range_dict['lt']
            from_date_ts = datetime2ts(ts2datetime(from_ts))
            to_date_ts = datetime2ts(ts2datetime(to_ts))
            if from_date_ts != to_date_ts:
                iter_date_ts = from_date_ts
                while iter_date_ts <= to_date_ts:
                    iter_next_date_ts = iter_date_ts + DAY
                    new_range_dict_list.append({'range':{'timestamp': {'gte': iter_date_ts, 'lt':iter_next_date_ts}}})
                    iter_date_ts = iter_next_date_ts
                if new_range_dict_list[0]['range']['timestamp']['gte'] < from_ts:
                    new_range_dict_list[0]['range']['timestamp']['gte'] = from_ts
                if new_range_dict_list[-1]['range']['timestamp']['lt'] > to_ts:
                    new_range_dict_list[-1]['range']['timestamp']['lt'] = to_ts
            else:
                new_range_dict_list = [{'range':{'timestamp':{'gte':from_ts, 'lt':to_ts}}}]
        else:
            new_pattern_list.append(pattern_item)
    #step2: iter to search user who pulish weibo meet pattern list
    #step2.1: split user to bulk action
    #step2.2: iter to search user meet pattern condition for different date
    user_count = len(user_portrait_result)
    iter_count = 0
    hit_user_set = set()
    while iter_count < user_count:
        iter_user_list = [portrait_item['_id'] for portrait_item in user_portrait_result[iter_count: iter_count+DETECT_ITER_COUNT]]
        #get uid nest_body_list
        iter_user_pattern_condition_list = [{'terms': {'uid': iter_user_list}}]
        iter_user_pattern_condition_list.append(new_pattern_list)
        #iter date to search different flow_text es
        for range_item in new_range_dict_list:
            iter_date_pattern_condition_list = [item for item in iter_user_pattern_condition_list]
            iter_date_pattern_condition_list.append(range_item)
            range_from_ts = range_item['range']['timestamp']['gte']
            range_from_date = ts2datetime(range_from_ts)
            flow_index_name = flow_text_index_name_pre + range_from_date
            try:
                flow_text_exist = es_flow_text.search(index=flow_index_name, doc_type=flow_text_index_type, \
                        body={'query':{'bool':{'must': iter_date_pattern_condition_list}}, 'size':MAX_VALUE}, _source=False, fields=['uid'])['hits']['hits']
            except:
                flow_text_exist = []
            #get hit user set
            for flow_text_item in flow_text_exist:
                uid = flow_text_item['fields']['uid'][0]
                hit_user_set.add(uid)

        iter_count += DETECT_ITER_COUNT
    #identify the hit user list ranked by score
    rank_hit_user = []
    for user_item in user_portrait_result:
        uid = user_item['_id']
        uid_set = set(uid)
        if uid in hit_user_set:
            rank_hit_user.append(uid)
    return rank_hit_user


#use to deal attribute_pattern detect type2----no attribute condition, just use pattern condition
#input: pattern_list, filter_dict
#output: results --- ranked by filter condition influence or importance
def pattern_filter_attribute(pattern_list, filter_dict):
    results = {}
    #step1: adjust the date condition for date
    new_pattern_list = []
    new_range_dict_list = []
    for pattern_item in pattern_list:
        if 'range' in pattern_item:
            range_dict = pattern_item['range']
            from_ts = range_dict['timestamp']['gte']
            to_ts = range_dict['timestamp']['lt']
            from_date_ts = datetime2ts(ts2datetime(from_ts))
            to_date_ts = datetime2ts(ts2datetime(to_ts))
            if from_date_ts != to_date_ts:
                iter_date_ts = from_date_ts
                while iter_date_ts < to_date_ts:
                    iter_next_date_ts = iter_date_ts + DAY / 48
                    new_range_dict_list.append({'range':{'timestamp':{'gte':iter_date_ts, 'lt':iter_next_date_ts}}})
                    iter_date_ts = iter_next_date_ts
                if new_range_dict_list[0]['range']['timestamp']['gte'] < from_ts:
                    new_range_dict_list[0]['range']['timestamp']['gte'] = from_ts
                if new_range_dict_list[-1]['range']['timestamp']['lt'] > to_ts:
                    new_range_dict_list[-1]['range']['timestamp']['lt'] = to_ts
            else:
                new_range_dict_list = [{'range': {'timestamp':{'gte': from_ts, 'lt': to_ts}}}]
        else:
            new_pattern_list.append(pattern_item)
    #step2.1: iter to search user who meet pattern condition
    #step2.2: filter who is in user_portrait and meet filter_dict
    all_hit_user = {}
    for range_item in new_range_dict_list:
        iter_date_pattern_condition_list = [item for item in new_pattern_list]
        iter_date_pattern_condition_list.append(range_item)
        range_from_ts = range_item['range']['timestamp']['gte']
        range_from_date = ts2datetime(range_from_ts)
        flow_index_name = flow_text_index_name_pre + range_from_date
        print 'flow_index_name:', flow_index_name
        try:
            flow_text_exist = es_flow_text.search(index=flow_index_name, doc_type=flow_text_index_type,\
                    body={'query':{'bool':{'must': iter_date_pattern_condition_list}}, 'size': MAX_VALUE}, _source=False, fields=['uid'])['hits']['hits']
        except:
            flow_text_exist = []
        #pattern user set
        pattern_user_set = set([flow_text_item['fields']['uid'][0] for flow_text_item in flow_text_exist])
        pattern_user_list = list(pattern_user_set)
        #filter by user_portrait filter dict by bulk action
        pattern_user_count = len(pattern_user_list)
        iter_count = 0
        #add filter dict
        inter_portrait_condition_list = []
        inter_portrait_condition_list.append({'range':{'importance':{'gte': filter_dict['importance']['gte'], 'lt': filter_dict['importance']['lt']}}})
        inter_portrait_condition_list.append({'range':{'influence':{'gte': filter_dict['influence']['gte'], 'lt':filter_dict['influence']['lt']}}})
        
        while iter_count < pattern_user_count:
            iter_user_list = pattern_user_list[iter_count: iter_count + DETECT_ITER_COUNT]
            #get uid nest_body_list
            nest_body_list = []
            for iter_user in iter_user_list:
                nest_body_list.append({'term': iter_user})
            inter_portrait_condition_list.append({'bool':{'should': nest_body_list}})
            #search user in user_portrait
            '''
            try:
                in_portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
                        body={'query':{'bool':{'must': iter_portrait_condition_list}}, 'size': MAX_VALUE}, _source=False, fields=['influence','importance'])['hits']['hits']
            except:
                in_portrait_result = []
            '''
            in_portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body={'query':{'filtered':{'filter':{'terms': {'uid': iter_user_list}}}}, 'size':MAX_VALUE}, _source=False, fields=['influence', 'importance'])['hits']['hits']
            #add to all hit user
            for in_portrait_item in in_portrait_result:
                all_hit_user[in_portrait_item['_id']] = [in_portrait_item['fields']['influence'][0], in_portrait_item['fields']['importance'][0]]
            
            iter_count += DETECT_ITER_COUNT
    
    #sort all hit user by influence
    count = filter_dict['count']
    sort_all_hit_user = sorted(all_hit_user.items(), key=lambda x:x[1][0], reverse=True)[:count]
    #detect user list ranked by iinfluence
    rank_user_list = [sort_item[0] for sort_item in sort_all_hit_user]
    return rank_user_list


#use to detect group by attribute or pattern
#input: detect_task_information
#output: detect user list
#deal two scen---1) have attribute condition and filter by pattern 
#                2)no attribute condition, just use pattern condition
def attribute_pattern_detect(input_dict):
    results = {}
    task_information_dict = input_dict['task_information']
    task_name = task_information_dict['task_name']
    submit_user = task_information_dict['submit_user']
    task_id = task_information_dict['task_id']
    task_exist_mark = identify_task_exist(task_id)
    if task_exist_mark == False:
        return 'task is not exist'
    query_condition_dict = input_dict['query_condition']
    filter_dict = query_condition_dict['filter']
    attribute_list = query_condition_dict['attribute']
    pattern_list = query_condition_dict['pattern']
    if len(attribute_list) != 0:
        #type1:have attribute condition and filter by pattern
        #step1: search user_portrait by attribute condition and filter condition
        count = MAX_DETECT_COUNT
        for filter_item in filter_dict:
            if filter_item == 'count':
                count = filter_dict[filter_item] * DETECT_COUNT_EXPAND
            else:
                filter_value_from = filter_dict[filter_item]['gte']
                filter_value_to = filter_dict[filter_item]['lt']
                attribute_list.append({'range':{filter_item: {'gte': filter_value_from, 'lt': filter_value_to}}})
        try:
            user_portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type ,\
                    body={'query':{'bool':{'must': attribute_list}}, 'size':count}, _source=False)['hits']['hits']
        except:
            user_portrait_result = []
        #step1.2:change process proportion
        process_mark = change_process_proportion(task_id, 30)
        if process_mark == 'task is not exist':
            return 'task is not exist'
        elif process_mark == False:
            return process_mark
        if len(pattern_list) != 0:
            #step2: filter user by pattern condition
            filter_user_result = attribute_filter_pattern(user_portrait_result, pattern_list)
        else:
            #step2: get user_list from user_portrait_result
            filter_user_result = [item['_id'] for item in user_portrait_result]
        #change process mrak
        process_mark = change_process_proportion(task_id, 60)
        if process_mark == 'task is not exist':
            return 'task is not exist'
        elif process_mark == False:
            return process_mark
    else:
        #type2: no attribute condition, just use pattern condition
        #step1: search pattern list and filter by in-user_portrait and filter_dict
        filter_user_result = pattern_filter_attribute(pattern_list, filter_dict)
        #step2.2: change process proportion
        process_mark = change_process_proportion(task_id, 60)
        if process_mark == 'task is not exist':
            return 'task is not exist'
        elif process_mark == False:
            return process_mark
    
    #step3: filter user list by filter count
    count = filter_dict['count']
    results = filter_user_result[:count]
    return results


#use to detect group by pattern
#input: detect_task_information
#output: detect user list
#deal one scen: just user pattern condition
def new_pattern_detect(input_dict):
    results = {}
    task_information_dict = input_dict['task_information']
    task_id = task_information_dict['task_id']
    task_exist_mark = identify_task_exist(task_id)
    if task_exist_mark == False:
        return 'task is not exist'
    query_condition_dict = input_dict['query_condition']
    filter_dict = query_condition_dict['filter']
    pattern_list = query_condition_dict['pattern']
    #step1: search pattern list and filter by in-user_portrait and filter_dict
    filter_user_result = pattern_filter_attribute(pattern_list, filter_dict)
    #step2: change process proportion
    process_mark = change_process_proportion(task_id, 60)
    if process_mark == 'task is not exist':
        return 'task is not exist'
    elif process_mark == False:
        return process_mark
    #step3: filter user list by filter count
    count = filter_dict['count']
    results = filter_user_result[:count]
    return results

#use to detect group by event
#input: input_dict
#output: user list ranked by evaluation index--influence
#deal two scen---1)have attribute condition and filter by flow_text
#             ---2)no attribtue condition, just flow_text condition
def event_detect(input_dict):
    results = {}
    task_information_dict = input_dict['task_information']
    task_name = task_information_dict['task_name']
    submit_user = task_information_dict['submit_user']
    task_id = task_information_dict['task_id']
    task_exist_mark = identify_task_exist(task_id)
    if task_exist_mark == False:
        return 'task is not exist'
    query_condition_dict = input_dict['query_condition']
    filter_dict = query_condition_dict['filter']
    attribute_list = query_condition_dict['attribute']
    event_list = query_condition_dict['event']
    if len(attribute_list) != 0:
        #step1: get user by attribute user_portrait condition
        count = MAX_DETECT_COUNT
        for filter_item in filter_dict:
            if filter_item == 'count':
                count = filter_dict[filter_item] * DETECT_COUNT_EXPAND
            else:
                filter_value_from = filter_dict[filter_item]['gte']
                filter_value_to = filter_dict[filter_item]['lt']
                attribute_list.append({'range':{filter_item: {'gte': filter_value_from, 'lt': filter_value_to}}})
        try:
            user_portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
                    body={'query':{'bool': {'should':attribute_list}}, 'sort':[{'influence': {'order': 'desc'}}],'size':count})['hits']['hits']
        except:
            user_portrait_result = []
        #change process proportion
        process_mark = change_process_proportion(task_id, 30)
        if process_mark == 'task is not exist':
            return 'task is not exist'
        elif process_mark == False:
            return process_mark

        if len(event_list) != 0:
            #type1: have attribute condition and filter by flow_text
            #step2.1: filter by event--text
            filter_user_list = attribute_filter_pattern(user_portrait_result, event_list)
        else:
            #step2.2: get uid list from user_portrait_result
            filter_user_list = [item['_id'] for item in user_portrait_result]
        #change process proportion
        process_mark = change_process_proportion(task_id, 60)
        if process_mark == 'task is not exist':
            return 'task is not exist'
        elif process_mark == False:
            return process_mark
    else:
        #type2: no attribute condition, just flow_text condition
        filter_user_list = pattern_filter_attribute(event_list, filter_dict)
        #change process proportion
        process_mark = change_process_proportion(task_id, 60)
        if process_mark == 'task is not exist':
            return 'task is not exist'
        elif process_mark == False:
            return process_mark

    #step3: filter user list by filter count
    count = int(filter_dict['count'])
    if len(filter_user_list) == 0:
        results = filter_user_list
    else:
        results = filter_user_list[:count]
    return results

#use to save detect results to es
#input: uid list (detect results)
#output: status (True/False)
def save_detect_results(detect_results, task_id):
    mark = False
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_id)['_source']
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        task_exist_result['uid_list'] = json.dumps(detect_results)
        task_exist_result['detect_process'] = 100
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_id, body=task_exist_result)
        mark = True

    return mark

#use to change detect task process proportion
#input: task_name, proportion
#output: status (True/False)
def change_process_proportion(task_id, proportion):
    mark = False
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_id)['_source']
    except:
        task_exist_result = {}
        return 'task is not exist'
    if task_exist_result != {}:
        task_exist_result['detect_process'] = proportion
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_id, body=task_exist_result)
        mark = True

    return mark


#use to add task to redis queue when the task  detect process fail
#input: input_dict
#output: status
def add_task2queue(input_dict):
    status = True
    try:
        r_group.lpush(group_detect_queue_name, json.dumps(input_dict))
    except:
        status = False

    return status


#use to get detect information from redis queue
#input: NULL
#output: task_information_dict (from redis queue---gruop_detect_task)
def get_detect_information():
    task_information_dict = {}
    try:
        task_information_string = r_group.rpop(group_detect_queue_name)
    except:
        task_information_string = ''
    #test
    #r_group.rpush(group_detect_queue_name, task_information_string)
    if task_information_string:
        task_information_dict = json.loads(task_information_string)
    else:
        task_information_dict = {}

    return task_information_dict

#main function to group detect
def compute_group_detect():
    results = {}
    while True:
        #step1:read detect task information from redis queue
        detect_task_information = get_detect_information()
        if detect_task_information != {}:
            start_ts = time.time()
            task_information_dict = detect_task_information['task_information']
            task_name = task_information_dict['task_name']
            submit_user = task_information_dict['submit_user']
            task_id = task_information_dict['task_id']
            #step1: modify filter dict evalute index to abnormal
            filter_dict = detect_task_information['query_condition']['filter']
            importance_from = filter_dict['importance']['gte']
            importance_to = filter_dict['importance']['lt']
            new_importance_from ,new_importance_to = modify_evaluate_index(importance_from, importance_to, 'importance')
            influence_from = filter_dict['influence']['gte']
            influence_to = filter_dict['influence']['lt']
            new_influence_from, new_influence_to = modify_evaluate_index(influence_from, influence_to, 'influence')
            filter_dict['importance']['gte'] = new_importance_from
            filter_dict['importance']['lt'] = new_importance_to
            filter_dict['influence']['gte'] = new_influence_from
            filter_dict['influence']['lt'] = new_influence_to
            detect_task_information['query_condition']['filter'] = filter_dict
            #step2:according task type to do group detect
            detect_task_type = task_information_dict['detect_type']
            if detect_task_type == 'single':
                detect_results = single_detect(detect_task_information)
            elif detect_task_type == 'multi':
                detect_results = multi_detect(detect_task_information)
            elif detect_task_type == 'attribute':
                detect_results =  attribute_pattern_detect(detect_task_information)
            elif detect_task_type == 'event':
                detect_results = event_detect(detect_task_information)
            elif detect_task_type == 'pattern':
                detect_results = new_pattern_detect(detect_task_information)
            #step3:identify the return---'task is not exist'/'false'/normal_results
            #print 'detect results:', detect_results
            if detect_results != 'task is not exist':
                #step4:save detect results to es (status=1 and process=100 and add uid_list)
                mark = save_detect_results(detect_results, task_id)
                #step5:add task_information_dict to redis queue when detect process fail
                if mark == False:
                    status = add_task2queue(detect_task_information)
        else:
            break


    
if __name__=='__main__':
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/detect/cron_detect.py&start&' + log_time_date
    
    try:
        compute_group_detect()
    except Exception, e:
        print e, '&error&' + ts2date(time.time())
    
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/detect/cron_detect.py&end&' + log_time_date

    #test
    '''
    importance_from = 0
    importance_to = 100
    new_importance_from, new_importance_to = modify_evaluate_index(importance_from, importance_to, 'importance')
    influence_from = 0
    influence_to = 100
    new_influence_from, new_influence_to = modify_evaluate_index(influence_from, influence_to, 'influence')
    
    single_input_dict = {'task_information':{'task_id': 'test','task_name': 'single', 'task_type':'detect', 'submit_date': 1453002410, 'submit_user':'admin', 'detect_process':0, 'state':'test', 'detect_type':'single'}, \
            'query_condition':{'attribute':[], 'structure':{'comment':'1', 'retweet':'1', 'hop':'2'}, 'attribute_weight':0, 'structure_weight':0.5, \
            'seed_user':{'uid': '1665808371'}, 'text':[], 'filter':{'count': 100, 'importance':{'gte':new_importance_from, 'lt':new_importance_to}, 'influence':{'gte':new_influence_from, 'lt':new_influence_to}}}}
    results = single_detect(single_input_dict)
    print 'results:', results
   
    multi_input_dict = {'task_information':{'task_id': 'test', 'task_name': 'test2', 'task_type':'detect', 'submit_date':1453002410, 'submit_user':'admin', 'detect_process':0, 'state':'test', 'detect_type':'multi', \
            'uid_list':['1665808371','1223354542']},\
            'query_condition':{'attribute':[], 'structure':{'comment':'1', 'retweet':'1', 'hop':'2'}, 'attribute_weight':0.5, 'structure_weight':0.5 ,\
            'text':[{'wildcard':{'text':'*'+'1'+'*'}}, {'range':{'timestamp':{'gte':1377964800, 'lt':1378483200}}}], \
            'filter':{'count':100, 'importance':{'gte':new_importance_from, 'lt':new_importance_to},\
            'influence':{'gte':new_influence_from, 'lt':new_influence_to}}}}
    results = multi_detect(multi_input_dict)
    print 'results:', results
    
    attribute_pattern_dict = {'task_information':{'task_name':'test', 'task_type':'detect', 'submit_date':1453002410, 'submit_user':'admin', 'detect_process':0, 'state':'test', 'detect_type':'attribute'},\
            'query_condition':{'attribute':[{'wildcard':{'domain':'*'+'媒体'+'*'}}, {'wildcard':{'topic': '*'+'民生类_社会保障'+'*'}}],\
            'pattern':[{'range':{'timestamp':{'gte':1377964800, 'lt':1378483200}}}, {'terms':{'message_type':1}}], \
            'filter':{'count':100, 'importance':{'gte':new_importance_from, 'lt':new_importance_to},\
            'influence':{'gte':new_influence_from, 'lt':new_influence_to}}}}
    #results = attribute_pattern_detect(attribute_pattern_dict)
    event_dict = {'task_information':{'task_name':'poiu', 'task_type':'detect', 'submit_date':1453002410, 'submit_user':'admin', 'detect_process':0, 'state':'test', 'detect_type': 'event'},\
            'query_condition':{'attribute':[{'wildcard':{'domain':'*'+'媒体'+'*'}}, {'wildcard':{'topic': '*'+'民生类_社会保障'+'*'}}],\
            'event':[{'wildcard':{'text': '*'+'1'+'*'}}, {'range':{'timestamp':{'gte':1377964800, 'lt':1378483200}}}],\
            'filter':{'count':100, 'importance':{'gte':new_importance_from, 'lt':new_importance_to},\
            'influence':{'gte':new_influence_from, 'lt':new_influence_to}}}}

    #event_dict = {'task_information':{'task_name':'test', 'task_type':'detect', 'submit_date':1453002410, 'submit_user':'admin', 'detect_process':0, 'state':'test', 'detect_type':'event'},\
    #        'query_condition':{'attribute':[], 'event':[{'wildcard':{'text': '*'+'1'+'*'}}, {'range':{'timestamp':{'gte':1377964800, 'lt':1378483200}}}],\
    #        'filter':{'count':100, 'importance':{'gte':new_importance_from, 'lt':new_importance_to},\
    #        'influence':{'gte':new_influence_from, 'lt':new_influence_to}}}}
    results = event_detect(event_dict)
    print 'results:', results
    save_mark = save_detect_results(results, 'poiu')
    '''
