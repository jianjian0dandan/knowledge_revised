# -*- coding: UTF-8 -*-
'''
recommentation
save uid list should be in
'''
import IP
import sys
import time
import datetime
import math
import json
import redis
import math
from elasticsearch import Elasticsearch
# from update_activeness_record import update_record_index
from knowledge.global_utils import R_RECOMMENTATION as r
# from knowledge.global_utils import R_RECOMMENTATION_OUT as r_out
from knowledge.global_utils import R_CLUSTER_FLOW3 as r_cluster
from knowledge.global_utils import R_CLUSTER_FLOW2 as r_cluster2
from knowledge.global_utils import es_user_portrait as es
from knowledge.global_utils import es_recommendation_result, recommendation_index_name, recommendation_index_type
from knowledge.global_utils import es_user_profile, portrait_index_name, portrait_index_type, profile_index_name, profile_index_type
from knowledge.global_utils import ES_CLUSTER_FLOW1 as es_cluster
# from knowledge.global_utils import es_bci_history, bci_history_index_name, bci_history_index_type, ES_SENSITIVE_INDEX, DOCTYPE_SENSITIVE_INDEX
# from knowledge.filter_uid import all_delete_uid
from knowledge.time_utils import ts2datetime, datetime2ts
from knowledge.parameter import DAY, WEEK, RUN_TYPE, RUN_TEST_TIME,MAX_VALUE,sensitive_score_dict

WEEK = 7

def identify_in(data, uid_list):
    in_status = 1
    compute_status = 0
    compute_hash_name = 'compute'
    compute_uid = r.hkeys(compute_hash_name)
    for item in data:
        date = item[0] # identify the date form '2013-09-01' with web
        uid = item[1]
        status = item[2]
        relation_string = item[3]
        recommend_style = item[4]
        submit_user = item[5]
        value_string = []
        identify_in_hashname = "identify_in_" + str(date)
        r.hset(identify_in_hashname, uid, in_status)
        if status == '1':
            in_date = date
            compute_status = '1'
        elif status == '2':
            in_date = date
            compute_status = '2'
        r.hset(compute_hash_name, uid, json.dumps([in_date, compute_status, relation_string, recommend_style, submit_user,0]))
    return True

#submit new task and identify the task name unique in es-group_result and save it to redis list
def submit_task(input_data):
    status = 0 # mark it can not submit
    task_name = input_data['task_name']
    submit_user = input_data['submit_user']
    task_id = input_data['task_id']
    try:
        result = es_recommendation_result.get(index=recommendation_index_name, doc_type=recommendation_index_type, id=task_id)['_source']
    except:
        status = 1
    
    if status != 0 and 'uid_file' not in input_data:
        input_data['status'] = 0 # mark the task not compute
        count = len(json.loads(input_data['uid_list']))
        input_data['count'] = count
        input_data['submit_user'] = submit_user
        # add_es_dict = {'task_information': input_data, 'query_condition':''}
        es_recommendation_result.index(index=recommendation_index_name, doc_type=recommendation_index_type, id=task_id, body=input_data)
        if input_data['cal_style'] == 0:
            group_analysis_queue_name = 'recommendation_in_now'
        if input_data['cal_style'] == 1:
            group_analysis_queue_name = 'recommendation_in_later'
        r.lpush(group_analysis_queue_name, json.dumps(input_data))
    return status



# identify in by upload file to admin user
# input_data = {'date':'2013-09-01', 'upload_data':[], 'user':submit_user}
def submit_identify_in_uid(input_data):
    date = input_data['date']
    submit_user = input_data['user']
    operation_type = input_data['operation_type']
    compute_status = input_data['compute_status'] 
    relation_string = input_data['relation_string'] 
    recommend_style = input_data['recommend_style']
    hashname_submit = 'submit_recomment_' + date
    hashname_influence = 'recomment_' + date + '_influence'
    hashname_sensitive = 'recomment_' + date + '_sensitive'
    compute_hash_name = 'compute'
    # submit_user_recomment = 'recomment_' + submit_user + '_' + str(date)
    auto_recomment_set = set(r.hkeys(hashname_influence)) | set(r.hkeys(hashname_sensitive))
    upload_data = input_data['upload_data']
    line_list = upload_data.split('\n')
    uid_list = []
    invalid_uid_list = []
    for line in line_list:
        uid = line.split('\r')[0]
        #if len(uid)==10:
        #    uid_list.append(uid)
        if uid != '':
            uid_list.append(uid)
    if len(invalid_uid_list)!=0:
        return False, 'invalid user info', invalid_uid_list
    #identify the uid is not exist in user_portrait and compute
    #step1: filter in user_portrait
    new_uid_list = []
    have_in_uid_list = []
    try:
        exist_portrait_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':uid_list}, _source=False)['docs']
    except:
        exist_portrait_result = []
    if exist_portrait_result:
        for exist_item in exist_portrait_result:
            if exist_item['found'] == False:
                new_uid_list.append(exist_item['_id'])
            else:
                have_in_uid_list.append(exist_item['_id'])
    else:
        new_uid_list = uid_list
   
    #step2: filter in compute
    new_uid_set = set(new_uid_list)
    compute_set = set(r.hkeys('compute'))
    in_uid_set = list(new_uid_set - compute_set)
    print 'new_uid_set:', new_uid_set 
    print 'in_uid_set:', in_uid_set
    if len(in_uid_set)==0:
        return False, 'all user in'
    #identify the final add user
    final_submit_user_list = []
    for in_item in in_uid_set:
        if in_item in auto_recomment_set:
            tmp = json.loads(r.hget(hashname_submit, in_item))
            recommentor_list = tmp['operation'].split('&')
            recommentor_list.append(str(submit_user))
            new_list = list(set(recommentor_list))
            tmp['operation'] = '&'.join(new_list)
        else:
            tmp = {'system':'0', 'operation':submit_user}
        if operation_type == 'submit':
            r.hset(compute_hash_name, in_item, json.dumps([in_date, compute_status, relation_string, recommend_style, submit_user, 0 ]))
            r.hset(hashname_submit, in_item, json.dumps(tmp))
            # r.hset(submit_user_recomment, in_item, '0')
        final_submit_user_list.append(in_item)
    return True, invalid_uid_list, have_in_uid_list, final_submit_user_list

def get_final_submit_user_info(uid_list):
    final_results = []
    try:
        profile_results = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids': uid_list})['docs']
    except:
        profile_results = []
    try:
        bci_history_results =es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={'ids': uid_list})['docs']
    except:
        bci_history_results = []
    #get bci_history max value
    now_time_ts = time.time()
    search_date_ts = datetime2ts(ts2datetime(now_time_ts - DAY))
    bci_key = 'bci_' + str(search_date_ts)
    query_body = {
        'query':{
             'match_all':{}
        },
        'sort': [{bci_key:{'order': 'desc'}}],
        'size': 1
    }
    #try:
    bci_max_result = es_bci_history.search(index=bci_history_index_name, doc_type=bci_history_index_type, body=query_body, _source=False, fields=[bci_key])['hits']['hits']
    #except:
    #    bci_max_result = {}
    if bci_max_result:
        bci_max_value = bci_max_result[0]['fields'][bci_key][0]
    else:
        bci_max_value = MAX_VALUE
    iter_count = 0
    for uid in uid_list:
        try:
            profile_item = profile_results[iter_count]
        except:
            profile_item = {}
        try:
            bci_history_item = bci_history_results[iter_count]
        except:
            bci_history_item = {}
        if profile_item and profile_item['found'] == True:
            uname = profile_item['_source']['nick_name']
            location = profile_item['_source']['user_location']
        else:
            uname = ''
            location = ''
        if bci_history_item and bci_history_item['found'] == True:
            fansnum = bci_history_item['_source']['user_fansnum']
            statusnum = bci_history_item['_source']['weibo_month_sum']
            try:
                bci = bci_history_item['_source'][bci_key]
                normal_bci = math.log(bci / bci_max_value * 9 + 1, 10) * 100
            except:
                normal_bci = ''
        else:
            fansnum = ''
            statusnum = ''
            normal_bci = ''
        final_results.append([uid, uname, location, fansnum, statusnum, normal_bci])
        iter_count += 1

    return final_results

def submit_identify_in(input_data):
    result_mark = False
    result_mark = submit_identify_in_uid(input_data)

    if len(result_mark) == 4:
        final_submit_user_list = result_mark[-1]
        if final_submit_user_list:
            final_submit_user_info = get_final_submit_user_info(final_submit_user_list)
        else:
            final_submit_user_info = []
        result_mark = list(result_mark)[:3]
        result_mark.append(final_submit_user_info)
    return result_mark

# show recommentation in uid
def recommentation_in(input_ts, recomment_type, submit_user):
    date = ts2datetime(input_ts)
    recomment_results = []
    # read from redis
    results = []
    hash_name = 'recomment_'+str(date) + "_" + recomment_type
    identify_in_hashname = "identify_in_" + str(date)
    # submit_user_recomment = "recomment_" + submit_user + "_" + str(date) # 用户自推荐名单
    results = r.hgetall(hash_name)
    if not results:
        return []
    # search from user_profile to rich the show information
    recommend_list = set(r.hkeys(hash_name))
    identify_in_list = set(r.hkeys("compute"))
    # submit_user_recomment = set(r.hkeys(submit_user_recomment))
    recomment_results = list(recommend_list - identify_in_list)
    # recomment_results = list(set(recomment_results) - submit_user_recomment)

    if recomment_results:
        results = get_user_detail(date, recomment_results, 'show_in', recomment_type)
    else:
        results = []
    return results


#get user detail
#output: uid, uname, location, fansnum, statusnum, influence
def get_user_detail(date, input_result, status, user_type="influence", auth=""):
    bci_date = ts2datetime(datetime2ts(date) - DAY)
    results = []
    if status=='show_in':
        uid_list = input_result
    if status=='show_compute':
        uid_list = input_result.keys()
    if status=='show_in_history':
        uid_list = input_result.keys()
    if date!='all':
        index_name = 'bci_' + ''.join(bci_date.split('-'))
    else:
        now_ts = time.time()
        now_date = ts2datetime(now_ts)
        index_name = 'bci_' + ''.join(now_date.split('-'))
    tmp_ts = str(datetime2ts(date) - DAY)
    sensitive_string = "sensitive_score_" + tmp_ts
    query_sensitive_body = {
        "query":{
            "match_all":{}
        },
        "size":1,
        "sort":{sensitive_string:{"order":"desc"}}
    }
    try:
        top_sensitive_result = es_bci_history.search(index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX, body=query_sensitive_body, _source=False, fields=[sensitive_string])['hits']['hits']
        top_sensitive = top_sensitive_result[0]['fields'][sensitive_string][0]
    except Exception, reason:
        print Exception, reason
        top_sensitive = 400
    index_type = 'bci'
    user_bci_result = es_cluster.mget(index=index_name, doc_type=index_type, body={'ids':uid_list}, _source=True)['docs']  #INFLUENCE,fans,status
    user_profile_result = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list}, _source=True)['docs'] #个人姓名，注册地
    # bci_history_result = es_bci_history.mget(index=bci_history_index_name, doc_type=bci_history_index_type, body={"ids":uid_list}, fields=['user_fansnum', 'weibo_month_sum'])['docs']
    # sensitive_history_result = es_bci_history.mget(index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX, body={'ids':uid_list}, fields=[sensitive_string], _source=False)['docs']
    max_evaluate_influ = get_evaluate_max(index_name)
    for i in range(0, len(uid_list)):
        uid = uid_list[i]
        bci_dict = user_bci_result[i]
        profile_dict = user_profile_result[i]
        # bci_history_dict = bci_history_result[i]
        # sensitive_history_dict = sensitive_history_result[i]
        #print sensitive_history_dict
        try:
            bci_source = bci_dict['_source']
        except:
            bci_source = None
        if bci_source:
            influence = bci_source['user_index']
            influence = math.log(influence/float(max_evaluate_influ['user_index']) * 9 + 1 ,10)
            influence = influence * 100
        else:
            influence = ''
        try:
            profile_source = profile_dict['_source']
        except:
            profile_source = None
        if profile_source:
            uname = profile_source['nick_name'] 
            location = profile_source['user_location']
            try:
                fansnum = bci_dict['fields']['user_fansnum'][0]
            except:
                fansnum = 0
            try:
                statusnum = bci_dict['fields']['weibo_month_sum'][0]
            except:
                statusnum = 0
        else:
            uname = uid
            location = ''
            try:
                fansnum = bci_dict['fields']['user_fansnum'][0]
            except:
                fansnum = 0
            try:
                statusnum = bci_dict['fields']['weibo_month_sum'][0]
            except:
                statusnum = 0
        if status == 'show_in':
            if user_type == "sensitive":
                tmp_ts = datetime2ts(date) - DAY
                tmp_data = r_cluster.hget("sensitive_"+str(tmp_ts), uid)
                if tmp_data:
                    sensitive_dict = json.loads(tmp_data)
                    sensitive_words = sensitive_dict.keys()
                else:
                    sensitive_words = []
                if sensitive_history_dict.get('fields',0):
                    #print sensitive_history_dict['fields'][sensitive_string][0]
                    #print top_sensitive
                    sensitive_value = math.log(sensitive_history_dict['fields'][sensitive_string][0]/float(top_sensitive)*9+1, 10)*100
                    #print "sensitive_value", sensitive_value
                else:
                    sensitive_value = 0
                results.append([uid, uname, location, fansnum, statusnum, influence, sensitive_words, sensitive_value])
            else:
                results.append([uid, uname, location, fansnum, statusnum, influence])
            if auth:
                hashname_submit = "submit_recomment_" + date
                tmp_data = json.loads(r.hget(hashname_submit, uid))
                recommend_list = (tmp_data['operation']).split('&')
                admin_list = []
                admin_list.append(tmp_data['system'])
                admin_list.append(list(set(recommend_list)))
                admin_list.append(len(recommend_list))
                results[-1].extend(admin_list)
        if status == 'show_compute':
            in_date = json.loads(input_result[uid])[0]
            compute_status = json.loads(input_result[uid])[1]
            if compute_status == '1':
                compute_status = '3'
            results.append([uid, uname, location, fansnum, statusnum, influence, in_date, compute_status])
        if status == 'show_in_history':
            in_status = input_result[uid]
            if user_type == "sensitive":
                tmp_ts = datetime2ts(date) - DAY
                tmp_data = r_cluster.hget("sensitive_"+str(tmp_ts), uid)
                if tmp_data:
                    sensitive_dict = json.loads(tmp_data)
                    sensitive_words = sensitive_dict.keys()
                if sensitive_history_dict.get('fields', 0):
                    sensitive_value = math.log(sensitive_history_dict['fields'][sensitive_string][0]/float(top_sensitive)*9+1, 10)*100
                else:
                    sensitive_value = 0
                results.append([uid, uname, location, fansnum, statusnum, influence, in_status, sensitive_words, sensitive_value])
            else:
                results.append([uid, uname, location, fansnum, statusnum, influence, in_status])

    return results

def get_evaluate_max(index_name):
    max_result = {}
    index_type = 'bci'
    evaluate_index = ['user_index']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size':1,
            'sort':[{evaluate: {'order': 'desc'}}]
            }
        # try:
        result = es_cluster.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        # except Exception, e:
        # raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result

def recommentation_in_auto(date, submit_user):
    results = []
    #run type
    if RUN_TYPE == 1:
        now_date = search_date
    else:
        now_date = ts2datetime(datetime2ts(RUN_TEST_TIME))
    recomment_hash_name = 'recomment_' + now_date + '_auto'
    # print recomment_hash_name,'============'
    recomment_influence_hash_name = 'recomment_' + now_date + '_influence'
    recomment_sensitive_hash_name = 'recomment_' + now_date + '_sensitive'
    recomment_submit_hash_name = 'recomment_' + submit_user + '_' + now_date
    recomment_compute_hash_name = 'compute'
    # #step1: get auto
    # auto_result = r.hget(recomment_hash_name, 'auto')
    # if auto_result:
    #     auto_user_list = json.loads(auto_result)
    # else:
    #     auto_user_list = []
    #step2: get admin user result
    admin_result = r.hget(recomment_hash_name, submit_user)
    admin_user_list = []
    if admin_result:
        admin_result_dict = json.loads(admin_result)
    else:
        return None
    final_result = []
    #step3: get union user and filter compute/influence/sensitive
    for k,v in admin_result_dict.iteritems():
        admin_user_list = v
        union_user_auto_set = set(admin_user_list)
        influence_user = set(r.hkeys(recomment_influence_hash_name))
        sensitive_user = set(r.hkeys(recomment_sensitive_hash_name))
        compute_user = set(r.hkeys(recomment_compute_hash_name))
        been_submit_user = set(r.hkeys(recomment_submit_hash_name))
        filter_union_user = union_user_auto_set - (influence_user | sensitive_user | compute_user | been_submit_user)
        auto_user_list = list(filter_union_user)
        #step4: get user detail
        if auto_user_list == []:
            return auto_user_list
        results = get_user_detail(now_date, auto_user_list, 'show_in', 'auto')
        for detail in results:  #add root
            re_detail = detail
            re_detail.append(k)
            final_result.append(re_detail)
    return final_result