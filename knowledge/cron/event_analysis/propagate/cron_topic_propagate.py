# -*- coding: utf-8 -*-

import sys
import json

#from config import db
#from model import PropagateCount, PropagateKeywords, PropagateWeibos
#from propagate_time_weibo import PropagateTimeWeibos


reload(sys)
sys.path.append('../../../')
#from global_config import db
from time_utils import datetime2ts, ts2HourlyTime

from global_utils import es_event
from global_config import event_analysis_name,event_type,event_text,event_text_type


Minute = 60
Fifteenminutes = 15 * 60
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24

N = 10 # top N设置---确定后放在配置文件中
TOP_KEYWORDS_LIMIT = 50
TOP_WEIBOS_LIMIT = 50
MTYPE_COUNT = 3

RESP_ITER_KEYS = ['_id', 'user', 'retweeted_uid', 'retweeted_mid', 'text', 'timestamp', 'reposts_count', 'bmiddle_pic', 'geo', 'comments_count', 'sentiment', 'terms']
SORT_FIELD = 'reposts_count'



def save_results_es(calc, topic, results, during, klimit=TOP_KEYWORDS_LIMIT, wlimit=TOP_WEIBOS_LIMIT):


	if calc == 'time_results':

		id = topic

		#results = json.dumps(results)

		try:
			item_exist = es_event.get(index=event_analysis_name,doc_type=event_type,id=id)['_source']
			try:
				time_results = json.loads(item_exist['time_results'])
			except:
				time_results = []
			time_results.append(results)
			es_event.update(index=event_analysis_name,doc_type=event_type,id=id,body={'doc':{'time_results':json.dumps(time_results)}})
		except Exception,e:
			es_event.index(index=event_analysis_name,doc_type=event_type,id=id,body={'time_results':json.dumps(results)})


			
def propagateCronTopic(topic, start_ts, over_ts, sort_field=SORT_FIELD, \
    save_fields=RESP_ITER_KEYS, during=Fifteenminutes, w_limit=TOP_WEIBOS_LIMIT, k_limit=TOP_KEYWORDS_LIMIT):
	if topic and topic != '':
		start_ts = int(start_ts)
		over_ts = int(over_ts)

		over_ts = ts2HourlyTime(over_ts, during)
		interval = (over_ts - start_ts) / during

		time_results = []

		for i in range(interval,0,-1):	#每15分钟计算一次
			mtype_count = {}	#每类微博的数量
			mtype_kcount = {}	#每类微博的TOPK关键词
			mtype_weibo = {}	#三种类型的微博

			begin_ts = over_ts - during * i
			end_ts = begin_ts + during
			mtype_count = compute_mtype_count(topic, begin_ts, end_ts,during)
		
			time_results.append([end_ts,mtype_count])

		save_results_es('time_results', topic, time_results, during)


def compute_mtype_count(topic, begin_ts, end_ts,during):
	all_mtype_dict = {}
	#print begin_ts,end_ts
	query_body = {
		'query':{
			'bool':{
				'must':[
					{'range':{
						'timestamp':{'gte': begin_ts, 'lt':end_ts}
					}},
					{'term':{'en_name':topic}}#topic}}  jln
				]
			}
		},
		'aggs' :{
			'all_interests':{
				'terms':{
					'field': 'message_type',
					'size': MTYPE_COUNT
				}
			}
		}
	}

	weibo_mtype_count = es_event.search(index=event_text, doc_type=event_text_type,body=query_body)\
						['aggregations']['all_interests']['buckets']
	print es_event,event_text,event_text_type
	print 'weibo_mtype_count:::::::::::::::::',weibo_mtype_count
	print begin_ts,end_ts,len(weibo_mtype_count)
	iter_mtype_dict = {}
	for mtype_item in weibo_mtype_count:
		mtype = mtype_item['key']
		mtype_count = mtype_item['doc_count']
		try:
			iter_mtype_dict[mtype] += mtype_count
		except:
			iter_mtype_dict[mtype] = mtype_count

	return iter_mtype_dict

def getEsIndexName(topic_name):
	#body={"query": {"match_all": {}}}
	query_body = {
		'query':{
			'match':{
				'name': topic_name
			}
		}
	}
	try:
		res = es_event.search(index ='topics',body = query_body)['hits']['hits']
		return res[0]['_source']['index_name']
	except:
		return -1



def getTopicByName(topic):
	if topic == 'liyue':
		id = 0
	elif topic == 'laohu':
		id = 1
	else:
		id = -1
	return id

if __name__ == '__main__':
	'''
	#正式部分代码
	topic = sys.argv[1]
	start_date = sys.argv[2] # '2015-02-23'
	end_date = sys.argv[3] # '2015-03-02'
	'''

	#测试用代码
	topic = '奥运会'
	start_date = '2016-08-03'
	end_date = '2016-08-10'

	topic = topic.decode('utf-8')
	#topic_id = getTopicByName(topic)
	#topic_index_name = getEsIndexName(topic)
	topic_index_name = 'zui_gao_fa_di_zhi_yan_se_ge_ming'
	start_date = '2017-01-14'
	end_date = '2017-01-17'
	'''
	#话题id异常处理
	if topic_id == -1:
		print 'Topic Error'
		exit(-1)
	'''
	start_ts = datetime2ts(start_date)
	end_ts = datetime2ts(end_date)
	#得到es中相关微博
	#es_search_weibo = getEsWeiboByTopic(topic_index_name)

	print 'topic: ', topic.encode('utf-8'), 'from %s to %s' % (start_ts, end_ts)
	duration = Fifteenminutes
	propagateCronTopic(topic_index_name, start_ts, end_ts, during=duration)

	#print topic,start_date,end_date,start_ts,end_ts
	#print len(es_search_weibo)

#新建一个测试任务，跑这个代码