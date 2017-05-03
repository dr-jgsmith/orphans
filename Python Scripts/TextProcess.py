# -*- coding: utf-8 -*-
"""
seed_search
Created on Tue Nov 22 01:10:08 2016

@author: smith
"""
import os
import csv
import requests
import json
import numpy as np
from textblob import TextBlob
import networkx as nx
from bitarray import bitarray
import nltk, re
from gensim import corpora, models, similarities
import scholarly
import wikipedia
import matplotlib.pyplot as plt
from itertools import tee
from collections import defaultdict
from pprint import pprint


class TextProcessor:

    def __init__(self):
        self.sentList = []        
        self.corp = []
        self.com_seq = []
        self.edges = []
        self.bin_set = []
        self.text_sdr = []
        self.stage = []
        self.stop_list = ['for', 'a', 'the', 'to', 'too', '"drop', 'in', 'but', 'am', 'ie', 'i.e.', 'of', 'I', ']', '[', '...', '–', '-', '____', '___', ',' , '+', '/w', '>']
        self.alphabet = []
    
    def getFileType(self, filename):
        self.filename = filename
        self.filepath, self.file_extension = os.path.splitext(self.filename)
        return self.file_extension
        
    
    def tag_text(self, text):
        self.text = text
        
        t = TextBlob(self.text)
        
        self.seq2 = [k[0].lemmatize().lower() for k in t.tags if k[0] not in self.stop_list if len(k[0]) > 2]
        self.test = ' '.join(self.seq2)
            
        self.r = TextBlob(self.test)
        self.sentence = self.r.tags
        self.sentList.append(self.sentence)
        return self.sentList
            
    def np_chunker(self):
        self.grammar = """
                            NP: {<N.+>?<J.+>?<V.+>*<N.+>+}
                       """
        cp = nltk.RegexpParser(self.grammar)
        self.result = cp.parse(self.sentence)
        
        for i in self.result:
            self.seq = []
            print("Printing i: ", i)
            for j in i:
                print("Printing j: ",j[0])
                self.seq.append(j[0])
            self.com_seq.append(self.test)    
            self.com_seq.append(self.seq)

        self.trans_doc = [x for x in self.com_seq if len(x[0]) > 2]
        print(self.trans_doc)
        return self.trans_doc       
        
    def sparse_vec(self):
        self.frequency = defaultdict(int)

        for text in self.trans_doc:
            print("Printing... ", text)
            
            self.dictionary = corpora.Dictionary(self.trans_doc)
            self.dictionary.save('data_dump.dic')    
            self.dictionary.token2id
            
            self.corpus = [self.dictionary.doc2bow(text) for text in self.trans_doc]
        
    def word2sdr(self):
        for i in self.trans_doc:
            for j in i:
                self.bi = ''.join('{0:064b}'.format(ord(x), 'b') for x in j)
                print(j, self.bi)
                
                self.x = np.binary_repr(self.bi)
                print(self.x)
            
            self.bin_set.append(self.bi)
        
    def genet_sem(self):
        for i in self.trans_doc:
            for j in i:
                self.bin_letter = ' '.join('{0:064b}'.format(ord(x), 'b') for x in j)
                print(self.bin_letter)
                
    
    def text2sdr(self):
        j = self.bin_set
        
        x = int(j[0]) 
        y = int(j[1])
    
        print(x, y)
        merge = x&y
        
        print(merge)
        #pprint(self.union)     
    
    def convenrt2bit(self):
        a = bitarray()
        for i in self.trans_doc:
            for j in i:
                self.n = j + ' '
                a.fromstring(self.n)
                print(self.n, a)
                
    
    def learnAlphaB(self):
        a = bitarray()
        for i in self.trans_doc:
            for j in i:
                split = list(j)
                for x in split:
                    print(x)
                    a.fromstring(x)
                    self.spr_l = dok_matrix(a)
                    print(self.spr_l)
                    break
                    
                    
        
    def lda_model(self, topics):
        self.topics = topics
        self.lda = models.LdaModel(self.corpus, id2word=self.dictionary, num_topics=self.topics)
            
        self.corp_lda = self.lda[self.corpus]
            
        for doc in self.corp_lda:
            print(doc)
        
        print(self.lda.print_topics(self.topics))
        
    
    #Edges will be very important as the will direct co-occurence in documents fingerprints    
    def get_edges(self):
        for j in self.trans_doc:
            a, b = tee(j)
            next(b, None)
            self.pairs = zip(a, b)
            for i in self.pairs:
                print(i)
                self.edges.append(i)

    
    def get_edge_graph(self):
        G = nx.DiGraph()
        
        G.add_edges_from(self.edges)
        #nx.draw(G, with_labels=True)
        
        nx.draw_spring(G,node_size=1, with_labels=True, edge_color='b',alpha=.2,font_size=10)
        
        plt.show() 
        
    def get_path_graph(self):
        G = nx.DiGraph()
        for j in self.trans_doc:
            G.add_path(j)
        
        #nx.draw(G, with_labels=True)
        
        nx.draw_spring(G,node_size=0,with_labels=True,edge_color='b',alpha=.2,font_size=10)
        
        plt.show()
        
        
class TextSearch:
    
    def __init__(self, term):
        self.term = term
    
    def search_scholar(self):
        search_query = scholarly.search_pubs_query(self.term)
        self.result = next(search_query).fill()
        print(self.result)
    
    def search_news(self):
        for item in self.term:
            base = "http://www.faroo.com/api?q="
            connector = "&start=1&length=10&l=en&src=news&f=json"
            api_key = "&key=NWPsWfgdnoKG8KLL56rzN8Zosbk_"
            search = base+self.term+connector+api_key
            
            r = requests.get(search)
            
            self.news_text = r.text
            if self.news_text == "<h1>HTTP/1.1 429 Rate limit exceeded</h1>":
                pass
            else:
                print(self.news_text)
                
                self.news = json.loads(self.news_text)
                print(self.news)
            
                for i, entry in enumerate(self.news['results']):
                    print(entry['title'])
        
    def search_web(self):
        for item in self.term:
            base = "http://www.faroo.com/api?q="
            connector = "&start=1&length=10&l=en&src=web&f=json"
            api_key = "&key=NWPsWfgdnoKG8KLL56rzN8Zosbk_"
            search = base+self.term+connector+api_key
            
            r = requests.get(search)
            
            #self.web_text = str(r.content, 'cp437', errors='ignore')
            
            self.web_text = r.text
            if self.web_text == "<h1>HTTP/1.1 429 Rate limit exceeded</h1>":
                pass
            else:
                print(self.web_text)
                
                self.web = json.loads(self.web_text)
                print(self.web)
            
                for i, entry in enumerate(self.web['results']):
                    print(entry['title'])
                    
    def search_wiki(self):
        self.summary = wikipedia.summary(self.term)
        print(self.summary)
        return self.summary
    
    def recurse_search(self, depth):
        self.depth = depth
        



#Basic usage:
s = TextSearch("climate change")

#Define where to search, i.e. wikipedia, google scholar, news, etc.
text = s.search_wiki()

data = TextProcessor()
data.tag_text(text)
data.np_chunker()
data.get_edges()
data.get_path_graph()

"""
data.get_edges()
data.get_graph()

start project 
search by topic
Get doc list
Save metadata to db - including url
retrieve url
convert document into raw text
process text
retrieve word/sequence list

elif self.file_extension == '.pdf':
        parsePDF()
    elif self.file_extension == '.csv':
        parseDOC()
    elif self.file_extension == '.html':
        parseHTML()
"""


