# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
from knowledge.model import *
from knowledge.extensions import db
from knowledge.global_utils import get_theme,get_group
from knowledge.index.get_result import get_people,get_event,get_org
from knowledge.time_utils import ts2date

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
    return render_template('sysadmin/myfocus_focus.html')

@mod.route('/focus/get_focus_people_data')
def get_focus_people_data():

    submit_user = g.user.email
    people_result = get_people(submit_user,'all')
    print people_result

    return json.dumps(people_result)

@mod.route('/focus/get_focus_org_data')
def get_focus_org_data():

    submit_user = g.user.email
    org_result = get_org(submit_user,'all')
    
    return json.dumps(org_result)

@mod.route('/focus/get_focus_event_data')
def get_focus_event_data():

    submit_user = g.user.email
    event_result = get_event(submit_user,'all')
    
    return json.dumps(event_result)


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
def myfocus_group_get_data():#我的群体

    submit_user = g.user.email
    result = get_group('',submit_user)
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

@mod.route('/add_people/', methods=['GET','POST'])
def myfocus_add_people():#加入我的关注-人物

    result = 'Success'
    user_name = request.form['user_name']
    uid = request.form['uid']
    label = request.form['label']
    date_time = ts2date(time.time())
    old_items = db.session.query(PeopleAttention).filter((PeopleAttention.peopleID==uid)&(PeopleAttention.name==user_name)).all()
    if len(old_items):
        result = 'Exist'
    else:
        new_item = PeopleAttention(name=user_name, peopleID=uid, label=label, attentionTime=date_time)
        db.session.add(new_item)
        db.session.commit()

    return json.dumps(result)

@mod.route('/add_org/', methods=['GET','POST'])
def myfocus_add_org():#加入我的关注-机构

    result = 'Success'
    user_name = request.form['user_name']
    uid = request.form['uid']
    label = request.form['label']
    date_time = ts2date(time.time())
    old_items = db.session.query(OrgAttention).filter((OrgAttention.orgID==uid)&(OrgAttention.name==user_name)).all()
    if len(old_items):
        result = 'Exist'
    else:
        new_item = OrgAttention(name=user_name, orgID=uid, label=label, attentionTime=date_time)
        db.session.add(new_item)
        db.session.commit()

    return json.dumps(result)

@mod.route('/add_event/', methods=['GET','POST'])
def myfocus_add_event():#加入我的关注-机构

    result = 'Success'
    user_name = request.form['user_name']
    uid = request.form['uid']
    label = request.form['label']
    date_time = ts2date(time.time())
    old_items = db.session.query(EventAttention).filter((EventAttention.eventID==uid)&(EventAttention.name==user_name)).all()
    if len(old_items):
        result = 'Exist'
    else:
        new_item = EventAttention(name=user_name, eventID=uid, label=label, attentionTime=date_time)
        db.session.add(new_item)
        db.session.commit()

    return json.dumps(result)   

@mod.route('/delete_focus_people/', methods=['GET','POST'])
def myfocus_delete_focus_people():#删除关注的人
    
    submit_user = g.user.email
    people_id = request.args.get('people_id','')
    print people_id
    old_items = db.session.query(PeopleAttention).filter((PeopleAttention.peopleID==people_id)&(PeopleAttention.name==submit_user)).all()
    print old_items,submit_user
    for old_item in old_items:
        db.session.delete(old_item)
    db.session.commit()

    result = 'success'
    return json.dumps(result)   

@mod.route('/delete_focus_org/', methods=['GET','POST'])
def myfocus_delete_focus_org():#删除关注的人
    
    submit_user = g.user.email
    org_id = request.args.get('org_id','')
    print org_id
    old_items = db.session.query(OrgAttention).filter((OrgAttention.orgID==org_id)&(OrgAttention.name==submit_user)).all()
    print old_items,submit_user
    for old_item in old_items:
        db.session.delete(old_item)
    db.session.commit()

    result = 'success'
    return json.dumps(result)   

@mod.route('/delete_focus_event/', methods=['GET','POST'])
def myfocus_delete_focus_event():#删除关注的人
    
    submit_user = g.user.email
    event_id = request.args.get('event_id','')
    print event_id
    old_items = db.session.query(EventAttention).filter((EventAttention.eventID==event_id)&(EventAttention.name==submit_user)).all()
    print old_items,submit_user
    for old_item in old_items:
        db.session.delete(old_item)
    db.session.commit()

    result = 'success'
    return json.dumps(result)   

    
    
