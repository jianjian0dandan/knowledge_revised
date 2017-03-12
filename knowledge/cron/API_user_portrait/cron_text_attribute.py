#-*- coding: UTF-8 -*-
'''
compute the user attribute about text
data source: weibo api
scene: add user to user portrait
'''
from flow_infomation import get_flow_information_v2
from topic.test_topic import topic_classfiy

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
    fansnum_max = get_fansnum_max()
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
        #add user flow information: hashtag, activity_geo, keywords
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
        
        #add user character_sentiment attribute
        character_sentiment = character_sentiment_result_dict[user]
        results['character_sentiment'] = character_sentiment
        #add user character_text attribtue
        character_text = character_text_result_dict[user]
        results['character_text'] = character_text
        
        #add user profile attribute
        register_dict = register_result[str(user)]
        results = dict(results, **register_dict)
        #add user_evaluate attribute---importance
        results['importance'] = get_importance(results['domain'], results['topic_string'], results['fansnum'], fansnum_max)
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