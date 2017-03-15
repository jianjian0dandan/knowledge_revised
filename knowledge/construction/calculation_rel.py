# -*-coding:utf-8-*-
from global_utils import es_user_portrait as es
from event_relationship import event_input
from person_organization import person_organization
from es_data_collection import get_people_dict, get_people_max, get_event_dict, get_event_max, people_calculate, \
    event_calculate
from global_config import *
from neo4j_event import nodes_rels

# 对es的数据创建neo4j图数据库

def create_nodes_people(tiem):
    result = people_calculate(tiem)
    list = []
    for item in result:
        list.append(item["_id"])




def create_nodes_event(tiem):
    list = []
    result = event_calculate(tiem)
    for item in result:
        list.append(item["_id"])



# 计算事件关系
def calculation_event(time):
    event_dict = get_event_dict(time)
    max_dict = get_event_max(time)
    list = []
    # 输出数据：
    # event_dis 事件描述和权重字典
    # 示例：
    # {event1:{'dis':string,'weight':weight},event2:{'dis':string,'weight':weight},...}
    #
    # contain_list 事件关系列表
    # 示例：[[event1,event2,'contain'],[event1,event2,'contain'],...]
    #    输出数据：
    #     event_dis 事件描述和权重字典
    #     示例：
    #     {event1:{'dis':string,'weight':weight},event2:{'dis':string,'weight':weight},...}
    #
    #     contain_list 事件关系列表
    #     示例：[[event1,event2,'contain'],[event1,event2,'contain'],...]
    event_dis, contain_list = event_input(event_dict, max_dict)
    # 对数据存放到es中
    for event_id in event_dict:
        es.update(index=event_analysis_name, doc_type=event_type, id=event_id, body={"doc": {event_dict[event_id]}})
    # 对节点进行创建
    if len(contain_list) == 1:
        item = contain_list[0]
        list = [[[2, item[0]], item[1], [2, item[2]]], ]
    elif len(contain_list > 1):
        for node_node_rel in contain_list:
            item = [[2, node_node_rel[0]], node_node_rel[2], [2, node_node_rel[1]]]
            list.append(item)
    result = nodes_rels(list)
    return result


# 计算人物关系
def calculation_people(time):
    # 输入数据：
    #  people_dict 人物属性字典，键是人物uid，值是人物对应的属性
    # 需要的属性：influence,importance,activeness,sensitive
    # 示例：
    # {uid1:{'influence':influence,'importance':importance,'activeness':activeness,'sensitive':sensitive},
    #  uid2:{'influence':influence,'importance':importance,'activeness':activeness,'sensitive':sensitive},...}
    #
    # max_data 每个字段对应的最大值，类型是字典
    # 示例：{'influence':influence,'importance':importance,'activeness':activeness,'sensitive':sensitive}
    #
    # 输出数据:
    # node_weight 节点权重字典，键是uid，值是该节点对应的权重
    # people_list 人物节点列表，存储人物uid
    # organization_list 机构节点列表，存储机构uid
    # colleague_list 业务关联关系列表，示例：[[uid1,uid2,'colleague'],[uid1,uid2,'colleague'],...]
    # interaction_list 交互关系列表,示例：[[uid1,uid2,'friend',weight],[uid1,uid2,'friend',weight],...]

    people_dict = get_people_dict(time)
    max_dict = get_people_max(time)
    node_weight, people_list, organization_list, colleague_list, interaction_list = person_organization(people_dict,
                                                                                                        max_dict)
    if len(interaction_list) == 1:
        item = interaction_list[0]
        list = [[[2, item[0]], item[1], [2, item[2]]], ]
    elif len(interaction_list > 1):
        for node_node_rel in interaction_list:
            item = [[2, node_node_rel[0]], node_node_rel[2], [2, node_node_rel[1]]]
            list.append(item)
    result = nodes_rels(list)
    return result


if __name__ == '__main__':
    print "ss"
