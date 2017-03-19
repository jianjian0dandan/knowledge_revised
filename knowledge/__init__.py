# -*- coding: utf-8 -*-

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from extensions import db, security, user_datastore, admin, User, Role, roles_users
from flask.ext.security import SQLAlchemyUserDatastore
from flask_admin.contrib import sqla
from knowledge.index.views import mod as indexModule
from knowledge.theme.views import mod as themeModule
from knowledge.group.views import mod as groupModule
from knowledge.relation.views import mod as relationModule
from knowledge.construction.views import mod as constructionModule
from knowledge.brust.views import mod as brustModule
from knowledge.sysadmin.views import mod as adminModule

import model

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost/knowledge_management?charset=utf8'
    #app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask-admin.db'

    # Create modules
    app.register_blueprint(indexModule)
    app.register_blueprint(themeModule)
    app.register_blueprint(groupModule)
    app.register_blueprint(relationModule)
    app.register_blueprint(constructionModule)
    app.register_blueprint(adminModule)
    app.register_blueprint(brustModule)

    app.config['DEBUG'] = True

    app.config['ADMINS'] = frozenset(['youremail@yourdomain.com'])
    app.config['SECRET_KEY'] = 'SecretKeyForSessionSigning'
    
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:@%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_HOST, MYSQL_DB)
    app.config['SQLALCHEMY_ECHO'] = False
    '''
    app.config['DATABASE_CONNECT_OPTIONS'] = {}

    app.config['THREADS_PER_PAGE'] = 8

    app.config['CSRF_ENABLED'] = True
    app.config['CSRF_SESSION_KEY'] = 'somethingimpossibletoguess'
    
    # Enable the toolbar?
    app.config['DEBUG_TB_ENABLED'] = app.debug
    # Should intercept redirects?
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    # Enable the profiler on all requests, default to false
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    # Enable the template editor, default to false
    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    # debug toolbar
    # toolbar = DebugToolbarExtension(app)

    # Create database
    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    # init security
    security.init_app(app, datastore=user_datastore)

    # init admin
    admin.init_app(app)
    admin.add_view(sqla.ModelView(User, db.session))
    admin.add_view(sqla.ModelView(Role, db.session))
    
    return app

