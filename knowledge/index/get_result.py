# -*- coding: utf-8 -*-

import json
import csv
import os
import time
import math
import re
import heapq
from datetime import date
from datetime import datetime
from elasticsearch.helpers import scan
import knowledge.model
from knowledge.model import *
from knowledge.extensions import db
from knowledge.global_config import *
from knowledge.global_utils import *
from knowledge.global_utils import R_RECOMMENTATION as r,ES_CLUSTER_FLOW1 as es_cluster,get_evaluate_max as get_evaluate_max_all
from knowledge.parameter import DAY
from knowledge.time_utils import ts2datetime, datetime2ts

org_list = [1,2,3,4,5,6,7,8]
black_location = [u'北京',u'天津',u'上海',u'重庆',u'河北',u'山西',u'辽宁',u'吉林',u'黑龙江',u'江苏',u'浙江',u'安徽',u'福建',u'江西',u'山东',u'河南',\
                    u'湖北',u'湖南',u'广东',u'海南',u'四川',u'贵州',u'云南',u'陕西',u'甘肃',u'青海',u'台湾',u'内蒙古',u'广西',u'西藏',u'宁夏',u'新疆',u'香港',u'澳门']

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0][0]
            if elem[0] > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]


def uid_name(uid_list,result):

    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result[uid]['name'] = uid
            continue
        else:
            data = item['_source']
            try:
                result[uid]['name'] = data['uname']
            except:
                result[uid]['name'] = uid

    return result

def uid_name_list(uid_list):#以字典形式返回

    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return '-1'
    uname = dict()
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            uname[uid] = uid
            continue
        else:
            data = item['_source']
            try:
                if not data['uname']:
                    uname[uid] = uid
                else:
                    uname[uid] = data['uname']
            except KeyError:
                uname[uid] = uid

    return uname

def uid_name_list_withtype(uid_list):#以字典形式返回uname和type

    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return '-1'
    uname = dict()
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            #uname[uid] = [uid,user_type]
            continue
        else:
            data = item['_source']
            u_type = data['verify_type']
            if u_type in org_list:
                user_type = 'org'
            else:
                user_type = 'people'
                
            try:
                if not data['uname']:
                    name = uid
                else:
                    name = data['uname']
            except KeyError:
                name = uid
            uname[uid] = [name,user_type]

    return uname

def uid_2_name_list(uid_list):#以列表形式返回

    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return '-1'
    uname = []
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            uname.append([uid,uid])
            continue
        else:
            data = item['_source']
            try:
                name = data['uname']
            except KeyError:
                name = uid
            if name:
                uname.append([uid,name])
            else:
                uname.append([uid,uid])

    return uname

def uid_name_type(uid_list):#获取用户的昵称和认证类型

    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return '-1'
    uname = dict()
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            uname[uid] = {'name':uid,'type':''}
            continue
        else:
            data = item['_source']
            try:
                name = data['uname']
                if not name:
                    name = uid
                else:
                    pass
            except KeyError:
                name = uid
            u_type = data['verify_type']
            uname[uid] = {'name':name,'type':u_type}

    return uname

def eventid_name(uidlist,result):

    search_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result[uid]['name'] = uid
            continue
        else:
            data = item['_source']
            try:
                result[uid]['name'] = data['name']
            except:
                result[uid]['name'] = uid

    return result

def event_id_name_list(uidlist):#以列表形式返回

    result = []
    search_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result.append([uid,uid])
            continue
        else:
            data = item['_source']
            try:
                name = data['name']
            except:
                name = uid
            if name:
                result.append([uid,name])
            else:
                result.append([uid,uid])

    return result
            
def get_people(name,count):#获取我关注的人物

    infors = db.session.query(PeopleAttention).filter(PeopleAttention.name==name).all()
    result = dict()
    uid_list = []
    if count == 'all':#获取所有数据
        for infor in infors:
            uid = infor.peopleID
            uid_list.append(uid)
            result[uid] = {'label':infor.label,'time':str(infor.attentionTime),'name':'','uid':uid}
    else:
        n = 0
        for infor in infors:
            n = n + 1
            if n > count:
                break
            uid = infor.peopleID
            uid_list.append(uid)
            result[uid] = {'label':infor.label,'time':str(infor.attentionTime),'name':'','uid':uid}

    if len(uid_list) > 0:
        result = uid_name(uid_list,result)
    
    return result.values()

def get_event(name,count):#获取我关注的事件

    infors = db.session.query(EventAttention).filter(EventAttention.name==name).all()
    result = dict()
    uid_list = []
    
    if count == 'all':#获取所有数据
        for infor in infors:
            uid = infor.eventID
            uid_list.append(uid)
            result[uid] = {'label':infor.label,'time':str(infor.attentionTime),'name':'','uid':uid}
    else:
        n = 0
        for infor in infors:
            n = n + 1
            if n > count:
                break
            uid = infor.eventID
            uid_list.append(uid)
            result[uid] = {'label':infor.label,'time':str(infor.attentionTime),'name':'','uid':uid}

    if len(uid_list) > 0:
        result = eventid_name(uid_list,result)
    
    return result.values()

def get_org(name,count):#获取我关注的机构

    infors = db.session.query(OrgAttention).filter(OrgAttention.name==name).all()
    result = dict()
    uid_list = []
    if count == 'all':#获取所有数据
        for infor in infors:
            uid = infor.orgID
            uid_list.append(uid)
            result[uid] = {'label':infor.label,'time':str(infor.attentionTime),'name':'','uid':uid}
    else:
        n = 0
        for infor in infors:
            n = n + 1
            if n > count:
                break
            uid = infor.orgID
            uid_list.append(uid)
            result[uid] = {'label':infor.label,'time':str(infor.attentionTime),'name':'','uid':uid}

    if len(uid_list) > 0:
        result = uid_name(uid_list,result)
    
    return result.values()

def get_hot_weibo():#获取热门微博
    
    end_ts = time.time()
    start_ts = 1479312000#2016-11-17  end_ts-24*3600        
        
    query_body = {
        "query":{
            "bool":{
                "must":[{'range':{'detect_ts':{'gt':start_ts,'lt':end_ts}}}],
            }
        },
        "size":2
    }
    search_results = es_social_sensing_text.search(index=social_sensing_index_name, doc_type=social_sensing_index_type, body=query_body)['hits']['hits']
    n = len(search_results)
    result = []
    uid_list = []
    if n > 0:
        for item in search_results:
            mid = item['_id'].encode('utf-8')
            data = item['_source']
            text = data['text'].encode('utf-8')
            uid = data['uid'].encode('utf-8')
            uid_list.append(uid)
            ts = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(data['timestamp'])))
            result.append({'mid':mid,'text':text,'uid':uid,'time':ts})

    if len(result) > 0:
        uname_dict = uid_name_list(uid_list)

    if uname_dict == '-1':
        new_result = []
        for item in result:
            uid = item['uid']
            item['uname'] = uid
            new_result.append(item)
    else:
        new_result = []
        for item in result:
            uid = item['uid']
            item['uname'] = uname_dict[uid]
            new_result.append(item)
        
    return new_result    

# show recommentation in uid
def recommentation_in(input_ts, recomment_type):
    date = ts2datetime(input_ts)
    recomment_results = []
    results = []
    hash_name = 'recomment_'+str(date) + "_" + recomment_type
    identify_in_hashname = "identify_in_" + str(date)
    results = r.hgetall(hash_name)
    if not results:
        return []
    recommend_list = set(r.hkeys(hash_name))
    identify_in_list = set(r.hkeys("compute"))
    recomment_results = list(recommend_list - identify_in_list)[0:3]

    if recomment_results:
        results = get_user_detail(date, recomment_results)
    else:
        results = []
    return results

def get_evaluate_max(index_name):
    max_result = {}
    index_type = 'bci'
    evaluate_index = ['user_index']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size':1,
            'sort':[{evaluate: {'order': 'desc'}}]
            }
        result = es_cluster.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result

#get user detail
#output: uid, uname, location, fansnum, statusnum, influence
def get_user_detail(date, input_result):
    bci_date = ts2datetime(datetime2ts(date) - DAY)
    results = []
    uid_list = input_result
    if date!='all':
        index_name = 'bci_' + ''.join(bci_date.split('-'))
    else:
        now_ts = time.time()
        now_date = ts2datetime(now_ts)
        index_name = 'bci_' + ''.join(now_date.split('-'))
    index_type = 'bci'
    user_bci_result = es_cluster.mget(index=index_name, doc_type=index_type, body={'ids':uid_list}, _source=True)['docs']  #INFLUENCE,fans,status
    user_profile_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':uid_list}, _source=True)['docs'] #个人姓名，注册地
    max_evaluate_influ = get_evaluate_max(index_name)
    for i in range(0, len(uid_list)):
        uid = uid_list[i]
        bci_dict = user_bci_result[i]
        profile_dict = user_profile_result[i]

        try:
            bci_source = bci_dict['_source']
        except:
            bci_source = None
        if bci_source:
            influence = bci_source['user_index']
            influence = math.log(influence/float(max_evaluate_influ['user_index']) * 9 + 1 ,10)
            influence = influence * 100
        else:
            influence = ''
        try:
            profile_source = profile_dict['_source']
        except:
            profile_source = None
        if profile_source:
            uname = profile_source['nick_name'] 
            location = profile_source['user_location']
            try:
                fansnum = bci_dict['fields']['user_fansnum'][0]
            except:
                fansnum = 0
            try:
                statusnum = bci_dict['fields']['weibo_month_sum'][0]
            except:
                statusnum = 0
        else:
            uname = uid
            location = ''
            try:
                fansnum = bci_dict['fields']['user_fansnum'][0]
            except:
                fansnum = 0
            try:
                statusnum = bci_dict['fields']['weibo_month_sum'][0]
            except:
                statusnum = 0

        results.append({'uid':uid, 'uname':uname, 'location':location, 'fansnum':fansnum, 'statusnum':statusnum, 'influence':round(influence,2)})

    return results

def get_hot_people():#获取热门人物

    input_ts = 1480176000#time.time()
    results = recommentation_in(input_ts, 'influence')
    return results

def get_map_count(max_count):#获取地图统计

    location_result = dict()
    no_location_count = 0
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}}, index=portrait_name, doc_type=portrait_type)
    while True:
        try:
            count = count + 1
            if count > max_count:
                break
            scan_re = s_re.next()['_source']
            try:
                location = scan_re['location']
                if not location:
                    no_location_count += 1
                    continue
                if len(location.split(' '))>1:
                    location = location.split(' ')[0]
                if location in set(black_location):
                    try:
                        location_result[location] += 1
                    except:
                        location_result[location] = 1
                else:
                    continue
            except:
                no_location_count += 1
        except StopIteration:
            print 'ALL done'
            break

    result_list = []
    for k,v in location_result.iteritems():
        result_list.append({'name':k,'value':v})
    return result_list

def get_detail_per_org_map(uid_list):#根据id查询人物和机构的location

    if len(uid_list) == 0:
        return []
    result = []
    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for i in range(0,len(search_result)):
        item = search_result[i]
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']
            if not data['uname']:
                name = uid
            else:
                name = data['uname']

            if not data['location'] or not len(data['location'].split(' ')):
                continue
            else:
                lo = data['location'].split(' ')[0]
                if lo in set(black_location):
                    location = data['location']
                else:
                    continue                    
            
            result.append([uid,name,location])

    return result

def get_detail_event_map(uid_list):#根据uid查询事件的location

    if len(uid_list) == 0:
        return []
    result = []
    search_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for i in range(0,len(search_result)):
        item = search_result[i]
        uid = item['_id']
        if not item['found']:
            continue
        else:
            data = item['_source']
            if not data['name']:
                name = uid
            else:
                name = data['name'].replace('&',',')
            try:
                if not data['real_geo'] or not data['real_geo'] in set(black_location):                 
                    continue
                else:
                    location = data['real_geo']
            except KeyError:
                continue
            
            result.append([uid,name,location])

    return result 

def get_type_key(item):
    if item == '1':#人物
        return people_primary
    elif item == '2':#事件
        return event_primary
    elif item == '0':#机构
        return org_primary
    elif item == '3':#专题
        return special_event_primary
    elif item == '4':#群体
        return group_primary
    elif item == '5':#wiki
        return wiki_primary
    else:
        return 'Not Found'

def get_detail_person(uid_list,user_name):

    if len(uid_list) == 0:
        return {}
    result = {}
    evaluate_max = get_evaluate_max_all()
    date = 1480176000#time.time()
    bci_date = ts2datetime(date - DAY)
    index_name = 'bci_' + ''.join(bci_date.split('-'))
    index_type = 'bci'
    user_bci_result = es_cluster.mget(index=index_name, doc_type=index_type, body={'ids':uid_list}, _source=True)['docs']
    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for i in range(0,len(search_result)):
        item = search_result[i]
        uid = item['_id']
        if not item['found']:
            #result[uid] = {}
            continue
        else:
            data = item['_source']
            if not data['uname']:
                name = ''
            else:
                name = data['uname']
            domain = data['domain']
            if not data['location']:
                location = ''
            else:
                location = data['location']           
            if not data['verify_type']:
                verified = ''
            else:
                if data['verify_type'] not in org_list:
                    verified = ver_data[data['verify_type']]
                else:
                    #result[uid] = {}
                    continue
            importance = normal_index(data['sensitive'],evaluate_max['sensitive'])
            influence = normal_index(data['influence'],evaluate_max['influence'])
            activeness = normal_index(data['activeness'],evaluate_max['activeness'])
            picture = data['photo_url']

            try:
                work_tag = data['function_mark']
                tags = work_tag.split('&')
                tag_list = []
                for tag in tags:
                    u,t = tag.split('_')
                    if u == user_name:
                        tag_list.append(t)
            except:
                tag_list = []
            
            bci_dict = user_bci_result[i]
            try:
                fansnum = bci_dict['fields']['user_fansnum'][0]
            except:
                fansnum = 0
            
            result[uid] = {'name':name,'domain':domain,'picture':picture,'importance':importance,'influence':influence,'activeness':activeness,'location':location,'verified':verified,'tag':tag_list,'fansnum':fansnum}

    return result

def get_detail_org(uid_list,user_name):

    if len(uid_list) == 0:
        return {}
    result = {}
    evaluate_max = get_evaluate_max_all()
    date = 1480176000#time.time()
    bci_date = ts2datetime(date - DAY)
    index_name = 'bci_' + ''.join(bci_date.split('-'))
    index_type = 'bci'
    user_bci_result = es_cluster.mget(index=index_name, doc_type=index_type, body={'ids':uid_list}, _source=True)['docs']
    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for i in range(0,len(search_result)):
        item = search_result[i]
        uid = item['_id']
        if not item['found']:
            #result[uid] = {}
            continue
        else:
            data = item['_source']
            if not data['uname']:
                name = ''
            else:
                name = data['uname']

            if not data['location']:
                location = ''
            else:
                location = data['location']          
            if not data['verify_type']:
                #result[uid] = {}
                continue
            else:
                if data['verify_type'] in org_list:
                    verified = ver_data[data['verify_type']]
                else:
                    #result[uid] = {}
                    continue
            importance = normal_index(data['sensitive'],evaluate_max['sensitive'])
            influence = normal_index(data['influence'],evaluate_max['influence'])
            activeness = normal_index(data['activeness'],evaluate_max['activeness'])
            picture = data['photo_url']
                
            try:
                work_tag = data['function_mark']
                tags = work_tag.split('&')
                tag_list = []
                for tag in tags:
                    u,t = tag.split('_')
                    if u == user_name:
                        tag_list.append(t)
            except:
                tag_list = []

            bci_dict = user_bci_result[i]
            try:
                fansnum = bci_dict['fields']['user_fansnum'][0]
            except:
                fansnum = 0
            
            result[uid] = {'name':name,'picture':picture,'location':location,'verified':verified,'tag':tag_list,'fansnum':fansnum,'importance':importance,'influence':influence,'activeness':activeness}

    return result

def get_detail_event(uid_list,user_name):

    if len(uid_list) == 0:
        return {}
    result = {}
    search_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={"ids": uid_list})["docs"]
    if len(search_result) == 0:
        return result
    for item in search_result:
        uid = item['_id']

        if not item['found']:
            #result[uid] = {}
            continue
        else:
            data = item['_source']
            
            try:
                if not data['name']:
                    name = uid
                else:
                    name = data['name']
            except KeyError:
                name = uid
            
            try:
                if data['real_geo'] != 'NULL':
                    geo = data['real_geo']
                else:
                    geo = ''
            except KeyError:
                geo = ''
            try:
                category = EN_CH_EVENT[data['event_type'].strip()]
            except KeyError:
                category = ''

            try:
                time_ts = ts2date(data['start_ts'])
            except KeyError:
                time_ts = ts2date(time.time())

            try:
                work_tag = data['work_tag']
                tags = work_tag.split('&')
                tag_list = []
                for tag in tags:
                    u,t = tag.split('_')
                    if u == user_name:
                        tag_list.append(t)
            except:
                tag_list = []

            try:
                weibo = data['weibo_count']
            except KeyError:
                weibo = 0

            try:
                people = data['uid_count']
            except KeyError:
                people = 0

            try:
                keywords = data['keywords']
                ks = keywords.split('&')
                keyword = '&'.join(ks[0:10])
            except KeyError:
                keyword = ''
                
            result[uid] = {'name':name,'geo':geo,'event_type':category,'time_ts':time_ts,'tag':tag_list,'weibo':weibo,'people':people,'des':keyword}

    return result

def get_relation_node(user_id,node_type,card_type,user_name):#获取关联节点

    node_key = get_type_key(node_type)
    card_key = get_type_key(card_type)
    
    if node_key == 'Not Found' or card_key == 'Not Found':#未找到匹配类型
        return [],-1
    if node_key == people_primary:
        if card_key == people_primary:#uid-uid
            start_index_name = node_index_name
            end_index_name = node_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_person(uid_list,user_name)#获取用户详细信息
            flag = 1
        elif card_key == event_primary:#uid-event
            start_index_name = node_index_name
            end_index_name = event_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_event(uid_list,user_name)#获取事件详细信息
            flag = 2
        else:#uid-org
            start_index_name = node_index_name
            end_index_name = org_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_org(uid_list,user_name)#获取用户详细信息
            flag = 0

    elif node_key == event_primary:
        if card_key == people_primary:#event-uid
            start_index_name = event_index_name
            end_index_name = node_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_person(uid_list,user_name)#获取用户详细信息
            flag = 1
        elif card_key == event_primary:#event-event
            start_index_name = event_index_name
            end_index_name = event_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_event(uid_list,user_name)#获取事件详细信息
            flag = 2
        else:#event-org
            start_index_name = event_index_name
            end_index_name = org_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_org(uid_list,user_name)#获取机构详细信息
            flag = 0

    elif node_key == org_primary:
        if card_key == people_primary:#org-uid
            start_index_name = org_index_name
            end_index_name = node_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_person(uid_list,user_name)#获取用户详细信息
            flag = 1
        elif card_key == event_primary:#org-event
            start_index_name = org_index_name
            end_index_name = event_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_event(uid_list,user_name)#获取事件详细信息
            flag = 2
        else:#org-org
            start_index_name = org_index_name
            end_index_name = org_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_org(uid_list,user_name)#获取机构详细信息
            flag = 0
    elif node_key == wiki_primary:
        uid = show_wiki_related(user_id)
        if not len(uid):
            return []
        if card_key == people_primary:#wiki-uid
            start_index_name = wiki_url_index_name
            end_index_name = node_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,uid,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_person(uid_list,user_name)#获取用户详细信息
            flag = 1
        elif card_key == event_primary:#wiki-event
            start_index_name = wiki_url_index_name
            end_index_name = event_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,uid,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_event(uid_list,user_name)#获取事件详细信息
            flag = 2
        else:#wiki-org
            start_index_name = wiki_url_index_name
            end_index_name = org_index_name
            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[r]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,uid,end_index_name,card_key,card_key)
            p_result = graph.run(c_string)
            uid_list = []
            for item in p_result:
                uid_list.append(item[0])
            result = get_detail_org(uid_list,user_name)#获取机构详细信息
            flag = 0
    else:
        result = {}
        flag = -1
##    elif node_key == special_event_primary:
##        if card_key == people_primary:#special_event-uid
##            start_index_name = node_index_name
##            end_index_name = node_index_name
##            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-()-[]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
##            p_result = graph.run(c_string)
##            uid_list = []
##            for item in p_result:
##                uid_list.append(item[0])
##            result = get_detail_person(uid_list,user_name)#获取用户详细信息
##            flag = 1
##        elif card_key == event_primary:#special_event-event
##            start_index_name = node_index_name
##            end_index_name = event_index_name
##            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-()-[]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
##            p_result = graph.run(c_string)
##            uid_list = []
##            for item in p_result:
##                uid_list.append(item[0])
##            result = get_detail_person(uid_list,user_name)#获取用户详细信息
##            flag = 2
##        else:#special_event-org
##            start_index_name = node_index_name
##            end_index_name = org_index_name
##            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-()-[]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
##            p_result = graph.run(c_string)
##            uid_list = []
##            for item in p_result:
##                uid_list.append(item[0])
##            result = get_detail_org(uid_list,user_name)#获取用户详细信息
##            flag = 0
##
##    elif node_key == group_primary:
##        if card_key == people_primary:#group-uid
##            start_index_name = group_index_name
##            end_index_name = node_index_name
##            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-()-[]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
##            p_result = graph.run(c_string)
##            uid_list = []
##            for item in p_result:
##                uid_list.append(item[0])
##            result = get_detail_person(uid_list,user_name)#获取用户详细信息
##            flag = 1
##        elif card_key == event_primary:#group-event
##            start_index_name = group_index_name
##            end_index_name = event_index_name
##            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-()-[]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
##            p_result = graph.run(c_string)
##            uid_list = []
##            for item in p_result:
##                uid_list.append(item[0])
##            result = get_detail_person(uid_list,user_name)#获取用户详细信息
##            flag = 2
##        else:#group-org
##            start_index_name = group_index_name
##            end_index_name = org_index_name
##            c_string = 'START n=node:%s(%s="%s"),m=node:%s("%s:*") MATCH (n)-[]-()-[]-(m) return m.%s LIMIT 100' % (start_index_name,node_key,user_id,end_index_name,card_key,card_key)
##            p_result = graph.run(c_string)
##            uid_list = []
##            for item in p_result:
##                uid_list.append(item[0])
##            result = get_detail_org(uid_list,user_name)#获取用户详细信息
##            flag = 0
    

    return result,flag

def event_id_name(uidlist):

    result = dict()
    search_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return {}
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result[uid] = uid
            continue
        else:
            data = item['_source']
            try:
                name = data['name'].encode('utf-8')
                if not name:
                    result[uid] = uid
                else:
                    result[uid] = name
            except:
                result[uid] = uid

    return result

def peo_id_name(uidlist):

    result = dict()
    search_result = es_user_portrait.mget(index=portrait_name, doc_type=portrait_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return {}
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result[uid] = uid
            continue
        else:
            data = item['_source']
            try:
                name = data['uname'].encode('utf-8')
                if not name:
                    result[uid] = uid
                else:
                    result[uid] = name
            except:
                result[uid] = uid

    return result

def top_id_name(uidlist):

    result = dict()
    search_result = es_special_event.mget(index=special_event_name, doc_type=special_event_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return {}
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result[uid] = uid
            continue
        else:
            data = item['_source']
            try:
                name = data['topic_name'].encode('utf-8')
                if not name:
                    result[uid] = uid
                else:
                    result[uid] = name
            except:
                result[uid] = uid

    return result

def group_id_name(uidlist):

    result = dict()
    search_result = es_group.mget(index=group_name, doc_type=group_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return {}
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result[uid] = uid
            continue
        else:
            data = item['_source']
            try:
                name = data['group_name'].encode('utf-8')
                if not name:
                    result[uid] = uid
                else:
                    result[uid] = name
            except:
                result[uid] = uid

    return result

def wiki_id_name(uidlist):

    result = dict()
    search_result = es_wiki.mget(index=wiki_index_name, doc_type=wiki_type_name, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return {}
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result[uid] = uid
            continue
        else:
            data = item['_source']
            try:
                name = data['name'].encode('utf-8')
                if not name:
                    result[uid] = uid
                else:
                    result[uid] = name
            except:
                result[uid] = uid

    return result

def event2time(uidlist):#获取最新加入图谱的事件

    result = dict()
    event_time = TopkHeap(5)
    search_result = es_event.mget(index=event_analysis_name, doc_type=event_text_type, body={"ids": uidlist})["docs"]
    if len(search_result) == 0:
        return {}
    for item in search_result:
        uid = item['_id']
        if not item['found']:
            result[uid] = uid
            continue
        else:
            data = item['_source']
            try:
                name = data['name'].encode('utf-8')
                if not name:
                    result[uid] = uid
                else:
                    result[uid] = name
            except:
                result[uid] = uid
            try:
                ts = data['finish_ts']
            except:
                ts = int(time.time())
            event_time.Push((ts,uid))

    event_data = event_time.TopK()
    event_list = []
    for item in event_data:
        event_list.append(item[1])
    return event_list,result

def get_all_graph():#获取首页图谱

    total_event = []
    p_string = 'START n=node:%s("%s:*") return n.event_id' % (event_index_name,event_primary)
    p_result = graph.run(p_string)
    for item in p_result:
        node1 = item[0]
        if node1 not in total_event:
            total_event.append(node1)

    if len(total_event) > 0:
        total_list,result_eve = event2time(total_event)
    else:
        total_list = []
        result_eve = {}
        
    peo_list = []
    eve_end_list = []
    top_list = []
    wiki_list = []
    r_relation = []
    for e_id in total_list:
        p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return r,m,labels(m) LIMIT 200' % (event_index_name,event_primary,e_id)
        p_result = graph.run(p_string)    
        for item in p_result:
            node2_k = item[2][0]
            node2_v = dict(item[1]).values()[0]
            r = item[0].type()
            if node2_k == people_node:#人物
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
                r_relation.append([node1,node2_v,'people',r])
            elif node2_k == org_node:#机构
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
                r_relation.append([node1,node2_v,'org',r])
            elif node2_k == event_node:#事件
                if node2_v not in eve_end_list:
                    eve_end_list.append(node2_v)
                r_relation.append([node1,node2_v,'event',r])
            elif node2_k == special_event_node:#专题
                if node2_v not in top_list:
                    top_list.append(node2_v)
                r_relation.append([node1,node2_v,'topic',r])
            elif node2_k == wiki_node:#维基
                if node2_v not in wiki_list:
                    wiki_list.append(node2_v)
                r_relation.append([node1,node2_v,'wiki',r])
            else:
                continue

    if len(peo_list) > 0:
        result_peo = peo_id_name(peo_list)
    else:
        result_peo = {}
    if len(top_list) > 0:
        result_top = top_id_name(top_list)
    else:
        result_top = {}
    if len(eve_end_list) > 0:
        result_eve_end = event_id_name(eve_end_list)
    else:
        result_eve_end = {}
    if len(wiki_list) > 0:
        result_wiki = wiki_id_name(wiki_list)
    else:
        result_wiki = {}

    relation = []
    for item in r_relation:
        flag = item[2]
        if flag == 'people':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'org':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'event':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_eve_end[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'topic':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_top[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'wiki':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_wiki[item[1]],item[2],item[3]])
            except KeyError:
                continue
        else:
            continue

    return relation

def get_people_graph(uid):#获取人物节点图谱

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return n.uid,r,m,labels(m) LIMIT 200' % (node_index_name,people_primary,uid)
    p_result = graph.run(p_string)
    peo_list = []
    eve_list = []
    gro_list = []
    wiki_list = []
    r_relation = []
    for item in p_result:
        node1 = item[0]
        if node1 not in peo_list:
            peo_list.append(node1)
        node2_k = item[3][0]
        node2_v = dict(item[2]).values()[0]
        r = item[1].type()
        if node2_k == people_node:#人物
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            r_relation.append([node1,node2_v,'people',r])
        elif node2_k == org_node:#机构
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            r_relation.append([node1,node2_v,'org',r])
        elif node2_k == event_node:#事件
            if node2_v not in eve_list:
                eve_list.append(node2_v)
            r_relation.append([node1,node2_v,'event',r])
        elif node2_k == group_node:#群体
            if node2_v not in gro_list:
                gro_list.append(node2_v)
            r_relation.append([node1,node2_v,'group',r])
        elif node2_k == wiki_node:#维基
            if node2_v not in wiki_list:
                wiki_list.append(node2_v)
            r_relation.append([node1,node2_v,'wiki',r])
        else:
            continue

    if len(peo_list) > 0:
        result_peo = peo_id_name(peo_list)
    else:
        result_peo = {}
    if len(eve_list) > 0:
        result_eve = event_id_name(eve_list)
    else:
        result_eve = {}
    if len(gro_list) > 0:
        result_gro = group_id_name(gro_list)
    else:
        result_gro = {}
    if len(wiki_list) > 0:
        result_wiki = wiki_id_name(wiki_list)
    else:
        result_wiki = {}

    relation = []
    for item in r_relation:
        flag = item[2]
        if flag == 'people':
            try:
                relation.append([item[0],result_peo[item[0]],'people',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'org':
            try:
                relation.append([item[0],result_peo[item[0]],'people',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'event':
            try:
                relation.append([item[0],result_peo[item[0]],'people',item[1],result_eve[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'group':
            try:
                relation.append([item[0],result_peo[item[0]],'people',item[1],result_gro[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'wiki':
            try:
                relation.append([item[0],result_peo[item[0]],'people',item[1],result_wiki[item[1]],item[2],item[3]])
            except KeyError:
                continue
        else:
            continue

    if len(relation) == 0:
        relation.append([uid,result_peo[uid],'people','','','',''])
    
    return relation

def get_event_graph(uid):#获取事件节点图谱

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return n.event_id,r,m,labels(m) LIMIT 200' % (event_index_name,event_primary,uid)

    p_result = graph.run(p_string)
    peo_list = []
    eve_list = []
    top_list = []
    wiki_list = []
    r_relation = []
    for item in p_result:
        node1 = item[0]
        if node1 not in eve_list:
            eve_list.append(node1)
        node2_k = item[3][0]
        node2_v = dict(item[2]).values()[0]
        r = item[1].type()
        if node2_k == people_node:#人物
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            r_relation.append([node1,node2_v,'people',r])
        elif node2_k == org_node:#机构
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            r_relation.append([node1,node2_v,'org',r])
        elif node2_k == event_node:#事件
            if node2_v not in eve_list:
                eve_list.append(node2_v)
            r_relation.append([node1,node2_v,'event',r])
        elif node2_k == special_event_node:#专题
            if node2_v not in top_list:
                top_list.append(node2_v)
            r_relation.append([node1,node2_v,'topic',r])
        elif node2_k == wiki_node:#维基
            if node2_v not in wiki_list:
                wiki_list.append(node2_v)
            r_relation.append([node1,node2_v,'wiki',r])
        else:
            continue

    if len(peo_list) > 0:
        result_peo = peo_id_name(peo_list)
    else:
        result_peo = {}
    if len(eve_list) > 0:
        result_eve = event_id_name(eve_list)
    else:
        result_eve = {}
    if len(top_list) > 0:
        result_top = top_id_name(top_list)
    else:
        result_top = {}
    if len(wiki_list) > 0:
        result_wiki = wiki_id_name(wiki_list)
    else:
        result_wiki = {}

    relation = []
    for item in r_relation:
        flag = item[2]
        if flag == 'people':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'org':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'event':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_eve[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'topic':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_top[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'wiki':
            try:
                relation.append([item[0],result_eve[item[0]],'event',item[1],result_wiki[item[1]],item[2],item[3]])
            except KeyError:
                continue
        else:
            continue

    if len(relation) == 0:
        relation.append([uid,result_eve[uid],'event','','','',''])
        
    return relation

def get_org_graph(uid):#获取机构节点图谱
    
    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return n.org_id,r,m,labels(m) LIMIT 200' % (org_index_name,org_primary,uid)

    p_result = graph.run(p_string)
    peo_list = []
    eve_list = []
    gro_list = []
    wiki_list = []
    r_relation = []
    for item in p_result:
        node1 = item[0]
        if node1 not in peo_list:
            peo_list.append(node1)
        node2_k = item[3][0]
        node2_v = dict(item[2]).values()[0]
        r = item[1].type()
        if node2_k == people_node:#人物
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            r_relation.append([node1,node2_v,'people',r])
        elif node2_k == org_node:#机构
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            r_relation.append([node1,node2_v,'org',r])
        elif node2_k == event_node:#事件
            if node2_v not in eve_list:
                eve_list.append(node2_v)
            r_relation.append([node1,node2_v,'event',r])
        elif node2_k == group_node:#群体
            if node2_v not in gro_list:
                gro_list.append(node2_v)
            r_relation.append([node1,node2_v,'group',r])
        elif node2_k == wiki_node:#维基
            if node2_v not in wiki_list:
                wiki_list.append(node2_v)
            r_relation.append([node1,node2_v,'wiki',r])
        else:
            continue

    if len(peo_list) > 0:
        result_peo = peo_id_name(peo_list)
    else:
        result_peo = {}
    if len(eve_list) > 0:
        result_eve = event_id_name(eve_list)
    else:
        result_eve = {}
    if len(gro_list) > 0:
        result_gro = group_id_name(gro_list)
    else:
        result_gro = {}
    if len(wiki_list) > 0:
        result_wiki = wiki_id_name(wiki_list)
    else:
        result_wiki = {}

    relation = []
    for item in r_relation:
        flag = item[2]
        if flag == 'people':
            try:
                relation.append([item[0],result_peo[item[0]],'org',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'org':
            try:
                relation.append([item[0],result_peo[item[0]],'org',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'event':
            try:
                relation.append([item[0],result_peo[item[0]],'org',item[1],result_eve[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'group':
            try:
                relation.append([item[0],result_peo[item[0]],'org',item[1],result_gro[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'wiki':
            try:
                relation.append([item[0],result_peo[item[0]],'org',item[1],result_wiki[item[1]],item[2],item[3]])
            except KeyError:
                continue
        else:
            continue

    if len(relation) == 0:
        relation.append([uid,result_peo[uid],'org','','','',''])

    return relation

def get_special_event_graph(uid):#获取专题节点图谱

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return n.event,r,m,labels(m) LIMIT 200' % (special_event_index_name,special_event_primary,uid)

    p_result = graph.run(p_string)
    eve_list = []
    top_list = []
    peo_list = []
    r_relation = []
    for item in p_result:
        node1 = item[0]
        if node1 not in top_list:
            top_list.append(node1)
        node2_k = item[3][0]
        node2_v = dict(item[2]).values()[0]
        r = item[1].type()
        if node2_k == event_node:#事件
            if node2_v not in eve_list:
                eve_list.append(node2_v)
            r_relation.append([node1,'topic',node2_v,'event',r])
        else:
            continue

    for eve in eve_list:
        p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return r,m,labels(m) LIMIT 10' % (event_index_name,event_primary,eve)
        p_result = graph.run(p_string)
        for item in p_result:
            node2_k = item[2][0]
            node2_v = dict(item[1]).values()[0]
            r = item[0].type()
            if node2_k == people_node:#人物
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
                r_relation.append([eve,'event',node2_v,'people',r])
            elif node2_k == org_node:#机构
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
                r_relation.append([eve,'event',node2_v,'org',r])
            elif node2_k == event_node:#事件
                if node2_v not in eve_list:
                    eve_list.append(node2_v)
                r_relation.append([eve,'event',node2_v,'event',r])
            else:
                continue
    
    if len(eve_list) > 0:
        result_eve = event_id_name(eve_list)
    else:
        result_eve = {}
    if len(top_list) > 0:
        result_top = top_id_name(top_list)
    else:
        result_top = {}
    if len(peo_list) > 0:
        result_peo = peo_id_name(peo_list)
    else:
        result_peo = {}

    relation = []
    for item in r_relation:
        flag = item[3]
        flag1 = item[1]
        if flag1 == 'topic':
            try:
                relation.append([item[0],result_top[item[0]],'topic',item[2],result_eve[item[2]],item[3],item[4]])
            except KeyError:
                continue
        elif flag1 == 'event':
            if flag == 'event':
                try:
                    relation.append([item[0],result_eve[item[0]],'event',item[2],result_eve[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            elif flag == 'people':
                try:
                    relation.append([item[0],result_eve[item[0]],'event',item[2],result_peo[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            elif flag == 'org':
                try:
                    relation.append([item[0],result_eve[item[0]],'event',item[2],result_peo[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            else:
                continue
        else:
            continue

    if len(relation) == 0:
        relation.append([uid,result_top[uid],'topic','','','',''])
    
    return relation

def get_group_graph(uid):#获取群体节点图谱

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return n.group,r,m,labels(m) LIMIT 200' % (group_index_name,group_primary,uid)

    p_result = graph.run(p_string)
    peo_list = []
    gro_list = []
    eve_list = []
    peo_list1 = []
    org_list1 = []
    r_relation = []
    for item in p_result:
        node1 = item[0]
        if node1 not in gro_list:
            gro_list.append(node1)
        node2_k = item[3][0]
        node2_v = dict(item[2]).values()[0]
        r = item[1].type()
        if node2_k == people_node:#人物
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            if node2_v not in peo_list1:
                peo_list1.append(node2_v)
            r_relation.append([node1,'group',node2_v,'people',r])
        elif node2_k == org_node:#机构
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            if node2_v not in org_list1:
                org_list1.append(node2_v)
            r_relation.append([node1,'group',node2_v,'org',r])
        else:
            continue

    for peo in peo_list1:
        p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return r,m,labels(m) LIMIT 10' % (node_index_name,people_primary,peo)
        p_result = graph.run(p_string)
        for item in p_result:
            node2_k = item[2][0]
            node2_v = dict(item[1]).values()[0]
            r = item[0].type()
            if node2_k == people_node:#人物
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
                r_relation.append([peo,'people',node2_v,'people',r])
            elif node2_k == org_node:#机构
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
                r_relation.append([peo,'people',node2_v,'org',r])
            elif node2_k == event_node:#事件
                if node2_v not in eve_list:
                    eve_list.append(node2_v)
                r_relation.append([peo,'people',node2_v,'event',r])
            else:
                continue

    for org in org_list1:
        p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return r,m,labels(m) LIMIT 10' % (org_index_name,org_primary,org)
        p_result = graph.run(p_string)
        for item in p_result:
            node2_k = item[2][0]
            node2_v = dict(item[1]).values()[0]
            r = item[0].type()
            if node2_k == people_node:#人物
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
                r_relation.append([org,'org',node2_v,'people',r])
            elif node2_k == org_node:#机构
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
                r_relation.append([org,'org',node2_v,'org',r])
            elif node2_k == event_node:#事件
                if node2_v not in eve_list:
                    eve_list.append(node2_v)
                r_relation.append([org,'org',node2_v,'event',r])
            else:
                continue

    if len(eve_list) > 0:
        result_eve = event_id_name(eve_list)
    else:
        result_eve = {}
    if len(peo_list) > 0:
        result_peo = peo_id_name(peo_list)
    else:
        result_peo = {}
    if len(gro_list) > 0:
        result_gro = group_id_name(gro_list)
    else:
        result_gro = {}

    relation = []
    for item in r_relation:
        flag = item[3]
        flag1 = item[1]
        if flag1 == 'group':
            if flag == 'people':
                try:
                    relation.append([item[0],result_gro[item[0]],'group',item[2],result_peo[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            elif flag == 'org':
                try:
                    relation.append([item[0],result_gro[item[0]],'group',item[2],result_peo[item[2]],item[3],item[4]])
                except KeyError:
                    continue
        elif flag1 == 'people':
            if flag == 'people':
                try:
                    relation.append([item[0],result_peo[item[0]],'people',item[2],result_peo[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            elif flag == 'org':
                try:
                    relation.append([item[0],result_peo[item[0]],'people',item[2],result_peo[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            elif flag == 'event':
                try:
                    relation.append([item[0],result_peo[item[0]],'people',item[2],result_eve[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            else:
                continue
        elif flag1 == 'org':
            if flag == 'people':
                try:
                    relation.append([item[0],result_peo[item[0]],'people',item[2],result_peo[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            elif flag == 'org':
                try:
                    relation.append([item[0],result_peo[item[0]],'people',item[2],result_peo[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            elif flag == 'event':
                try:
                    relation.append([item[0],result_peo[item[0]],'people',item[2],result_eve[item[2]],item[3],item[4]])
                except KeyError:
                    continue
            else:
                continue
        else:
            continue

    if len(relation) == 0:
        relation.append([uid,result_gro[uid],'group','','','',''])
    
    return relation

def show_wiki_related(name):

    conn = getconn()
    cur = conn.cursor()
    sql = "select Url from wiki where Name=%s "
    html_id = cur.execute(sql, (name,))
    if html_id:
        html_id_sql = cur.fetchmany(html_id)
        url = html_id_sql[0][0]
    else:
        url = ''

    return url

def get_wiki_graph(uname):#获取维基节点图谱

    uid = show_wiki_related(uname)
    if not len(uid):
        return []
    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[r]-(m) return n.url,r,m,labels(m) LIMIT 200' % (wiki_url_index_name,wiki_primary,uid)

    p_result = graph.run(p_string)
    peo_list = []
    event_list = []
    wiki_list = []
    r_relation = []
    for item in p_result:
        node1 = item[0]
        if node1 not in wiki_list:
            wiki_list.append(node1)
        node2_k = item[3][0]
        node2_v = dict(item[2]).values()[0]
        r = item[1].type()
        if node2_k == people_node:#人物
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            r_relation.append([node1,node2_v,'people',r])
        elif node2_k == org_node:#机构
            if node2_v not in peo_list:
                peo_list.append(node2_v)
            r_relation.append([node1,node2_v,'org',r])
        elif node2_k == event_node:#事件
            if node2_v not in event_list:
                event_list.append(node2_v)
            r_relation.append([node1,node2_v,'event',r])
        else:
            continue

    if len(peo_list) > 0:
        result_peo = peo_id_name(peo_list)
    else:
        result_peo = {}
    if len(event_list) > 0:
        result_eve = event_id_name(event_list)
    else:
        result_eve = {}
    if len(wiki_list) > 0:
        result_wiki = wiki_id_name(wiki_list)
    else:
        result_wiki = {}

    relation = []
    for item in r_relation:
        flag = item[2]
        if flag == 'people':
            try:
                relation.append([item[0],result_wiki[item[0]],'wiki',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'org':
            try:
                relation.append([item[0],result_wiki[item[0]],'wiki',item[1],result_peo[item[1]],item[2],item[3]])
            except KeyError:
                continue
        elif flag == 'event':
            try:
                relation.append([item[0],result_wiki[item[0]],'wiki',item[1],result_eve[item[1]],item[2],item[3]])
            except KeyError:
                continue
        else:
            continue

    if len(relation) == 0:
        relation.append([uid,result_wiki[uid],'wiki','','','',''])

    return relation            
            
def get_people_geo(uid):#根据人物id查询人物的地图

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[]-(m) return m,labels(m) LIMIT 500' % (node_index_name,people_primary,uid)
    p_result = graph.run(p_string)
    peo_list = [uid]
    org_list = []
    event_list = []
    for item in p_result:
        id_key = dict(item[0]).values()[0]
        id_type = item[1][0]
        if id_type == people_node:
            peo_list.append(id_key)
        elif id_type == org_node:
            org_list.append(id_key)
        elif id_type == event_node:
            event_list.append(id_key)
        else:
            continue

    event_result = get_detail_event_map(event_list)
    people_result = get_detail_per_org_map(peo_list)
    org_relation = get_detail_per_org_map(org_list)
    
    return event_result,people_result,org_relation

def get_event_geo(uid):#根据事件id查询事件的地图

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[]-(m) return m,labels(m) LIMIT 500' % (event_index_name,event_primary,uid)
    p_result = graph.run(p_string)
    peo_list = []
    org_list = []
    event_list = [uid]
    for item in p_result:
        id_key = dict(item[0]).values()[0]
        id_type = item[1][0]
        if id_type == people_node:
            peo_list.append(id_key)
        elif id_type == org_node:
            org_list.append(id_key)
        elif id_type == event_node:
            event_list.append(id_key)
        else:
            continue

    event_result = get_detail_event_map(event_list)
    people_result = get_detail_per_org_map(peo_list)
    org_relation = get_detail_per_org_map(org_list)
    
    return event_result,people_result,org_relation

def get_org_geo(uid):#根据机构id查询机构的地图

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[]-(m) return m,labels(m) LIMIT 500' % (org_index_name,org_primary,uid)
    p_result = graph.run(p_string)
    peo_list = []
    org_list = [uid]
    event_list = []
    for item in p_result:
        id_key = dict(item[0]).values()[0]
        id_type = item[1][0]
        if id_type == people_node:
            peo_list.append(id_key)
        elif id_type == org_node:
            org_list.append(id_key)
        elif id_type == event_node:
            event_list.append(id_key)
        else:
            continue

    event_result = get_detail_event_map(event_list)
    people_result = get_detail_per_org_map(peo_list)
    org_relation = get_detail_per_org_map(org_list)
    
    return event_result,people_result,org_relation

def get_topic_geo(uid):#根据专题id查询专题的地图

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[]-(m) return m,labels(m) LIMIT 500' % (special_event_index_name,special_event_primary,uid)
    p_result = graph.run(p_string)
    event_list = []    
    for item in p_result:
        id_key = dict(item[0]).values()[0]
        id_type = item[1][0]
        if id_type == event_node:
            event_list.append(id_key)
        else:
            continue

    peo_list = []
    org_list = []
    for uid in event_list:
        p_string = 'START n=node:%s(%s="%s") MATCH (n)-[]-(m) return m,labels(m) LIMIT 500' % (event_index_name,event_primary,uid)
        p_result = graph.run(p_string)
        for item in p_result:
            id_key = dict(item[0]).values()[0]
            id_type = item[1][0]
            if id_type == people_node:
                peo_list.append(id_key)
            elif id_type == org_node:
                org_list.append(id_key)
            else:
                continue

    event_result = get_detail_event_map(event_list)
    people_result = get_detail_per_org_map(peo_list)
    org_relation = get_detail_per_org_map(org_list)
    
    return event_result,people_result,org_relation

def get_group_geo(uid):#根据群体id查询群体的地图

    p_string = 'START n=node:%s(%s="%s") MATCH (n)-[]-(m) return m,labels(m) LIMIT 500' % (group_index_name,group_primary,uid)
    p_result = graph.run(p_string)
    peo_list = []
    org_list = []
    for item in p_result:
        id_key = dict(item[0]).values()[0]
        id_type = item[1][0]
        if id_type == people_node:
            peo_list.append(id_key)
        elif id_type == org_node:
            org_list.append(id_key)
        else:
            continue

    event_result = []
    people_result = get_detail_per_org_map(peo_list)
    org_relation = get_detail_per_org_map(org_list)
    
    return event_result,people_result,org_relation

def get_all_geo():#地图链接：获取地址

##    event_list = []
##    p_string = 'START n=node:%s("%s:*") return n.event_id LIMIT 200' % (event_index_name,event_primary)
##    result = graph.run(p_string)
##    for item in result:
##        event_list.append(item[0])
##    event_result = get_detail_event_map(event_list)
##    
##    peo_list = []
##    p_string = 'START n=node:%s("%s:*") return n.uid LIMIT 300' % (node_index_name,people_primary)
##    result = graph.run(p_string)
##    for item in result:
##        peo_list.append(item[0])
##    peo_result = get_detail_per_org_map(peo_list)
##
##    org_list = []
##    p_string = 'START n=node:%s("%s:*") return n.org_id LIMIT 300' % (org_index_name,org_primary)
##    result = graph.run(p_string)
##    for item in result:
##        org_list.append(item[0])
##    org_result = get_detail_per_org_map(org_list)

    total_event = []
    p_string = 'START n=node:%s("%s:*") return n.event_id' % (event_index_name,event_primary)
    p_result = graph.run(p_string)
    for item in p_result:
        node1 = item[0]
        if node1 not in total_event:
            total_event.append(node1)

    if len(total_event) > 0:
        total_list,result_eve = event2time(total_event)
    else:
        total_list = []
        result_eve = {}
        
    peo_list = []
    org_list = []
    for e_id in total_list:
        p_string = 'START n=node:%s(%s="%s") MATCH (n)-[]-(m) return m,labels(m) LIMIT 200' % (event_index_name,event_primary,e_id)
        p_result = graph.run(p_string)    
        for item in p_result:
            node2_k = item[1][0]
            node2_v = dict(item[0]).values()[0]
            if node2_k == people_node:#人物
                if node2_v not in peo_list:
                    peo_list.append(node2_v)
            elif node2_k == org_node:#机构
                if node2_v not in org_list:
                    org_list.append(node2_v)
            elif node2_k == event_node:#事件
                if node2_v not in total_list:
                    total_list.append(node2_v)
            else:
                continue

    if len(peo_list) > 0:
        peo_result = get_detail_per_org_map(peo_list)
    else:
        peo_result = []
    if len(org_list) > 0:
        org_result = get_detail_per_org_map(org_list)
    else:
        org_result = []
    if len(total_list) > 0:
        event_result = get_detail_event_map(total_list)
    else:
        event_result = []
        
    return event_result,peo_result,org_result









        
