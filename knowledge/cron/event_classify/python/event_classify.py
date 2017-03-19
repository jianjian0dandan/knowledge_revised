# -*- coding: utf-8 -*-

import os
import scws
import csv
import re
from svmutil import *
from utils import cut_filter,classify_list,abs_path

def get_classify(text,d_first):

    word_dict = []
    reader = csv.reader(file(abs_path+'/svm_model/feature_%s.csv' % d_first, 'rb'))
    for w,c in reader:
        word_dict.append([w,c])

    prob_y = []
    prob_x = []
    xi = {}
    for item in word_dict:                        
        if item[0] in text:
            xi[int(item[1])] = float(text.count(item[0]))

    prob_x += [xi]
    prob_y += [float(1)]

    m = svm_load_model(abs_path+'/svm_model/train_%s.model' % d_first)
    p_label, p_acc, p_val  = svm_predict(prob_y, prob_x, m)
    
    if str(int(p_label[0])) == '1':
        return d_first
    else:
        return 'other'

def cut_weibo(data):

    classify_dict = {'diplomacy':0,'disaster':0,'financial_work':0,'macro_economy':0,'chinese_party':0,'public_security':0,'national':0,'military':0}
    text = ''
    count = 0
    for item in data:        
        text_str = cut_filter(item)
        if not len(text_str):
            continue
        if count == 0:
            text = text + text_str
        else:
            text = text + '。' + text_str
        count = count + 1

    for i in range(0,len(classify_list)):
        flag = get_classify(text,classify_list[i])
        if flag == 'other':
            continue
        else:
            classify_dict[flag] = classify_dict[flag] + 1

    result = 'other'
    flag = 0
    for k,v in classify_dict.iteritems():
        if v > 0:
            flag = flag + 1
            result = k

    if flag > 1:
        label = 'other'
    else:
        label = result

    return label

def test_data(name):

    text_list = []
    reader = csv.reader(file('./event_data/%s.csv' % name, 'rb'))
    count = 0
    for line in reader:
        try:
            text = line[0]
        except:
            continue
        text_list.append(text)

    return text_list

if __name__ == '__main__':

    data_list = ['aomen','jiedaibao','jierjisi','jinji','social-security','yilake']
    for name in data_list:
        data = test_data(name)
        #label = cut_weibo_new(data)
        label = cut_weibo(data)
        print name,label
