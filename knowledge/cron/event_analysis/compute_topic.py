#-*-coding:utf-8-*-
import sys,json
sys.path.append('../../')
from global_utils import R_ADMIN as r
from global_utils import topic_queue_name,es_flow_text,flow_text_index_type,flow_text_index_name_pre
from global_config import weibo_es,weibo_index_name,weibo_index_type,topic_index_name,topic_index_type,\
						MAX_FREQUENT_WORDS,MAX_LANGUAGE_WEIBO,NEWS_LIMIT
from flow_text_mappings import get_mappings
import datetime,time
from time_utils import ts2datetime
import traceback
import os
'''
sys.path.append('./geo')
sys.path.append('./language/fix')
sys.path.append('./network')
sys.path.append('./propagate')
sys.path.append('./sentiment')
from city_repost_search import repost_search
from count_keyword import count_fre
from cron_topic_identify import compute_network
from cron_topic_propagate import propagateCronTopic
from cron_topic_sentiment import sentimentTopic
'''
'''
from geo.city_repost_search import repost_search
from geo.cron_topic_city import cityTopic
from network.cron_topic_identify import compute_network
from propagate.cron_topic_propagate import propagateCronTopic
from sentiment.cron_topic_sentiment import sentimentTopic
from language.fix.count_keyword import count_fre
'''
#from propagate.cron_topic_propagate import propagateCronTopic
from network.cron_topic_identify import compute_network


def get_by_name(name):
	query_body=query_body = {'query':{'term':{'name':name}}}
	result = weibo_es.search(index=topic_index_name,doc_type=topic_index_type,body=query_body)['hits']['hits']
	#print result[0]['_source']
	return json.dumps(result[0]['_source'])



def compute_topic_task():
	print time.time()
	while  True:
		#print r.rpop(topic_queue_name)
		#task = r.rpop(topic_queue_name)
		task=get_by_name('叶简明')
		if not task:
			break
		else:
			task = json.loads(task)
			print task
			topic = task['name']
			en_name = task['en_name']
			start_ts = int(task['start_ts'])  #timestamp
			end_ts = int(task['end_ts'])   #timestamp
			submit_user = task['submit_user']
			comput_status = task['comput_status']
			task_id = str(start_ts)+'_'+str(end_ts)+'_'+en_name+'_'+submit_user
			
			exist_flag = exist(task_id)
			#get_topic_weibo(topic,en_name,start_ts,end_ts)
			if exist_flag:
				#start compute
				#try:
				# weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':-1}})
				# print 'finish change status'
				# #geo
				
				# repost_search(en_name, start_ts, end_ts)
				# print 'finish geo_1 analyze'
				# cityTopic(en_name, start_ts, end_ts)
				# print 'finish geo analyze'
				# # #language
				# count_fre(en_name, start_ts=start_ts, over_ts=end_ts,news_limit=NEWS_LIMIT,weibo_limit=MAX_LANGUAGE_WEIBO)
				# print 'finish language analyze'
				# #time
				# propagateCronTopic(en_name, start_ts, end_ts)
				# print 'finish time analyze'

				#network
				compute_network(en_name, start_ts, end_ts)
				print 'finish network analyze'

				#sentiment
				# sentimentTopic(en_name, start_ts=start_ts, over_ts=end_ts)
				# print 'finish sentiment analyze'
				#finish compute
				print weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':1,'finish_ts':int(time.time())}})
				print 'finish change status done'
				# except:
				# 	raise
				# 	break
				break
			else:
				pass

def exist(task_id):
	try:
		task_exist = weibo_es.get(index=topic_index_name,doc_type=topic_index_type,id=task_id)['_source']
	except:
		task_exist = {}
	if not task_exist:
	    return False
	else:
	    return True

def get_topic_weibo(topic,en_name,start_ts,end_ts):
	query_body = {'query':{'match_all':{}},'sort':'timestamp','size':1}
	try:
		task_exist = weibo_es.search(index=en_name,doc_type=topic_index_type,body=query_body)['hits']['hits']
	except:
		get_mappings(en_name)
	find_flow_texts(start_ts,end_ts,topic,en_name)


def find_flow_texts(start_ts,end_ts,topic,en_name):   #多个wildcard/时间戳的range
	# if RUN_TYPE == 1:
	#     today = datetime.date.today() 
	# else:
	#     today = datetime.date(2016,05,23)
	query_body = {'query':{'wildcard':{'text':'*'+topic+'*'}}}
	index_names = get_day_zero(start_ts,end_ts)
	result = []
	index_list = []
	for index_name in index_names:
		index_list.append(flow_text_index_name_pre+index_name)
	result = es_flow_text.search(index=index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
	print flow_text_index_name_pre+index_name,es_flow_text,len(result)
	if result:
		save_es(en_name,result)



def get_day_zero(start_ts,end_ts):
	DAY = 24*60*60#*1000
	HOUR = 60*60
	start = float(start_ts)-float(start_ts)%DAY+HOUR*16 
	end = float(end_ts)-float(end_ts)%DAY+HOUR*16 

	during = (end - start)/DAY
	end_time = time.localtime(int(end))[:3]
	end = datetime.date(*end_time)

	return [str(end + datetime.timedelta(days=-i)) for i in range(int(during)+1)]

def save_es(en_name,result):
	bulk_action = []
	count = 0
	tb = time.time()
	for weibos in result:
		#try:
		source = weibos['_source']
		action = {'index':{'_id':weibos['_id']}}
		bulk_action.extend([action,source])
		count += 1
		if count % 1000 == 0:
		    weibo_es.bulk(bulk_action, index=en_name, doc_type=topic_index_type, timeout=100)
		    bulk_action = []
		    print count
		    if count % 10000 == 0:
		        te = time.time()
		        print "index 10000 per %s second" %(te - tb)
		        tb = te
	print "all done"
	if bulk_action:
	    weibo_es.bulk(bulk_action, index=en_name, doc_type=topic_index_type, timeout=100)
	return 1

def yejianming():
	en_name='ye-jian-ming-1482830875'
	#get_mappings(en_name)
	result=[]
	for files in os.listdir('/home/ubuntu2/jiangln/yejianming_17'):
		f=open('/home/ubuntu2/jiangln/yejianming_17/'+files,'r')
		print files
		result.extend(json.loads(f.read()))
		#len_f = len(json.loads(f.read()))
		#print len_f
		#result.append({files:len_f})
	#print result

	save_es_ye(en_name,result)


def save_es_ye(en_name,result):
	bulk_action = []
	count = 0
	tb = time.time()
	for weibos in result:
		#try:
		source = weibos
		action = {'index':{'_id':weibos['mid']}}
		bulk_action.extend([action,source])
		count += 1
		if count % 1000 == 0:
		    weibo_es.bulk(bulk_action, index=en_name, doc_type=topic_index_type, timeout=100)
		    bulk_action = []
		    print count
		    if count % 10000 == 0:
		        te = time.time()
		        print "index 10000 per %s second" %(te - tb)
		        tb = te
	print "all done"
	if bulk_action:
	    weibo_es.bulk(bulk_action, index=en_name, doc_type=topic_index_type, timeout=100)
	return 1


if __name__ == '__main__':
	#compute_topic_task()
	#get_topic_weibo('画画','huahua','1377964800','1378137600')
	yejianming()
	#et_by_name('叶简明')