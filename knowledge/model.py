# -*- coding: utf-8 -*-

from extensions import db

__all__ = ['User', 'Topic', 'Group', 'PeopleAttention', 'EventAttention', 'PeopleHistory', 'EventHistory']

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)#系统用户名
    password = db.Column(db.String(20))#密码

    def __init__(self, name, password):
        self.name = name
        self.password = password

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    topicName = db.Column(db.String(50))#专题名称
    event = db.Column(db.Text)#主要事件（top5）
    eventCount = db.Column(db.Integer)#事件数量
    createTime = db.Column(db.Date)#创建时间
    modifyTime = db.Column(db.Date)#最近修改时间

    def __init__(self, name, topicName, event, eventCount, createTime, modifyTime):
        self.name = name
        self.topicName = topicName
        self.event = event
        self.eventCount = eventCount
        self.createTime = createTime
        self.modifyTime = modifyTime

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    groupName = db.Column(db.String(50))#群体名称
    people = db.Column(db.Text)#主要人物（top5）
    peopleCount = db.Column(db.Integer)#人物数量
    createTime = db.Column(db.Date)#创建时间
    modifyTime = db.Column(db.Date)#最近修改时间

    def __init__(self, name, groupName, people, peopleCount, createTime, modifyTime):
        self.name = name
        self.groupName = groupName
        self.people = people
        self.peopleCount = peopleCount
        self.createTime = createTime
        self.modifyTime = modifyTime

class PeopleAttention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    peopleID = db.Column(db.String(20))#人物id
    label = db.Column(db.String(20))#人物的业务标签
    attentionTime = db.Column(db.Date)#关注时间

    def __init__(self, name, peopleID, label, attentionTime):
        self.name = name
        self.peopleID = peopleID
        self.label = label
        self.attentionTime = attentionTime

class EventAttention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))#系统用户名
    eventID = db.Column(db.String(20))#事件id
    label = db.Column(db.String(20))#事件的业务标签
    attentionTime = db.Column(db.Date)#关注时间

    def __init__(self, name, eventID, label, attentionTime):
        self.name = name
        self.eventID = eventID
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
    eventID = db.Column(db.String(20))#事件id
    modifyRecord = db.Column(db.Text)#修改记录
    modifyTime = db.Column(db.Date)#修改时间

    def __init__(self, name, eventID, modifyRecord, modifyTime):
        self.name = name
        self.eventID = eventID
        self.modifyRecord = modifyRecord
        self.modifyTime = modifyTime

