# -*- coding: utf-8 -*-
import sys
import json
import datetime
#from topics import _all_topics

sys.path.append('../../../')
from time_utils import * #datetime2ts, ts2HourlyTime
from global_config import event_analysis_name,event_type,event_text,event_text_type
from global_utils import es_event,es_user_portrait,portrait_index_name,portrait_index_type
from global_utils import bci_day_pre,bci_day_type
from parameter import RUN_TYPE,RUN_TEST_TIME

def get_users(topic,begin_ts,end_ts):
	uid_list = set()
	query_body = {   
	    'query':{
	        'bool':{
	            'must':[
	                {'term':{'en_name':topic}},
	                {'range':{
	                    'timestamp':{'gte': begin_ts, 'lt':end_ts} 
	                }
	            }]
	        }
	    },
	    'size':999999999
	}
	result = es_event.search(index=event_text,doc_type=event_text_type, fields=['uid'],body=query_body)['hits']['hits']
	for i in result:
		uid_list.add(i['fields']['uid'][0])
	print len(uid_list)
	if RUN_TYPE == 0:
		post = datetime2ts(RUN_TEST_TIME) #datetimestr2ts(RUN_TEST_TIME) 
		post = ts2datetimestr(post)
	else:
		post = ts2datetimestr(time.time())
		
	print  bci_day_pre+post,bci_day_type,es_user_portrait
	user_result = es_user_portrait.mget(index=bci_day_pre+post ,doc_type=bci_day_type,body={'ids':list(uid_list)})['docs']
	
	user_influence_dict = {}
	for i in user_result:
		#print i
		if i['found']:
			i = i['_source']
			user_influence_dict[i['user']] = i['user_index']
			#print i,type(i)
			
			#print i['activeness'],i['influence'],i['fansnum']

	user = sorted(user_influence_dict.iteritems(),key=lambda x:x[1],reverse=True)[:100]
	#print user

	try:
		es_event.update(index=event_analysis_name,doc_type=event_type,id=topic,body={'doc':{'user_results':json.dumps(user)}})
	except Exception,e:
	    es_event.index(index=event_analysis_name,doc_type=event_type,id=topic,body={'user_results':json.dumps(user)})


if __name__ == '__main__':
	topic = 'zui_gao_fa_di_zhi_yan_se_ge_ming'
	start_date = 1484323200#'2017-01-14'
	end_date = 1484582400#'2017-01-17'

	get_users(topic,start_date,end_date)