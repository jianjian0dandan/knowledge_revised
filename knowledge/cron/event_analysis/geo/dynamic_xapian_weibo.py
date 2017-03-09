# -*- coding: utf-8 -*-

import os
#from global_config import XAPIAN_WEIBO_TOPIC_DATA_PATH
#from xapian_case.xapian_backend import XapianSearch

def getXapianWeiboByDate(datestr):
    # datestr: 20130908    
    stub_file = path + datestr
    if os.path.exists(stub_file):
        print 'step--stub exist'
        xapian_search_weibo = XapianSearch(stub=stub_file, schema_version='5')
        return xapian_search_weibo
    else:
        print 'stub not exist'
        return None


def getXapianWeiboByTopic(topic_id='545f4c22cf198b18c57b8014'):
    stub_file = XAPIAN_WEIBO_TOPIC_DATA_PATH + 'stub/xapian_weibo_topic_stub_' + str(topic_id)
    if os.path.exists(stub_file):
        print 'stub exist'
        xapian_search_weibo = XapianSearch(stub=stub_file, schema_version='5')
        return xapian_search_weibo
    else:
        print 'stub not exist'
        return None

def getXapianWeiboByDuration(datestr_list):
    stub_file_list = []

    for datestr in datestr_list:
        stub_file = path + datestr
        if os.path.exists(stub_file):
            stub_file_list.append(stub_file)

    if len(stub_file_list):
        xapian_search_weibo = XapianSearch(stub=stub_file_list, include_remote=True, schema_version='5')
        return xapian_search_weibo

    else:
        return None
