# -*- coding: UTF-8 -*-

import os
import time
import re
import scws
import csv
import sys
import json
import heapq
import gensim
from gensim import corpora, models, similarities
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from config import SW as sw, black_word as black, cx_dict, re_cut

tr4w = TextRank4Keyword()

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

def get_keyword(w_text, n_gram):
    '''
        输入数据：
        w_text:将所有微博拼成一条文本
        n_gram:时间窗口大小，一般都取2

        输出数据：
        data_result：关键词列表，[[word1,weight1],[word2,weight2],...]
    '''

    tr4w.analyze(text=w_text, lower=True, window=n_gram)
    word_list = dict()
    k_dict = tr4w.get_keywords(500, word_min_len=2)
    n = len(k_dict)
    keyword = TopkHeap(n)
    for item in k_dict:
        if item.word.encode('utf-8').isdigit() or item.word.encode('utf-8') in black:
            continue
        keyword.Push((item.weight,item.word.encode('utf-8')))

    keyword_data = keyword.TopK()

    data_result = []
    for i in range(0,len(keyword_data)):
        data_result.append([keyword_data[i][1],keyword_data[i][0]])
    return data_result

def get_topic_word(texts,nt):
    '''
        输入数据：
        text:list对象，一条记录表示一条分词之后的微博文本
        nt:需要的topic的数量

        输出数据：
        topic的list
    '''
    
    ##生成字典
    dictionary=corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=None)
    corpus = [dictionary.doc2bow(text) for text in texts if len(dictionary.doc2bow(text))]

    if not len(corpus):
        return 'Null'
    
    ##生成tf-idf矩阵
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    ##LDA模型训练
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=nt, update_every=1, chunksize=5000, passes=1)

    topics=lda.show_topics(num_topics=nt, num_words=10, log=False, formatted=True)

    return topics

###以下仅供测试使用
def get_weibo_test():

    uid_dict = dict()
    uid_tr = dict()
    texts = ''
    reader = csv.reader(file('./text_data/text_0.csv', 'rb'))
    count = 0
    for uid,text,ts,geo in reader:
        w_text = re_cut(text)
        if count == 0:
            texts = texts + w_text
        else:
            texts = texts + '。' + w_text
        words = sw.participle(w_text)
        word_list = []
        for word in words:
            if word[0] not in black and word[1] in cx_dict and len(word[0])>3:
                if uid_dict.has_key(uid):
                    uid_dict[uid].append(word[0])
                else:
                    uid_dict[uid] = []
                    uid_dict[uid].append(word[0])
                word_list.append(word[0])
        count = count + 1
        if len(word_list):        
            if uid_tr.has_key(uid):
                uid_tr[uid].append(word_list)
            else:
                uid_tr[uid] = []
                uid_tr[uid].append(word_list)

    uid_list = []
    text_list = []
    for k,v in uid_dict.iteritems():
        uid_list.append(k)
        text_list.append(v)

    return texts,text_list

if __name__ == '__main__':

    w_text,text_list = get_weibo_test()
    topics = get_topic_word(text_list,10)
    keywords = get_keyword(w_text, 2)
    print topics
    print keywords
    
