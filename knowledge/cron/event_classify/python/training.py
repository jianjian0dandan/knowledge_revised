# -*- coding: utf-8 -*-

import os
import sys
import re
import scws
import csv
import heapq
import random
from collections import Counter
from svmutil import *
from imblearn.over_sampling import SMOTE
##from sklearn import svm
##from sklearn import metrics
##from sklearn.cross_validation import train_test_split
from gensim import corpora, models, similarities
from utils import single_word_whitelist,black_word,load_scws,cx_dict

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0][0]
            if elem[0] > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

sw = load_scws()

def read_csv(d_time):

    text_list = []
    word_dict = dict() 
    files = os.listdir('./train_data/%s/' % d_time)
    for filename in files:
        f = open('./train_data/%s/%s' % (d_time,filename))
        count = 0
        text = ''
        for line in f:
            count = count + 1
            print count
            line = line.decode('gbk', 'ignore')
            line = line.encode('utf-8')
            w_text = line.strip('\n\t\r')
            w_text = w_text.replace(' ','')
            
            text = text + w_text
        f.close()
        text_list.append(text)

    return text_list

def read_csv_2(d_time):

    reader = csv.reader(file('./train_data/%s.csv' % d_time, 'rb'))
    text_list = []
    print d_time
    for line in reader:
        title = line[0].strip('\n\t\r')
        text = ''.join(line[1:len(line)])
        text = text.strip('\n\t\r')
        text_list.append(title+text)

    with open('./train_data/%s.csv' % d_time, 'wb') as f:
        writer = csv.writer(f)
        for item in text_list:
            row = []
            row.append(item)
            writer.writerow(row)
    f.close()

def get_tfidf(data_list):

    dictionary_p = corpora.Dictionary([])
    data_text = []
    for d in data_list:
        reader = csv.reader(file('./train_data/%s.csv' % d, 'rb'))
        entries = []
        for line in reader:
            kw_pos = sw.participle(line[0])            
            for kw in kw_pos:
                if kw[1] in cx_dict and len(kw[0]) > 3 and kw[0] not in black_word:
                    entries.append(kw[0])
        dictionary_p.add_documents([entries])
        data_text.append(entries)

    corpus_data = []
    for text in data_text:
        f_word = dictionary_p.doc2bow(text)
        corpus_data.append(f_word)

    tfidf = models.TfidfModel(corpus_data)

    
    for i in range(0,len(corpus_data)):
        name = data_list[i]
        with open('./train_data/%s_tfidf.csv' % name, 'wb') as f:
            writer = csv.writer(f)
            item = tfidf[corpus_data[i]]
            keyword = TopkHeap(500)
            for k,v in item:
                keyword.Push((v,dictionary_p[k].encode('utf-8')))

            keyword_data = keyword.TopK()
            for item in keyword_data:                
                writer.writerow((item[1],item[0]))
        f.close()

def load_word(d):

    word_list = []
    reader = csv.reader(file('./train_data/%s_tfidf.csv' % d, 'rb'))
    for word,weight in reader:
        word_list.append(word)

    return word_list

def load_word_other(d_name):

    data_list = ['diplomacy','disaster','financial_work','macro_economy','chinese_party','public_security','national','military']
    word_list = []
    for d in data_list:
        if d == d_name:
            continue
        reader = csv.reader(file('./train_data/%s_tfidf.csv' % d, 'rb'))
        for word,weight in reader:
            word_list.append(word)

    return word_list

def load_text(d):

    word_list = []
    reader = csv.reader(file('./train_data/%s.csv' % d, 'rb'))
    for line in reader:
        word_list.append(line[0])

    return word_list

def load_text_other(d_name):

    data_list = ['diplomacy','disaster','financial_work','macro_economy','chinese_party','public_security','national','military']
    word_list = []
    for d in data_list:
        if d == d_name:
            continue
        reader = csv.reader(file('./train_data/%s.csv' % d, 'rb'))
        for line in reader:
            word_list.append(line[0])

    return word_list

def train_data(d_first,d_second):

    w_first = load_word(d_first)
    w_second = load_word(d_second)
    w_first.extend(w_second)

    text_first = load_text(d_first)
    text_second = load_text(d_second)
    n = len(text_first)
    text_first.extend(text_second)
    

    with open('./svm_model/train_%s_%s.txt' % (d_first,d_second), 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(text_first)):
            row = []
            if i < n:
                f_items = '' + '1'
            else:
                f_items = '' + '0'
            item = text_first[i]
            for k in range(0,len(w_first)):
                if w_first[k] in item:
                    f_items = f_items + ' ' + str(k+1) + ':' + str(item.count(w_first[k]))
            row.append(f_items)
            writer.writerow((row))
    f.close()

    with open('./svm_model/feature_%s_%s.csv' % (d_first,d_second), 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(w_first)):
            writer.writerow(([w_first[i],i+1]))
    f.close()

def train_model(d_first,d_second):

    y, x = svm_read_problem('./svm_model/train_%s_%s.txt' % (d_first,d_second))
    m = svm_train(y, x, '-c 4 -h 0 -t 0 -v 5')
    return m
    #svm_save_model('./svm_model/train_%s_%s.model' % (d_first,d_second),m)

def train_data_new(d_first,label):#over-sampling

    w_first = load_word(d_first)
    w_second = load_word_other(d_first)
    w_total = w_first + w_second

    text_first = load_text(d_first)
    text_second = load_text_other(d_first)

    text_x = []
    text_y = []
    for item in text_first:
        text_y.append(1)
        row = []
        for k in w_total:
            if k in item:
                row.append(item.count(k))
            else:
                row.append(0)
        text_x.append(row)

    for item in text_second:
        text_y.append(0)
        row = []
        for k in w_total:
            if k in item:
                row.append(item.count(k))
            else:
                row.append(0)
        text_x.append(row)

    sm = SMOTE(kind=label)
    #print Counter(text_y)
    X_resampled, y_resampled = sm.fit_sample(text_x, text_y)
    #print Counter(y_resampled)
    
    with open('./svm_model/train_%s.txt' % d_first, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(X_resampled)):
            row = []
            f_item = str(y_resampled[i])
            item = X_resampled[i]
            for k in range(0,len(item)):
                if item[k] != 0:
                    f_item = f_item + ' ' + str(k+1) + ':' + str(item[k])
            row.append(f_item)
            writer.writerow((row))

    with open('./svm_model/feature_%s.csv' % d_first, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(w_total)):
            writer.writerow(([w_total[i],i+1]))
    f.close()

def train_model_new(d_first):

    y, x = svm_read_problem('./svm_model/train_%s.txt' % d_first)
    m = svm_train(y, x, '-c 1 -h 0 -t 0')
    #m = svm_train(y, x, '-c 4 -h 0 -t 0 -v 5')
    svm_save_model('./svm_model/train_%s.model' % d_first,m)    

def get_train_data(dict_x,dict_y,i):

    train_x = []
    train_y = []
    for k in range(1,6):
        if k == i:
            continue
        train_x.extend(dict_x[k])
        train_y.extend(dict_y[k])

    return train_x,train_y

def get_computing(p_label,ty):

    tp = 0
    tn = 0
    fp = 0
    fn = 0
    c = 0

    for i in range(0,len(p_label)):
        if str(int(p_label[i])) == '0' and str(int(ty[i])) == '0':
            tn = tn + 1
        elif str(int(p_label[i])) == '1' and str(int(ty[i])) == '1':
            tp = tp + 1
        elif str(int(p_label[i])) == '0' and str(int(ty[i])) == '1':
            fn = fn + 1
        elif str(int(p_label[i])) == '1' and str(int(ty[i])) == '0':
            fp = fp + 1
        else:
            c = c + 1

    print tp,tn,fp,fn
    p = float(tp)/float(tp+fp)
    n = float(tp)/float(tp+fn)
    f = float(p*n*2)/float(p+n)
    return p,n,f

def train_data_cross_two(d_first,d_second):

    w_first = load_word(d_first)
    w_second = load_word(d_second)
    w_total = w_first + w_second

    text_first = load_text(d_first)
    text_second = load_text(d_second)

    dict_x = dict()
    dict_y = dict()
    count = 1
    for item in text_first:
        flag = count%5 + 1
        count = count + 1
        if dict_y.has_key(flag):
            dict_y[flag].append(1)
        else:
            dict_y[flag] = [1]
        row = []
        for k in w_total:
            if k in item:
                row.append(item.count(k))
            else:
                row.append(0)
        if dict_x.has_key(flag):
            dict_x[flag].append(row)
        else:
            dict_x[flag] = [row]

    count = 1
    for item in text_second:
        flag = count%5 + 1
        count = count + 1
        if dict_y.has_key(flag):
            dict_y[flag].append(0)
        else:
            dict_y[flag] = [0]
        row = []
        for k in w_total:
            if k in item:
                row.append(item.count(k))
            else:
                row.append(0)
        if dict_x.has_key(flag):
            dict_x[flag].append(row)
        else:
            dict_x[flag] = [row]

    result = dict()
    for k_l in range(1,6):
        test_x = dict_x[k_l]
        test_y = dict_y[k_l]
        train_x,train_y = get_train_data(dict_x,dict_y,k_l) 
    
        with open('./svm_model/train_%s.txt' % d_first, 'wb') as f:
            writer = csv.writer(f)
            for i in range(0,len(train_x)):
                row = []
                f_item = str(train_y[i])
                item = train_x[i]
                for k in range(0,len(item)):
                    if item[k] != 0:
                        f_item = f_item + ' ' + str(k+1) + ':' + str(item[k])
                row.append(f_item)
                writer.writerow((row))

        with open('./svm_test/test_%s.txt' % d_first, 'wb') as f:
            writer = csv.writer(f)
            for i in range(0,len(test_x)):
                row = []
                f_item = str(test_y[i])
                item = test_x[i]
                for k in range(0,len(item)):
                    if item[k] != 0:
                        f_item = f_item + ' ' + str(k+1) + ':' + str(item[k])
                row.append(f_item)
                writer.writerow((row))

        y, x = svm_read_problem('./svm_model/train_%s.txt' % d_first)
        m = svm_train(y, x, '-c 1 -h 0 -t 0')
        ty, tx = svm_read_problem('./svm_test/test_%s.txt' % d_first)
        p_label, p_acc, p_val  = svm_predict(ty, tx, m)
        p,r,f = get_computing(p_label,ty)

        result[k_l] = [p,r,f]

    return result

def train_data_cross(d_first,label):#over-sampling

    w_first = load_word(d_first)
    w_second = load_word_other(d_first)
    w_total = w_first + w_second

    text_first = load_text(d_first)
    text_second = load_text_other(d_first)

    dict_x = dict()
    dict_y = dict()
    count = 1
    for item in text_first:
        flag = count%5 + 1
        count = count + 1
        if dict_y.has_key(flag):
            dict_y[flag].append(1)
        else:
            dict_y[flag] = [1]
        row = []
        for k in w_total:
            if k in item:
                row.append(item.count(k))
            else:
                row.append(0)
        if dict_x.has_key(flag):
            dict_x[flag].append(row)
        else:
            dict_x[flag] = [row]

    count = 1
    for item in text_second:
        flag = count%5 + 1
        count = count + 1
        if dict_y.has_key(flag):
            dict_y[flag].append(0)
        else:
            dict_y[flag] = [0]
        row = []
        for k in w_total:
            if k in item:
                row.append(item.count(k))
            else:
                row.append(0)
        if dict_x.has_key(flag):
            dict_x[flag].append(row)
        else:
            dict_x[flag] = [row]

    result = dict()
    for k_l in range(1,6):
        test_x = dict_x[k_l]
        test_y = dict_y[k_l]
        train_x,train_y = get_train_data(dict_x,dict_y,k_l) 
        sm = SMOTE(kind=label)
        X_resampled, y_resampled = sm.fit_sample(train_x,train_y)
    
        with open('./svm_model/train_%s.txt' % d_first, 'wb') as f:
            writer = csv.writer(f)
            for i in range(0,len(X_resampled)):
                row = []
                f_item = str(y_resampled[i])
                item = X_resampled[i]
                for k in range(0,len(item)):
                    if item[k] != 0:
                        f_item = f_item + ' ' + str(k+1) + ':' + str(item[k])
                row.append(f_item)
                writer.writerow((row))

        with open('./svm_test/test_%s.txt' % d_first, 'wb') as f:
            writer = csv.writer(f)
            for i in range(0,len(test_x)):
                row = []
                f_item = str(test_y[i])
                item = test_x[i]
                for k in range(0,len(item)):
                    if item[k] != 0:
                        f_item = f_item + ' ' + str(k+1) + ':' + str(item[k])
                row.append(f_item)
                writer.writerow((row))

        y, x = svm_read_problem('./svm_model/train_%s.txt' % d_first)
        m = svm_train(y, x, '-c 1 -h 0 -t 0')
        ty, tx = svm_read_problem('./svm_test/test_%s.txt' % d_first)
        p_label, p_acc, p_val  = svm_predict(ty, tx, m)
        p,r,f = get_computing(p_label,ty)

        result[k_l] = [p,r,f]

    return result
##        with open('./svm_model/feature_%s.csv' % d_first, 'wb') as f:
##            writer = csv.writer(f)
##            for i in range(0,len(w_total)):
##                writer.writerow(([w_total[i],i+1]))
##        f.close()
    
if __name__ == '__main__':

    data_list = ['diplomacy','disaster','financial_work','macro_economy','chinese_party','public_security','national','military']

####    #get_tfidf(data_list)
##    name_list = ['regular', 'borderline1', 'borderline2', 'svm']
    name_list = ['borderline2']
##    result = dict()
    for name in name_list:
##        row = dict()
        for i in range(0,len(data_list)):
##            r = train_data_cross(data_list[i],name)
            train_data_new(data_list[i],name)
            train_model_new(data_list[i])
##            row[data_list[i]] = r
##        result[name] = row
####
##    with open('./result/result_over_new.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for k,v in result.iteritems():
##            for k1,v1 in v.iteritems():
##                for k2,v2 in v1.iteritems(): 
##                    writer.writerow((k,k1,v2[0],v2[1],v2[2]))
##    f.close()
    #data_list = ['diplomacy','disaster','financial_work','macro_economy','chinese_party','public_security','national','military']

    result = dict()
    for i in range(0,len(data_list)):
        for j in range(i+1,len(data_list)):
            m = train_data_cross_two(data_list[i],data_list[j])
####            train_data(data_list[i],data_list[j])
####            m = train_model(data_list[i],data_list[j])
            result[data_list[i]+'&'+data_list[j]] = m
##
    with open('./result/result_two_new.csv', 'wb') as f:
        writer = csv.writer(f)
        for k,v in result.iteritems():
            k1,k2 = k.split('&')
            for km,v1 in v.iteritems():
                writer.writerow((k1,k2,v1[0],v1[1],v1[2]))
    f.close()
##    for d_time in data_first:
##        read_csv_2(d_time)

##    with open('./train_data/military.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for item in text_list:
##            row = []
##            row.append(item)
##            writer.writerow(row)
##    f.close()

        
