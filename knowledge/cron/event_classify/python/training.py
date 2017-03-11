# -*- coding: utf-8 -*-

import os
import sys
import re
import scws
import csv
import heapq
from svmutil import *
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

def load_text(d):

    word_list = []
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
    m = svm_train(y, x, '-c 4 -h 0')
    svm_save_model('./svm_model/train_%s_%s.model' % (d_first,d_second),m)
    
if __name__ == '__main__':

    data_list = ['diplomacy','disaster','financial_work','macro_economy','chinese_party','public_security','national','military']

    get_tfidf(data_list)

    for i in range(0,len(data_list)):
        for j in range(i+1,len(data_list)):
            train_data(data_list[i],data_list[j])
            train_model(data_list[i],data_list[j])

    

##    for d_time in data_first:
##        read_csv_2(d_time)

##    with open('./train_data/military.csv', 'wb') as f:
##        writer = csv.writer(f)
##        for item in text_list:
##            row = []
##            row.append(item)
##            writer.writerow(row)
##    f.close()

        
