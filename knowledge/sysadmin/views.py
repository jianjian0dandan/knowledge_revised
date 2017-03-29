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

    submit_user = g.user.email
    result = get_theme('',submit_user)
    
    return render_template('sysadmin/myfocus_topic.html',result = result)

@mod.route('/group/')
@login_required
def myfocus_group():#我的群体

    submit_user = g.user.email
    result = get_group('',submit_user)
    
    return render_template('sysadmin/myfocus_group.html',result = result)

@mod.route('/focus/')
@login_required
def myfocus_focus():#我的关注

    submit_user = g.user.email
    people_result = get_people(submit_user,'all')
    event_result = get_event(submit_user,'all')
    org_result = get_org(submit_user,'all')
    result = {'people':people_result,'event':event_result,'org':org_result}
    
    return render_template('sysadmin/myfocus_focus.html',result = result)
