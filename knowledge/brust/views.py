# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
import json
import csv
import os
import time
from datetime import date
from datetime import datetime

mod = Blueprint('brust', __name__, url_prefix='/brust')

@mod.route('/test/')
def brust_analysis():

    return render_template('brust/test.html')

