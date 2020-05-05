# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 15:53:15 2019

@author: Леонид
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ConCorCoeff import concordance_correlation_coefficient as CCC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from moving_average import moving_average 
from sklearn.externals import joblib
from ModelEnd import model
from prepair_data_key_SKU_price import make_data
from prepair_data_key_SKU_price import ComaToPoint

from datetime import datetime

from sklearn.linear_model import LinearRegression as LR
from sklearn.linear_model import LinearRegression as SVR
from col_model import col_model

import os.path
import sys
key=pd.read_csv("key_SKU.csv",delimiter=";")
sku=list(key["SKU"])

#df1 = pd.read_csv("data.csv",delimiter=";",
#                 encoding="windows-1251")
#encoding = [
#            'utf-8',
#            'cp500',
#            'utf-16',
#            'GBK',
#            'windows-1251',
#            'ASCII',
#            'US-ASCII',
#            'Big5'
#            ]
encoding = [
            'utf-8',
            'windows-1251'
            ]



flag=0
for enc in encoding:
    try:
        df1 = pd.read_csv("data.csv",delimiter=",",
                 encoding=enc)
    except (UnicodeDecodeError, LookupError):
        pass
    else:
        flag=1
        print('Данные считаны')
        break
if flag==0:
    print('Ошибка чтения файла')
    sys.exit()

df1=ComaToPoint(df1)
plt.close("all")
if not os.path.exists("graphs"):
    os.makedirs("graphs") 
#segm=get_all_segment(df1)

n_day=10
Sta=[]
Log=[]
for it in range(len(sku)):
    now0 = datetime.now()
    s=sku[it]
    #готовим данные. Извлекаем из общей выборки данные по соответствующей SKU
    try:
        dm, elast=make_data(df1,  s)
    except:
        sta=[s]
        
        sta.append("недостаточно данных")
        Sta.append(sta)
        continue

    if len(dm)<10:
        sta=[s]
        
        sta.append("недостаточно данных")
        Sta.append(sta)
        continue
    sta=[s, len(dm)]
    
    #на основе полученной выборки формируем выход и удаляем его из выборки    
    Y=dm["Num"]
    del dm["Num"]
    #формируем бинарную маску. Mask - матрица масок, где каждая строка это маска
    # на входы. По принципу включения исключения входа. Маска делается с учетом
    #того, что первый вход - цена и он всегда присутствует в модели
    #маска формируется перебором всех возможных комбинаций оставшихся входов. 
        
        #считаем устойчивый коэффициент
    try:
        stlb=["Price"]        
        X=dm[stlb]        
        X=X.values
        y=Y.values
        
#        lr=LR()
        if len(y)<30:
            lr=col_model( n_clasters=1, base_model="LR")
        else:
            lr=col_model( n_clasters=2, base_model="LR")
        lr=lr.fit(X, y)
        price_trand=np.linspace(np.min(X), np.max(X), 1000)
        y_trand=lr.predict(price_trand[:, np.newaxis])
        y_mod=lr.predict(X)
        elast=elast.values
        y_elast=lr.predict(elast[:,0][:, np.newaxis])
        y_elast=y_elast[:, np.newaxis]
        if (y_elast[2, 0]+y_elast[1, 0])!=0:
            
            k_elast_1_LR=(((y_elast[2, 0]-y_elast[1, 0])/(elast[2, 0]-elast[1, 0]))*
                     ((elast[2, 0]+elast[1, 0])/(y_elast[2, 0]+y_elast[1, 0])))
        else:
            k_elast_1_LR=0
        if (y_elast[3, 0]+y_elast[0, 0])!=0:
            k_elast_5_LR=(((y_elast[3, 0]-y_elast[0, 0])/(elast[3, 0]-elast[0,0]))*
                     ((elast[3, 0]+elast[0, 0])/(y_elast[3, 0]+y_elast[0, 0])))
        else:
            k_elast_5_LR=0
        sta.append(k_elast_1_LR)
        sta.append(k_elast_5_LR)
        c_train=CCC(y[:, np.newaxis], y_mod[:, np.newaxis])
        
        curent=curent=np.array([X[-1,0]])
        y_curent=lr.predict(curent[:, np.newaxis])
        
        
        
        Sta.append(sta)
    except:
        print("Ошибка сбора файла Result.csv "+sku[it])
        continue
        
    
    #отрисовка графиков
    try:
        s1=s.replace('/', '')
        s1=s1.replace('\\' , '')
        s1=s1.replace('*' , '')
        plt.figure()
#        plt.plot(y, "r-", label="Выборка")
#        plt.plot(y_mod, "b--", label="Модель")
        plt.plot(X[:, 0], y, "bo",  label="Выборка")
        plt.plot(price_trand, y_trand, "r-", label="Модель")
        plt.plot(curent, y_curent, "go", label="Curent")
        plt.plot(elast[1:3,0], y_elast[1:3,0], "yo", label="elast 1%")
        plt.plot([elast[0,0], elast[-1,0]], 
                 [y_elast[0,0],y_elast[-1,0]] , "ko", label="elast 5%")
        
        plt.legend()
        plt.title("Trand "+s+"точ. "+str(np.round(c_train, 2)))        
        plt.savefig("graphs\\"+s1+"_trand.png")
        plt.close("all")

    except:
        print("Ошибка отрисовки графиков")
        continue
    
    now1 = datetime.now()
    now=now1-now0
    s=str(now)
    s=s[0:-7]
    print("Время обучения: {0}".format(s))

try:
   
    # print("разница = {0} ({1}%)".format(dist, distProc))
    col=["SKU",  "Обеспеченность данных", 
         "k_elast_1_LR","k_elast_5_LR"]
    Sta=pd.DataFrame(Sta, columns=col)
    Sta=Sta.round(2)
    Sta.to_csv("Result.csv", sep="\t")
except:
    print("Ошибка вывода файл result.csv")    
    
try:        
    Log=pd.DataFrame(Log, columns=["SKU", "c_train","c_test","best_feature",
                                   "best_model","time_learn", "Year", "Month",
                                   "Day", "Time"])
        
    if os.path.exists("Log.csv")==False:
        Log.to_csv("Log.csv", mode='a')
    else:
        Log.to_csv("Log.csv", header=False, mode='a')
        
    print("work completed")
    #plt.show()
except:
    print("Ошибка вывода файл Log.csv")
    
    