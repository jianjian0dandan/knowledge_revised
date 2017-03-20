# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required
import json
import csv
import os
import time
from datetime import date
from datetime import datetime

mod = Blueprint('theme', __name__, url_prefix='/theme')

@mod.route('/')
@login_required
def theme_analysis():#专题概览

    return render_template('theme/theme_main.html')

@mod.route('/add/')
@login_required
def theme_add():#新建专题

    return render_template('theme/theme_add.html')

@mod.route('/modify/')
@login_required
def theme_modify():#编辑专题

    return render_template('theme/theme_modify.html')

@mod.route('/compare/')
@login_required
def theme_compare():#专题对比

    return render_template('theme/theme_compare.html')

@mod.route('/result/')
@login_required
def theme_result():#专题查看

    return render_template('theme/theme_result.html')

