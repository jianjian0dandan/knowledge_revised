#-*- coding: UTF-8 -*-
'''
compute the user attribute about text
data source: weibo api
scene: add user to user portrait
'''
import csv
import sys
import json
import time
from flow_infomation import get_flow_information_v2
from user_profile import get_profile_information
from evaluate_index import get_importance, get_activity_time, get_activeness, get_influence
from topic.test_topic import topic_classfiy
from domain.test_domain_v2 import domain_classfiy
sys.path.append('../../')
from global_utils import bci_day_pre, bci_day_type, es_bci, es_user_portrait
from global_utils import portrait_index_name, portrait_index_type
from parameter import RUN_TYPE, RUN_TEST_TIME
from time_utils import ts2datetime

#get funsnum_max from bci_date
def get_fansnum_max(uid_list):
	#fansnum_max
	query_body = {
        'query':{
            'match_all':{}
            },
        'size': 1,
        'sort': [{'fansnum': {'order': 'desc'}}]
        }
    ts = time.time()
    if RUN_TYPE == 1:
        now_date = ts2datetime(ts - 24*3600)
    else:
        now_date = RUN_TEST_TIME  
    bci_index_name = bci_day_pre +''.join(now_date.split('-'))
    try:
        fansnum_max_results = es_bci.search(index=bci_index_name, doc_type=bci_day_type, body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    fansnum_max = fansnum_max_results[0]['_source']['fansnum']
    #user_fansnum_dict
    search_result = es_bci.mget(index=bci_index_name, doc_type=bci_day_type, body={'ids':uid_list},_source=True)['docs']
    user_fansnum_dict = dict()
    for search_item in search_result:
    	try:
            user_fansnum_dict[search_item] = search_result['user_fansnum']
	    except:
	    	user_fansnum_dict[search_item] = 0
	return fansnum_max, user_fansnum_dict


def save_user_results(bulk_action):
    print 'save utils bulk action len:', len(bulk_action)
    #print 'bulk action:', bulk_action
    es_user_portrait.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type, timeout=60)
    return True  

#use to compute new user attribute by redis_user2portrait.py
#version: write in 2016-02-28
def test_cron_text_attribute_v2(user_keywords_dict, user_weibo_dict, online_pattern_dict, character_start_ts):
    status = False
    print 'start cron_text_attribute'
    uid_list = user_keywords_dict.keys()
    
    #get user flow information: hashtag, activity_geo, keywords, ip
    print 'get flow result'
    flow_result = get_flow_information_v2(uid_list, user_keywords_dict)
    print 'flow result len:', len(flow_result)
    
    #get user profile information
    print 'get register result'
    register_result = get_profile_information(uid_list)
    print 'register result len:', len(register_result)
    
    #get user topic and domain by bulk action
    print 'get topic and domain'
    topic_results_dict, topic_results_label = topic_classfiy(uid_list, user_keywords_dict)
    domain_results = domain_classfiy(uid_list, user_keywords_dict)
    domain_results_dict = domain_results[0]
    domain_results_label = domain_results[1]
    print 'topic result len:', len(topic_results_dict)
    print 'domain result len:', len(domain_results_dict)
    
    #get user fansnum max
    fansnum_max, user_fansnum_dict = get_fansnum_max(uid_list)
    #get user activeness by bulk_action
    print 'get activeness results'
    activeness_results = get_activity_time(uid_list)
    print 'activeness result len:', len(activeness_results)
    #get user inlfuence by bulk action
    print 'get influence'
    influence_results = get_influence(uid_list)
    print 'influence results len:', len(influence_results)
    
    # compute text attribute
    bulk_action = []
    count = 0
    for user in uid_list:
        count += 1
        results = {}       
        #get user text attribute: online_pattern
        results['online_pattern'] = json.dumps(online_pattern_dict[user])
        try:
            results['online_pattern_aggs'] = '&'.join(online_pattern_dict[user].keys())
        except:
            results['online_pattern_aggs'] = ''
        results['uid'] = str(user)
        #add user flow information: hashtag, activity_geo, keywords, ip
        flow_dict = flow_result[str(user)]
        results = dict(results, **flow_dict)
        
        #add user topic attribute
        user_topic_dict = topic_results_dict[user]
        user_label_dict = topic_results_label[user]
        results['topic'] = json.dumps(user_topic_dict)         # {'topic1_en':pro1, 'topic2_en':pro2...}
        results['topic_string'] = topic_en2ch(user_label_dict) # 'topic1_ch&topic2_ch&topic3_ch'
        
        #add user domain attribute
        user_domain_dict = domain_results_dict[user]
        user_label_dict = domain_results_label[user]
        results['domain_v3'] = json.dumps(user_domain_dict) # [label1_en, label2_en, label3_en]
        results['domain'] = domain_en2ch(user_label_dict)      # label_ch   
        
        #add user profile attribute
        register_dict = register_result[str(user)]
        results = dict(results, **register_dict)
        #add user_evaluate attribute---importance
        results['importance'] = get_importance(results['domain'], results['topic_string'], user_fansnum_dict[user], fansnum_max)
        #add user_evaluate attribute---activeness
        user_activeness_time = activeness_results[user]
        user_activeness_geo = json.loads(results['activity_geo_dict'])[-1]
        results['activeness'] = get_activeness(user_activeness_geo, user_activeness_time)
        #add user_evaluate attribute---influence
        results['influence'] = influence_results[user]
        
        #bulk_action
        action = {'index':{'_id': str(user)}}
        bulk_action.extend([action, results])
        
    status = save_user_results(bulk_action)
    
    return status