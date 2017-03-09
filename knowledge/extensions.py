# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import admin

db = SQLAlchemy()
admin = admin.Admin(name=u'XXX系统 数据库管理')
