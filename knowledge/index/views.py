# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
mod = Blueprint('index', __name__, url_prefix='/index')

@mod.route('/')
@login_required
def index():#首页
    
    return render_template('index/knowledge_home.html')

@mod.route('/graph/')
@login_required
def get_graph():#图谱页面

    return render_template('index/knowledgeGraph.html')

@mod.route('/map/')
@login_required
def get_map():#地图页面

    return render_template('index/baidu_map.html')

@mod.route('/person/')
@login_required
def get_person():#人物属性页面

    return render_template('index/person.html')

@mod.route('/event/')
@login_required
def get_event():#事件属性页面

    return render_template('index/event.html')

@mod.route('/organization/')
@login_required
def get_organization():#机构属性页面

    return render_template('index/organization.html')

@mod.route('/cards/')
@login_required
def get_card():#卡片罗列页面

    return render_template('index/card_display.html')
