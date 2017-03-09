#-*-coding:utf-8-*-
import sys,json
sys.path.append('../../')
#from global_utils import R_ADMIN as r
from global_utils import topic_queue_name,es_flow_text,flow_text_index_type,flow_text_index_name_pre
from global_config import weibo_es,weibo_index_name,weibo_index_type,topic_index_name,topic_index_type,\
                        MAX_FREQUENT_WORDS,MAX_LANGUAGE_WEIBO,NEWS_LIMIT
from flow_text_mappings import get_mappings
import datetime,time
from time_utils import ts2datetime
from elasticsearch.helpers import scan
import traceback
import redis,requests
from global_config import event_text,event_text_type

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

from geo.city_repost_search import repost_search
from geo.cron_topic_city import cityTopic
from network.cron_topic_identify import compute_network
from propagate.cron_topic_propagate import propagateCronTopic
from sentiment.cron_topic_sentiment import sentimentTopic
#from language.fix.count_keyword import count_fre

#from user_portrait.info_consume.topic_geo_analyze.utils import province_weibo_count
#from user_portrait.info_consume.topic_sen_analyze.utils import get_sen_time_count

from elasticsearch import Elasticsearch
zhishitupu_es=Elasticsearch('219.224.134.225:9037',timeout=1000)
redis_host = "219.224.134.213"
redis_port = "7381"
r=redis.StrictRedis(host=redis_host, port=redis_port, db=10)


def compute_topic_task():
    print time.time()
    while  True:
        #print r.rpop(topic_queue_name)
        task = r.rpop('event_portrait_task')
        #if not task:
	    #   break
        if  task:
	        continue
        else:
           # task = json.loads(task)
            task=['雾霾','type','1480003100','1480176000','1483500427743']
            topic = task[0]#['name']
            #en_name = task['en_name']
            start_ts = int(task[2])  #timestamp
            end_ts = int(task[3])   #timestamp
            submit_ts = int(task[4])
            try:
                keywords = task['keywords']
            except:
                keywords = ''
            #comput_status = task['status']

            task_id = 'event-'+str(start_ts)+'-'+str(end_ts)+'-'+str(submit_ts)
            en_name = task_id
            t1=time.time()
            exist_flag = exist(task_id)
            #keywords=keywords.split('&')
            get_topic_weibo(topic,task_id,start_ts,end_ts,keywords)
            print exist_flag
            if exist_flag:
                #start compute
                #try:
                weibo_counts,uid_counts=counts(start_ts,end_ts,topic,en_name,keywords)
                count_fre(en_name, start_ts=start_ts, over_ts=end_ts,news_limit=NEWS_LIMIT,weibo_limit=MAX_LANGUAGE_WEIBO)




                weibo_es.index(index='topics',doc_type='text',id=task_id,body={'name':topic,'start_ts':start_ts,'end_ts':end_ts,'submit_ts':submit_ts,'comput_status':0,'en_name':task_id})
                weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':-1,'weibo_counts':weibo_counts,'uid_counts':uid_counts}})
                print 'finish change status'
                #geo
                
                repost_search(en_name, start_ts, end_ts)
                weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':-2}})
                print 'finish geo_1 analyze'
                cityTopic(en_name, start_ts, end_ts)
                weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':-3}})
                print 'finish geo analyze'
                #language
                count_fre(en_name, start_ts=start_ts, over_ts=end_ts,news_limit=NEWS_LIMIT,weibo_limit=MAX_LANGUAGE_WEIBO)
                weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':-4}})
                print 'finish language analyze'
                #time
                propagateCronTopic(en_name, start_ts, end_ts)
                weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':-5}})
                print 'finish time analyze'

                #network
                compute_network(en_name, start_ts, end_ts)
                weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':-6}})
                print 'finish network analyze'

                #sentiment
                sentimentTopic(en_name, start_ts=start_ts, over_ts=end_ts)
                print 'finish sentiment analyze'
                #finish compute

                print weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'comput_status':1,'finish_ts':int(time.time())}})
                save_to_es(task_id,start_ts,end_ts,submit_ts,weibo_counts,uid_counts)
                print 'finish change status done'
            break
        t2=time.time()-t1
        print task_id,t2
                # except:
                #   raise
                #   break
                #get_attr(en_name, start_ts, end_ts)
            # else:
            #     pass

def exist(task_id):
    #print task_id
    try:
        task_exist = zhishitupu_es.get(index='event_status',doc_type='text',id=task_id)['_source']
    except:
        task_exist = {}
    if not task_exist:
        return False
    else:
        return True

def get_topic_weibo(topic,en_name,start_ts,end_ts,keywords):
    query_body = {'query':{'match_all':{}},'sort':'timestamp','size':1}
    try:
        task_exist = weibo_es.search(index=en_name,doc_type=topic_index_type,body=query_body)['hits']['hits']
    except:
        get_mappings(en_name)
    find_flow_texts_scan(start_ts,end_ts,topic,en_name,keywords)


def find_flow_texts(start_ts,end_ts,topic,en_name,keywords):   #多个wildcard/时间戳的range
    # if RUN_TYPE == 1:
    #     today = datetime.date.today() 
    # else:
    #     today = datetime.date(2016,05,23)
    keywords_list = []
    for i in keywords:
    	keywords_list.append({'query':{'wildcard':{'text':'*'+i+'*'}}})
    index_names = get_day_zero(start_ts,end_ts)
    query_body = {'query':{'bool':{'must':keywords_list}}}
    print index_names
    result = []
    index_list = []
    for index_name in index_names:
        index_list.append(flow_text_index_name_pre+index_name)
    result = es_flow_text.search(index=index_list,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
    print flow_text_index_name_pre+index_name,es_flow_text,len(result)
    if result:
        save_es(en_name,result)

def find_flow_texts_scan(start_ts,end_ts,topic,en_name,keywords):
    index_names = get_day_zero(start_ts,end_ts)
    if len(keywords) ==0:
        query_body = {'query':{'wildcard':{'text':'*'+topic+'*'}}}
    else:
    #keywords_list = [{'wildcard':{'text':'*'+topic+'*'}}]
        keywords_list = []
        for i in keywords:
            print i
            keywords_list.append({'wildcard':{'text':'*'+i+'*'}})
        query_body = {'query':{'bool':{'should':keywords_list,'minimum_should_match':'60%'}}}
    
    print query_body
    result = []
    index_list = []
    for index_name in index_names:
        index_list.append(flow_text_index_name_pre+index_name)
    s_re = scan(es_flow_text,index=index_list,doc_type=flow_text_index_type,query=query_body)
    bulk_action = []
    count = 0
    tb = time.time()
    while True:
        try:
            if count > 5000:
                break
            scan_re = s_re.next()
            _id = scan_re['_id']
            source = scan_re['_source']
            source['en_name'] = en_name
            action = {"index":{"_id":_id}}
            bulk_action.extend([action, source])
	    count += 1
	    if count % 1000 == 0:
	        weibo_es.bulk(bulk_action, index=event_text, doc_type=event_text_type, timeout=100)
	        bulk_action = []
	        print count
                if count % 10000 == 0:
	    	    te = time.time()
	    	    print "index 10000 per %s second" %(te - tb)
	    	    tb = te
	except StopIteration:
            print "all done"
    if bulk_action:
        weibo_es.bulk(bulk_action, index=event_text, doc_type=event_text_type, timeout=100)

    return 1


def counts(start_ts,end_ts,topic,en_name,keywords):
    index_names = get_day_zero(start_ts,end_ts)   
    if len(keywords) ==0:
        query_body = {'query':{'wildcard':{'text':'*'+topic+'*'}}}
    #keywords_list = [{'wildcard':{'text':'*'+topic+'*'}}]
    else:
        keywords_list = []
        for i in keywords:
            print i
            keywords_list.append({'wildcard':{'text':'*'+i+'*'}})
        
        query_body = {'query':
            			{'bool':
            				{'should':keywords_list,
            				'minimum_should_match':'60%'}}
            	     }
    query_body['aggs']={'diff_uids':{'cardinality':{'field':'uid'}}}
    print query_body
    result = []
    index_list = []
    weibo_count = 0
    for index_name in index_names:
        index_list.append(flow_text_index_name_pre+index_name)
    #result = es_flow_text.count(index=index_list,doc_type=flow_text_index_type,body=query_body)['count']
    result = es_flow_text.search(index=index_list,doc_type=flow_text_index_type,body=query_body)
    #print result
    weibo_counts=result['hits']['total']
    uid_counts=result['aggregations']['diff_uids']['value']

    #task_id = str(start_ts)+'_'+str(end_ts)+'_'+en_name+'_'+submit_user
    #print weibo_es.update(index=topic_index_name,doc_type=topic_index_type,id=task_id,body={'doc':{'weibo_counts':weibo_counts,'uid_counts':uid_counts}})
    return  result['hits']['total'],result['aggregations']['diff_uids']['value']

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
                tb = ts
    print "all done"
    if bulk_action:
        weibo_es.bulk(bulk_action, index=en_name, doc_type=topic_index_type, timeout=100)
    return 1

def get_attr(en_name, start_ts, end_ts):
    during = end_ts-start_ts
    geo = province_weibo_count(en_name,start_ts,end_ts)
    sen = get_sen_time_count(en_name,start_ts,end_ts,during)
    weibo_count = weibo_es.count(index=en_name)


def save_to_es(task_id,start_ts,end_ts,submit_ts,weibo_counts,uid_counts):
    data = {'topic':task_id,'start_ts':start_ts,'end_ts':end_ts,'pointerval':21600}
    #rq = requests.get('http://219.224.134.225:9042')
    event_ip = '219.224.134.225:9042'
    '''
    #rq = requests.get('http://'+event_ip+'/topic_language_analyze/submit_task/',params=i)
    #    i['topic']=result['topic'][0]['en_name'] 
    #    sql_find=copy.deepcopy(i)
    #    sql_find['topic']=sql_find['topic'][:20]
    #    sql_find['pointInterval']=21600
    '''
    result = {'weibo_counts':weibo_counts,'uid_counts':uid_counts,'start_ts':start_ts,'en_name':task_id,'submit_ts':submit_ts}

    rq = requests.get('http://'+event_ip+'/topic_sen_analyze/sen_time_count/',params=data)
    result['sen_time_count'] = rq.text
    #print result['sen_time_count']
    rq = requests.get('http://'+event_ip+'/topic_geo_analyze/geo_weibo_count/',params=data)
    result['geo_weibo_count'] = rq.text
    rq = requests.get('http://'+event_ip+'/topic_language_analyze/topics_river/',params=data)
    result['topics_river'] = rq.text
    rq = requests.get('http://'+event_ip+'/topic_language_analyze/search_topic/',params={'keyword':data['topic']})
    result['topic'] = rq.text
    rq = requests.get('http://'+event_ip+'/topic_sen_analyze/sen_time_count/',params=data)
    result['sen_time_count'] = rq.text
    rq = requests.get('http://'+event_ip+'/topic_network_analyze/get_trend_maker/',params=data)
    result['trend_maker'] = rq.text
    rq = requests.get('http://'+event_ip+'/topic_network_analyze/get_trend_pusher/',params=data)
    result['trend_pusher'] = rq.text
    rq = requests.get('http://'+event_ip+'/topic_network_analyze/get_pagerank/',params=data)
    result['pagerank'] = rq.text
    rq = requests.get('http://'+event_ip+'/topic_time_analyze/time_order_weibos/',params=data)
    result['time_order_weibo'] = rq.text
    
    zhishitupu_es.index(index='event_analysis',doc_type='text',id=task_id,body=result)
    zhishitupu_es.update(index='event_status',doc_type='text',id=task_id,body={'doc':{'status':2}})


if __name__ == '__main__':
    zhishitupu_es.index(index='event_status',doc_type='text',id='event-1480003100-1480176000-1483500427743',body={'status':1,'start_time':'1480003100','end_time':'1480176000','event':'雾霾'})
    #counts('1480262400','1480867200','中国知识产权申请量世界第一','zhong-guo-zhi-shi-chan-quan-shen-qing-liang-shi-jie-di-yi-1482079340',['中国','知识产权','第一'],'admin')
    #counts('1480262400','1480867200','中国知识产权申请量世界第一','zhong-guo-zhi-shi-chan-quan-shen-qing-liang-shi-jie-di-yi-1482079340',['中国','知识产权','第一'],'admin')
    compute_topic_task()
    #print weibo_es.delete(index='topics',doc_type='text',body={'query':})
    #counts('1480262400','1480867200','中国知识产权申请量世界第一','zhongguo',['中国','知识产权','第一')
    #get_topic_weibo('画画','huahua','1377964800','1378137600')
    #weibo_count = weibo_es.count(index='aoyunhui')
    #print weibo_count
