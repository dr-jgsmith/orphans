# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 17:18:19 2017

@author: justi
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 21:31:03 2016

@author: smith
"""

#the voronoi

from scipy.spatial import Voronoi, voronoi_plot_2d
import csv
import numpy as np
import matplotlib.pyplot as plt

f = csv.reader(open("fm_data_us.csv", 'r'))

points = []

next(f)
for row in f:
    p = []

    #farmers market
    lat = row[20] 
    lon = row[21]

    try:
        x = float(lat)
        y = float(lon)
        p.append(x)
        p.append(y)
        points.append(p)
        print(p)
    except Exception:
        print("skipped error.")
        pass
    

data = np.array(points)
vor = Voronoi(data)
voronoi_plot_2d(vor)
plt.show()
f.close()