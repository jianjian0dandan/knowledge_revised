#-*-coding:utf-8-*-
import sys,json
sys.path.append('./knowledge')
sys.path.append('./knowledge/cron')
sys.path.append('../../')

#from global_utils import R_ADMIN as r
from global_utils import es_event,topic_queue_name,es_flow_text,flow_text_index_type,flow_text_index_name_pre
from global_config import event_task_name,event_task_type,event_analysis_name,event_type
from global_config import MAX_FREQUENT_WORDS,MAX_LANGUAGE_WEIBO,NEWS_LIMIT
from flow_text_mappings import get_mappings
import datetime,time
from time_utils import ts2datetime
from elasticsearch.helpers import scan
import traceback
import redis,requests
from global_utils import event_text,event_text_type
import re
from parameter import RUN_TYPE
from sys import argv
#from geo.city_repost_search import repost_search
from geo.cron_topic_city import cityTopic
#from network.cron_topic_identify import compute_network
from propagate.cron_topic_propagate import propagateCronTopic
from sentiment.cron_topic_sentiment import sentimentTopic
from language.cron_topic_language import compute_real_info
sys.path.append('../')
from get_relationship.event_relationship import event_input
from global_utils import event_node,event_primary,event_index_name

from manage_neo4j.neo4j_relation import nodes_rels,create_person
from elasticsearch import Elasticsearch
from global_config import redis_host,redis_port,contain
# "219.224.134.213"
# "7381"
r=redis.StrictRedis(host=redis_host, port=redis_port, db=10)


def get_task():
    #加个结束时间大于当前时间的判断  要不要更新
    query_body = {'query':{'term':{'compute_status':0}},'sort':{'submit_ts':{'order':'asc'}},'size':100000}
    result = es_event.search(index=event_task_name,doc_type=event_task_type,body=query_body)
    return result['hits']['hits']

def continue_compute():
    ts = time.time()
    query_body = {'query':{'term':{'range':{'end_ts':{'gte':time.time()}}}},'sort':{'submit_ts':{'order':'asc'}},'size':100000}
    result = es_event.search(index=event_task_name,doc_type=event_task_type,body=query_body)
    return result['hits']['hits']


def immediate_compute(task_id):
    # try:
    task = es_event.get(index=event_task_name,doc_type=event_task_type,id=task_id)
    compute_task(task)
    # except:
        # return None


def compute_topic_task():
    print time.time()
    tasks = get_task()
    print 'len tasks:',len(tasks)
    if not tasks:
        return None
    for task in tasks:
        if RUN_TYPE == 0:
            compute_task(task)
        else:
            ts = time.time()
            if ts > task['_source']['end_ts']:
                continue
            else:
                compute_task(task)



def compute_task(task):
    print task
    # task=['雾霾','type','1480003100','1480176000','1483500427743']
    task_id = task['_id']
    task = task['_source']
    topic = task['name']#task[0]#['name']
    #en_name = task['en_name']
    RUN_TYPE = 1
    if RUN_TYPE == 0:
        start_ts = 1480003200#task['start_ts']
        begin_ts = 1480003200
        end_ts = 1480176000#task['end_ts']
    else:
        start_ts = task['start_ts']
        begin_ts = task['start_ts']
        end_ts = task['end_ts']

    try:
        start_ts = task['compute_ts']
        task['compute_ts'] = time.time()
    except:
        task['compute_ts'] = time.time()

    if end_ts > time.time():
        end_ts = time.time()
    submit_ts = task['submit_ts']#int(task[4])
    #可选的计算关系realtion  用&连接的字符串
    relation = task['relation_compute']#task[5]  

    keywords = task['keywords'].split('&')    #关键词或者mid
    #compute_status = task['status']
    # mid = task['mid']
    # task_id = 'event-'+str(start_ts)+'-'+str(end_ts)+'-'+str(submit_ts)
    en_name = task_id
    t1=time.time()
    re_mid = re.compile('^\d{16}$')
    try:
        mid = re.match(re_mid,task_id).group()
    except:
        mid = ''
    exist_flag = exist(task_id)
    get_topic_weibo(topic,task_id,start_ts,end_ts,keywords,mid)
    print exist_flag
    if exist_flag:
        #start compute
        #try:

        resu = create_person(event_node,event_primary,en_name,event_index_name)
        if resu == 'Node Wrong':
            return 'Node Wrong'
        weibo_counts,uid_counts=counts(start_ts,end_ts,topic,en_name,keywords)

        es_event.update(index=event_task_name,doc_type=event_task_type,id=task_id,body={'doc':{'compute_status':-1}})

        # es_event.index(index=event_analysis_name,doc_type=event_type,id=task_id,body={'name':topic,'start_ts':start_ts,'end_ts':end_ts,'submit_ts':submit_ts,'compute_status':0,'en_name':task_id,'relation_compute':relation})
        task['compute_status']=-1
        task['weibo_counts']=weibo_counts
        task['uid_counts']=uid_counts
        try:
            flag = es_event.get(index=event_analysis_name,doc_type=event_type,id=task_id)['_source']
            w_counts = flag['weibo_counts']+weibo_counts
            u_counts = flag['uid_counts']+uid_counts
            es_event.update(index=event_analysis_name,doc_type=event_type,id=task_id,body={'doc':{'compute_status':-1,'weibo_counts':w_counts,'uid_counts':u_counts}})
        except:
            es_event.index(index=event_analysis_name,doc_type=event_type,id=task_id,body=task)
            es_event.update(index=event_analysis_name,doc_type=event_type,id=task_id,body={'doc':{'hashtag_dict':'','topics':'','geo_results':'','real_geo':'','real_auth':'','sentiment_results':'','time_results':'','hashtag':'','real_time':'','user_results':'','real_person':'','keywords_list:''}})

        print 'finish change status'
        
        if es_event.get(index=event_analysis_name,doc_type=event_type,id=task_id)['_source']['weibo_counts'] == 0:
            return 1

        #geo
        
        cityTopic(en_name, start_ts, end_ts)
        es_event.update(index=event_analysis_name,doc_type=event_type,id=task_id,body={'doc':{'compute_status':-2}})
        print 'finish geo analyze'
        #language
        compute_real_info(en_name, begin_ts, end_ts,relation,task['submit_user'],task['submit_ts'])
        es_event.update(index=event_analysis_name,doc_type=event_type,id=task_id,body={'doc':{'compute_status':-3}})
        print 'finish language analyze'
        #time
        propagateCronTopic(en_name, start_ts, end_ts)
        es_event.update(index=event_analysis_name,doc_type=event_type,id=task_id,body={'doc':{'compute_status':-4}})
        print 'finish time analyze'

        
        #sentiment
        sentimentTopic(en_name, start_ts=start_ts, over_ts=end_ts)
        print 'finish sentiment analyze'
        #finish compute

        print es_event.update(index=event_analysis_name,doc_type=event_type,id=task_id,body={'doc':{'compute_status':1,'finish_ts':int(time.time())}})
        print 'finish change status done'
        print time.time()
        
        if('contain' in relation.split('&')):
            #计算关系
            related_event_ids = event_input(keywords,en_name)
            rel_list = []
            for i in related_event_ids:
                create_person(event_node,event_primary,i,event_index_name)
                rel_list.append([[2,en_name],'contain',[2,i]])
            nodes_rels(rel_list)

        es_event.update(index=event_task_name,doc_type=event_task_type,id=task_id,body={'doc':{'compute_status':1}})


    
    t2=time.time()-t1
    print task_id,t2
            # except:
            #   raise
            #   break
            #get_attr(en_name, start_ts, end_ts)
        # else:
        #     pass
    return 1

def exist(task_id):
    #print task_id
    try:
        task_exist = es_event.get(index=event_task_name,doc_type=event_task_type,id=task_id)['_source']
    except:
        task_exist = {}
    if not task_exist:
        return False
    else:
        return True

def get_topic_weibo(topic,en_name,start_ts,end_ts,keywords,mid):
    query_body = {'query':{'match_all':{}},'sort':'timestamp','size':1}
    try:
        task_exist = es_event.search(index=en_name,doc_type=event_type,body=query_body)['hits']['hits']
    except:
        get_mappings(en_name)
    find_flow_texts_scan(start_ts,end_ts,topic,en_name,keywords,mid)


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

def find_flow_texts_scan(start_ts,end_ts,topic,en_name,keywords,mid):
    index_names = get_day_zero(start_ts,end_ts)
    #mid = re.compile('^\d{16}$')
    if len(keywords) ==0 and len(mid)==0:
        query_body = {'query':{'wildcard':{'text':'*'+topic+'*'}},'size':100000}
    elif len(mid) == 16:
    #elif len(mid.findall(keywords))>0:
        # query_body = {'query':{'term':{'root_mid':mid}}}
        query_body = {'query':{'bool':{'should':[{'term':{'root_mid':mid}},{'term':{'mid':mid}}]}},'size':100000}
    else:
    #keywords_list = [{'wildcard':{'text':'*'+topic+'*'}}]
        keywords_list = []
        for i in keywords:
            print i
            # keywords_list.append({'wildcard':{'text':'*'+i+'*'}})
            # keywords_list.append({'term':{'keywords_string':i}})
            keywords_list.append({'wildcard':{'keywords_string':'*'+i+'*'}})

        query_body = {'query':{'bool':{'should':keywords_list,'minimum_should_match':'70%'}},'size':100000}
        if len(keywords)==2:
            query_body = {'query':{'bool':{'should':keywords_list,'minimum_should_match':2}},'size':100000}


    print query_body
    result = []
    index_list = []
    for index_name in index_names:
        index_list.append(flow_text_index_name_pre+index_name)
    for i in index_list:
        try:
            result = es_flow_text.search(index=i,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
            print i,es_flow_text,len(result)
            if result:
                save_es(en_name,result)
        except:
            continue


def counts(start_ts,end_ts,topic,en_name,keywords):
    query_body = {   
        'query':{
            'match_all':{}
            # 'term':{'en_name':topic}
        },
        'aggs':{'diff_uids':{'cardinality':{'field':'uid'}}},
        'size':999999
    }
    result = []
    index_list = []
    weibo_count = 0
    print es_event,en_name,event_text_type,query_body
    result = es_event.search(index=en_name ,doc_type=event_text_type,body=query_body)
    #print result
    weibo_counts=result['hits']['total']
    uid_counts=result['aggregations']['diff_uids']['value']
    print weibo_counts,uid_counts
    #task_id = str(start_ts)+'_'+str(end_ts)+'_'+en_name+'_'+submit_user
    #print es_event.update(index=event_analysis_name,doc_type=event_type,id=task_id,body={'doc':{'weibo_counts':weibo_counts,'uid_counts':uid_counts}})
    return  weibo_counts,uid_counts


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
        source['en_name'] = en_name
        action = {'index':{'_id':weibos['_id']}}
        bulk_action.extend([action,source])
        count += 1
        if count % 1000 == 0:
            es_event.bulk(bulk_action, index=en_name, doc_type=event_type, timeout=100)
            bulk_action = []
            print count
            if count % 10000 == 0:
                te = time.time()
                print "index 10000 per %s second" %(te - tb)
                tb = te
    print "all done"
    if bulk_action:
        es_event.bulk(bulk_action, index=en_name, doc_type=event_type, timeout=100)
    return 1

def get_attr(en_name, start_ts, end_ts):
    during = end_ts-start_ts
    geo = province_weibo_count(en_name,start_ts,end_ts)
    sen = get_sen_time_count(en_name,start_ts,end_ts,during)
    weibo_count = es_event.count(index=en_name)


def uid_diff():
    s_re = scan(es_event,index='user_portrait_0312',doc_type='user')
    uid_list = set()
    while True:
        try:
            scan_re = s_re.next()
            uid_list.add(scan_re['_id'])
        except:
            print len(uid_list)
            break
    result = es_event.get(index='event_result',doc_type='text',id='bei-jing-fang-jia-zheng-ce-1480176000')['_source']
    event_uid = set(json.loads(result['user_results']).keys())
    print len(event_uid)
    print uid_list - event_uid
    print event_uid - uid_list

if __name__ == '__main__':
    # es_event.index(index='event_status',doc_type='text',id='event-1480003100-1480176000-1483500427743',body={'status':1,'start_time':'1480003100','end_time':'1480176000','event':'雾霾'})
    #counts('1480262400','1480867200','中国知识产权申请量世界第一','zhong-guo-zhi-shi-chan-quan-shen-qing-liang-shi-jie-di-yi-1482079340',['中国','知识产权','第一'],'admin')
    #counts('1480262400','1480867200','中国知识产权申请量世界第一','zhong-guo-zhi-shi-chan-quan-shen-qing-liang-shi-jie-di-yi-1482079340',['中国','知识产权','第一'],'admin')
    #compute_topic_task()
    # print es_event.delete(index='event_result',doc_type='text',id='bei-jing-fang-jia-zheng-ce-1480176000')
    #counts('1480262400','1480867200','中国知识产权申请量世界第一','zhongguo',['中国','知识产权','第一')
    #get_topic_weibo('画画','huahua','1377964800','1378137600')
    #weibo_count = es_event.count(index='aoyunhui')
    #print weibo_count
    # counts(1484323200,1484582400,'zui_gao_fa_di_zhi_yan_se_ge_ming','zui_gao_fa_di_zhi_yan_se_ge_ming','zui_gao_fa_di_zhi_yan_se_ge_ming')
    # es_event.delete(index='event_task',doc_type='event',id='4045701413449427')
    # es_event.index(index='event_task',doc_type='event',id='4045701413449427',body={'name':'test_task','start_ts':1480003200,'end_ts':1480176000,'submit_ts':1480089600,'compute_status':0,'en_name':'4045701413449427','relation_compute':'join&discuss&contain','event_type':'娱乐','keywords':'张杰跳&深圳&落地&这是&来吧&热浪','submit_user':'jln','recommend_style':'jln','immediate_compute':0})
    # compute_topic_task()
    if argv[1] == 'imme':   #python event_compute.py imme task_id
        task_id = argv[2]
        immediate_compute(task_id)
    else:
        compute_topic_task() #python event_compute.py ontime
