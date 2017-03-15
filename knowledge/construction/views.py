# -*-coding:utf-8-*-
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect,make_response,request
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from utils import recommentation_in, recommentation_in_auto, submit_task
from knowledge.time_utils import ts2datetime, datetime2ts
from knowledge.parameter import RUN_TYPE, RUN_TEST_TIME, DAY

test_time = datetime2ts(RUN_TEST_TIME)


mod = Blueprint('construction', __name__, url_prefix='/construction')


@mod.route('/test/')
def add_node():
    return render_template('construction/test.html')

@mod.route('/show_in/')
def ajax_recommentation_in():
	#按影响力推荐，按敏感度推荐
    date = request.args.get('date', '2016-11-27') # '2013-09-01'
    recomment_type = request.args.get('type', 'influence')  #influence  sensitive
    submit_user = request.args.get('submit_user', 'admin') # 提交人
    input_ts = datetime2ts(date)
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = test_time
    if now_ts - 3600*24*7 >= input_ts:
        return json.dumps([])
    else:
        results = recommentation_in(input_ts, recomment_type, submit_user)
    return json.dumps(results)


# show auto recommentation
@mod.route('/show_auto_in/')
def ajax_show_auto_in():
	#按关注用户推荐
    date = request.args.get('date', '') # 2013-09-01
    submit_user = request.args.get('submit_user', 'admin')
    results = recommentation_in_auto(date, submit_user)
    if not results:
        results = []
    return json.dumps(results)


# 超级管理员确认入库
@mod.route('/admin_identify_in/')
def ajax_admin_identify_in():
    results = 0
    date = request.args.get('date', '') # date = '2013-09-07'
    uid_string = request.args.get('uid_list', '')
    uid_list = uid_string.split(',')
    uu_rel = request.args.get('uu_rel', '')  #a,b,c,d
    uu_rel_list = uu_rel.split(',')
    ue_rel = request.args.get('ue_rel', '')
    ue_rel_list = ue_rel.split(',')
    uo_rel = request.args.get('uo_rel', '')
    uo_rel_list = uo_rel.split(',')
    rel_list = [uu_rel_list, ue_rel_list, uo_rel_list,]
    status = request.args.get('status', '2') # 1 compute right now; 2 appointment
    recommend_style = request.args.get('recommend_style', '')
    submit_user  = request.args.get('submit_user', 'admin')
    ts = time.time()
    task_id = str(submit_user) + str(ts)
    status = submit_task(input_data)

    return json.dumps(results)

# submit group analysis task and save to redis as lists
# submit group task: task name should be unique
# input_data is dict ---two types
# one type: {'u_type':'user/organization', 'submit_date':x, 'uid_list':[], 'relation_list':[], 'cal_style':0/1, 'recommend_style':'', 'task_name':x, 'submit_user':submit_user}
# two type: {'u_type':'user/organization', 'submit_date':x, 'uid_file':filename, 'relation_list':[], 'cal_style':0/1, 'recommend_style':'file','task_name':x, 'submit_user':submit_user}
@mod.route('/submit_task/',methods=['GET', 'POST'])
def ajax_submit_task():
    input_data = dict()
    input_data = request.get_json()
    input_data = {'u_type':'user/organization', 'submit_date':'x', 'uid_list':json.dumps(['3036528532','5825134863']), 'relation_list':json.dumps(['friend']), 'cal_style':0, 'recommend_style':'', 'submit_user':'submit_user'}
    try:
        submit_user = input_data['submit_user']
    except:
        return 'no submit_user information'
    try:
    	task_name = input_data['task_name']
    except:
    	task_name = submit_user + '_' + str(int(time.time()))
        input_data['task_name'] = task_name
    task_id = submit_user + '_' + str(int(time.time()))
    input_data['task_id'] = task_id
    now_ts = int(time.time())
    input_data['submit_date'] = now_ts
    status = submit_task(input_data)
    return json.dumps(status)


# 手动输入
@mod.route('/submit_identify_in/', methods=['GET', 'POST'])
def ajax_submit_identify_in():
    results = 0 # mark fail
    input_data = request.get_json()
    #input_data={'date': 2016-03-13, 'upload_data':[], user':submit_user, 'operation_type': 'show'/'submit'} type=uid/uname/url 
    #upload_data stucture same to detect/views/mult_person
    print 'input_data:', input_data
    results = submit_identify_in(input_data)
    return json.dumps(results)

