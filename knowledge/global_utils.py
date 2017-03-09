# -*-coding:utf-8-*-

import redis
from py2neo import Graph
from elasticsearch import Elasticsearch
from global_config import *

# user profile info
es_user_profile = Elasticsearch(user_profile_host, timeout=600)
profile_index_name = "weibo_user"
profile_index_type = "user"

# user portrait system
es_user_portrait = Elasticsearch(user_portrait_host, timeout=600)

# flow text system
es_flow_text = Elasticsearch(flow_text_host, timeout=600)

# km user portrait
es_km_user_portrait = Elasticsearch(km_user_portrait_host,timeout=600)

# km event 
es_event = Elasticsearch(event_host, timeout=600)

# The process state is stored
es_calculate_status = Elasticsearch(calculate_status_host, timeout=600)

graph = Graph(neo4j_data_path, user=neo4j_name, password=neo4j_password)

r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

# user portrait interface: push user into redis list
r_user = redis.StrictRedis(host=redis_host, port=redis_port, db=10)

#jln  event redis
topic_queue_name='EVENT_portrait_task'

flow_text_index_name_pre = 'flow_text_' # flow text: 'flow_text_2013-09-01'
flow_text_index_type = 'text'

#neo4j查询事件名

# event2id
def event_name_to_id(en_name):
    query_body = {
        "query":{
            "match":{
                'name':en_name
            }
        }
    }
    name_results = es_event.search(index=event_name, doc_type=event_type, \
                body=query_body,fields=['en_name'])['hits']['hits'][0]['fields']
    for k,v in name_results.iteritems():
        ch_name = v[0]
    return ch_name

# event_search_sth
def es_search_sth(en_name,fields_list):
    print fields_list
    query_body = {
        "query":{
            "match":{
                'en_name':en_name
            }
        }
    }
    sth_results = es_event.search(index=event_analysis_name, doc_type=event_type, \
                body=query_body,fields=fields_list)['hits']['hits'][0]['fields']
    for k,v in sth_results.iteritems():
        sth_name = v[0]
    return sth_name

#es：事件id查找事件名
def event_name_search(en_name):
    query_body = {
        "query":{
            "match":{
                '_id':en_name
            }
        }
    }
    name_results = es_event.search(index=event_name, doc_type=event_type, \
                body=query_body,fields=['name'])['hits']['hits'][0]['fields']
    for k,v in name_results.iteritems():
        ch_name = v[0]
    return ch_name

#查找uid对应的字段
def user_search_sth(en_name,fields_list):
    query_body = {
        "query":{
            "match":{
                '_id':en_name
            }
        }
    }
    try:
        name_results = es_user_portrait.search(index=portrait_name, doc_type=portrait_type, \
                body=query_body, fields=fields_list)['hits']['hits'][0]['fields']
    except:
        name_dict = {}
        for i in fields_list:
            name_dict[i] =''
        return name_dict
    name_dict = {}
    for k,v in name_results.iteritems():
        name_dict[k] = v[0]
    # print ch_name.encode('utf-8')
    return name_dict

#查找uid对应的名字
def user_name_search(en_name):
    query_body = {
        "query":{
            "match":{
                '_id':en_name
            }
        }
    }
    try:
        name_results = es_user_portrait.search(index=portrait_name, doc_type=portrait_type, \
                body=query_body, fields=['uname'])['hits']['hits'][0]['fields']
    except:
        return ''
    for k,v in name_results.iteritems():
        ch_name = v[0]
    # print ch_name.encode('utf-8')
    return ch_name

#查找该专题下事件关联的用户信息,用户卡片
def related_user_search(uid_list,sort_flag):
    query_body = {
        'query':{
            'terms':{'uid':uid_list}
            },
        'size':200,
        "sort": [{sort_flag:'desc'}]
    }
    fields_list = ['activeness', 'influence','sensitive','uname','fansnum',\
                   'domain','topic_string','user_tag','uid','photo_url','activity_geo_aggs', 'statusnum']

    event_detail = es_user_portrait.search(index=portrait_name, doc_type=portrait_type, \
                body=query_body, _source=False, fields=fields_list)['hits']['hits']
    detail_result = []
    for i in event_detail:
        fields = i['fields']
        detail = dict()
        for i in fields_list:
            try:
                detail[i] = fields[i][0]
            except:
                detail[i] = 'null'
        detail_result.append(detail)
    return detail_result


# 查找该专题下的包含事件卡片信息，事件卡片
def event_detail_search(eid_list,sort_flag):
    query_body = {
        'query':{
            'terms':{'en_name':eid_list}
            },
        'size':100,
        "sort": [{sort_flag:'desc'}]
    }
    fields_list = ['name', 'en_name', 'weibo_counts','start_ts','location','uid_counts','user_tag','description','photo_url']

    event_detail = es_event.search(index=event_analysis_name, doc_type=event_type, \
                body=query_body, _source=False, fields=fields_list)['hits']['hits']
    detail_result = []
    for i in event_detail:
        fields = i['fields']
        detail = dict()
        for i in fields_list:
            try:
                detail[i] = fields[i][0]
            except:
                detail[i] = 'null'
        detail_result.append(detail)
    return detail_result



#jln
R_CLUSTER_FLOW1 = redis.StrictRedis(host=REDIS_CLUSTER_HOST_FLOW1, port=REDIS_CLUSTER_PORT_FLOW1)
R_CLUSTER_FLOW2 = redis.StrictRedis(host=REDIS_CLUSTER_HOST_FLOW2, port=REDIS_CLUSTER_PORT_FLOW2)
######
R_CLUSTER_FLOW3 = redis.StrictRedis(host=REDIS_CLUSTER_HOST_FLOW2, port=REDIS_CLUSTER_PORT_FLOW2)


def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1):
    return redis.StrictRedis(host, port, db)
redis_flow_text_mid = _default_redis(host=REDIS_TEXT_MID_HOST, port=REDIS_TEXT_MID_PORT, db=2)

redis_host_list = ["1", "2"]
#use to save retweet/be_retweet
retweet_r_1 = _default_redis(host=RETWEET_REDIS_HOST,port=RETWEET_REDIS_PORT, db=1)
retweet_r_2 = _default_redis(host=RETWEET_REDIS_HOST, port=RETWEET_REDIS_PORT, db=2)
retweet_redis_dict = {'1':retweet_r_1, '2':retweet_r_2}
#use to save comment/be_comment
comment_r_1 = _default_redis(host=COMMENT_REDIS_HOST, port=COMMENT_REDIS_PORT, db=1)
comment_r_2 = _default_redis(host=COMMENT_REDIS_HOST, port=COMMENT_REDIS_PORT, db=2)
comment_redis_dict = {'1':comment_r_1, '2':comment_r_2}
#use to save network retweet/be_retweet
daily_retweet_redis = _default_redis(host=REDIS_CLUSTER_HOST_FLOW1,port=REDIS_CLUSTER_PORT_FLOW1,db=4)


R_0 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
R_1 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
R_2 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=2)
R_3 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=3)
R_4 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
R_5 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
R_6 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=6)
R_7 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=7)
R_8 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=8)
R_9 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=9)
R_10 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=10)
R_11 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=11)
#bci_history jln
R_12 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=12)

R_DICT = {'0':R_0, '1':R_1, '2':R_2, '3':R_3, '4':R_4, '5':R_5, '6':R_6, '7':R_7,\
          '8':R_8, '9':R_9, '10':R_10, '11':R_11, '12':R_12}

R_SENTIMENT_ALL = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=11)
#use to save user domain in user_portrait
R_DOMAIN = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=12)
r_domain_name = 'user_domain'
#use to save user topic in user_portrait
R_TOPIC = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=13)
r_topic_name = 'user_topic'
#use to save domain sentiment trend
R_DOMAIN_SENTIMENT = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=12)
r_domain_sentiment_pre = 'sentiment_domain_'
#use to save topic sentiment trend
R_TOPIC_SENTIMENT = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=13)
r_topic_sentiment_pre = 'sentiment_topic_'



#use to save sentiment keywords task information to redis queue
R_SENTIMENT_KEYWORDS = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=10)
r_sentiment_keywords_name = 'sentiment_keywords_task'


#use to save sentiment keywords task information to redis queue
R_NETWORK_KEYWORDS = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=10)
r_network_keywords_name = 'network_keywords_task'

# social sensing redis
R_SOCIAL_SENSING = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=14)

topic_queue_name = 'topics_task'
#jln   add topic computing in db15
R_ADMIN = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=15)

#use to write portrait user list to redis as queue for update_day and update_week
update_day_redis = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
UPDATE_DAY_REDIS_KEY = 'update_day'
update_week_redis  = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
UPDATE_WEEK_REDIS_KEY = 'update_week'
update_month_redis = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
UPDATE_MONTH_REDIS_KEY = 'update_month'

'''
# elasticsearch initialize, one for user_profile, one for user_portrait
es_user_profile = Elasticsearch(USER_PROFILE_ES_HOST, timeout = 600)
es_bci_history = Elasticsearch(USER_PROFILE_ES_HOST, timeout=600)
es_sensitive = Elasticsearch(USER_PROFILE_ES_HOST, timeout=600)
es_user_portrait = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 6000)
es_social_sensing = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_prediction = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_flow_text = Elasticsearch(FLOW_TEXT_ES_HOST, timeout=600)
es_group_result = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout=1000)
es_retweet = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_comment = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_be_comment = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_copy_portrait = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_tag = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout=600)
es_sentiment_task = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_network_task = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_rank_task = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_operation = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout=600)

# elasticsearch index_name and index_type
profile_index_name = 'weibo_user'  # user profile es
profile_index_type = 'user'
portrait_index_name = 'user_portrait_1222' # user portrait
portrait_index_type = 'user'
flow_text_index_name_pre = 'flow_text_' # flow text: 'flow_text_2013-09-01'
flow_text_index_type = 'text'
# week retweet/be_retweet relation es
retweet_index_name_pre = '1225_retweet_' # retweet: 'retweet_1' or 'retweet_2'
retweet_index_type = 'user'
be_retweet_index_name_pre = '1225_be_retweet_' #be_retweet: 'be_retweet_1'/'be_retweet_2'
be_retweet_index_type = 'user'
# week comment/be_comment relation es
comment_index_name_pre = '1225_comment_'
comment_index_type = 'user'
be_comment_index_name_pre = '1225_be_comment_'
be_comment_index_type = 'user'
# es for activeness history, influence history and pagerank
#copy_portrait_index_name = 'user_portrait_1222'#'this_is_a_copy_user_portrait'
copy_portrait_index_name = 'this_is_a_copy_user_portrait'
copy_portrait_index_type = 'user'
# es for group detect and analysis
group_index_name = 'group_manage'
group_index_type = 'group'

# es for sentiment keywords task
sentiment_keywords_index_name = 'sentiment_keywords_task'
sentiment_keywords_index_type = 'sentiment'

# es for social sensing
sensing_index_name = 'manage_sensing_task'
sensing_doc_type = 'task'

#es for bci history
bci_history_index_name = 'bci_history'
bci_history_index_type = 'bci'

#es_sensitive
sensitive_index_name = 'sensitive_history'
sensitive_index_type = 'sensitive'

# 存储user_portrait的重要度/活跃度/影响力和敏感度，与es_flow1一致
ES_COPY_USER_PORTRAIT = _default_es_cluster_flow1(host=ES_COPY_USER_PORTAIT_HOST)
COPY_USER_PORTRAIT_INFLUENCE = "copy_user_portrait_influence"
COPY_USER_PORTRAIT_INFLUENCE_TYPE = 'bci'
COPY_USER_PORTRAIT_IMPORTANCE = "copy_user_portrait_importance"
COPY_USER_PORTRAIT_IMPORTANCE_TYPE = 'importance'
COPY_USER_PORTRAIT_ACTIVENESS = "copy_user_portrait_activeness"
COPY_USER_PORTRAIT_ACTIVENESS_TYPE = 'activeness'
COPY_USER_PORTRAIT_SENSITIVE = "copy_user_portrait_sensitive"
COPY_USER_PORTRAIT_SENSITIVE_TYPE = 'sensitive'
'''
'''
jln:query_to_es
2016.8.8
'''
def getTopicByNameStEt(topic,start_date,end_date):

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'start_ts':start_date}},
                    {'term':{'end_ts':end_date}},
                    {'term':{'name':topic}}
                ]
            }
        }
    }
    search_result = topic_es.search(index=topic_index_name,doc_type=topic_index_type,body=query_body)['hits']['hits']
    return search_result

def getWeiboByNameStEt(topic,start_date,end_date):
    print weibo_es
    query_body= {
        'query':{
            'filtered':{
                'filter':{
                    'range':{'timestamp':{'gte':start_date,'lte':end_date}}
                    }
            }
        }
    }
    search_result = weibo_es.search(index=topic,doc_type=weibo_index_type,body=query_body)
    print search_result
    return search_result
