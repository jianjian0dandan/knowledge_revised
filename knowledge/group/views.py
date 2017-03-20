# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
import csv

mod = Blueprint('group', __name__, url_prefix='/group')

@mod.route('/')
@login_required
def group_analysis():#群体概览

    return render_template('group/group_main.html')

@mod.route('/add/')
@login_required
def group_add():#新建群体

    return render_template('group/group_add.html')

@mod.route('/modify/')
@login_required
def group_modify():#编辑群体

    return render_template('group/group_modify.html')

@mod.route('/compare/')
@login_required
def group_compare():#群体对比

    return render_template('group/group_compare.html')

@mod.route('/result/')
@login_required
def group_result():#群体查看

    return render_template('group/group_result.html')
