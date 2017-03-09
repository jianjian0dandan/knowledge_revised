# -*- coding: UTF-8 -*-
'''
test: search the user profile information from xapian
'''
import json
from xapian_case.xapian_backend import XapianSearch

XAPIAN_USER_DATA_PATH = '/home/xapian/xapian_user/'
xapian_search_user = XapianSearch(path=XAPIAN_USER_DATA_PATH, name='master_timeline_user', schema_version=1)

def search_uname2uid(uname):
    query_dict = {'name': uname}
    count, results = xapian_search_user.search(query=query_dict, fields=['_id', 'name'])
    if count != 0:
        for item in results():
            uid = item['_id']
    else:
        uid = None

    return uid
