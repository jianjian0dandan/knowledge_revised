# -*-coding:utf-8-*-
from knowledge.global_utils import r_user as r
from knowledge.global_utils import es_calculate_status as es
import json


def user_push_redis(uid_list, task_name, upload_time, ):
    result = [task_name, upload_time, uid_list]
    r.lpush("user_portrait_task", json.dumps(result))
    es.index(index="user_status", doc_type="text", id=task_name,
             body={"upload_time": upload_time, "status": 1, "uid": uid_list,
                   "user_count": len(uid_list), "founder": "zsj", "complete_time": 0})
    print "user redis success !"


def event_push_redis(event_name, event_type, start_time, end_time, upload_time):
    result = [event_name, event_type, start_time, end_time, upload_time]
    r.lpush("event_portrait_task", json.dumps(result))
    event_id = "event" + "-" + start_time + "-" + end_time + "-" + str(upload_time)
    es.index(index="event_status", doc_type="text", id=event_id,
             body={"upload_time": upload_time, "complete_time": 0, "status": 1, "founder": "zsj", "event": event_name,
                   "start_time": start_time, "end_time": end_time, "event_type": event_type})
    print "user redis success !"


def get_status(uid, es_index_name):
    es_results = es.get(index=es_index_name, doc_type="text", id=uid)
    return es_results["_source"]["status"]


def get_user_mapping():
    index_info = {
        'settings': {
            "number_of_replicas": 0,
            "number_of_shards": 5,
        },
        'mappings': {
            'text': {
                'properties': {
                    'founder': {
                        'type': 'string',
                        'index': 'no'
                    },
                    'upload_time': {
                        'type': 'long',
                        'index': 'no'
                    },
                    'complete_time': {
                        'type': 'long',
                        'index': 'no'
                    },

                    'status': {
                        'type': 'integer',
                        'index': 'no'
                    },
                    'uid': {
                        'type': 'string',
                        'index': 'no'
                    },
                    'user_count': {
                        'type': 'integer',
                        'index': 'no'
                    }
                }
            }
        }
    }
    return index_info


def get_event_mapping():
    index_info = {
        'settings': {
            "number_of_replicas": 0,
            "number_of_shards": 5,
        },
        'mappings': {
            'text': {
                'properties': {
                    'founder': {
                        'type': 'string',
                        'index': 'no'
                    },
                    'upload_time': {
                        'type': 'long',
                        'index': 'no'
                    },
                    'complete_time': {
                        'type': 'long',
                        'index': 'no'
                    },

                    'status': {
                        'type': 'integer',
                        'index': 'no'
                    },
                    'event': {
                        'type': 'string',
                        'index': 'no'
                    },
                    'start_time': {
                        'type': 'date',
                        'index': 'no'
                    },
                    'end_time': {
                        'type': 'date',
                        'index': 'no'
                    }
                }
            }
        }
    }
    return index_info
