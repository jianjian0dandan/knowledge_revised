# -*-coding:utf-8-*-

from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch

user_profile_host = ["219.224.134.216:9201"]
user_portrait_host = ["219.224.134.225:9037"]#["219.224.134.225:9037"]
flow_text_host = ["219.224.134.216:9201"]
km_user_portrait_host = ["219.224.134.225:9037"]
user_portrait_port = "9200"
event_host = ["219.224.134.225:9037"]
event_port = "9200"
group_host = ["219.224.134.225:9037"]
special_event_host = ["219.224.134.225:9037"]
calculate_status_host=["219.224.134.225:9037"]
neo4j_host = "219.224.134.213"
neo4j_port = "7474"


# neo4j 索引(index)
node_index_name = "node_index" # primary_key: uid
topic_index_name = "topic_index" # primary_key: topic
domain_index_name = "domain_index" # primary_key: domain
location_index_name = "location_index" #primary_key: location
event_index_name = "event_index" # primary_key: event
org_index_name = "org_index" # primary_key: org_id
tag_index_name = "tag_index" # primary_key: tag
special_event_index_name = "special_event_index" # primary_key: event
group_index_name = "group_index" # primary_key: group
#neo4j node_type
people_node = "User"
org_node = "Org"
event_node = "Event"
special_event_node = "SpecialEvent"
group_node = "Group"
#neo4j node primary_key
people_primary = "uid"
org_primary = "org_id"
event_primary = "event_id"
special_event_primary = "event"
group_primary = "group"
# 港澳台，电信诈骗
event_type_index_name = "event_type_index" # primary: type
group_index_name = "group_index" # primary: group, rel: group


domain_list = [u'高校', u'境内机构', u'境外机构', u'媒体', u'境外媒体', u'民间组织', u'法律机构及人士', \
        u'政府机构及人士', u'媒体人士', u'活跃人士', u'草根', u'其他', u'商业人士']
topic_list = [u'文体类_娱乐', u'科技类', u'经济类', u'教育类', u'民生类_环保', \
        u'民生类_健康', u'军事类', u'政治类_外交', u'文体类_体育', u'民生类_交通', \
        u'其他类', u'政治类_反腐', u'民生类_就业', u'政治类_暴恐', u'民生类_住房', \
        u'民生类_法律', u'政治类_地区和平', u'政治类_宗教', u'民生类_社会保障']



# Relationship: User,Organization-Event
join = "join" # 参与事件
discuss = "discuss"#参与舆论
other_rel = "other_relationship" #其他关系

user_event_relation = ['join','discuss','other_relationship']

# Relationship: Event-Event
contain = "contain"  #--主题关联
event_other = 'event_other'#其他关系

event_special = "special_event" # 专题

event_relation_list = ['contain','event_other']


# Relatioship: User--User
friend = "friend" #交互
relative = "relative" #亲属
leader = "leader" #上下级关系
colleague = "colleague" #自述关联
ip_relation = "ip_relation" #IP关联
user_tag = "user_tag"#其他

user_user_relation = ['friend','relative','leader','colleague','ip_relation','user_tag']

# Relatioship: Organization--User,Organization
or_friend = "friend" #交互
or_colleague = "colleague" #业务关联
organization_tag = "organization_tag"#其他

organization_relation_list = ['friend','colleague','organization_tag']

group_rel = "group"

# For User Portrait Computing
ALL_PERSON_RELATION_LIST = ['friend','colleague','ip_relation']
ALL_VERIFIED_RELATION_LIST = ['friend','colleague']

# For Event Computing
ALL_EVENT_RELATION_LIST = ['join','discuss','contain']

WEIBO_ES_HOST = '219.224.134.216:9204'
weibo_es = Elasticsearch(WEIBO_ES_HOST,timeout=1000)
weibo_index_name = 'weibo'
weibo_index_type ='text'
topics_river_index_name='topics_river'
topics_river_index_type='text'
subopinion_index_type='text'
subopinion_index_name='subopinion'


#jln info_consume
mtype_kv = {'origin':1, 'comment': 2, 'forward':3}
emotions_kv = {'happy': 1, 'angry': 2, 'sad': 3, 'news': 4}
emotions_zh_kv = {'happy': '高兴', 'angry': '愤怒', 'sad': '悲伤', 'news': '新闻'}

#jln
SENTIMENT_TYPE_COUNT = 7
SENTIMENT_FIRST = ['0', '1', '7']
SENTIMENT_SECOND = ['2', '3', '4', '5', '6']
MAX_REPOST_SEARCH_SIZE = '100'
MAX_FREQUENT_WORDS = 100
MAX_LANGUAGE_WEIBO = 200
NEWS_LIMIT = 100



REDIS_CLUSTER_HOST_FLOW2 = '219.224.134.213'#'219.224.134.212'
REDIS_CLUSTER_PORT_FLOW2 = '6666'
#flow2用了
REDIS_HOST = '219.224.134.213'#'219.224.134.212'
REDIS_PORT = '6666'#'6381'
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

# use to identify the db number of redis-97
R_BEGIN_TIME = '2016-11-21'


ES_COPY_USER_PORTAIT_HOST = ["219.224.134.216:9201", "219.224.134.217:9201","219.224.134.218:9201"]
ES_CLUSTER_HOST_FLOW1 = ["219.224.134.216:9201", "219.224.134.217:9201","219.224.134.218:9201"]


# #mysql
# MYSQL_HOST = '219.224.134.225' 
# MYSQL_USER = 'root'
# MYSQL_DB = 'knowledge_management'

# SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@219.224.134.225/knowledge_management'
# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# Session = sessionmaker(bind=engine)
# # db = SQLAlchemy(app)

user_list = [-1,0,200,220,400]
auth_list = [1,2,3,4,5,6,7,8]

user_type ='user'
auth_type ='auth'

social_sensing_host = ["219.224.134.225:9037"]
social_sensing_text = ["219.224.134.225:9037"]
redis_host = "219.224.134.213"
redis_port = "7381"

portrait_name = "user_portrait_0312"
flow_text_index_name_pre = 'flow_text_'
portrait_type = "user"
flow_text_type = "text"

event_task_name = "event_task"#"event" # 事件基本信息
event_analysis_name = 'event_result'#"event_analysis" # 事件分析结果
event_text = "event_text"
event_text_type ="text"
event_task_type ="event"
event_type = "text"
neo4j_name = "neo4j"
neo4j_password = "Bh123456"
neo4j_data_path = 'http://219.224.134.213:7474/db/data'


group_name = 'group'
group_type = 'group'
special_event_name = 'speicial_event'
special_event_type = 'event'

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

#bci_
bci_es_host = ['219.224.134.216:9201']


#jln info_consume
mtype_kv = {'origin':1, 'comment': 2, 'forward':3}
emotions_kv = {'happy': 1, 'angry': 2, 'sad': 3, 'news': 4}
emotions_zh_kv = {'happy': '高兴', 'angry': '愤怒', 'sad': '悲伤', 'news': '新闻'}

#jln
SENTIMENT_TYPE_COUNT = 7
SENTIMENT_FIRST = ['0', '1', '7']
SENTIMENT_SECOND = ['2', '3', '4', '5', '6']
MAX_REPOST_SEARCH_SIZE = '100'
MAX_FREQUENT_WORDS = 100
MAX_LANGUAGE_WEIBO = 200
NEWS_LIMIT = 100


REDIS_CLUSTER_HOST_FLOW1 = '219.224.134.213'
REDIS_CLUSTER_HOST_FLOW1_LIST = ["219.224.134.211", "219.224.134.212", "219.224.134.213"]
REDIS_CLUSTER_PORT_FLOW1 = '6670'#'6379'
REDIS_CLUSTER_PORT_FLOW1_LIST = ["6379", "6380"]

#JLN for keyword find user
REDIS_KEYWORD_HOST = '219.224.134.222' #212(3-12)
REDIS_KEYWORD_PORT = '6381'
#flow2用了

# social sensing
index_sensing = "manage_sensing_task"
type_sensing = "task"
id_sensing = "social_sensing_task"
social_sensing_index_name = 'social_sensing_text'
social_sensing_index_type = 'text'

topic_value_dict = {"art": 1, "computer":2, "economic":7, "education":7.5, "environment":8.7, "medicine":7.8,"military":7.4, "politics":10, "sports":4, "traffic":6.9, "life":1.8, "anti-corruption":9.5, "employment":6, "fear-of-violence":9.3, "house":6.4, "law":8.6, "peace":5.5, "religion":7.6, "social-security":8.6}
zh_data = ['文体类_娱乐','科技类','经济类','教育类','民生类_环保','民生类_健康',\
                '军事类','政治类_外交','文体类_体育','民生类_交通','其他类',\
                        '政治类_反腐','民生类_就业','政治类_暴恐','民生类_住房','民生类_法律',\
                                '政治类_地区和平','政治类_宗教','民生类_社会保障']

name_list = ['art','computer','economic','education','environment','medicine',\
                'military','politics','sports','traffic','life',\
                        'anti-corruption','employment','fear-of-violence','house',\
                                'law','peace','religion','social-security']

#verified index
ver_data = {-1:'普通用户',0:'名人',1:'政府',2:'企业',3:'媒体',4:'校园',5:'网站',\
            6:'应用',7:'团体机构',8:'待审企业',200:'初级达人',220:'中高级达人',400:'已故V用户'}

TOPIC_ABS_PATH = "/home/ubuntu2/huxiaoqian/knowledge/knowledge_revised/knowledge/cron/model_file/topic"

DOMAIN_ABS_PATH = '/home/ubuntu2/huxiaoqian/knowledge/knowledge_revised/knowledge/cron/model_file/domain'

peo_list = [-1,0,200,220,400]
org_list = [1,2,3,4,5,6,7,8]
