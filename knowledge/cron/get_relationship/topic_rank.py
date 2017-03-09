# -*- coding: UTF-8 -*-
import gensim
from gensim import corpora, models, similarities, matutils
import time
import datetime
import csv
import heapq
import networkx as nx
import numpy as np
from config import re_cut,SW,black_word,single_word_whitelist,cx_dict,MAX_COUNT

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

def get_topic_word(texts,nt):
    '''
    text:list对象，一条记录表示一个用户发布
    nt:需要的topic的数量
    '''
    
    ##生成字典
    dictionary=corpora.Dictionary(texts)
    #dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=None)
    corpus = [dictionary.doc2bow(text) for text in texts if len(dictionary.doc2bow(text))]

    if not len(corpus):
        return 'Null'
    
    ##生成tf-idf矩阵
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    #print corpus_tfidf
    ##LDA模型训练
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=nt, update_every=1, chunksize=5000, passes=1)

    total_number = lda.num_topics

    shown = []
    for i in range(0,total_number):
        topic = lda.state.get_lambda()[i]#根据topicid获取对应的词语及其概率
        topic = topic / topic.sum()  # normalize to probability distribution
        topn = len(topic)
        #print topic
        bestn = matutils.argsort(topic, topn, reverse=True)
        result = [(lda.id2word[id].encode('utf-8'), value) for id, value in [(id, topic[id]) for id in bestn]]
        shown.append((i, result))

    d_topic = list(lda.get_document_topics(corpus))

    return shown,d_topic

def combine(word_list, window = 2):
    """构造在window下的单词组合，用来构造单词之间的边。
    
    Keyword arguments:
    word_list  --  list of str, 由单词组成的列表。
    windows    --  int, 窗口大小。
    """
    if window < 2: window = 2
    for x in xrange(1, window):
        if x >= len(word_list):
            break
        word_list2 = word_list[x:]
        res = zip(word_list, word_list2)
        for r in res:
            yield r

def get_graph(_vertex_source,window,topic_result):

    sorted_words   = []
    word_index     = {}
    index_word     = {}
    words_number   = 0
    for word_list in _vertex_source:
        for word in word_list:
            if not word in word_index:
                word_index[word] = words_number
                index_word[words_number] = word
                words_number += 1

    graph = np.zeros((words_number, words_number))
    personalization = get_personalization(topic_result,index_word)
    for word_list in _vertex_source:
        for w1, w2 in combine(word_list, window):
            if w1 in word_index and w2 in word_index:
                index1 = word_index[w1]
                index2 = word_index[w2]
                graph[index1][index2] = float(graph[index1][index2]) + 1.0
                graph[index2][index1] = float(graph[index2][index1]) + 1.0

    nx_graph = nx.from_numpy_matrix(graph)
    pagerank_config = 0.85
    scores = nx.pagerank(nx_graph, pagerank_config, personalization)# this is a dict
    sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse=True)
    count = 0
    for index, score in sorted_scores:
        if count >= MAX_COUNT:
            break
        sorted_words.append([index_word[index],score])
        count = count + 1

    return sorted_words

def get_personalization(topic_result,index_word):

    word_dict = dict()
    for word,weight in topic_result:
        word_dict[word] = weight
    personalization = dict()
    n = len(index_word)
    union_set = set(word_dict.keys()) & set(index_word.values())
    m = len(union_set)
    count = 0
    for v in union_set:
        count = count + word_dict[v]
    remain_p = 1 - count
    for k,v in index_word.iteritems():
        if word_dict.has_key(v):
            personalization[k] = word_dict[v]#float(m)/float(n)*word_dict[v]
        else:
            if (n-m) == 0:
                personalization[k] = 0
            else:
                personalization[k] = float(remain_p)/float(n-m)#float(1)/float(n)#需要在确定

    return personalization
        
def get_final_result(word_list):#最终的排序

    n = len(word_list)
    keyword = TopkHeap(n)
    for k,v in word_list:
        keyword.Push((v,k))

    keyword_data = keyword.TopK()
    return keyword_data

def list2dict(data):

    data_list = []
    for item in data:
        item_dict = dict()
        for k,v in item:
            item_dict[k] = v
        data_list.append(item_dict)

    return data_list


                


    
    
