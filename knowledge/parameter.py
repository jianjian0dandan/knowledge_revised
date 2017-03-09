# -*-coding:utf-8-*-

from global_config import *

RUN_TYPE = 0

# 关系类型与后续节点primary key的关系
rel_node_mapping = {join: "event_id", other_rel: "event_id",maker:"event_id",pusher:"event_id", \
        group_rel: "group", contain: "event_id", event_special:"event_id", \
        friend: "uid", relative: "uid", colleague: "uid", user_tag: "uid", \
        "domain": "domain", "topic": "topic", "location": "location", "event":"event_id"}


rel_node_type_mapping = {join: "Event", other_rel: "Event", \
        group_rel: "Group", contain: "Event", event_special:"SpecialEvent", \
        friend: "User", relative: "User", colleague: "User", user_tag: "Tag", \
        "domain": "Domain", "topic": "Topic", "location": "Location", "event": "Event"}


# 首页显示最多节点数
index_threshold = 500


CHARACTER_TIME_GAP = 7

WEIBO_API_INPUT_TYPE = 1 # 1 mark: need compute sentiment

DAY = 24*3600
RUN_TEST_TIME  = '2016-03-13'
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

