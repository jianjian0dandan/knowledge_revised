# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
import json
import csv
import os
import time
from datetime import date
from datetime import datetime
import csv

mod = Blueprint('group', __name__, url_prefix='/group')

@mod.route('/test/')
def group():
    return render_template('group/test.html')
