# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
import json
import csv
import os
import time
from datetime import date
from datetime import datetime


mod = Blueprint('relation', __name__, url_prefix='/relation')

@mod.route('/test/')
def relation_index():

    return render_template('relation/test.html')



    
