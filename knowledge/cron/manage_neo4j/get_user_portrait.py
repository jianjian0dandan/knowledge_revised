# -*-coding:utf-8-*-

import time
import json
import redis
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


es = Elasticsearch("219.224.134.213:9200", timeout=600)
user_keys = ["domain", "uid", "importance", "influence", "activity_geo", "uname", "hashtag", "fansnum","tendency", "photo_url", "statusnum", "gender", "topic_string", "activeness", "location", "friendsnum", "character_sentiment", "character_text"]
es_scan = scan(es, query={"query":{"match_all":{}}, "size":1000}, index="user_portrait_1222", doc_type="user")
f = open("user_portrait.txt", "wb")
while 1:
    try:
        k = es_scan.next()
        scan_re = k["_source"]
        user_dict = dict()
        for key in user_keys:
            user_dict[key] = scan_re[key]
        f.write(json.dumps(user_dict)+"\n")
    except StopIteration:
        print "all done"
        break

f.close()


