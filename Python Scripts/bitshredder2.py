# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 09:08:02 2016

@author: smith
@title: bitshredder2
"""
import os
import math
import csv
import requests
import json
import numpy as np
from collections import OrderedDict
from itertools import cycle
from more_itertools import unique_everseen
from textblob import TextBlob
import networkx as nx
from bs4 import BeautifulSoup
import pandas as pd
from scipy.sparse import lil_matrix, csr_matrix
import nltk, re

import scholarly
import wikipedia
import matplotlib.pyplot as plt
from itertools import tee
from collections import defaultdict
from pprint import pprint

from PIL import Image

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
    
    def url_search(self, url, depth):
        self.url = url
        self.depth = depth
        
        self.s = requests.Session()
        
        
        headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        self.r = self.s.get(url)
        
        texts = self.r.text
        self.visible_texts = self.clean_html(texts)
        
        soup = BeautifulSoup(c)
        for link in soup.find_all("a"):
		print(link.get("href"))
        
        return self.visible_texts
    
    
    def clean_html(self, html):
        """
        Copied from NLTK package.
        Remove HTML markup from the given string.
    
        :param html: the HTML string to be cleaned
        :type html: str
        :rtype: str
        
        """
        self.html = html
        str_html = str(self.html)
    
        # First we remove inline JavaScript/CSS:
        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", str_html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
        # Next we can remove the remaining tags:
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        # Finally, we deal with whitespace
        cleaned = re.sub(r"&nbsp;", " ", cleaned)
        cleaned = re.sub(r"[\s]", "  ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        cleaned = re.sub(r"  ", "\n", cleaned)
        
        self.tmp = cleaned.split()
        #print(tmp)
        
        
        return(self.tmp)
    

class SDR:
    
    def __init__(self, searchterm):
        self.term = searchterm
        
        self.a  = TextSearch(self.term)
                      
        self.result = self.a.search_wiki()
        #self.result = "Some string content here so that we can train the neurons of the machine brain. I think it is all rather amazing. What do you think?"
        
        self.bitlist = []
        
        self.chars = []
        self.sentences = []
       
        self.letter_list = []
        self.letter_list_ind = []
        
        self.char_list = []
        self.char_list_ind = []
        
        self.num_index = []
        self.sparse_ind = []
        self.base_index = []
        
        self.seq = []
        self.s_sparse = pd
        

    def split_sentence(self):
        self.b = TextBlob(self.result)
        self.sent = self.b.sentences
        for x in self.sent:
            self.sentences.append(x)
        
        return self.sentences
        
    def split_words(self):
         self.word = self.result.split()
         
         return self.word
    
    def split_char(self):
        for x in self.word:
            self.j = list(x)
            self.chars.append(self.j)
        
        return self.chars
       
    def get_bitlist(self, raw_list):
        self.raw_list = raw_list
        self.word_n = 251
        self.wows_array = []
        self.index_list = []
        for i in raw_list:
            print(i)
            for j in i:
                print(j)
                self.word_array = [0]*self.word_n
                self.word_array.insert(ord(j), 1)
                self.index_list.append(ord(j))
            
            self.wows_array.append(self.word_array)  
            self.index_list.append(0)  
        
        return self.wows_array, self.index_list
        
    def index_bits(self):
        self.word_bits = []
        
        tmp = []
        for i in self.index_list:
            
            if i > 0:
                tmp.append(i)
            else:
                tmp_list = [0]
                self.word_bits.append(tmp)
                self.word_bits.append(tmp_list)
                tmp = []
#experimental using lists
    def list_as_index(self):
         
        lindx = len(self.word_bits)
        self.wbits_indx = list(range(lindx))
        
    def get_list_item(self, colnum):
        self.colnum = colnum
        #retreives the unicode representation of a string/must be converted using the chr() method
        self.seq_itm = self.word_bits[self.colnum]
        
        return self.seq_itm
   # def get_list_uniq(self):    
    
    def convrt_list2w(self, sequence):
        self.sequence = sequence
        z = []
        for i in self.sequence:
            z.append(chr(i))
            
        self.y = ''.join(z)
        return self.y
        
    def get_n_grams(self, grams):
        self.grams = grams
        self.n_grams_list = []
    
        self.t_list = self.wbits_indx[0::2]
        
        x = 0
        y = self.grams
        
        for i in self.t_list:
            
            z = self.t_list[x:y]
            
            x = x + (self.grams-1)
            y = y + (self.grams-1)
            
            if not z:
                break
            else:
                self.n_grams_list.append(z)
        
    def get_unique_list(self):
        
        self.uni_set = list(unique_everseen(self.word_bits))
                
        return self.uni_set
        
    def translate(self, list_of_list):

        self.list_of_list = list_of_list
        self.t_text = []
        
        t = ''
        for i in self.list_of_list:
            tmp = []
            for j in i:
                s = chr(j)
                tmp.append(s)
            self.t_text.append(tmp)
        
        tmp = []
        for k in self.t_text:
            self.uni_t = ''.join(k)   
            tmp.append(self.uni_t)
        
        self.uni_text = ' '.join(tmp)
        return self.uni_text
        
        
#Beginning of working set      
    def index_sparse_list(self):
        self.word_n = len(self.word_bits)
        self.sparse_array = []
        
        for item in self.word_bits:
            print(item)
            #zeros = []
            for j in item:
                zeros = [0]*self.word_n
                if j < self.word_n:
                    zeros[j] = 1
                else:
                    pass
         
                self.sparse_array.append(zeros)
            
            zeros = [0]*self.word_n
            self.sparse_array.append(zeros)
            
        for i in self.sparse_array:
            print(len(i))
        
        print(len(self.sparse_array))
        
        self.test_arr = np.array(self.sparse_array)
        
    def index_sparse_arr(self):
        
        self.sparse_doc = csr_matrix(self.test_arr)
        print(self.sparse_doc)
        
        self.dense_arr = csr_matrix.todense(self.sparse_doc)        
        
        self.im = Image.fromarray(self.dense_arr * 225)
        self.im.show()
        
        
       
    def charINDEX(self):
        count = 0
        self.n = 500
        tmp = []
        while (count < self.n):
            self.full_sparse = [0]*self.n
            self.full_sparse.insert(count,1)
            tmp.append(self.full_sparse)
            count = count+1
            
        self.char_set = lil_matrix(tmp)
        print(self.char_set)
        
        self.char_dense = lil_matrix.todense(self.char_set)
        self.im = Image.fromarray(self.char_dense * 255)
        self.im.show()
        
    
    def wordINDEX(self):
        self.word_list = []
        
        [self.word_list.append(w) for w in self.word if w not in self.word_list]

        self.n_words = len(self.word_list)

        self.word_set = []
        
        for x in self.word_list:
            
            self.word_arr = [0]*self.n_words
            #self.iloc = self.word_list.index(x)
            self.word_arr[self.word_list.index(x)] = 1
            self.word_set.append(self.word_arr)
        
        print(self.word_set, self.n_words)
        
        
    def textInd(self):
        for i in self.word_list:
            chrs = list(i)
            self.sum_list = []
            for x in chrs:
                y = ord(x)
                self.sum_list.append(y)
                
        print(self.sum_list, sum(self.sum_list))
                      
        
phrase = "climate change"
s = SDR(phrase)
s.split_words()
f = s.split_char()
s.get_bitlist(f)
s.index_bits()
