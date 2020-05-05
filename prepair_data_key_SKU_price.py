# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:55:45 2019

make data whith sku


"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, date, time



def make_data(df, sku):
    #function for prepair data for modeling
    #df is all data-check-transaction
    #sku - is SKU for modeling
    
    df1=df[df["SKU"]==sku]
    #заменяем пропуски в скидке на ноль
    df1["Скидка"]=df1["Скидка"].fillna(0)
    df1["Price"]=(df1["Сумма"])/df1["Количество"]
    df1["NWD"]=1
    df1["NWD"]=list(map(lambda g, m, d: date(g, m, d).isocalendar()[1], 
                   df1["Год"], df1["Месяц"], df1["День"]))
    c=df1.groupby(['Год', "NWD"])["Price"].mean()
    c2=df1.groupby(['Год', "NWD"])["Количество"].sum()
    
    ban=pd.DataFrame({"Price":c, "Num":c2})
    
    
    ban.to_csv("temp.csv")
    ban=pd.read_csv("temp.csv")
    ban["Year"]=ban["Год"]
    del ban["Год"]
    ban.to_csv("temp.csv")
    ban=pd.read_csv("temp.csv")
    
    ban.columns=['T', 'NWD', 'Price', 'Num', 'Year']
    ban=ban[['Price', 'Year', 'NWD',  "T", 'Num' ]]    
    del df1
    

    ban=ban.dropna()
    
    
    
    elast=ban.iloc[-1, :]
    elast=pd.DataFrame(elast)
    elast=elast.T
    elast=pd.concat([elast, elast, elast, elast])
    elast.index=[0,1,2,3]
    price=ban["Price"].iloc[-1]
    elast["Price"][0]=price-price*0.05
    elast["Price"][1]=price-price*0.01
    elast["Price"][2]=price+price*0.01
    elast["Price"][3]=price+price*0.05
    
    return ban, elast

def ComaToPoint(df):
    
    df['Сумма'] = df['Сумма'].astype(str)
    df['Сумма'] = [x.replace(',', '.') for x in df['Сумма']]
    df['Сумма'] = df['Сумма'].astype(float)

    df['Скидка'] = df['Скидка'].astype(str)
    df['Скидка'] = [x.replace(',', '.') for x in df['Скидка']]
    df['Скидка'] = df['Скидка'].astype(float)

    
    return df
    
 
    


    
    