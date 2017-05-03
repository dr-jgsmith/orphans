# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 17:20:27 2017

@author: justi
"""

import requests
import lxml
from bs4 import BeautifulSoup
import csv
import sys


string_search = "https://twitter.com/search?q="
term = "walking"
prox = "%20near%3A%22"
radius = "%2C%20WA%22%20within%3A15mi&src=typd&lang=en"

with open('citydatapointswa.csv', "rt") as csvfile:
    posts = csv.reader(csvfile)
    for row in posts:
    	place = row[0]
    	if " " in place == True:
    		place = place.replace(" ", "%20")
    		combined = string_search+term+prox+place+radius
    	else:
    		combined = string_search+term+prox+place+radius
    		print(combined)

f = open("twitterNews.txt", "wb")
for line in combined:
	r = requests.get(combined)
	c = r.content
	print(c)
	f.write(c)
	soup = BeautifulSoup(c)
	for link in soup.find_all("a"):
		print(link.get("href"))