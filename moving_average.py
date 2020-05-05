# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 20:00:28 2019

@author: Леонид
"""
import numpy as np
#import matplotlib.pyplot as plt

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

#n=11
#t=np.array(dm["Num"])
#x=moving_average(t, n=n)
#plt.figure()
#plt.plot(t[int(n/2):-int(n/2)], "r--")
#plt.plot(x, "b")