# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 17:18:48 2017

@author: justi
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:23:25 2016

@author: smith
"""
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import csv

def closure_graph(synset, fn):
    seen = set()
    graph = nx.DiGraph()

    def recurse(s):
        if not s in seen:
            seen.add(s)
            graph.add_node(s.name)
            for s1 in fn(s):
                graph.add_node(s1.name)
                graph.add_edge(s.name, s1.name)
                recurse(s1)

    recurse(synset)
    return(graph)
    

f = csv.reader(open("TWO_COLUMN.csv", 'r')) #Edge List
f2 = csv.writer(open("New_TWO_COLUMN.csv", 'w', newline=""))

l = []
l2 = []
next(f)
for i in f:
    w = i[0]
    x = i[1]
    
    w2 = w.split()
    x2 = x.split()
    
    for i in w2:
        l.append(i)
        
    for j in x2:
        l2.append(j)
    
text = nltk.tag.pos_tag(l)

#text = word_tokenize(text)
    
print(text)

w = wn.synset("dog.n.01") 
g = closure_graph(w, lambda s: s.hypernyms())
#pos = graphviz_layout(graph)
pos = nx.DiGraph(g)
nx.draw(g)
nx.draw_networkx_labels(g, pos=nx.DiGraph(g), labels=True)

plt.show()
    