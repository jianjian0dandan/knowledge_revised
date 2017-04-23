# -*- coding: UTF-8 -*-

import os
import time
import scws
import csv
import sys
import json
import heapq
from config import *
from elasticsearch.helpers import scan
sys.path.append('../manage_neo4j/')
from neo4j_relation import *

def search_es_by_name(dict_name,dict_value,s_uid,flag):#根据对应的属性查询es_user_portrait

    result_uid = []
    query_body = {
        "query":{
            "bool":{
                "should":[{"term":{dict_name:dict_value}}],
                "minimum_should_match": 1
            }
        },
        "size":2000
    }
    search_results = es_user_portrait.search(index=portrait_name, doc_type=portrait_type, body=query_body)['hits']['hits']
    n = len(search_results)
    if n > 0:
        for item in search_results:
            uid = item['_id'].encode('utf-8')
            if uid == s_uid:
                continue
            else:
                data = item['_source']
                if flag == 0:#机构节点                    
                    if data['verify_type'] in org_list:
                        result_uid.append(uid)
                else:#人物节点
                    if data['verify_type'] not in org_list:
                        result_uid.append(uid)

    return result_uid

def search_bci(dict_name,max_influenc,min_influence,s_uid,flag):#根据对应的属性查询es_bci

    result_uid = []
    query_body = {
        "query":{
            "bool":{
                "must":[{"range":{dict_name:{"from":max_influenc,"to":min_influence}}}],
            }
        },
        "size":2000
    }
    search_results = es_bci.search(index=bci_day_pre+TIME_STR, doc_type=bci_day_type, body=query_body)['hits']['hits']
    n = len(search_results)
    if n > 0:
        for item in search_results:
            uid = item['_id'].encode('utf-8')
            if uid == s_uid:
                continue
            else:
                result_uid.append(uid)

    r_list = []
    search_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids": result_uid})["docs"]#判断哪些是人物，哪些是机构
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']
            if flag == 0:#机构节点                    
                if data['verify_type'] in org_list:
                    r_list.append(uid)
            else:#人物节点
                if data['verify_type'] not in org_list:
                    r_list.append(uid)
##            if data['verified_type'] in type_list:
##                r_list.append(uid)

    return r_list

def get_interaction_by_uid(uidlist):#根据uid查询用户的交互情况

    s_uid = uidlist[-1]
    ts = get_db_num(time.time())    
    ori_list = set()
    other_dict = dict()
    search_result = es_retweet.mget(index=retweet_index_name_pre+str(ts), doc_type=retweet_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_retweet']
            data = eval(data)
            if uid == s_uid:
                ori_list = ori_list|set(data.keys())
            else:
                if other_dict.has_key(uid):
                    other_dict[uid].extend(data.keys())
                else:
                    other_dict[uid] = data.keys()

    search_result = es_retweet.mget(index=be_retweet_index_name_pre+str(ts), doc_type=be_retweet_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_be_retweet']
            data = eval(data)
            if uid == s_uid:
                ori_list = ori_list|set(data.keys())
            else:
                if other_dict.has_key(uid):
                    other_dict[uid].extend(data.keys())
                else:
                    other_dict[uid] = data.keys()
  
    search_result = es_comment.mget(index=comment_index_name_pre+str(ts), doc_type=comment_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_comment']
            data = eval(data)
            if uid == s_uid:
                ori_list = ori_list|set(data.keys())
            else:
                if other_dict.has_key(uid):
                    other_dict[uid].extend(data.keys())
                else:
                    other_dict[uid] = data.keys()

    search_result = es_comment.mget(index=be_comment_index_name_pre+str(ts), doc_type=be_comment_index_type, body={"ids": uidlist})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']['uid_be_comment']
            data = eval(data)
            if uid == s_uid:
                ori_list = ori_list|set(data.keys())
            else:
                if other_dict.has_key(uid):
                    other_dict[uid].extend(data.keys())
                else:
                    other_dict[uid] = data.keys()

    result = []
    for k,v in other_dict.iteritems():
        union_set = set(v)&set(ori_list)
        if float(len(union_set))/float(len(ori_list)) >= person_sta:
            result.append(k)
    
    return result

def scan_event_node(uidlist):#从事件中获取共同参与的用户

    s_uid = uidlist[-1]
    event_result = dict()
    s_re = scan(es_event, query={'query':{'match_all':{}}}, index=event_analysis_name, doc_type=event_text_type)
    while True:
        try:
            scan_re = s_re.next()['_source']
            data = eval(scan_re['user_results']).keys()
            union_set = set(data)&set(uidlist)
            if len(union_set) > 0:
                for u in union_set:
                    if event_result.has_key(u):
                        event_result[u].append(scan_re['en_name'])
                    else:
                        event_result[u] = [scan_re['en_name']]
            else:
                pass
        except StopIteration:
            print 'ALL done'
            break

    try:
        s_event = event_result[s_uid]
    except KeyError:
        return []

    result = []
    for k,v in event_result.iteritems():
        if k != s_uid:
            if float(len(set(v)&set(s_event)))/eve_sta:
                result.append(k)

    return result
    

def people_similarity(node_dict):
    '''
        人物相似度计算主函数
        输入数据：
        node_dict 节点属性字典（一个节点），没有该属性对应的值写空（''）
        示例:{'uid':uid,'domain':domain,'location':location,'activity_ip':activity_ip,'verified_type':type}
        
        输出数据：
        similarity_list 与该用户相似的用户
    '''

    if len(node_dict) < 5:
        return []

    try:
        s_uid = node_dict['uid']
        if not s_uid:
            return []
    except KeyError:
        return []

    try:
        node_type = node_dict['verified_type']        
    except KeyError:
        return []

    flag = 0
    if node_type in org_list:#机构节点
        flag = 0
    else:#人物节点
        flag = 1

    try:
        domain = node_dict['domain']
        if not domain:#查找domain相同的用户
            domain_uid = search_es_by_name('domain',domain,s_uid,flag)
        else:
            domain_uid = []
    except KeyError:
        domain_uid = []
        
    try:
        location = node_dict['location']
        if not location:#查找location相同的用户
            location_uid = search_es_by_name('location',location,s_uid,flag)
        else:
            location_uid = []
    except KeyError:
        location_uid = []

    try:
        activity_ip = node_dict['activity_ip']
        if not activity_ip:#查找activity_ip相同的用户
            activity_ip_uid = search_es_by_name('activity_ip',activity_ip,s_uid,flag)
        else:
            activity_ip_uid = []
    except KeyError:
        activity_ip_uid = []
        
    search_result = es_bci.mget(index=bci_day_pre+TIME_STR, doc_type=bci_day_type, body={"ids": [s_uid]})["docs"]
    if len(search_result) == 0:
        influence_uid = []
    else:
        for item in search_result:
            uid = item['_id']
            if not item['found']:
                influence = ''
            else:
                data = item['_source']
                influence = data['user_index']

        if not influence:#查找影响力在一定范围内的用户
            max_influence = influence*MAX_I
            min_influence = influence*MIN_I
            influence_uid = search_bci('user_index',max_influenc,min_influence,s_uid,flag)
        else:
            influence_uid = []

    total_uid = ((set(domain_uid)|set(location_uid))|set(activity_ip_uid))|set(influence_uid)#求uid的并集
    total_uid = list(total_uid)
    total_uid.append(s_uid)

    i_list = get_interaction_by_uid(total_uid)
    e_list = scan_event_node(total_uid)

    whole_result = domain_uid
    whole_result.extend(location_uid)
    whole_result.extend(activity_ip_uid)
    whole_result.extend(influence_uid)
    whole_result.extend(i_list)
    whole_result.extend(e_list)

    result_dict = dict()
    similarity = []
    for u in whole_result:
        try:
            result_dict[u] = result_dict[u] + 1
        except KeyError:
            result_dict[u] = 1

    for k,v in result_dict.iteritems():
        if v >= com_sta:
            similarity.append(k)

    return similarity

def search_event_es(dict_name,dict_value,s_uid):#根据对应的属性查询es_event

    result_uid = []
    if dict_name == 'keywords':
        words = dict_value.split('&')
        w_list = []
        for w in words:
            w_list.append({"wildcard":{"keywords":'*'+str(w)+'*'}})
        n = int(len(words)*event_sta)
        if n < 2:
            n = 1

        query_body = {
            "query":{
                "bool":{
                    "should":w_list,
                    "minimum_should_match": n
                }
            },
            "size":2000
        }
    else:
        query_body = {
            "query":{
                "bool":{
                    "should":[{"term":{dict_name:dict_value}}],
                    "minimum_should_match": 1
                }
            },
            "size":2000
        }
    search_results = es_event.search(index=event_analysis_name, doc_type=event_text_type, body=query_body)['hits']['hits']
    n = len(search_results)

    if n > 0:
        for item in search_results:
            uid = item['_id'].encode('utf-8')
            if uid == s_uid:
                continue
            else:
                result_uid.append(uid)

    return result_uid

def search_event_people(uid_result,s_uid):#根据对应的人物查找相似事件

    result = []
    s_re = scan(es_event, query={'query':{'match_all':{}}}, index=event_analysis_name, doc_type=event_text_type)
    while True:
        try:
            scan_re = s_re.next()['_source']
            id_str = scan_re["en_name"]+'-'+scan_re["submit_ts"]
            if id_str == s_uid:
                continue
            data = eval(scan_re['user_results']).keys()
            union_set = set(data)&set(uid_result.keys())
            if len(union_set) > 0:
                result.append(id_str)
            else:
                pass
        except StopIteration:
            print 'ALL done'
            break

    return result

def event_similarity(node_dict):
    '''
        事件相似度计算主函数
        输入数据：
        e_dict 节点属性字典（一个节点），没有该属性对应的值写空（''）
        示例:{'event_id':uid,'type':type,'location':location,'keyword':keyword,'user_results':user_results}
        keyword是以"&"连接的字符串
        user_results是一个字典（按照事件es里面的格式）
        
        输出数据：
        similarity_list 与该事件相似的事件
    '''

    if len(node_dict) < 5:
        return []

    try:
        s_uid = node_dict['event_id']
        if not s_uid:
            return []
    except KeyError:
        return []

    try:
        e_type = node_dict['type']
        if e_type:#查找type相同的用户
            type_uid = search_event_es('event_type',e_type,s_uid)
        else:
            type_uid = []
    except KeyError:
        type_uid = []
        
    try:
        location = node_dict['location']
        if location:#查找location相同的用户
            location_uid = search_event_es('real_geo',location,s_uid)
        else:
            location_uid = []
    except KeyError:
        location_uid = []

    try:
        keyword = node_dict['keyword']        
        if keyword:#查找keyword相同的用户
            keyword_uid = search_event_es('keywords',keyword,s_uid)
        else:
            keyword_uid = []
    except KeyError:
        keyword_uid = []

    try:
        user_results = node_dict['user_results']
        if not user_results:#查找user_results相同的用户
            user_results_uid = search_event_people(user_results,s_uid)
        else:
            user_results_uid = []
    except KeyError:
        user_results_uid = []

    whole_result = type_uid
    whole_result.extend(location_uid)
    whole_result.extend(keyword_uid)
    whole_result.extend(user_results_uid)

    result_dict = dict()
    similarity = []
    for u in whole_result:
        try:
            result_dict[u] = result_dict[u] + 1
        except KeyError:
            result_dict[u] = 1

    for k,v in result_dict.iteritems():
        if v >= com_sta_eve:
            similarity.append(k)

    return similarity

def get_topic_by_topic_key(t_key):#根据专题id查询专题下的事件

    result = []
    search_result = es_special_event.mget(index=special_event_name, doc_type=special_event_type, body={"ids": t_key})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            break
        else:
            data = item['_source']
            e_list = data['event'].encode('utf-8')
            result = e_list.split('&')
        break

    return result

def get_group_by_group_key(g_key):#根据群体id查询群体下的人物

    result = []
    search_result = es_group.mget(index=group_name, doc_type=group_type, body={"ids": g_key})["docs"]
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            break
        else:
            data = item['_source']
            p_list = data['people'].encode('utf-8')
            result = p_list.split('&')
        break

    return result

def get_people_att_by_keys(people_list):#根据人物id获取人物详细属性

    if len(people_list) == 0:
        return {}
    result_dict = {}
    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": people_list})["docs"]#判断哪些是人物，哪些是机构
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result_dict[uid] = {}
            continue
        else:
            data = item['_source']
            domain = data['domain'].encode('utf-8')
            location = data['location'].encode('utf-8')
            activity_ip = data['activity_ip']
            verified_type = data['verify_type']
            result_dict[uid] = {'uid':uid,'domain':domain,'location':location,'activity_ip':activity_ip,'verified_type':verified_type}

    return result_dict            

def get_event_att_by_keys(event_list):#根据事件id获取事件详细属性

    if len(event_list) == 0:
        return {}
    result_dict = {}
    search_result = es_event.mget(index=event_analysis_name, doc_type=event_type, body={"ids": event_list})["docs"]#判断哪些是人物，哪些是机构
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result_dict[uid] = {}
            continue
        else:
            data = item['_source']
            e_type = data['event_type']
            location = data['real_geo'].encode('utf-8')
            keyword = data['keywords'].encode('utf-8')
            user_results = json.loads(data['user_results'])
            result_dict[uid] = {'event_id':uid,'type':e_type,'location':location,'keyword':keyword,'user_results':user_results}

    return result_dict

def topic_similarity(t_key):
    '''
        专题相似度计算主函数
        输入数据：
        t_key 专题id
        
        输出数据：
        similarity_list 与该专题相似的事件id列表
    '''

    event_list = get_topic_by_topic_key([t_key])#根据专题id查询专题下的事件

    event_att = get_event_att_by_keys(event_list)#根据事件id获取事件详细属性

    result_dict = dict()
    for k,v in event_att.iteritems():
        s_list = event_similarity(v)
        for s in s_list:
            try:
                result_dict[s] = result_dict[s] + 1
            except KeyError:
                result_dict[s] = 1
    
    similarity_list = []
    for k,v in result_dict.iteritems():
        if v >= (len(event_list)*topic_rate):
            similarity_list.append(k)

    return similarity_list

def crowd_similarity(g_key):
    '''
        群体相似度计算主函数
        输入数据：
        g_key 群体id

        输出数据：
        similarity_list 与该群体相似的人物或机构id列表
    '''

    people_list = get_group_by_group_key([g_key])#根据群体id查询群体下的人物

    people_att = get_people_att_by_keys(people_list)#根据人物id获取人物详细属性

    result_dict = dict()
    for k,v in people_att.iteritems():
        s_list = people_similarity(v)
        for s in s_list:
            try:
                result_dict[s] = result_dict[s] + 1
            except KeyError:
                result_dict[s] = 1
    
    similarity_list = []
    for k,v in result_dict.iteritems():
        if v >= (len(people_list)*group_rate):
            similarity_list.append(k)

    return similarity_list


if __name__ == '__main__':
##    p_1 = {'domain':'草根','location':'北京','topic':'媒体&娱乐&鹿晗','hashtag':'演唱会&音乐会','label':'娱乐分子&娱乐达人',\
##        'weight':89,'event':{'111':2,'222':2.5},'people':{'111':73,'222':65,'333':33}}
##    p_2 = {'domain':'草根','location':'重庆','topic':'政治&习近平&鹿晗','hashtag':'演唱会&两会','label':'政治&社会主义',\
##        'weight':89,'event':{'111':2,'333':1},'people':{'111':73,'444':65,'333':33}}
##    e_1 = {'des':'土耳其&爆炸&大使馆','label':'政治安全',\
##        'weight':4,'event':{'111':2,'222':2.5},'people':{'111':73,'222':65,'333':33}}
##    e_2 = {'des':'台湾&大巴&爆炸','label':'车祸',\
##        'weight':3,'event':{'111':2,'333':1},'people':{'111':73,'444':65,'333':33}}
##    t_1 = {'event':{'111':2,'222':2.5},'people':{'111':73,'222':65,'333':33}}
##    t_2 = {'event':{'111':2,'333':1},'people':{'111':73,'444':65,'333':33}}
##    q_1 = {'event':{'111':2,'222':2.5},'people':{'111':73,'222':65,'333':33}}
##    q_2 = {'event':{'111':2,'333':1},'people':{'111':73,'444':65,'333':33}}

##    p_1 = {'uid':"5014862797",'domain':u"活跃人士",'location': "",'activity_ip':u"1.180.215.52",'verified_type':""}
##    s = people_similarity(p_1)
##    print len(s)
##    e_1 = {'event_id': "xi-la-li-1480176000",'type':"政治",'location':"美国",'keyword':"希拉里&美国&川普&特朗普&总统&中国&政治&现在&大选&奥巴马&摊手&媒体&选举&国家&克林顿&计票&民主&女权&这是&选票&世界&当选&民主党&问题&投票&觉得&选举人&精英&竞选&女人&女性&看到&是不是&绿党&人民&支持者&要求&利益&翻盘&上台&肯定&成为&选民&经济&演讲&代表&白宫&需要&继续&邮件&时间&第一&制度&感觉&共和党&调查&只能&反转&发现&朴槿惠&关系&报道&票数&社会&事件&发表&视频&政策&日本&估计&英国&反对&改变&所谓&候选人&民众&白人&以为&失败&事情&博文&影响&加州&机会&比较&美帝&厉害&布什&团队&移民&政府&政客&宣布&男人&专家&传统&老师&作弊&螳臂当车&俄罗斯&消息&最近&决定&历史&选择&了解&准备&今年&赵薇&普选&还要&黑客&原因&第二&粉丝&背后&全世界&包括&当时&出现&时代&生活&内战&中国人&黑人&不想&华人&华盛顿&国会&相信&中东&白左&以前&无法&全球&国际&期待&进行&群众&分析&精神&朋友&多人&意思&造谣&数据&文章&获得&获胜&台湾&申请&记者&赢家&资金&公开&普京&哆啦&证明&纽约时报&国务卿&法律&胜利&领导&统计&战争&不够&未来&公司&攻击&情况&韩国&天下&网络&预测&里面&承认&规则&回来&质疑&商人&说明&超过&说话&游行&逻辑&希拉&考虑&保护&人权&独立&能力&威斯康星州&力量&头条&人生&操纵&组织&孩子&人类&英语&底层&领先&当初&优势&穆斯林&权力&放弃&赢得&民调&存在&人们&电子&行为&完了&选出&四年&折腾&告诉&增加&纽约&转载&教育&辩论&毕竟&信息&女儿&证据&权利&军事&计划&事实&国人&执政&又是&全国&有没有&教授&东西&骗子&错误&华尔街&承诺&脑子&方面&剧情&感恩节&呼声&系统&观点&主席&言论&进入&沙特&带来&发生&人士&意义&监狱&网友&关键&尊重&集团&革命&大学&默克尔&分裂&伊拉克&导致&能够&左派&战略&亚裔&宣传&游戏&照片&律师&套路&地方&网站&蔡英文&反华&民意&理由&谣言&记得&资源&德国&欧洲&密歇根&一群&威胁&文明&面对&主流&威斯康星&呼吁&实际&思想&阵营&方舟&桑德斯&智商&得到&每日&奥运会&学校&逆转&流氓&宾州&策略&贸易&不知&极端&屁股&我要&可能性&阴谋&不服&密歇根州&说是&治国&背景&过来&方式&新浪&领导人&摇摆&学习&难民&有希&不说&民粹&过去&资本&立场&官员&挑战&企业&我国&婊子&老百姓&威斯康&下台&起诉&技术&老公&福利&阶层&简直&都可&下去&先生&讨论&足够&算是&恶心&态度&愿意&样子&因素&歧视&差距&真相&处理&不断&联邦&显示&现实&正义&垃圾&女权主义&下来&想想&内容&看见&文化&大陆&拒绝&统治&翻身&大众&验票&落选&想要&没用&手段&死人&治疗&抗议&犯罪&老婆&之间&儿子&暗杀&实力&伊斯兰&势力&大妈&亚太&关心&疯狂&市场&奥运&中美&无赖&金融&造成&对手&基金会&威斯康辛州&全球化&动画&收入&明星&最高法院&经历&外国&理解&父母&西方&牛逼&实现&翻译&不利&大战&越来越&推动&失去&提议&财团&正是&此前&没什么&任命&工人&联盟&说法&胜出&集体&发起&设计&资助&意外&思维&心里&提供&看出&家庭&投资&讨厌&全美&认输&威斯康辛&马云&委员会&地位&看好&北美&母亲&丑闻&一家&右边&特朗&父亲&天朝&社交&面的&科技&人民币&水平&俄国&穷人&瞬间&明年&参选&办法&腐败&舆论",'user_results':eval('{"1974576991": {"user_type": "auth", "influ": 1717.5974370721115}, "1909203062": {"user_type": "user", "influ": 900.9415105996019}, "2368711070": {"user_type": "user", "influ": 561.704312563331}, "1649750547": {"user_type": "user", "influ": 1195.4388980337415}, "1979899604": {"user_type": "user", "influ": 792.775023782225}, "2074684137": {"user_type": "user", "influ": 612.3611519080147}, "1926182351": {"user_type": "user", "influ": 572.9848165134941}, "1705564917": {"user_type": "user", "influ": 761.0508666150653}, "1414084240": {"user_type": "user", "influ": 1208.30993127556}, "1748285415": {"user_type": "user", "influ": 727.1913360540692}, "1639127253": {"user_type": "user", "influ": 566.484090075582}, "1895431523": {"user_type": "user", "influ": 816.5499616959212}, "5513346012": {"user_type": "user", "influ": 587.0592813054908}, "2635695961": {"user_type": "user", "influ": 1427.8604869010194}, "1105596542": {"user_type": "user", "influ": 829.8839549034828}, "1892184703": {"user_type": "user", "influ": 559.6078113614014}, "3187525994": {"user_type": "user", "influ": 1031.028480608735}, "1889213710": {"user_type": "user", "influ": 1155.4230820309065}, "1236837852": {"user_type": "user", "influ": 773.3255042854014}, "2041206327": {"user_type": "user", "influ": 1041.7765717759712}, "1596329427": {"user_type": "user", "influ": 1288.2358172101328}, "2736165120": {"user_type": "user", "influ": 793.5326697420938}, "2011445377": {"user_type": "user", "influ": 616.1211164386189}, "1864241383": {"user_type": "user", "influ": 594.5799057713394}, "1971861621": {"user_type": "user", "influ": 952.7269170352293}, "5346801743": {"user_type": "user", "influ": 886.4368721112769}, "1402138343": {"user_type": "user", "influ": 756.5700539804611}, "2269443552": {"user_type": "user", "influ": 770.8142230568656}, "1167257004": {"user_type": "user", "influ": 691.165138097124}, "2133521832": {"user_type": "user", "influ": 611.5730037345224}, "5957911434": {"user_type": "user", "influ": 618.6606965674098}, "3878104984": {"user_type": "user", "influ": 585.0557762551261}, "1589153251": {"user_type": "user", "influ": 789.5696696087236}, "2968258964": {"user_type": "user", "influ": 893.4347358027588}, "1560442584": {"user_type": "user", "influ": 1522.4607161276945}, "1639498782": {"user_type": "auth", "influ": 782.2995851219649}, "1645776681": {"user_type": "user", "influ": 860.5321422059983}, "5590704704": {"user_type": "user", "influ": 1017.8367896757889}, "2042052593": {"user_type": "user", "influ": 632.3038850523591}, "1252957604": {"user_type": "user", "influ": 790.8067399106587}, "3710258141": {"user_type": "user", "influ": 804.9800301368685}, "3477513373": {"user_type": "user", "influ": 780.2882857158389}, "1978454793": {"user_type": "user", "influ": 615.3816925989823}, "3756744195": {"user_type": "user", "influ": 571.2977061563738}, "3758960483": {"user_type": "user", "influ": 760.3712503248655}, "5953365159": {"user_type": "user", "influ": 592.0429677375141}, "3114175427": {"user_type": "auth", "influ": 665.5724730898726}, "1645090081": {"user_type": "user", "influ": 646.278333903989}, "1960785875": {"user_type": "auth", "influ": 1476.9905853579307}, "2537882762": {"user_type": "user", "influ": 1206.5402514888135}, "1665808371": {"user_type": "user", "influ": 1339.7151146639715}, "1723895777": {"user_type": "user", "influ": 608.4899739425454}, "2144789105": {"user_type": "user", "influ": 1445.761008568923}, "2029362613": {"user_type": "user", "influ": 586.4941128666045}, "3794240230": {"user_type": "user", "influ": 570.1769270565275}, "2372395793": {"user_type": "user", "influ": 962.431864423903}, "2175063843": {"user_type": "user", "influ": 884.354279143976}, "3939426052": {"user_type": "user", "influ": 1079.393631140594}, "1453874424": {"user_type": "user", "influ": 741.8416797379413}, "1826799355": {"user_type": "user", "influ": 557.5745482653364}, "3881380517": {"user_type": "user", "influ": 760.8900997488631}, "3591358947": {"user_type": "user", "influ": 666.8102875619303}, "5308665252": {"user_type": "user", "influ": 673.2418652843628}, "3515267842": {"user_type": "user", "influ": 1006.9501308022718}, "2035895904": {"user_type": "user", "influ": 695.4355249477771}, "1891366595": {"user_type": "user", "influ": 605.5101592712199}, "1695652643": {"user_type": "user", "influ": 588.7600444128282}, "2672803044": {"user_type": "auth", "influ": 1103.8047079026321}, "1791283533": {"user_type": "auth", "influ": 708.8459652456226}, "1571963253": {"user_type": "user", "influ": 559.2157088947456}, "1926641510": {"user_type": "user", "influ": 803.8528374696124}, "2150758415": {"user_type": "user", "influ": 956.6736128850014}, "2159290653": {"user_type": "user", "influ": 730.5932335528926}, "2611641094": {"user_type": "user", "influ": 1050.6149545650228}, "3320770181": {"user_type": "user", "influ": 706.5534804205071}, "1182425635": {"user_type": "user", "influ": 1322.6374258986832}, "5370547595": {"user_type": "user", "influ": 784.018275610497}, "1656316841": {"user_type": "auth", "influ": 838.5886135427581}, "1670458304": {"user_type": "user", "influ": 982.9474950256379}, "6014403348": {"user_type": "user", "influ": 636.6055616740256}, "5829145369": {"user_type": "user", "influ": 818.877576460175}, "1698233740": {"user_type": "auth", "influ": 1130.4727518290306}, "5695595505": {"user_type": "user", "influ": 711.7262837216955}, "3031762330": {"user_type": "user", "influ": 901.1735313456029}, "3021362331": {"user_type": "user", "influ": 832.4848341545144}, "1259914383": {"user_type": "user", "influ": 1159.2025840062745}, "5603237555": {"user_type": "user", "influ": 880.7039510806422}, "6004281123": {"user_type": "user", "influ": 905.4586057664941}, "2774905435": {"user_type": "user", "influ": 582.3336715448435}, "2615417307": {"user_type": "user", "influ": 977.4802297233327}, "1912150611": {"user_type": "user", "influ": 1269.6607465232667}, "1649470535": {"user_type": "user", "influ": 837.3903801063709}, "1887344341": {"user_type": "auth", "influ": 1677.6689924521957}, "5890154765": {"user_type": "user", "influ": 622.0667951698731}, "5874905192": {"user_type": "user", "influ": 704.0773242994675}, "1111681197": {"user_type": "user", "influ": 1373.6963915084834}, "5647657235": {"user_type": "user", "influ": 716.0103505955892}, "1403497553": {"user_type": "user", "influ": 872.8499489295797}, "2855852714": {"user_type": "user", "influ": 1088.820600845368}, "1801817195": {"user_type": "auth", "influ": 1083.8435421383708}}')}
##    s = event_similarity(e_1)
##    print s
    t_1 = "zheng-zhi-zhuan-ti-_admin@qq.com"
    s = topic_similarity(t_1)
    print s
    q_1 = "mei-xuan-qun-ti-_admin@qq.com"
    s = crowd_similarity(q_1)
    print s
    












        
