# -*-coding:utf-8-*-
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
from neo4j_event import select_rels_all, select_rels, create_person, create_rel_from_uid2group,  \
    update_node, update_node_or_node_rel, delete_rel, delete_node,nodes_rels,get_es_status,select_event_es,\
    select_people_es
from knowledge.global_config import *
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from knowledge.global_utils import es_event, R_RECOMMENTATION as r
from knowledge.global_utils import es_user_portrait as es, portrait_index_name, portrait_index_type
from knowledge.global_utils import es_related_docs, user_docs_name, user_docs_type, event_docs_name, event_docs_type
from knowledge.global_config import event_task_name, event_task_type 
from utils import recommentation_in, recommentation_in_auto, submit_task, identify_in, submit_event, submit_event_file,\
                  relation_add, search_user, search_event, search_node_time_limit, show_node_detail, edit_node,\
                  deal_user_tag, create_node_or_node_rel, show_relation, update_event, submit_identify_in,\
                  node_delete, delete_relation, deal_event_tag, show_weibo_list, show_wiki, show_wiki_related,show_wiki_basic
from knowledge.time_utils import ts2datetime, datetime2ts, ts2datetimestr
from knowledge.parameter import RUN_TYPE, RUN_TEST_TIME, DAY
from knowledge.global_config import event_analysis_name, event_type
from knowledge.model import PeopleHistory, EventHistory
from knowledge.extensions import db

test_time = datetime2ts(RUN_TEST_TIME)
# from draw_redis import *

# from knowledge.global_utils import event_name_search

mod = Blueprint('construction', __name__, url_prefix='/construction')

@mod.route('/')
@login_required
def construction_main():#导航页
    return render_template('construction/construction_main.html')

@mod.route('/graph_add/')
@login_required
def construction_graph_add():#图谱添加
    return render_template('construction/graph_add.html')

@mod.route('/graph_modify/')
@login_required
def construction_graph_modify():#图谱编辑
    _type = request.args.get('_type', '')
    _id = request.args.get('_id', '')
    return render_template('construction/graph_modify.html',_id=_id,_type=_type)

@mod.route('/node/')
def add_node():
    return render_template('construction/addmap.html')

@mod.route('/wiki/')
def weiki():
    return render_template('construction/wiki.html')

@mod.route('/show_in/')
def ajax_recommentation_in():
    #按影响力推荐，按敏感度推荐
    date = request.args.get('date', '2016-11-27') # '2013-09-01'
    recomment_type = request.args.get('type', 'influence')  #influence  sensitive
    submit_user = request.args.get('submit_user', 'admin') # 提交人
    node_type = request.args.get('node_type', 'user') # user  org
    input_ts = datetime2ts(date)
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = test_time
    if now_ts - 3600*24*7 >= input_ts:
        return json.dumps([])
    else:
        results = recommentation_in(input_ts, recomment_type, submit_user, node_type)
    return json.dumps(results)

# show auto recommentation
@mod.route('/show_auto_in/')
def ajax_show_auto_in():
    #按关注用户推荐
    date = request.args.get('date', '2016-11-27') # 2013-09-01
    submit_user = request.args.get('submit_user', 'admin')
    node_type = request.args.get('node_type', 'user') # user  org
    results = recommentation_in_auto(date, submit_user, node_type)
    if not results:
        results = []
    return json.dumps(results)

# 推荐方式确认入库
@mod.route('/admin_identify_in/')
def ajax_admin_identify_in():
    results = 0
    date = request.args.get('date', '2016-11-27') # date = '2016-11-27'
    uid_string = request.args.get('uid_list', '1895944731,3811990435')
    uid_list = uid_string.split(',')
    relation_string = request.args.get('user_rel', 'friend,discuss') # split by ,
    status = request.args.get('status', '1') # 1 compute right now; 2 appointment
    recommend_style = request.args.get('recommend_style', 'influence')  #influence sensitive auto 
    node_type = request.args.get('node_type', '0') # '0':user  '1'：org
    submit_user  = request.args.get('submit_user', 'admin')
    data = []
    if date and uid_list:
        for uid in uid_list:
            print uid,'uid here!!!!!!!!'
            data.append([date, uid, status, relation_string, recommend_style, submit_user,node_type])
        results = identify_in(data,uid_list)
    else:
        results = 0
    return json.dumps(results)

# 立即更新人或机构
@mod.route('/update_user/')
def ajax_update_user():
    results = 0
    date = request.args.get('date', '2016-11-27') # date = '2016-11-27'
    node_type = request.args.get('node_type', '0') # '0':user  '1'：org
    uid = request.args.get('uid', '2298607941')
    recommend_style = request.args.get('recommend_style', 'influence')  #influence sensitive auto 
    submit_user  = request.args.get('submit_user', 'admin')
    relation_string = request.args.get('user_rel', 'friend') # split by ,
    relation_list = relation_string.split(',')
    r.rpush(uid, json.dumps([date, '1', node_type, relation_list, submit_user, recommend_style]))
    return json.dumps(1)

#上传文件方式人物入库
@mod.route('/submit_identify_in/', methods=['POST', 'GET' ])
def ajax_submit_identify_in():
    results = 0 # mark fail
    input_data = request.get_json()
    # print type(input_data),'=======!!!'
    #input_data={'date': 2016-03-13, 'upload_data':[],'node_type':'1/2', 'user':submit_user,'status':0,'relation_string':'', 'recommend_style':'upload/write', 'type':'uid', 'operation_type': 'show'/'submit'} 
    # input_data={'date': '2016-03-13', 'upload_data':[1198503091],'node_type':'0', 'user':'admin@qq.com','compute_status':'1','relation_string':'friend', 'recommend_style':'write',  'operation_type': 'submit'} 
    #upload_data stucture same to detect/views/mult_person
    # print 'input_data:', input_data
    results = submit_identify_in(input_data)  #[true, [sub_uid], [in_uid], [user_info]]
    return json.dumps(results)

#显示计算状态
@mod.route('/show_user_task_status/', methods=['GET', 'POST'])
def ajax_show_user_task_status():
    node_type = request.args.get('node_type', '0') # '0':user  '1'：org
    compute_name = 'compute'
    result = r.hgetall(compute_name)
    # return json.dumps(result)
    result_list = []
    for k,v in result.iteritems():
        detail = json.loads(v)
        if detail[2] == node_type:
            kv_list = [k]
            kv_list.extend(detail)
            result_list.append(kv_list)
        else:
            continue
    return json.dumps(result_list)

# show ts weibo
@mod.route("/show_weibo_list/")
def ajax_show_weibo_list():
    ts = request.args.get("ts", "1479571200")
    message_type = request.args.get("type", "1") # 1: origin, 3:retweet
    sort_item = request.args.get("sort", "retweeted") # 排序, retweeted, comment, timestamp, sensitive

    results = show_weibo_list(message_type,ts,sort_item)

    return json.dumps(results)

#事件提交任务,或手写
@mod.route('/submit_event/', methods=['GET', 'POST'])
def ajax_submit_event():
    input_data = dict()
    input_data = request.get_json()
    print input_data 
    # input_data = { 'submit_ts':'date', 'name':u'名&字', 'relation_list': 'join&discuss',\
    #            'cal_style':'cal_style', 'keywords':'keywords', 'start_ts':'start_ts', 'end_ts':'end_ts', 
    #            'event_type':'event_type', 'recommend_style':'recommend_style', 'status':0, 'submit_user':'admin','mid':'mid'}
    # input_data = {'submit_ts':'date', 'relation_compute': 'join&discuss',\
    #            'immediate_compute':'1', 'keywords':u'希拉里',
    #            'event_type':u'政治', 'recommend_style':'submit', 'compute_status':0, 'submit_user':'admin','event_ts':1480176000}
    result = submit_event(input_data)
    return json.dumps(result)

#事件更新
@mod.route('/event_update/')
def ajax_event_update():
    event_id = request.args.get('event_id', 'bei-jing-fang-jia-zheng-ce-1480176000') # '0':user  '1'：org
    relation_compute = request.args.get('relation_compute', '') #User , Org
    update_event(event_id, relation_compute)
    return '1'

#上传文件方式事件入库
@mod.route('/submit_event_file/', methods=['GET', 'POST'])
def ajax_submit_identify_file():
    results = 0 # mark fail
    input_data = request.get_json() #文件至少有keywords。
    # input_data={'submit_ts': '1480175030', 'immediate_compute':'1', 'relation_compute': 'join&discuss',
    # 'upload_data':[], 'submit_user':'admin','recommend_style':'file', 'compute_status':0} 
    #upload_data stucture same to detect/views/mult_person
    print 'input_data:', input_data
    results = submit_event_file(input_data)
    # print results,'===============00000000000'
    return json.dumps(results)  # True, submit_num

#事件任务状态
@mod.route('/show_event_task/')
def ajax_show_event_task():
    results = es_event.search(index=event_task_name, doc_type=event_task_type, body={"query":{"match_all":{}},"size":10000})['hits']['hits']
    result_list = []
    for i in results:
        result_list.append(i['_source'])
    return json.dumps(result_list)  #True submit_num

#关系添加，先搜点，事件的点需要改成事件名称
@mod.route('/search_node/')
def ajax_search_node():
    node_type = request.args.get('node_type', 'Event') #User , Org
    item = request.args.get('item', '1')
    if node_type == 'User' or node_type == 'Org':
        field = ['uid', 'uname']
        result = search_user(item, field,'', node_type)
    if node_type == 'Event':
        field = ['en_name', 'name']  
        result = search_event(item, field,'')
    return json.dumps(result)

#添加关系,上传文件
@mod.route('/relation_add/', methods=['GET', 'POST'])
def ajax_relation_add():
    # input_data = dict()
    input_data = request.get_json()
    # input_data = [['uid', u'5014862797', 'node_index', u'user_tag,测试2', 'uid',   \
    #              '2705119801', 'node_index']]  #other_relationship,测试   join
    result = relation_add(input_data)
    return json.dumps(result)  #[true] or[False, i(wrong num)]

#关系编辑，先查找
@mod.route('/relation_edit_search/', methods=['GET', 'POST'])
def ajax_relation_edit_search():
    node_type = request.args.get('node_type', 'User') #User , Org
    item = request.args.get('item', '1')
    if node_type == 'User' or node_type == 'Org':
        field = ['uid', 'uname']
        result = search_user(item, field, '', node_type)
    if node_type == 'Event':
        field = ['en_name', 'name']
        result = search_event(item, field, '')
    return json.dumps(result)

#关系编辑，先查询已有关系
@mod.route('/relation_show_edit/', methods=['GET', 'POST'])
def ajax_relation_show_edit():
    node_key1 = request.args.get('node_key1', 'uid')  # uid,event
    node1_id = request.args.get('node1_id', '2635695961')
    node1_index_name = request.args.get('node1_index_name', 'node_index')  # node_index event_index
    # rel = request.args.get('rel', '')
    node_key2 = request.args.get('node_key2', 'event_id')  # event_id,uid
    node2_id = request.args.get('node2_id', 'xi-la-li-1480176000')
    node2_index_name = request.args.get('node2_index_name', 'event_index')
    flag = show_relation(node_key1, node1_id, node1_index_name,  \
                                   node_key2, node2_id, node2_index_name)
    return json.dumps(flag)

#关系编辑，添加关系
@mod.route('/create_relation/')
def create_relation():
    node_key1 = request.args.get('node_key1', 'uid')  # uid,org_id, event_id
    node1_id = request.args.get('node1_id', '1497035431')
    node1_index_name = request.args.get('node1_index_name', 'node_index')  # node_index , org_index,event_index
    rel = request.args.get('rel', 'user_tag,0411')
    node_key2 = request.args.get('node_key2', 'uid')  # event,uid
    node2_id = request.args.get('node2_id', '2762995793')
    node2_index_name = request.args.get('node2_index_name', 'node_index')
    flag = create_node_or_node_rel(node_key1, node1_id, node1_index_name, rel, \
                                   node_key2, node2_id, node2_index_name)
    return json.dumps(flag)

#关系编辑，删除关系
@mod.route('/delete_relation/')
def ajax_delete_relation():
    node_key1 = request.args.get('node_key1', 'uid')  # uid,event
    node1_id = request.args.get('node1_id', '1565668374')
    node1_index_name = request.args.get('node1_index_name', 'node_index')  # node_index event_index
    rel = request.args.get('rel', u'friend')
    node_key2 = request.args.get('node_key2', 'uid')  # event,uid
    node2_id = request.args.get('node2_id', '2626682903')
    node2_index_name = request.args.get('node2_index_name', 'node_index')
    flag = delete_relation(node_key1, node1_id, node1_index_name, rel, \
                                   node_key2, node2_id, node2_index_name)
    return json.dumps(flag)

#节点编辑,查找展示表格
@mod.route('/node_edit_search/')
def ajax_node_edit():
    node_type = request.args.get('node_type', 'Event') #User , Org
    item = request.args.get('item', '1')
    editor = request.args.get('submit_user', 'admin@qq.com')  #admin
    start_ts = request.args.get('start_ts', '')  # 1504195000
    end_ts = request.args.get('end_ts', '')  # 1504195300
    if start_ts and end_ts:
        node_result = search_node_time_limit(node_type, item, start_ts, end_ts, editor)
    else:
        if node_type == 'User' or node_type == 'Org':
            field = ['uid', 'uname','location', 'influence', 'activeness', 'sensitive','keywords_string', 'function_mark']
            node_result = search_user(item, field, editor,node_type)
        if node_type == 'Event':
            # field = ['en_name', 'submit_ts',  'uid_counts', 'weibo_counts']
            field = ['en_name','name','event_type','real_time','real_geo','uid_counts','weibo_counts','keywords','work_tag','compute_status']
            node_result = search_event(item, field, editor)
    return json.dumps(node_result)

#特定节点编辑，先查找，展示
@mod.route('/node_edit_show/')
def ajax_node_edit_show():
    node_type = request.args.get('node_type', 'Org') #User , Org, Event
    item = request.args.get('item', '3230122083')  #id
    submit_user = request.args.get('submit_user', 'admin@qq.com')  #admin
    # item = request.args.get('item', 'ma-lai-xi-ya-zhua-huo-dian-xin-qi-zha-an-fan-1482126431')  #id
    result = show_node_detail(node_type, item, submit_user)
    # tag = deal_user_tag(item, submit_user, tag_value)[0]
    # result.append(tag)
    return json.dumps(result)

#特定节点删除
@mod.route('/node_delete/')
def ajax_node_delete():
    node_type = request.args.get('node_type', 'Event') #User , Org, Event
    item = request.args.get('item', '-1490615666')  #id
    submit_user = request.args.get('submit_user', 'admin@qq.com')  #admin
    # item = request.args.get('item', 'ma-lai-xi-ya-zhua-huo-dian-xin-qi-zha-an-fan-1482126431')  #id
    result = node_delete(node_type, item, submit_user)
    # tag = deal_user_tag(item, submit_user, tag_value)[0]
    # result.append(tag)
    return json.dumps(result)

#特定节点编辑，提交
@mod.route('/node_edit/')
def ajax_node_edit_():
    node_type = request.args.get('node_type', 'User') #User , Org
    item = request.args.get('item', '5779325975')  #id
    # item = request.args.get('item', 'xiang-gang-qian-zong-du-qian-ze-liang-you-er-ren-1482126431')  #id
    editor = request.args.get('submit_user', 'admin')  #admin
    # session = Session()
    if node_type == 'User' or node_type == 'Org':
        edit_num = 0
        field = [['topic_string', 'domain', 'function_description'],['related_docs'], ['function_mark']]
        for i in field[0]:
            i_value = request.args.get(i, '') #User , Org
            if i_value:
                edit_num += 1
                i_value = '&'.join(i_value.split(','))
                es.update(index=portrait_index_name,doc_type=portrait_index_type,id=item,body={'doc':{i:i_value}})
        for i in field[1]:
            i_value = request.args.get(i, '测试,www.baidu.com 测试2,www.weibo.com') #User , Org
            if i_value:
                edit_num += 1
                i_value = ' '.join(i_value.split(' '))
                try:
                    es_related_docs.update(index=user_docs_name,doc_type=user_docs_type, id=item,body={'doc':{i:i_value}})
                except:
                    es_related_docs.index(index=user_docs_name,doc_type=user_docs_type, id=item, body={i:i_value, 'uid':item})
        for i in field[2]:
            i_value = request.args.get(i, u'')
            if i_value:
                i_value = i_value
                edit_num += 1
                other_tag = deal_user_tag(item, editor)[1]
                if other_tag:
                    other_tag_l = other_tag
                else:
                    other_tag_l = []
                print other_tag_l,'other_tag_l1'
                user_tag = deal_user_tag(item, editor)[0]
                print user_tag,'user_tag'
                i_value = i_value.split(',')
                for ii in i_value:
                    other_tag_l.append(editor + '_' + ii)
                print other_tag_l
                tag_string = '&'.join(other_tag_l)
                es.update(index=portrait_index_name,doc_type=portrait_index_type,id=item,body={'doc':{i:tag_string}})
        if edit_num>0:
            pelple_history = PeopleHistory(name=editor, peopleID=item, modifyRecord='edit', modifyTime=datetime.now())
            db.session.add(pelple_history)
            db.session.commit()
        return json.dumps(True)
    elif node_type == 'Event':
        edit_num = 0
        field =  [['real_geo', 'real_time',  'event_type', 'real_person', 'real_auth', \
                   'start_ts', 'end_ts','description'], ['related_docs'], ['work_tag'],['real_time', 'start_ts', 'end_ts']]
        for i in field[0]:
            i_value = request.args.get(i, '') #User , Org
            if i_value:
                edit_num += 1
                i_value = '&'.join(i_value.split(','))
                es_event.update(index=event_analysis_name,doc_type=event_type,id=item,body={'doc':{i:i_value}})
        for i in field[1]:
            i_value = request.args.get(i, '') #User , Org
            if i_value:
                print i_value,'!!!!!!!!!1'
                edit_num += 1
                i_value = '+'.join(i_value.split(' '))
                # print i, i_value, event_docs_type, event_docs_name
                try:
                    es_related_docs.update(index=event_docs_name, doc_type=event_docs_type, id=item, body={'doc':{i:i_value}})
                except:
                    es_related_docs.index(index=event_docs_name, doc_type=event_docs_type, id=item, body={i:i_value, 'en_name':item})
        for i in field[2]:
            i_value = request.args.get(i, u'')
            if i_value:
                i_value = i_value
                edit_num += 1
                other_tag = deal_event_tag(item, editor)[1]
                event_tag = deal_event_tag(item, editor)[0]
                # print other_tag,'---------'
                if other_tag:
                    other_tag_l = other_tag
                else:
                    other_tag_l = []
                i_value = i_value.split(',')
                i_value = [ij for ij in set(i_value)]
                for ii in i_value:
                    # if ii not in event_tag:
                    other_tag_l.append(editor + '_' + ii)
                # print other_tag,'==========='
                tag_string = '&'.join(other_tag_l)
                es_event.update(index=event_analysis_name,doc_type=event_type,id=item,body={'doc':{i:tag_string}})
        for i in field[3]:
            i_value = request.args.get(i, '') #User , Org
            if i_value:
                edit_num += 1
                i_value = int(i_value)
                es_event.update(index=event_analysis_name,doc_type=event_type,id=item,body={'doc':{i:i_value}})
        if edit_num>0:
            event_history = EventHistory(name=editor, eventID=item, modifyRecord='edit', modifyTime=datetime.now())
            db.session.add(event_history)
            db.session.commit()
        return json.dumps(True)
    else:
        return '0'

@mod.route('/relation_edit/')


@mod.route('/relation/')
def add_relation():
    return render_template('construction/compile.html')


@mod.route('/read_file/', methods=['GET', 'POST'])
def read_node():
    f_name = request.form['new_words']

    uid_list = []
    line = f_name.split('\n')
    if len(line) == 0:
        return json.dumps('No Content!')

    for li in line:
        uid_list.append(li)

    return json.dumps(uid_list)

@mod.route('/read_relation/', methods=['GET', 'POST'])
def read_relation():
    f_name = request.form['new_words']

    uid_list = []
    line = f_name.split('\n')
    if len(line) == 0:
        return json.dumps('No Content!')

    for li in line:
        n1,t1,r,n2,t2 = li.split(',')
        uid_list.append([[t1,n1],r,[t2,n2]])

    return json.dumps(uid_list)


@mod.route('/select_relation/')
def select_relation():
    result_dict = {}
    list = []
    list1 = []
    result = select_rels_all("MATCH (n:Person)-[r]->(m) return n.uid,r,m.uid")
    for item in result:
        id = item[0]
        friend = item[1].type()
        print friend
        id2 = item[2]
        a = (id, friend, id2)
        list.append(a)
        list1.append(id)
        list1.append(id2)
    list1_set = [i for i in set(list1)]
    result_dict["relation"] = list
    result_dict["node"] = list1_set
    return json.dumps(result_dict)


# select node
@mod.route('/select_node/')
def select_node():
    list = []
    list_set = []
    result = select_rels_all("MATCH (n:Person)-[r]-() return n")
    for item in result:
        list.append(item)
    list_set = [i for i in set(list)]
    return json.dumps(list_set)


@mod.route('/select_event/')
def select_event_relation():
    result_dict = {}
    list = []
    list1 = []
    result = select_rels_all("MATCH (n:Person)-[r:admin]->(m) return n.uid,r,m.event_id")
    for item in result:
        id = item[0]
        friend = item[1].type()
        print friend
        id2 = item[2]
        a = (id, friend, id2)
        list.append(a)
        list1.append(id)
        list1.append(id2)
    list1_set = [i for i in set(list1)]
    result_dict["relation"] = list
    result_dict["node"] = list1_set
    return json.dumps(result_dict)


@mod.route('/select_event_node/')
def select_event_node():
    list = []
    list_set = []
    result = select_rels_all("MATCH (n:Person)-[r:admin]-(m) return n,m")
    for item in result:
        list.append(item[1])
        # list.append(item[2])
    list_set = [i for i in set(list)]
    return json.dumps(list_set)




@mod.route('/event_node_create/')
def add_node_event():
    event_name = request.args.get('event_name', '')
    event_type = request.args.get('event_type', '')
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    upload_time = request.args.get('upload_time', '')
    if event_name == '' or event_type == '' or start_time == '' or end_time == '' or upload_time == '':
        print ("event is null")
        return '0'
    event_push_redis(event_name, event_type, start_time, end_time, upload_time)
    return '1'


@mod.route('/user_upload_file/')
def upload_file():
    uid_list = request.args.get('uid_list', '')
    upload_time = request.args.get('upload_time', '')
    if uid_list == '' or upload_time == '':
        print ("null")
        return '0'
    print uid_list
    task_name = "user" + "-" + len(uid_list) + str(upload_time)
    user_push_redis(uid_list, task_name, upload_time)
    return '1'

# 对进来的数据进行模糊查询
@mod.route('/fuzzy_query/')
def fuzzy_query():
    node_type = request.args.get('node_type', 'User')  #Org, Event
    uid = request.args.get('uid', '1')
    if node_type == '' or uid == '':
        print "incoming there null"
        return '00'
    if node_type == 'User':  # user query
        c_string = "start n = node:%s('uid:*%s*') match (n) return n.uid order by n.id limit 10" % (node_index_name, uid)
        return c_string
        a = time.time()
        result = select_rels_all(c_string)
        print time.time()- a
        # result = select_people_es(result)
        return json.dumps(result)
    elif node_type == '2':  # event query
        c_string = "start n = node:%s('event:*%s*') match (n) return n order by n.id limit 10" % (event_index_name, uid)
        a = time.time()
        result = select_rels_all(c_string)
        print time.time()- a
        # result = select_event_es(result)
        return json.dumps(result)
    else:
        print "node_type is error"
        return '01'


# 对节点进行更新
@mod.route('/update_node/')
def update_nodes():
    node_type = request.args.get('node_type', '')
    uid = request.args.get('uid', '')
    attribute_dict = request.args.get('attribute_dict', '')
    if node_type == '' or uid == '' or attribute_dict == '':
        print "incoming there null"
        return '0'
    if node_type == '1':  # user update
        result = update_node("uid", uid, node_index_name, attribute_dict)
        if result:
            return "1"
        else:
            return "0"
    elif node_type == '2':  # event update
        result = update_node("event", uid, event_index_name, attribute_dict)
        if result:
            return "1"
        else:
            return "0"
    else:
        print "node_type is error"
        return "0"


# 删除节点   其中node_type代表传进来是对象，来判断是user还是event
@mod.route('/delete_node/')
def delete_nodes():
    node_type = request.args.get('node_type', '')
    uid = request.args.get('uid', '')
    if node_type == '' or uid == '':
        print "incoming there null"
        return '0'
    if node_type == '1':  # user update
        result = delete_node("uid", uid, node_index_name)
        if result:
            return "1"
        else:
            return "0"
    elif node_type == '2':  # event update
        result = delete_node("event", uid, event_index_name)
        if result:
            return "1"
        else:
            return "0"
    else:
        print "node_type is error"
        return "0"



@mod.route('/show_wiki/', methods=['GET', 'POST'])
def ajax_show_wiki():
    #
    input_data = request.get_json()
    input_data = {'name':u'中国城市生活质量指数列表','url':'https://wikipedia.kfd.me/wiki/%E4%B8%AD%E5%9B%BD%E5%9F%8E%E5%B8%82%E7%94%9F%E6%B4%BB%E8%B4%A8%E9%87%8F%E6%8C%87%E6%95%B0%E5%88%97%E8%A1%A8'}
    # print '0000000000000'
    results = show_wiki(input_data)
    html = "'''"
    html += results.encode("utf-8")
    html += "'''"
    return html

@mod.route('/show_wiki_basic/', methods=['GET', 'POST'])
def ajax_show_wiki_basic():
    #展示基本的
    input_data = request.get_json()
    input_data = {'name':u'中国城市生活质量指数列表','url':'https://wikipedia.kfd.me/wiki/%E4%B8%AD%E5%9B%BD%E5%9F%8E%E5%B8%82%E7%94%9F%E6%B4%BB%E8%B4%A8%E9%87%8F%E6%8C%87%E6%95%B0%E5%88%97%E8%A1%A8'}
    results = show_wiki_basic(input_data)
    # if not results:
    #     results = ''
    return json.dumps(results)

@mod.route('/show_wiki_related/', methods=['GET', 'POST'])
def ajax_show_wiki_related():
    #展示关联用户、机构、事件
    input_data = request.get_json()
    input_data = {'name':u'中国城市生活质量指数列表','url':'https://wikipedia.kfd.me/wiki/%E6%96%AF%E5%B8%8C%E6%B2%83%E9%87%8C%E7%BA%B3%E6%8B%89%E5%BB%B6'}
    results = show_wiki_related(input_data)
    # if not results:
    #     results = ''
    return json.dumps(results)


# 对2个节点的关系进行模糊查询
@mod.route('/node_or_node_query/')
def node_or_node_query():
    node1_uid = request.args.get('node1_uid', '')
    node1_type = request.args.get('node1_type','')
    node2_uid = request.args.get('node2_uid', '')
    node2_type = request.args.get('node2_type','')
    if node1_type== '2':
        node1_index_name=event_index_name
    else:
        node1_index_name=node_index_name
    if node2_type== '2':
        node2_index_name=event_index_name
    else:
        node2_index_name=node_index_name
    if node1_uid == '' or node2_uid == '':
        print ("incoming there null")
        return '0'
    c_string = "start start_node= node:%s('uid:*%s*'),end_node=node:%s('uid:*%s*') match (start_node)-[r]->(end_node) return start_node.uid,start_node.uname,r,end_node.uid,end_node.uname order by start_node.id limit 10" \
                % (node1_index_name, node1_uid, node2_index_name, node2_uid)
    print c_string
    result = select_rels_all(c_string)
    list = []
    for item in result:
        uid1 = item[0]
        uname1 = item[1]
        rel = item[2].type()
        uid2 = item[3]
        uname2 = item[4]

        result={}
        result["uid1"]=uid1
        result["uname1"]=uname1
        result["rel"]=rel
        result["uid2"]=uid2
        result["uname2"]=uname2
        list.append(result)
    return json.dumps(list)


# 对模糊查询的节点关系进行删除。
@mod.route('/node_or_node_delete/')
def node_or_node_delete():
    node1_uid = request.args.get('node1_uid', '')
    node2_uid = request.args.get('node2_uid', '')
    rel = request.args.get('rel', '')
    if node1_uid == '' or node2_uid == '':
        print "incoming there null"
    result = delete_rel('uid', node1_uid, node_index_name, rel, 'uid', node2_uid, node_index_name)
    if result:
        return '1'
    else:
        return '0'


# 对模糊查询的节点关系进行修改。
@mod.route('/node_or_node_update/')
def node_or_node_update():
    node1_uid = request.args.get('node1_uid', '')
    node2_uid = request.args.get('node2_uid', '')
    old_rel = request.args.get('old_rel', '')
    new_rel = request.args.get('new_rel', '')
    result =update_node_or_node_rel('uid',node1_uid,node_index_name,old_rel,new_rel,'uid',node2_uid,node_index_name)
    if result:
        return '1'
    else:
        return '0'

@mod.route('/nodes_or_nodes_rel/', methods=['GET', 'POST'])
def nodes_create_rels():
    result = request.args.get("list",'')
    result = result.split("|")
    list = []
    if len(result)==1:
        print "1"
        result =eval(result[0])
        list  = [[[result[0],result[1]],result[2],[result[3],result[4]]],]
    else :
        for item in result:
            item = eval(item)
            list.append([[item[0],item[1]],item[2],[item[3],item[4]]])
    result = nodes_rels(list)
    return json.dumps(result)



################################
@mod.route('/select_event_status/')
def select_event_status():
    list =[]
    results =get_es_status("event_status")
    for item in results:
        result= item["_source"]
        result["id"] =item["_id"]
        list.append(result)
    return json.dumps(list)


@mod.route('/select_user_status/')
def select_user_status():
    list =[]
    results =get_es_status("user_status")
    for item in results:
        result= item["_source"]
        result["id"] =item["_id"]
        list.append(result)
    return json.dumps(list)



@mod.route('/set_session/')
def set_session():
    response = make_response("hellow")
    response.set_cookie("Name","zhaishujie")
    return response

@mod.route('/get_session/')
def get_session():
    return request.cookies.get("Name")
