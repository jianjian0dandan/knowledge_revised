# -*-coding:utf-8-*-
from global_utils import es_user_portrait as es
from  elasticsearch.helpers import scan
from elasticsearch.exceptions import RequestError
from global_config import *


# 对所有数据进行遍历。获取所有ID，每1万条当成一个数据。
def get_all_id():
    s_re = scan(es, query={'query': {'match_all': {}}, 'size': 2000000000000000000}, index='user_portrait',
                doc_type='user',
                scroll='10m', )
    result = []
    list = []
    count = 0
    while (1):
        try:
            count += 1
            item = s_re.next()["_id"]
            list.append(item)
            if count == 10000:
                result.append(list)
                list = []
                count = 0
        except RequestError:
            print "hahha"
            break
    return result



# 对人物进行对接
def people_calculate(time):
    query_body = {
        "query": {
            "term": {
                "create_time": time
            }
        }
    }
    result = es.search(index=portrait_name, doc_type=portrait_type,
                       body=query_body)['hits']['hits']
    return result


def get_es():
    query_search = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match_all": {}
                    }
                ],
                "must_not": [],
                "should": []
            }
        },
        "from": 0,
        "size": 1000000,
        "sort": [],
        "facets": {}
    }
    result = es.search(index=portrait_name, doc_type=portrait_type,
                       body=query_search)['hits']['hits']
    return result


def get_people_dict(time):
    result = people_calculate(time)
    dict = {}
    for item in result:
        id = item["_id"]
        influence = item["_source"]["influence"]
        importance = item["_source"]["importance"]
        activeness = item["_source"]["activeness"]
        sensitive = item["_source"]["sensitive"]
        dict[id] = {"influence": influence, "importance": importance, "activeness": activeness, "sensitive": sensitive}
    return dict

def get_people_max(time):
    influenceMax = 0
    importanceMax = 0
    activenessMax = 0
    sensitiveMax = 0
    influence_es = scan(es, query={'query': {"filtered": {
        "filter": {
            "bool": {
                "must": [
                    {"term": {"create_time": time}}]}
        }
    }}, 'sort': {'influence': {'order': 'acs'}}, 'size': 999999999}, index=portrait_name, scroll='10m',
                    doc_type=portrait_type)
    importance_es = scan(es, query={'query': {"filtered": {
        "filter": {
            "bool": {
                "must": [
                    {"term": {"create_time": time}}]}
        }
    }}, 'sort': {'importance': {'order': 'acs'}}, 'size': 999999999}, index=portrait_name, scroll='10m',
                     doc_type=portrait_type)

    activeness_es = scan(es, query={'query': {"filtered": {
        "filter": {
            "bool": {
                "must": [
                    {"term": {"create_time": time}}]}
        }
    }}, 'sort': {'activeness': {'order': 'acs'}}, 'size': 999999999}, index=portrait_name, scroll='10m',
                     doc_type=portrait_type)

    sensitive_es = scan(es, query={'query': {"filtered": {
        "filter": {
            "bool": {
                "must": [
                    {"term": {"create_time": time}}]}
        }
    }}, 'sort': {'sensitive': {'order': 'acs'}}, 'size': 999999999}, index=portrait_name, scroll='10m',
                     doc_type=portrait_type)
    try:
        influenceMax = influence_es.next()["_source"]["influence"]
        importanceMax =importance_es.next()["_source"]["importance"]
        activenessMax =activeness_es.next()["_source"]["activeness"]
        sensitiveMax =sensitive_es.next()["_source"]["sensitive"]
    except RequestError:
        print "hha"
    max_date={"influence":influenceMax,"importance":importanceMax,"activeness":activenessMax,"sensitive":sensitiveMax}
    return max_date

# 对事件进行对接
def event_calculate(time):
    query_body = {
        "query": {
            "term": {
                "submit_ts": time
            }
        }
    }
    result = es.search(index=event_analysis_name, doc_type=event_type,
                       body=query_body)['hits']['hits']
    return result

#获取事件信息
def get_event_dict(item):
    result = event_calculate(item)
    dict = {}
    for item in result:
        id = item["_id"]
        type = item["_source"]["event_type"]
        weibo = item["_source"]["weibo_counts"]
        people = item["_source"]["uid_counts"]
        text = item["_source"]["time_order_weibo"]
        text = eval(text)
        list = []
        for ls in text:
            list.append(ls[1]['text'])
        dict[id] = {"text": list, "type": type, "weibo": weibo, "people": people}
    return dict


def get_event_max(item):
    weiboMax = 0
    peopleMax = 0
    weibo_es = scan(es, query={'query': {"filtered": {
        "filter": {
            "bool": {
                "must": [
                    {"term": {"submit_ts": item}}]}
        }
    }}, 'sort': {'weibo_counts': {'order': 'acs'}}, 'size': 999999999}, index=event_analysis_name, scroll='10m',
                    doc_type=event_type)
    people_es = scan(es, query={'query': {"filtered": {
        "filter": {
            "bool": {
                "must": [
                    {"term": {"submit_ts": item}}]}
        }
    }}, 'sort': {'uid_counts': {'order': 'acs'}}, 'size': 999999999}, index=event_analysis_name, scroll='10m',
                     doc_type=event_type)  # ,raise_on_error=False
    try:
        weiboMax = weibo_es.next()["_source"]["weibo_counts"]
        peopleMax = people_es.next()["_source"]["uid_counts"]
    except RequestError:
        print "hha"
    dict ={"weibo":weiboMax,"people":peopleMax}
    return dict


# if __name__ == '__main__':
#
#     people_dict=get_people_dict()
#     max_date = get_people_max()
#     print  max_date
#     print people_dict





    # result = event_calculate()
    # result = get_es()
    # a = {"comput_status": 1, "name": "\u96fe\u973e", "end_ts": 1480176000, "start_ts": 1480003200, "en_name": "event_1480003200_1480176000_1483500427743", "weibo_counts": 73242, "finish_ts": 1483533025, "uid_counts": 50849, "submit_ts": 1483500427743}
    # print type(a)
    # for item in result:
    #     rel = item["_source"]["topic"]
    #     rel = rel.encode("utf-8")
    #     rel = rel[1:-1]
    #     rel = eval(rel)
    #     print type(rel)
    # dict = {"media": "","document":"","tag":""}
    # for item in result:
    #     print item["_id"]
    #     print es.update(index="user_portrait", doc_type="user",
    #           id=item["_id"],
    #           body={"doc":dict})
    # print "success"
    # es.update(index="event_analysis", doc_type="text", id=item["_id"],  body={"doc":{"text":"更新", "user_fansnum": 100}})
    # es.delete(index='event_analysis',doc_type='text',id='event-1480003100-1480176000-1483500427743')
