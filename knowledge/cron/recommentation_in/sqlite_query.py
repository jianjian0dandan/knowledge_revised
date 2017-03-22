# -*- coding: utf-8 -*-

from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost/knowledge_management?charset=utf8' 
db = SQLAlchemy(app)

__all__ = ['Topic', 'Group', 'PeopleAttention', 'EventAttention', 'OrgAttention', 'PeopleHistory', 'EventHistory', 'OrgHistory',\
           'TopicHistory', 'GroupHistory']

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    topicName = db.Column(db.String(200))#专题名称
    event = db.Column(db.Text)#主要事件（top5）
    eventCount = db.Column(db.Integer)#事件数量
    createTime = db.Column(db.Date)#创建时间
    modifyTime = db.Column(db.Date)#最近修改时间
    label = db.Column(db.Text)#业务标签
    k_label = db.Column(db.Text)#自动标签

    def __init__(self, name, topicName, event, eventCount, createTime, modifyTime, label, k_label):
        self.name = name
        self.topicName = topicName
        self.event = event
        self.eventCount = eventCount
        self.createTime = createTime
        self.modifyTime = modifyTime
        self.label = label
        self.k_label = k_label

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    groupName = db.Column(db.String(200))#群体名称
    people = db.Column(db.Text)#主要人物（top5）
    peopleCount = db.Column(db.Integer)#人物数量
    createTime = db.Column(db.Date)#创建时间
    modifyTime = db.Column(db.Date)#最近修改时间
    label = db.Column(db.Text)#业务标签
    k_label = db.Column(db.Text)#自动标签

    def __init__(self, name, groupName, people, peopleCount, createTime, modifyTime, label, k_label):
        self.name = name
        self.groupName = groupName
        self.people = people
        self.peopleCount = peopleCount
        self.createTime = createTime
        self.modifyTime = modifyTime
        self.label = label
        self.k_label = k_label

class PeopleAttention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    peopleID = db.Column(db.String(20))#人物id
    label = db.Column(db.String(200))#人物的业务标签
    attentionTime = db.Column(db.Date)#关注时间

    def __init__(self, name, peopleID, label, attentionTime):
        self.name = name
        self.peopleID = peopleID
        self.label = label
        self.attentionTime = attentionTime

class EventAttention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    eventID = db.Column(db.String(200))#事件id
    label = db.Column(db.String(200))#事件的业务标签
    attentionTime = db.Column(db.Date)#关注时间

    def __init__(self, name, eventID, label, attentionTime):
        self.name = name
        self.eventID = eventID
        self.label = label
        self.attentionTime = attentionTime

class OrgAttention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    orgID = db.Column(db.String(20))#机构id
    label = db.Column(db.String(200))#事件的业务标签
    attentionTime = db.Column(db.Date)#关注时间

    def __init__(self, name, orgID, label, attentionTime):
        self.name = name
        self.orgID = orgID
        self.label = label
        self.attentionTime = attentionTime

class PeopleHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    peopleID = db.Column(db.String(20))#人物id
    modifyRecord = db.Column(db.Text)#修改记录
    modifyTime = db.Column(db.Date)#修改时间

    def __init__(self, name, peopleID, modifyRecord, modifyTime):
        self.name = name
        self.peopleID = peopleID
        self.modifyRecord = modifyRecord
        self.modifyTime = modifyTime

class EventHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    eventID = db.Column(db.String(200))#事件id
    modifyRecord = db.Column(db.Text)#修改记录
    modifyTime = db.Column(db.Date)#修改时间

    def __init__(self, name, eventID, modifyRecord, modifyTime):
        self.name = name
        self.eventID = eventID
        self.modifyRecord = modifyRecord
        self.modifyTime = modifyTime

class OrgHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    orgID = db.Column(db.String(20))#机构id
    modifyRecord = db.Column(db.Text)#修改记录
    modifyTime = db.Column(db.Date)#修改时间

    def __init__(self, name, orgID, modifyRecord, modifyTime):
        self.name = name
        self.orgID = orgID
        self.modifyRecord = modifyRecord
        self.modifyTime = modifyTime

class TopicHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    topicName = db.Column(db.String(200))#专题名称
    modifyRecord = db.Column(db.Text)#修改记录
    modifyTime = db.Column(db.Date)#修改时间

    def __init__(self, name, topicName, modifyRecord, modifyTime):
        self.name = name
        self.topicName = topicName
        self.modifyRecord = modifyRecord
        self.modifyTime = modifyTime

class GroupHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    groupName = db.Column(db.String(200))#群体名称
    modifyRecord = db.Column(db.Text)#修改记录
    modifyTime = db.Column(db.Date)#修改时间

    def __init__(self, name, groupName, modifyRecord, modifyTime):
        self.name = name
        self.groupName = orgID
        self.modifyRecord = modifyRecord
        self.modifyTime = modifyTime
