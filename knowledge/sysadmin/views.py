# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
import json
import csv
import os
import time
from datetime import date
from datetime import datetime

mod = Blueprint('sysadmin', __name__, url_prefix='/sysadmin')

@mod.route('/test/')
def myfocus():

    return render_template('sysadmin/test.html')


