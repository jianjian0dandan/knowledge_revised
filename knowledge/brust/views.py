# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
import json
import csv
import os
import time
from datetime import date
from datetime import datetime

from utils import show_weibo_detail, show_weibo_list, get_weibo_bursting


mod = Blueprint('brust', __name__, url_prefix='/brust')

@mod.route('/test/')
def brust_analysis():

    return render_template('brust/test.html')



# show all weibo
@mod.route('/show_weibo/')
def ajax_show_weibo():
    ts = request.args.get("ts", "")
    results = show_weibo_detail()

    return json.dumps(results)


# show ts weibo
@mod.route("/show_weibo_list/")
def ajax_show_weibo_list():
    ts = request.args.get("ts", "")
    message_type = request.args.get("type", "1") # 1: origin, 3:retweet
    sort_item = request.args.get("sort", "retweeted") # 排序, retweeted, comment, timestamp, sensitive

    results = show_weibo_list(message_type,ts,sort_item)

    return json.dumps(results)


@mod.route('show_weibo_bursting')
def ajax_show_weibo_bursting():
    mid = request.args.get("mid", "")
    results = get_weibo_bursting(mid)

    return json.dumps(results)




