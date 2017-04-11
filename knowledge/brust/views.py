# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime

from utils import get_time_series, show_weibo_list, get_weibo_bursting, current_status


mod = Blueprint('brust', __name__, url_prefix='/brust')

@mod.route('/')
@login_required
def brust_discover():#热点发现

    return render_template('brust/brust_main.html')

@mod.route('/result/')
@login_required
def brust_analysis():#突发分析
    mid = request.args.get("mid", "")
    return render_template('brust/brust_analysis.html',mid=mid)

# show all weibo trendline
@mod.route('/show_weibo/')
def ajax_show_weibo():
    ts = request.args.get("ts", "")
    result = get_time_series()
    # results = show_weibo_detail()

    return json.dumps(result)


# show ts weibo
@mod.route("/show_weibo_list/")
def ajax_show_weibo_list():
    ts = request.args.get("ts", "1479571200")
    message_type = request.args.get("type", "1") # 1: origin, 3:retweet
    sort_item = request.args.get("sort", "retweeted") # 排序, retweeted, comment, timestamp, sensitive

    results = show_weibo_list(message_type,ts,sort_item)

    return json.dumps(results)


@mod.route('/show_weibo_bursting/')
def ajax_show_weibo_bursting():
    mid = request.args.get("mid", "")
    results = get_weibo_bursting(mid)

    return json.dumps(results)


# 热门转发和评论微博
@mod.route('/show_current_hot_weibo/')
def ajax_show_current_hot_weibo():
    mid = request.args.get("mid", "")
    results = current_status(mid)

    return json.dumps(results)




