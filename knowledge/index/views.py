# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
mod = Blueprint('index', __name__, url_prefix='/index')

@mod.route('/login/')
def login():

    return render_template('index/login.html')

@mod.route('/')
def index():

    return render_template('index/knowledge_home.html')

@mod.route('/graph/')
def get_graph():

    return render_template('index/knowledgeGraph.html')

@mod.route('/map/')
def get_map():

    return render_template('index/baidu_map.html')

