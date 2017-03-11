# -*- coding: utf-8 -*-
"""使用svm分类器过滤垃圾
"""

import os
from utils import _default_mongo
from config import MONGO_DB_NAME, SUB_EVENTS_COLLECTION, \
        EVENTS_NEWS_COLLECTION_PREFIX, EVENTS_COLLECTION, COMMENT_COLLECTION

import sys
AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libsvm-3.17/python/')
sys.path.append(AB_PATH)
from sta_ad import test, choose_ad

def rubbish_filter(items, topicid):
    """svm 垃圾过滤器
    """
    texts = [item['content168'] for item in items]
    test(texts, topicid)
    labels = choose_ad(topicid)

    return labels

if __name__=="__main__":
    topic = "APEC2014"
    topicid = "54916b0d955230e752f2a94e"
    mongo = _default_mongo(usedb=MONGO_DB_NAME)
    results = mongo[COMMENT_COLLECTION + topicid].find()
    results = [r for r in results]

    from ad_filter import ad_filter

    rubbish_filter_inputs = []
    for r in results:
        r['content168'] = r['content168'].encode('utf-8')
        text, label = ad_filter(r)
        if label == 0:
            rubbish_filter_inputs.append(r)

    #libsvm垃圾过滤
    results = rubbish_filter(rubbish_filter_inputs, topicid)

