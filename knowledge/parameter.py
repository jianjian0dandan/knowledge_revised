# -*-coding:utf-8-*-

from global_config import *

RUN_TYPE = 0

# 关系类型与后续节点primary key的关系

rel_node_mapping = {join: "event_id", other_rel: "event_id", \
        group_rel: "group", contain: "event_id", event_special:"event_id", \
        friend: "uid", relative: "uid", colleague: "uid", user_tag: "uid", \
        "domain": "domain", "topic": "topic", "location": "location", "event":"event_id"}


# rel_node_type_mapping = {join: "Event", other_rel: "Event", \
#         group_rel: "Group", contain: "Event", event_special:"SpecialEvent", \
#         friend: "User", relative: "User", colleague: "User", user_tag: "Tag", \
#         "domain": "Domain", "topic": "Topic", "location": "Location", "event": "Event"}



# 首页显示最多节点数
index_threshold = 500


CHARACTER_TIME_GAP = 7

WEIBO_API_INPUT_TYPE = 1 # 1 mark: need compute sentiment

DAY = 24*3600
RUN_TEST_TIME  = '2016-11-27'
Fifteen = 60 * 15
HALF_HOUR = 1800
FOUR_HOUR = 3600*4
MAX_VALUE = 99999999
WEEK = 7
WEEK_TIME = 7*24*3600
MONTH = 30
MONTH_TIME = 30*24*3600
EXPIRE_TIME = 8*24*3600

# 敏感词等级评分, string类型
sensitive_score_dict = {
            "1": 1,
            "2": 5,
            "3": 10
}

# use to text_attribute
IP_TIME_SEGMENT = 4*3600
#人物推荐
#recommend in
RECOMMEND_IN_SENSITIVE_TOP = 2000
RECOMMEND_IN_BLACK_USER1 = '/home/ubuntu2/zxy/revised_knowledge/knowledge_revised/knowledge/cron/recommentation_in/blacklist_2.csv'
RECOMMEND_IN_BLACK_USER2 = '/home/ubuntu2/zxy/revised_knowledge/knowledge_revised/knowledge/cron/recommentation_in/blacklist_0808.txt'
RECOMMEND_IN_ACTIVITY_THRESHOLD = 50
RECOMMEND_IN_IP_THRESHOLD = 7
RECOMMEND_IN_RETWEET_THRESHOLD = 20
RECOMMEND_IN_MENTION_THRESHOLD = 15

#auto recommendation
RECOMMEND_IN_AUTO_DATE = 7
RECOMMEND_IN_AUTO_SIZE = 10
RECOMMEND_IN_AUTO_GROUP = 3
RECOMMEND_IN_AUTO_RANDOM_SIZE = 20
RECOMMEND_IN_OUT_SIZE = 50
RECOMMEND_IN_ITER_COUNT = 20
RECOMMEND_IN_MEDIA_PATH = '/home/ubuntu2/zxy/revised_knowledge/knowledge_revised/knowledge/cron/recommentation_in/media_user.txt'
RECOMMEND_MAX_KEYWORDS = 100
RECOMMEND_IN_WEIBO_MAX = 1000

SENTIMENT_SORT_EVALUATE_MAX = 999999999999

RECOMMENTATION_TOPK = 10000
##关系计算绝对路径
r_path = '/home/ubuntu2/yuanshi/knowledge-management/knowledge_revised/knowledge/cron/get_relationship'

##事件分类绝对路径
c_path = '/home/ubuntu2/yuanshi/knowledge-management/knowledge_revised/knowledge/cron/event_classify/python'
