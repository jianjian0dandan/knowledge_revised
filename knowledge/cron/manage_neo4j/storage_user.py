# -*-coding:utf-8-*-

import json
from elasticsearch import Elasticsearch
import time

es = Elasticsearch("219.224.134.225:9037", timeout=600)

count = 0
bulk_action = []
with open("user_portrait.txt", "r") as f:
    for line in f:
        source = json.loads(line)
        source["create_time"] = time.time()
        _id = source["uid"]
        bulk_action.extend([{"index":{"_id":_id}}, source])
        count += 1
        if count % 1000 == 0:
            es.bulk(bulk_action, index="user_portrait", doc_type="user", timeout=600)
            bulk_action = []

if bulk_action:
    es.bulk(bulk_action, index="user_portrait", doc_type="user", timeout=600)

print "finish"
