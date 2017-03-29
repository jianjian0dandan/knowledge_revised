# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from knowledge.global_utils import get_theme,get_group
from knowledge.index.get_result import get_people,get_event,get_org

mod = Blueprint('sysadmin', __name__, url_prefix='/sysadmin')

@mod.route('/index/')
@login_required
def myfocus():#导航页

    return render_template('sysadmin/myfocus_index.html')

@mod.route('/topic/')
@login_required
def myfocus_topic():#我的专题

    return render_template('sysadmin/myfocus_topic.html')

@mod.route('/group/')
@login_required
def myfocus_group():#我的群体
    return render_template('sysadmin/myfocus_group.html')

@mod.route('/focus/')
@login_required
def myfocus_focus():#我的关注

    submit_user = g.user.email
    people_result = get_people(submit_user,'all')
    event_result = get_event(submit_user,'all')
    org_result = get_org(submit_user,'all')
    result = {'people':people_result,'event':event_result,'org':org_result}
    
    return render_template('sysadmin/myfocus_focus.html',result = result)

@mod.route('/topic/get_data')
def myfocus_topic_get_data():#我的专题

    submit_user = g.user.email
    result = get_theme('',submit_user)
    topic_list=[]
    for item in result:
        topic_dic={}
        topic_dic["name"] = item[1]
        topic_dic["count"] = item[2]
        topic_dic["auto_label"] = item[3]
        topic_dic["buss_label"] = item[4]
        topic_dic["time"] = item[5]
        topic_list.append(topic_dic)

    return json.dumps(topic_list)

@mod.route('/group/get_data')
def myfocus_group_get_data():#我的专题

    submit_user = g.user.email
    result = get_theme('',submit_user)
    group_list=[]
    for item in result:
        group_dic={}
        group_dic["name"] = item[1]
        group_dic["count"] = item[2]
        group_dic["auto_label"] = item[3]
        group_dic["buss_label"] = item[4]
        group_dic["time"] = item[5]
        group_list.append(group_dic)

    return json.dumps(group_list)