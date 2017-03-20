# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime

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
