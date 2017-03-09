# -*-coding:utf-8-*-

from elasticsearch import Elasticsearch

user_profile_host = ["219.224.134.216:9201"]
user_portrait_host = ["219.224.134.212:9037"]
flow_text_host = ["219.224.134.216:9201"]
km_user_portrait_host = ["219.224.134.212:9037"]
user_portrait_port = "9200"
event_host = ["219.224.134.212:9037"]
event_port = "9200"
calculate_status_host=["219.224.134.212:9037"]
neo4j_host = "219.224.134.213"
neo4j_port = "7474"
redis_host = "219.224.134.213"
redis_port = "7381"

profile_index_name = "weibo_user"
profile_index_type = "user"
remote_portrait_name = "user_portrait_1222" # user portrait system
portrait_name = "user_portrait"
flow_text_name = "flow_text_2016-11-26"
portrait_type = "user"
flow_text_type = "text"
event_name = "event_task"#"event" # 事件基本信息
event_analysis_name = 'event_result'#"event_analysis" # 事件分析结果
event_text = "event_text"
event_text_type ="text"
event_type = "text"
neo4j_name = "neo4j"
neo4j_password = "database"
neo4j_data_path = 'http://219.224.134.213:7474/db/data'

# retweet&comment for test
retweet_comment_es_host = ['219.224.134.216:9201']
retweet_comment_port = "9201"
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

# neo4j 索引(index)
node_index_name = "node_index" # primary_key: uid
topic_index_name = "topic_index" # primary_key: topic
domain_index_name = "domain_index" # primary_key: domain
location_index_name = "location_index" #primary_key: location
event_index_name = "event_index" # primary_key: event
tag_index_name = "tag_index" # primary_key: tag
special_event_index_name = "special_event_index" # primary_key: event
# 港澳台，电信诈骗
event_type_index_name = "event_type_index" # primary: type
group_index_name = "group_index" # primary: group, rel: group


domain_list = [u'高校', u'境内机构', u'境外机构', u'媒体', u'境外媒体', u'民间组织', u'法律机构及人士', \
        u'政府机构及人士', u'媒体人士', u'活跃人士', u'草根', u'其他', u'商业人士']
topic_list = [u'文体类_娱乐', u'科技类', u'经济类', u'教育类', u'民生类_环保', \
        u'民生类_健康', u'军事类', u'政治类_外交', u'文体类_体育', u'民生类_交通', \
        u'其他类', u'政治类_反腐', u'民生类_就业', u'政治类_暴恐', u'民生类_住房', \
        u'民生类_法律', u'政治类_地区和平', u'政治类_宗教', u'民生类_社会保障']



# Relationship: User-Event
join = "join" # 参与讨论
pusher = "pusher"#趋势推动
maker = "maker"#趋势制造
other_rel = "other_relationship" #其他关系

user_event_relation = ['join','pusher','maker','other_relationship']

# Relationship: Event-Event
contain = "contain"  #--主题关联
event_other = 'event_other'#其他关系

event_special = "special_event" # 专题

event_relation_list = ['contain','event_other']


# Relatioship: User、Organization--User
friend = "friend" #交互
relative = "relative" #亲属（人与人的关系）
colleague = "colleague" #业务关联
user_tag = "user_tag"#其他

relation_list = ['friend','relative','colleague','user_tag']

group_rel = "group"

#机构和机构没有关系，

#jln:for getTopicByNameStEt
TOPIC_ES_HOST = '219.224.134.216:9204'
topic_es = Elasticsearch(TOPIC_ES_HOST,timeout=1000)
topic_index_name = 'topics'
topic_index_type ='text'

WEIBO_ES_HOST = '219.224.134.216:9204'
weibo_es = Elasticsearch(WEIBO_ES_HOST,timeout=1000)
weibo_index_name = 'weibo'
weibo_index_type ='text'
topics_river_index_name='topics_river'
topics_river_index_type='text'
subopinion_index_type='text'
subopinion_index_name='subopinion'

#jln
SENTIMENT_TYPE_COUNT = 7
SENTIMENT_FIRST = ['0', '1', '7']
SENTIMENT_SECOND = ['2', '3', '4', '5', '6']
MAX_REPOST_SEARCH_SIZE = '100'
MAX_FREQUENT_WORDS = 100
MAX_LANGUAGE_WEIBO = 200
NEWS_LIMIT = 100



REDIS_CLUSTER_HOST_FLOW1 = '219.224.134.212'
REDIS_CLUSTER_HOST_FLOW1_LIST = ["219.224.134.211", "219.224.134.212", "219.224.134.213"]
REDIS_CLUSTER_PORT_FLOW1 = '6669'#'6379'
REDIS_CLUSTER_PORT_FLOW1_LIST = ["6379", "6380"]
REDIS_CLUSTER_HOST_FLOW2 = '219.224.134.212'
REDIS_CLUSTER_PORT_FLOW2 = '6666'
#JLN for keyword find user
REDIS_KEYWORD_HOST = '219.224.134.212'
REDIS_KEYWORD_PORT = '6381'
#flow2用了
REDIS_HOST = '219.224.134.212'#'219.224.134.212'
REDIS_PORT = '6670'#'6381'
#uname to uid 
UNAME2UID_HOST = '219.224.134.211'
UNAME2UID_PORT = '7381'
# uname2uid in redis: {'weibo_user': {uname:uid, ...}}
UNAME2UID_HASH = 'weibo_user'
REDIS_TEXT_MID_HOST = '219.224.134.211' # 注意；和redis flow1的host/port相同
REDIS_TEXT_MID_PORT = '7381'
#flow3:retweet/be_retweet redis
RETWEET_REDIS_HOST = '219.224.134.215'#'219.224.134.212'
RETWEET_REDIS_PORT = '6667'#'6381'
#flow3:comment/be_comment redis
COMMENT_REDIS_HOST = '219.224.134.215'#'219.224.134.212'
COMMENT_REDIS_PORT = '6668'
ZMQ_VENT_PORT_FLOW1 = '6387'
ZMQ_CTRL_VENT_PORT_FLOW1 = '5585'
ZMQ_VENT_HOST_FLOW1 = '219.224.134.213'
ZMQ_CTRL_HOST_FLOW1 = '219.224.134.213'

ZMQ_VENT_PORT_FLOW2 = '6388'
ZMQ_CTRL_VENT_PORT_FLOW2 = '5586'

ZMQ_VENT_PORT_FLOW3 = '6389'
ZMQ_CTRL_VENT_PORT_FLOW3 = '5587'

ZMQ_VENT_PORT_FLOW4 = '6390'
ZMQ_CTRL_VENT_PORT_FLOW4 = '5588'

ZMQ_VENT_PORT_FLOW5 = '6391'
ZMQ_CTRL_VENT_PORT_FLOW5 = '5589'

#use to save txt file
WRITTEN_TXT_PATH = '/home/ubuntu2/txt'
REPLICA_BIN_FILE_PATH = '/home/ubuntu2/txt'

# csv file path
'''
BIN_FILE_PATH = '/home/ubuntu8/yuankun/data' # '219.224.135.93:/home/ubuntu8/yuankun'
'''
BIN_FILE_PATH = '/home/ubuntu2/txt'

# first part of csv file1

FIRST_FILE_PART = 'MB_QL_9_7_NODE'
