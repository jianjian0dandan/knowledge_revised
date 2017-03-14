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
def index():
    
    return render_template('index/knowledge_home.html')

@mod.route('/graph/')
@login_required
def get_graph():

    return render_template('index/knowledgeGraph.html')

@mod.route('/map/')
@login_required
def get_map():

    return render_template('index/baidu_map.html')

