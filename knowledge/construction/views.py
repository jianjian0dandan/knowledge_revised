# -*-coding:utf-8-*-
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect,make_response,request
import json
import csv
import os
import time
from datetime import date
from datetime import datetime


mod = Blueprint('construction', __name__, url_prefix='/construction')


@mod.route('/test/')
def add_node():
    return render_template('construction/test.html')


