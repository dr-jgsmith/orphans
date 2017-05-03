# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 17:21:05 2017

@author: justi
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:10:36 2016

@author: smith
@application: text-classification
@domain: qualtiative research
@required-packages: csv, textblob, matplotlib, json

"""
#Import necessary files and packages
import csv
import pandas as pd
import numpy as np
import json
import pickle
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

outfile = open('output4.csv', "w", newline="")
infile = open("training_data.csv", "rt")

f = csv.writer(outfile)
r = csv.reader(infile)

#create empty list to read data into memory
train_data = []
test_data = []

#import data from csv
next(r)
for row in r:
    t = row[2], row[7]
    print(t)
    train_data.append(t)
    #row[4], row[5], row[6], row[7], row[8])

print(train_data)
print(len(train_data))

print("Learning data set....")
cl = NaiveBayesClassifier(train_data)
        
print("Loading test data...")
for row in csv.reader(open("test_data.csv", "rt")):
    print("Classifying new data...")
    text = row[2]
    t = cl.classify(text)
    test = text, t
    print(test)
    test_data.append(test)
    f.writerow([test[0], test[1]])
    
print(cl.accuracy(test_data))   
#for i in test_data:
 #   print(i)


            
    


