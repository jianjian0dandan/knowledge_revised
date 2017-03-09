# -*- coding: utf-8 -*-

import os
import re
import csv
import time
import pynlpir
from pynlpir import nlpir
from text_process import get_keyword
from config import re_cut

pynlpir.open()
nh_set = ['personal name','Japanese personal name','transcribed personal name']
ns_set = ['toponym','transcribed toponym']
ni_set = ['organization/group name']
nt_set = ['time word','time morpheme']
time_list = ['年','月','日','时','分']
YEAR = time.strftime('%Y',time.localtime(time.time()))

def get_time(w):

    flag = 0
    for i in time_list:
        if i in w:
            index = w.find(i)
            try:
                item = int(w[0:index])
            except ValueError:
                continue
            flag = 1
            break

    return flag

def get_pos(text,nh_dict,ns_dict,nt_dict,ni_dict,title):

    result = pynlpir.segment(text, pos_names='child')
    for w1,c in result:
        w = w1.encode('utf-8')
        if c in ni_set:
            if w in title:
                try:
                    ni_dict[w] = ni_dict[w] + 2
                except KeyError:
                    ni_dict[w] = 2
            else:
                try:
                    ni_dict[w] = ni_dict[w] + 1
                except KeyError:
                    ni_dict[w] = 1
        elif c in nt_set:
            if get_time(w) and w not in nt_dict:
                nt_dict.append(w)
            
        elif c in ns_set:
            if w in title:
                try:
                    ns_dict[w] = ns_dict[w] + 2
                except KeyError:
                    ns_dict[w] = 2
            else:
                try:
                    ns_dict[w] = ns_dict[w] + 1
                except KeyError:
                    ns_dict[w] = 1
        elif c in nh_set:
            if w in title:
                try:
                    nh_dict[w] = nh_dict[w] + 2
                except KeyError:
                    nh_dict[w] = 2
            else:
                try:
                    nh_dict[w] = nh_dict[w] + 1
                except KeyError:
                    nh_dict[w] = 1
        else:
            pass

    return nh_dict,ns_dict,nt_dict,ni_dict

def get_time_from_dict(nt_dict):

    r_list = []
    for i in time_list:
        for item in nt_dict:
            if i in item:
                if i == '年':
                    index = item.find(i)
                    try:
                        y = int(item[0:index])
                        if y > YEAR:
                            continue
                    except:
                        continue
                r_list.append(item)
                break

    return r_list

def cut_main(text,title):

    nh_dict = dict()
    ns_dict = dict()
    nt_dict = []
    ni_dict = dict()
    ts = text.split('。')
    for t in ts:        
        nh_dict,ns_dict,nt_dict,ni_dict = get_pos(t,nh_dict,ns_dict,nt_dict,ni_dict,title)
    
    nh = sorted(nh_dict.iteritems(), key=lambda d:d[1], reverse = True)
    ns = sorted(ns_dict.iteritems(), key=lambda d:d[1], reverse = True)
    nt = get_time_from_dict(nt_dict)
    ni = sorted(ni_dict.iteritems(), key=lambda d:d[1], reverse = True)

    result = [nh,ni,ns]

    item = []
    for i in range(0,3):
        if len(result[i]):
            item.append(result[i][0][0])
        else:
            item.append('NULL')

    if len(nt):
        item.append(''.join(nt))
    elif len(nt_dict):
        item.append(nt_list[0])
    else:
        item.append('NULL')

    return item

def get_news_main(news_text):

    news = re_cut(news_text)
    if len(news):
        if '】' not in news:
            title = ''
            text = news
        else:
            title,text = news_text.split('】')
            if '【' in title:
                title = title[2:len(title)]
            else:
                title = title

        result = cut_main(text,title)
    else:
        result = 'Null'

    re_dict = {}
    name_list = ['people','organization','time','place']
    if result != 'Null':
        for i in range(0,len(result)):
            key = name_list[i]
            value = result[i]
            re_dict[key] = value
    else:
        re_dict = {'people':'Null','organization':'Null','time':'Null','place':'Null'}
        
    return result

if __name__ == '__main__':

    news_text = '【巴西球员坠机空难幸存者 生还只因一个动作据英国《每日邮报》报道，29日一架载有巴西足球运动员的飞机在哥伦比亚坠毁，造成71人死亡，仅有6人幸存，其中一名幸存的机组人员ErwinTumiri描述了飞机坠毁前的惊魂时刻。他说飞机当时突然开始直线下降，惊恐的乘客离开座位惊声尖叫。而他得以生还是因为...全文： http://m.weibo.cn/1686546714/4048313046903423'
    result = get_news_main(news_text)
    print result
    


    
