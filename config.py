# -*- coding: utf-8 -*-


# the debug toolbar is only enabled in debug mode
DEBUG = True

ADMINS = frozenset(['youremail@yourdomain.com'])
SECRET_KEY = 'SecretKeyForSessionSigning'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@localhost/knowledge_management?charset=utf8'
SQLALCHEMY_ECHO = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY= 'somethingimpossibletoguess'
