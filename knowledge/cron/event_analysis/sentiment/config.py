# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from xapian_weibo.xapian_backend import XapianSearch

cron_start = '2013-9-1'
cron_end = '2013-9-6'
SIMULATE_BASE_DATE = '2013-12-22 19:00:00'

emotions_kv = {'happy': 1, 'angry': 2, 'sad': 3, 'news': 4}
emotions_zh_kv = {'happy': '高兴', 'angry': '愤怒', 'sad': '悲伤', 'news': '新闻'}
fields_value = ['culture', 'education', 'entertainment', 'fashion', 'finance', 'media', 'sports', 'technology', 'oversea']
fields_id = {'culture': 1, 'education': 2, 'entertainment': 3, 'fashion': 4, 'finance': 5, 'media': 6, 'sports': 7, 'technology': 8, 'oversea': 9}

DOMAIN_LIST = ['culture', 'education', 'entertainment', 'fashion', 'finance', 'media', 'sports', 'technology', 'oversea', \
               'university', 'homeadmin', 'abroadadmin', 'homemedia', 'abroadmedia', 'folkorg', \
               'lawyer', 'politician', 'mediaworker', 'activer', 'grassroot', 'other']

IS_PROD = 3

if IS_PROD == 1:
    # XAPIAN_WEIBO_DATA_PATH = '/opt/xapian_weibo/data/20131210/'
    XAPIAN_USER_DATA_PATH = '/media/data/'
    # XAPIAN_DOMAIN_DATA_PATH = '/opt/xapian_weibo/data/20131130/'
    MASTER_TIMELINE_STUB = '/home/ubuntu12/dev/data/stub/master_timeline_weibo_stub'
    LEVELDBPATH = '/media/data/leveldb'
    COBAR_HOST = '192.168.2.31'
    COBAR_PORT = 8066
    COBAR_USER = 'cobar'
    REDIS_HOST = '192.168.2.31'
    REDIS_PORT = 6379
    MYSQL_DB = 'weibo'
    MYSQL_HOST = '192.168.2.31'
    MYSQL_USER = 'root'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://%s:@%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_HOST, MYSQL_DB)
    DYNAMIC_XAPIAN_WEIBO_STUB_PATH = '/home/ubuntu12/dev/data/stub/master_timeline_weibo_'
elif IS_PROD == 2:
    XAPIAN_WEIBO_DATA_PATH = '/opt/xapian_weibo/data/20131210/'
    XAPIAN_USER_DATA_PATH = '/opt/xapian_weibo/data/20131221/'
    XAPIAN_DOMAIN_DATA_PATH = '/opt/xapian_weibo/data/20131130/'
    MASTER_TIMELINE_STUB = '/home/mirage/dev/data/stub/master_timeline_weibo_stub'
    LEVELDBPATH = '/home/mirage/leveldb'
    REDIS_HOST = '219.224.135.60'
    REDIS_PORT = 6379
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@localhost/weibo?charset=utf8'
    DYNAMIC_XAPIAN_WEIBO_STUB_PATH = '/home/mirage/dev/data/stub/master_timeline_weibo_'
elif IS_PROD == 3:
    XAPIAN_WEIBO_DATA_PATH = '/home/ubuntu3/huxiaoqian/case/20140724/20140804/'
    XAPIAN_USER_DATA_PATH = '/home/ubuntu4/huxiaoqian/mcase/data/user-datapath/'
    XAPIAN_DOMAIN_DATA_PATH = '/opt/xapian_weibo/data/20131130/'  #无
    MASTER_TIMELINE_STUB = '/home/mirage/dev/data/stub/master_timeline_weibo_stub' #无
    LEVELDBPATH = '/home/ubuntu3/huxiaoqian/case_test/data/leveldbpath/' # 无  
    REDIS_HOST = '219.224.135.49'  #索引的redis服务器为49，应该用不到
    REDIS_PORT = 6379
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@219.224.134.223/weibocase?charset=utf8'
    DYNAMIC_XAPIAN_WEIBO_STUB_PATH = '/home/ubuntu4/ljh/csv/stub/topic/master_timeline_weibo_topic'
    

SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@219.224.134.223/weibocase?charset=utf8'

# Create application
app = Flask('xxx')

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)


def split_city(geo):
    geo = geo.split('&')
    if geo[0] == '中国':
        province = geo[1]
        try:
            city = geo[2]
        except:
            city = 'unknown'
    else:
        province = 'unknown'
        city = 'unknown'
    return province,city