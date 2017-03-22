# -*- coding: UTF-8 -*-
import sys
import json
import time
import random
from sqlite_query import db
from sqlite_query import PeopleAttention, EventAttention
# from sqlite_query import get_user_name
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION, es_tag, tag_index_name, tag_index_type,\
        es_user_portrait, portrait_index_name, portrait_index_type, \
        es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
        es_retweet, retweet_index_name_pre, retweet_index_type,\
        es_comment, comment_index_name_pre, comment_index_type,\
        be_es_retweet, be_retweet_index_name_pre, be_retweet_index_type,\
        be_es_comment, be_comment_index_name_pre, be_comment_index_type
from parameter import DAY,RUN_TYPE, RUN_TEST_TIME, RECOMMEND_IN_AUTO_DATE,\
        RECOMMEND_IN_AUTO_SIZE, RECOMMEND_IN_AUTO_GROUP,\
        RECOMMEND_IN_AUTO_RANDOM_SIZE, RUN_TYPE, RUN_TEST_TIME,\
        RECOMMEND_IN_OUT_SIZE, RECOMMEND_IN_ITER_COUNT,\
        RECOMMEND_IN_MEDIA_PATH, RECOMMEND_MAX_KEYWORDS, RECOMMEND_IN_WEIBO_MAX,\
        SENTIMENT_SORT_EVALUATE_MAX
from global_utils import es_user_profile, profile_index_name, profile_index_type
from global_config import R_BEGIN_TIME
from time_utils import datetime2ts, ts2datetime, ts2date


# def get_media_user():
#     media_user_list = []
#     f = open(RECOMMEND_IN_MEDIA_PATH, 'rb')
#     for line in f:
#         line_list = line.split('\n')
#         media_user_list.append(line_list[0])
#     return media_user_list


# get recommentation from hotspot information
def get_hotspot_recommentation():
    results = []
    #step1: get media uid from file
    media_user = get_media_user()
    #step2: get media user weibo keywords last day
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms': {'uid': media_user}
                    }
                }
            },
        'aggs':{
            'all_interests':{
                'terms':{
                    'field': 'keywords_string',
                    'size': RECOMMEND_MAX_KEYWORDS
                    }
                }
            }
        }
    #run type
    if RUN_TYPE == 1:
        date = ts2datetime(time.time() - DAY)
        sort_type = 'retweeted'
    else:
        date = ts2datetime(datetime2ts(RUN_TEST_TIME) - DAY)
        sort_type = 'timestamp'
    date = '2016-11-27'
    flow_text_index_name = flow_text_index_name_pre + date
    user_keywords_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                body=query_body)['aggregations']['all_interests']['buckets']
    keywords_list = [item['key'] for item in user_keywords_result]
    #step3: get same weibo list sort by retweet_count
    #step4: filter out user
    out_user_count = 0
    all_out_user = []
    sort_evaluate_max = SENTIMENT_SORT_EVALUATE_MAX
    while out_user_count < RECOMMEND_IN_OUT_SIZE:
        query_body = {
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'range': {sort_type: {'lt': sort_evaluate_max}}},
                                {'terms': {'keywords_string': keywords_list}}
                                ]
                            }
                        }
                    }
                },
            'sort': [{sort_type : {'order':'desc'}}],
            'size': RECOMMEND_IN_WEIBO_MAX
            }
        weibo_user = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, body=query_body)['hits']['hits']
        weibo_user_list = [item['_source']['uid'] for item in weibo_user]
        #filter out
        if weibo_user_list:
            weibo_user_list = list(set(weibo_user_list))
        out_weibo_user_list = filter_out(weibo_user_list)
        all_out_user.extend(out_weibo_user_list)
        all_out_user = list(set(all_out_user))
        out_user_count = len(all_out_user)
        sort_evaluate_max = weibo_user[-1]['_source'][sort_type]
    results = all_out_user
    return results


# get admin user
def get_admin_user():
    #test
    #user_list = ['admin@qq.com', 'linhao.lh@qq.com', 'test2@qq.com', 'wangqing', 'wangmeng']
    user_list = get_user_name()
    return user_list

# get recomment history
def get_recomment_history(admin_user, now_date):
    results = set()
    now_ts = datetime2ts(now_date)
    for i in range(RECOMMEND_IN_AUTO_DATE, 0, -1):
        iter_date = ts2datetime(now_ts - i * DAY)
        submit_user_recomment = 'recoment_' + admin_user + '_' + str(iter_date)
        recomment_user_list = set(R_RECOMMENTATION.hkeys(submit_user_recomment))
        results = results | recomment_user_list

    return results

# get tag history
def get_tag_history(admin_user, now_date):
    results = set()
    now_ts = datetime2ts(now_date)
    search_tag_list = []
    query_date_list = []
    for i in range(RECOMMEND_IN_AUTO_DATE, 0, -1):
        iter_date = ts2datetime(now_ts - i * DAY)
        query_date_list.append(iter_date)
    attribute_query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            #{'terms': {'date': query_date_list}},
                            {'term': {'user': admin_user}}
                            ]
                        }
                    }
                }
            }
        }
    try:
        attribute_result = es_tag.get(index=attribute_index_name, doc_type=attribute_index_type,\
                body=attribute_query_body)['hits']['hits']
    except:
        attribute_result = []
    tag_query_list = []
    for attribute_item in attribute_result:
        attribute_item_source = attribute_item['_source']
        attribute_name = attribute_item_source['attribute_name']
        attribute_value_string = attribute_item_source['attribute_value']
        item_tag_list = [attribute_name + '-' + attribute_value for attribute_value in attribute_value_string]
        tag_query_list.extend(item_tag_list)
    submit_user_attribute = admin_user + '-tag'
    portrait_query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms': {submit_user_attribute: tag_query_list}
                    }
                }
            },
        'size': RECOMMEND_IN_AUTO_SIZE
        }
    try:
        portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
                body=portrait_query_body, _source=False)['hits']['hits']
    except:
        portrait_result = []
    results = set([item['_id'] for item in portrait_result])

    return results

# get group history
def get_group_history(admin_user, now_date):
    results = set()
    now_ts = datetime2ts(now_date)
    start_ts = now_ts - DAY * RECOMMEND_IN_AUTO_DATE
    end_ts = now_ts
    #search group task
    query_body = {
        'query':{
            'bool':{
                'must':[
                    #{'range': {'submit_date':{'gte': start_ts, 'lt': end_ts}}},
                    {'term': {'submit_user': admin_user}},
                    {'term': {'task_type': 'analysis'}}
                    ]
                }
            },
        'size': RECOMMEND_IN_AUTO_GROUP
        }
    try:
        group_results = es_group_result.search(index=group_index_name, doc_type=group_index_type,\
                body=query_body, _source=False, fields=['uid_list'])['hits']['hits']
    except:
        group_results = []
    all_user_list = []
    for group_item in group_results:
        try:
            uid_list = group_item['fields']['uid_list']
        except:
            uid_list = []
        all_user_list.extend(uid_list)
    results = set(all_user_list)
    return results

# get social sensing history
def get_sensing_history(admin_user, now_date):
    results = set()
    now_ts = datetime2ts(now_date)
    start_ts = now_ts - DAY * RECOMMEND_IN_AUTO_DATE
    end_ts = now_ts
    #search social sensing task
    query_body = {
        'query':{
            'bool':{
                'must':[
                    #{'range': {'create_at': {'gte': start_ts, 'lt': end_ts}}},
                    {'term': {'create_by': admin_user}}
                    ]
                }
            },
        'size': RECOMMEND_IN_AUTO_GROUP
        }
    try:
        sensing_result = es_social_sensing.search(index=sensing_index_name, doc_type=sensing_doc_type,\
                body=query_body, _source=False, fields=['social_sensors'])['hits']['hits']
    except:
        sensing_result = []
    sensing_user_list = []
    for task_item in sensing_result:
        user_list = json.loads(task_item['fields']['social_sensors'][0])
        sensing_user_list.extend(user_list)
    results = set(sensing_user_list)
    return results


def get_db_num():
    date = ts2datetime(time.time())
    date_ts = datetime2ts(date)
    r_begin_ts = datetime2ts(R_BEGIN_TIME)
    db_number = ((date_ts - r_begin_ts) / (DAY * 7 )) % 2 + 1
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number


def union_dict(objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    
    return _total


def filter_out(all_user_set):
    out_results = []
    all_user_list = list(all_user_set)
    all_count = len(all_user_set)
    out_count = 0
    iter_count = 0
    while out_count < RECOMMEND_IN_OUT_SIZE:
        iter_user_list = all_user_list[iter_count: iter_count + RECOMMEND_IN_ITER_COUNT]
        if iter_user_list == []:
            break
        #out portrait
        try:
            in_portrait_result = es_user_portrait.mget(index=portrait_index_name, \
                    doc_type=portrait_index_type, body={'ids': iter_user_list})['docs']
        except:
            in_portrait_result = []
        for in_item in in_portrait_result:
            if in_item['found'] == False:
                out_count += 1
                out_results.append(in_item['_id'])
        iter_count += RECOMMEND_IN_ITER_COUNT
    return out_results


# get extend by history record
def get_extend(all_set):
    extend_result = set()
    retweet_comment_dict_list = []
    #step0: random get user
    user_count = len(all_set)
    all_user_list = list(all_set)
    if RECOMMEND_IN_AUTO_RANDOM_SIZE > len(all_user_list):
        silce = all_user_list
    else:
        silce = random.sample(all_user_list, RECOMMEND_IN_AUTO_RANDOM_SIZE)
    db_number = get_db_num()
    #step1: get retweet
    retweet_index_name = retweet_index_name_pre + str(db_number)
    try:
        retweet_result = es_retweet.mget(index=retweet_index_name, doc_type=retweet_index_type,\
                body={'ids': silce})['docs']
    except:
        retweet_result = []
    #step1.2: get uid retweet
    for retweet_item in retweet_result:
        try:
            if retweet_item['found']==True:
                uid_retweet_dict = retweet_item['_source']['uid_retweet']
                retweet_comment_dict_list.append(json.loads(uid_retweet_dict))
        except:
            pass

    #step2: get comment
    comment_index_name = comment_index_name_pre + str(db_number)
    try:
        comment_result = es_comment.mget(index=comment_index_name, doc_type=comment_index_type,\
                body={'ids': silce})['docs']
    except:
        comment_result = []
    #step2.2: get uid comment
    for comment_item in comment_result:
        try:
            if comment_item['found'] == True:
                retweet_comment_dict_list.append(json.loads(comment_item['_source']['uid_comment']))
        except:
            pass
        
    #step3: get be_retweet
    be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
    try:
        be_retweet_result = be_es_retweet.mget(index=be_retweet_index_name, doc_type=be_retweet_index_type,\
                body={'ids': silce})['docs']
    except:
        be_retweet_result = []
    #step3.2: get uid be retweeted
    for be_retweet_item in be_retweet_result:
        try:
            if be_retweet_item['found'] == True:
                retweet_comment_dict_list.append(json.loads(be_retweet_item['_source']['uid_be_retweet']))
        except:
            pass
    
    #step4: get be comment
    be_comment_index_name = be_comment_index_name_pre + str(db_number)
    try:
        be_comment_result = be_es_comment.mget(index=be_comment_index_name, doc_type=be_comment_index_type,\
                body={'ids': silce})['docs']
    except:
        be_comment_result = []
    #step4.2: get uid be comment
    for be_comment_item in be_comment_result:
        try:
            if be_comment_item['found'] == True:
                retweet_comment_dict_list.append(json.loads(be_comment_item['_source']['uid_be_comment']))
        except:
            pass
    #step5: union dict list
    union_retweet_comment_list = union_dict(retweet_comment_dict_list)
    #step6: filter in user portrait
    extend_result = filter_out(union_retweet_comment_list.keys())

    return extend_result

def query_attention_user():
    # session = Session()
    # user_result = db.session.query(User).all()  
    people_result = db.session.query(PeopleAttention).all()
    user_dict = {}    
    for r in people_result:
        user_dict[r.name] = []
    for r in people_result:
        user_dict[r.name].append(r.peopleID)
        # print r.name,'!!!'
        # print r.peopleID,'!!!!'
        # admin_list.append(r.email)
    return user_dict

def get_close_user(attention_id):
    extend_result = get_extend(attention_id)
    return extend_result

def search_user_type(uid_list):
    type_list = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, \
                body={'ids': uid_list},_source=False, fields=['id', 'verified_type'])['docs']
    user_list = []
    org_list = []
    for i in type_list:
        if i['found'] == False:
            user_list.append(i['_id'])
        else:
            # print i
            if not i.has_key('verified_type'):
                user_list.append(i['_id'])
                continue
            verified_type = i['fields']['verified_type'][0]
            if verified_type in org_list:
                org_list.append(i['_id'])
            else:
                user_list.append(i['_id'])
    return user_list,org_list  

# get recommentation from admin user operation,先查找用户关注的用户，再查找与之相关的用户
def get_operation_recommentation():
    results = {}
    now_ts = time.time()
    #run_type
    if RUN_TYPE == 1:
        now_date = ts2datetime(now_ts)
    else:
        now_date = RUN_TEST_TIME
    # user_dict = {'admin':['5825134863', '3036528532']}
    user_dict = query_attention_user()  #{admin:[a,b,c],...}
    # print user_dict,'!!!!!!!!!!!!!!!!!!!111'
    for k,v in user_dict.iteritems():
        user = k
        attention_ids = [i for i in set(v)]
        attention_dict_user = {}
        attention_dict_org = {}
        for attention_id in attention_ids:
            operation_results = get_close_user([attention_id])
            user_list,org_list = search_user_type(operation_results)
            if user_list:
                attention_dict_user[attention_id] = user_list
            if org_list:
                attention_dict_org[attention_id] = org_list
        save_type = 'operation'
        if attention_dict_user:
            save_results(save_type, user, attention_dict_user,'user')
        if attention_dict_org:
            save_results(save_type, user, attention_dict_org,'org')
    return results

# save results
def save_results(save_type, user, recomment_results, node_type):
    save_mark = False
    #run_type
    if RUN_TYPE == 1:
        now_date = ts2datetime(time.time())
    else:
        now_date = ts2datetime(datetime2ts(RUN_TEST_TIME))
    recomment_hash_name = 'recomment_' + now_date + '_auto_' + node_type
    # o_recomment_hash_name = 'recomment_' + now_date + '_auto_org'
    #print 'save operation results'
    R_RECOMMENTATION.hset(recomment_hash_name, user, json.dumps(recomment_results))
    save_mark = True
    return save_mark

# get user auto recommentation
def compute_auto_recommentation():
    #step1: get recommentation from hotspot information
    # hotspot_results = get_hotspot_recommentation()
    # save_type = 'hotspot'
    # save_results(save_type, hotspot_results)
    #step2: get recommentation from admin user operation
    operation_results = get_operation_recommentation()
    # save_type = 'operation'
    # save_results(save_type, operation_results)


if __name__=='__main__':
    log_time_start_ts = time.time()
    log_time_start_date = ts2datetime(log_time_start_ts)
    print 'cron/recommend_in/recommend_in_auto.py&start&' + log_time_start_date
    
    # try:
    compute_auto_recommentation()
    # except Exception, e:
    # print e, '&error&', ts2date(time.time())
    
    log_time_end_ts = time.time()
    log_time_end_date = ts2datetime(log_time_end_ts)
    print 'cron/recommend_in/recommend_in_auto.py&end&' + log_time_end_date

    #test
    #results = get_operation_recommentation()
    #print 'results:', results
    #media_user = get_media_user()
    #print 'media_user:', media_user
    #results = get_hotspot_recommentation()
    #print 'results:', results
    #results = get_admin_user()
    #print 'results:', results