# -*- coding: utf-8 -*-

import os
import scws
import csv
import re
from svmutil import *
from utils import cut_filter,classify_list,classify_dict,abs_path

def get_classify(text,d_first,d_second):

    word_dict = dict()
    reader = csv.reader(file(abs_path+'/svm_model/feature_%s_%s.csv' % (d_first,d_second), 'rb'))
    for w,c in reader:
        word_dict[str(w)] = c

    with open(abs_path+'/svm_test/test.txt', 'wb') as f:
        writer = csv.writer(f)
        for k,v in word_dict.iteritems():
            row = []
            f_row = ''
            f_row = f_row + str(1)
            if k in text:
                f_row = f_row + ' ' + str(v)+':'+str(text.count(k))
            row.append(f_row)
            writer.writerow((row))
    f.close()

    m = svm_load_model(abs_path+'/svm_model/train_%s_%s.model' % (d_first,d_second))
    y, x = svm_read_problem(abs_path+'/svm_test/test.txt')
    p_label, p_acc, p_val  = svm_predict(y, x, m)

    if p_label == '1':
        return d_first
    else:
        return d_second
    

def cut_weibo(data):

    text = ''
    count = 0
    for item in data:        
        text_str = cut_filter(item)
        if not len(text_str):
            continue
        if count == 0:
            text = text + text_str
        else:
            count = count + 1
            text = text + '。' + text_str
    
    for i in range(0,len(classify_list)):
        for j in range(i+1,len(classify_list)):
            flag = get_classify(text,classify_list[i],classify_list[j])
            classify_dict[flag] = classify_dict[flag] + 1

    nh = sorted(classify_dict.iteritems(), key=lambda d:d[1], reverse = True)

    sta_n = float(len(classify_dict)-1)*0.5

    if nh[0][1] >= sta_n:
        label = nh[0][0]
    else:
        label = 'other'

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

    data_list = ['jiedaibao','aomen','jinji','yilake','jierjisi']
    for name in data_list:
        data = test_data('aomen')
        label = cut_weibo(data)
        print label
