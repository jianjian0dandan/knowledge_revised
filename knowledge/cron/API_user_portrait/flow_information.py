# -*- coding: UTF-8 -*-
'''
acquire the information from flow
input: uid_list and date_ts
output: {uid:{attr:value}}
'''
import IP
import sys
import time
import json
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_CLUSTER_FLOW3 as r_cluster_3
from global_config import flow_text_index_name_pre, flow_text_type
from global_utils import es_flow_text
from global_utils import R_ADMIN as r_sensitive
from parameter import DAY, MAX_VALUE, sensitive_score_dict
from parameter import RUN_TYPE, RUN_TEST_TIME, WEEK, IP_TIME_SEGMENT
from time_utils import datetime2ts, ts2datetime, ts2date


test_ts = datetime2ts(RUN_TEST_TIME)
flow_text_index_type = flow_text_type

# use to compute flow information for new user attribute compute
# write in version: 2016-02-28
# input: uid_list, keywords_dict
def get_flow_information_v2(uid_list, all_user_keywords_dict):
    results = {}      
    #results = {uid:{'hashtag_dict':{},'hashtag':'', 'keywords_dict':{}, 'keywords_string':'', 'activity_geo':'', 'activity_geo_dict':dict, 'activity_geo_aggs':''}}
    iter_results = {} # iter_results = {uid:{'hashtag': hashtag_dict, 'geo':geo_dict, 'keywords':keywords_dict}}
    now_ts = time.time()
    #run_type
    today_sensitive_results = {}
    if RUN_TYPE == 1:
        now_date_ts = datetime2ts(ts2datetime(now_ts))
    else:
        now_date_ts = test_ts
    for i in range(WEEK,0,-1):
        ts = now_date_ts - DAY*i
        uid_day_geo = {}
        #compute hashtag and geo
        hashtag_results = r_cluster_3.hmget('hashtag_'+str(ts), uid_list)
        ip_results = r_cluster.hmget('new_ip_'+str(ts), uid_list)
        #compute sensitive_words
        sensitive_results = r_cluster_3.hmget('sensitive_'+str(ts), uid_list)
        count = 0 
        for uid in uid_list:
            #init iter_results[uid]
            if uid not in iter_results:
                iter_results[uid] = {'hashtag':{}, 'geo':{},'geo_track':[],'keywords':{}, 'sensitive':{}, 'school':{}, 'week_ip':{}, 'ip':{}}
            if uid not in today_sensitive_results:
                today_sensitive_results[uid] = {}
            #compute hashtag
            hashtag_item = hashtag_results[count]
            if hashtag_item:
                uid_hashtag_dict = json.loads(hashtag_item)
            else:
                uid_hashtag_dict = {}
            for hashtag in uid_hashtag_dict:
                try:
                    iter_results[uid]['hashtag'][hashtag] += uid_hashtag_dict[hashtag]
                except:
                    iter_results[uid]['hashtag'][hashtag] = uid_hashtag_dict[hashtag]
            #compute sensitive
            sensitive_item = sensitive_results[count]
            if sensitive_item:
                uid_sensitive_dict = json.loads(sensitive_item)
            else:
                uid_sensitive_dict = {}
            for sensitive_word in uid_sensitive_dict:
                try:
                    iter_results[uid]['sensitive'][sensitive_word] += uid_sensitive_dict[sensitive_word]
                except:
                    iter_results[uid]['sensitive'][sensitive_word] = uid_sensitive_dict[sensitive_word]
                if ts == now_date_ts - DAY:
                    try:
                        today_sensitive_results[uid][sensitive_word] += uid_sensitive_dict[sensitive_word]
                    except:
                        today_sensitive_results[uid][sensitive_word] = uid_sensitive_dict[sensitive_word]
            #compute geo
            uid_day_geo[uid] = {}
            ip_item = ip_results[count]
            if ip_item:
                uid_ip_dict = json.loads(ip_item)
            else:
                uid_ip_dict = {}
            for ip in uid_ip_dict:
                ip_count = len(uid_ip_dict[ip].split('&'))               
                geo, school = ip2city(ip)
                if geo:
                    try:
                        iter_results[uid]['geo'][geo] += ip_count
                    except:
                        iter_results[uid]['geo'][geo] = ip_count
                    try:
                        uid_day_geo[uid][geo] += ip_count
                    except:
                        uid_day_geo[uid][geo] = ip_count
                if school:
                    try:
                        iter_results[uid]['school'][school] += ip_count
                    except:
                        iter_results[uid]['school'][school] = ip_count
                #deal ip: job_ip&home_ip&active_ip
                ip_time_list= uid_ip_dict[ip].split('&')
                try:
                    iter_results[uid]['ip'][ip] += ip_count
                except:
                	iter_results[uid]['ip'] = {ip: ip_count}
                for ip_time_item in ip_time_list:
                	ip_timesegment = (int(ip_timestamp) - ts) / IP_TIME_SEGMENT
                	try:
                		iter_results[uid]['week_ip'][ip_timesegment][ip] += 1
                	except:
                		iter_results[uid]['week_ip'][ip_timesegment] = {ip: 1}
                #end deal ip
            iter_results[uid]['geo_track'].append(uid_day_geo[uid])
            count += 1
               
    #get keywords top
    for uid in uid_list:
        results[uid] = {}
        #hashtag
        hashtag_dict = iter_results[uid]['hashtag']
        results[uid]['hashtag_dict'] = json.dumps(hashtag_dict)
        results[uid]['hashtag'] = '&'.join(hashtag_dict.keys())
        #sensitive words
        sensitive_word_dict = iter_results[uid]['sensitive']
        results[uid]['sensitive_dict'] = json.dumps(sensitive_word_dict)
        results[uid]['sensitive_string'] = '&'.join(sensitive_word_dict.keys())
        sensitive_score = 0
        today_sensitive_results_user = today_sensitive_results[uid]
        for sensitive_item in today_sensitive_results_user:
            k = sensitive_item
            v = today_sensitive_results_user[sensitive_item]
            tmp_stage = r_sensitive.hget('sensitive_words', k)
            if tmp_stage:
                sensitive_score += v * sensitive_score_dict[str(tmp_stage)]
        results[uid]['sensitive'] = sensitive_score
        #geo
        geo_dict = iter_results[uid]['geo']
        geo_track_list = iter_results[uid]['geo_track']
        results[uid]['activity_geo_dict'] = json.dumps(geo_track_list)
        geo_dict_keys = geo_dict.keys()
        results[uid]['activity_geo'] = '&'.join(['&'.join(item.split('\t')) for item in geo_dict_keys])
        try:
            results[uid]['activity_geo_aggs'] = '&'.join([item.split('\t')[-1] for item in geo_dict_keys])
        except:
            results[uid]['activity_geo_aggs'] = ''
        #keywords
        keywords_dict = all_user_keywords_dict[uid]
        keywords_top50 = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)[:50]
        keywords_top50_string = '&'.join([keyword_item[0] for keyword_item in keywords_top50])
        results[uid]['keywords'] = json.dumps(keywords_top50)
        results[uid]['keywords_string'] = keywords_top50_string
        #school dict
        school_dict = iter_results[uid]['school']
        school_string = '&'.join(school_dict.keys())
        if school_dict != {}:
            is_school = '1'
        else:
            is_school = '0'
        results[uid]['is_school'] = is_school
        results[uid]['school_string'] = school_string
        results[uid]['school_dict'] = json.dumps(school_dict)
        #ip: job_ip&home_ip&activity_ip
        #activity_ip
        all_ip_dict = iter_results[uid]['ip']
        sort_all_ip = sorted(all_ip_dict.items(), key=lambda x:x[1], reverse=True)
        activity_ip = sort_all_ip[0]
        results[uid]['activity_ip'] = activity_ip
        #job_ip & home_ip
        week_time_ip_dict = iter_results[uid]['week_ip']
        for i in range(0, 6):
        	try:
        	    segment_dict = week_time_ip_dict[i]
            except:
            	week_time_ip_dict[i] = {}
        home_ip, job_ip = get_ip_description(week_time_ip_dict)
        results[uid]['home_ip'] = home_ip
        results[uid]['job_ip'] = job_ip
        
    return results

def get_ip_description(week_results):
	sort_week_result = sorted(week_results.items(), key=lambda x:x[0])
	job_segment_dict = union_dict(sort_week_result[2][1], sort_week_result[3][1])
	home_segment_dict = union_dict(sort_week_result[0][1], sort_week_result[5][1])
    sort_job_list = sorted(job_segment_dict.items(), key=lambda x:x[1], reverse=True)[0]
    sort_home_list = sorted(home_segment_dict.items(), key=lambda x:x[1], reverse=True)[0]
    job_ip = sort_job_list[0]
    home_ip = sort_home_list[0]
    return home_ip, job_ip 