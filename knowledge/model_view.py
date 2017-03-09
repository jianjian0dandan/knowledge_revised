# -*- coding: utf-8 -*-

import codecs

from flask.ext import login
from flask.ext.admin.contrib import sqlamodel

# Create customized model view class
class SQLModelView(sqlamodel.ModelView):
    column_display_pk = True
    column_labels = {}
    with codecs.open(r'knowledge_management/i18n/db_zh_cn.txt', 'r', encoding='utf-8') as tf:
        for line in tf.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            db_col_name, view_name = line.split()
            column_labels[db_col_name] = view_name

    def __init__(self, model, session,
                 name=None, category=None, endpoint=None, url=None):
        super(SQLModelView, self).__init__(model, session,
                                          name=name, category=category, endpoint=endpoint, url=url)

    def is_accessible(self):
        return True
        # return login.current_user.is_authenticated()
