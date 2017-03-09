# -*- coding: utf-8 -*-
import requests,json,copy
#from cron.info_consume.event_compute_topic import counts
#datapend({'topic':'aoyunhui','start_ts':1468944000,'end_ts':1471622400})
#r = requests.get('http://10.128.55.83:9003/topic_geo_analyze/geo_weibo_count/',params=data_dict)
data_list = []
#data_list.append({'topic':'数据库','keywords':'北京  数据库','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'老太熬夜卖菜为儿子买房','keywords':'老太  熬夜 卖菜','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'运钞车击毙男子获赔偿','keywords':'运钞车  击毙  获赔','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'西安护士怀孕二胎被迫辞职','keywords':'西安  护士  二胎  辞职','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'日本讨论部署萨德系统','keywords':'日本  部署 萨德','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'新加坡装甲车在香港被扣','keywords':'新加坡  装甲车  被扣','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'中国知识产权申请量世界第一','keywords':'中国  知识产权  第一','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'怀孕女教师被家长殴打','keywords':'怀孕  女教师  殴打','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'香港前总督谴责梁游二人','keywords':'彭定康  梁颂恒  梁颂恒','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'公安部挂牌督办十大电信欺诈案件','keywords':'公安部  督办 电信  诈骗','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'民进党议员称邀请达赖对抗大陆','keywords':'民进党  达赖 大陆','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'澳门选举法新增加爱国条例','keywords':'澳门  选举法 新增','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
data_list.append({'topic':'马来西亚抓获电信欺诈案犯','keywords':'电信  诈骗 马来西亚','start_ts':1480262400,'end_ts':1480867200,'submit_user':'admin'})
#data_list.append({'topic':'lao-tai-ao-ye-mai-cai-wei-er-zi-mai-fang-1482079340','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'yun-chao-che-ji-bi-nan-zi-huo-pei-chang-1482079340','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'xi-an-hu-shi-huai-yun-er-tai-bei-po-ci-zhi-1482079340','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'ri-ben-tao-lun-bu-shu-sa-de-xi-tong-1482071912','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'ri-ben-tao-lun-bu-shu-sa-de-xi-tong-1482071912','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'zhong-guo-zhi-shi-chan-quan-shen-qing-liang-shi-jie-di-yi-1482079340','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'huai-yun-nv-jiao-shi-bei-jia-chang-ou-da-1482079340','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'xiang-gang-qian-zong-du-qian-ze-liang-you-er-ren-1482079340','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'gong-an-bu-gua-pai-du-ban-shi-da-dian-xin-qi-zha-an-jian-1482127322','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'min-jin-dang-yi-yuan-cheng-yao-qing-da-lai-dui-kang-da-lu-1482126431','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'ao-men-xuan-ju-fa-xin-zeng-jia-ai-guo-tiao-li-1482126431','start_ts':1480262400,'end_ts':1480867200})
#data_list.append({'topic':'ma-lai-xi-ya-zhua-huo-dian-xin-qi-zha-an-fan-1482076312','start_ts':1480262400,'end_ts':1480867200})
#datapend({'topic':'范冰冰','start_ts':1479571200,'end_ts':1480435200,'submit_user':'admin'})
for i in data_list:
    #print i
    result = {}
    
    r = requests.get('http://10.128.55.83:9003/topic_language_analyze/search_topic_by_topic/',params={'topic':i['topic']})
    result['topic'] = json.loads(r.text)
    print result
    #r = requests.get('http://10.128.55.83:9003/topic_language_analyze/submit_task/',params=i)
    i['topic']=result['topic'][0]['en_name'] 
    sql_find=copy.deepcopy(i)
    sql_find['topic']=sql_find['topic'][:20]
    sql_find['pointInterval']=21600
    #r = requests.get('http://10.128.55.83:9003/topic_sen_analyze/sen_time_count/',params=sql_find)
    #result['sen_time_count'] = json.loads(r.text)
    #print result['sen_time_count']
    '''
    r = requests.get('http://10.128.55.83:9003/topic_geo_analyze/geo_weibo_count/',params=sql_find)
    result['geo_weibo_count'] = json.loads(r.text)
    r = requests.get('http://10.128.55.83:9003/topic_language_analyze/topics_river/',params=i)
    result['topics_river'] = json.loads(r.text)
    r = requests.get('http://10.128.55.83:9003/topic_language_analyze/search_topics/',params={'keyword':i['topic']})
    result['topic'] = json.loads(r.text)
    r = requests.get('http://10.128.55.83:9003/topic_sen_analyze/sen_time_count/',params=sql_find)
    result['sen_time_count'] = json.loads(r.text)
    r = requests.get('http://10.128.55.83:9003/topic_network_analyze/get_trend_maker/',params=sql_find)
    result['trend_maker'] = json.loads(r.text)
    r = requests.get('http://10.128.55.83:9003/topic_network_analyze/get_trend_pusher/',params=sql_find)
    result['trend_pusher'] = json.loads(r.text)
    r = requests.get('http://10.128.55.83:9003/topic_network_analyze/get_pagerank/',params=sql_find)
    result['pagerank'] = json.loads(r.text)
    r = requests.get('http://10.128.55.83:9003/topic_time_analyze/time_order_weibos/',params=i)
    result['time_order_weibo'] = json.loads(r.text)
    '''
    #r = requests.get('http://10.128.55.83:9003/topic_language_analyze/weibo_count/',params=i)
    #result['counts'] = json.loads(r.text)
    #print r.text
    print sql_find
    #r = requests.get('http://10.128.55.83:9003/topic_time_analyze/mtype_count/',params=sql_find)
    #result['time_type_weibo'] = json.loads(r.text)
    r = requests.get('http://10.128.55.83:9003/topic_time_analyze/time_order_weibos/',params=i)
    result['time_order_weibo'] = json.loads(r.text)
     
    #print result['time_type_weibo']
    f=open('1230/'+i['topic']+'_new.txt','w')
    f.write(json.dumps(result))
    f.close()
    #print json.loads(r.text)
    

