# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:36:57 2019

@author: Леонид
"""
import pandas as pd
from datetime import datetime, date, time

def ComaToPoint(df):
    
    df['Сумма'] = df['Сумма'].astype(str)
    df['Сумма'] = [x.replace(',', '.') for x in df['Сумма']]
    df['Сумма'] = df['Сумма'].astype(float)

    df['Скидка'] = df['Скидка'].astype(str)
    df['Скидка'] = [x.replace(',', '.') for x in df['Скидка']]
    df['Скидка'] = df['Скидка'].astype(float)

    
    return df
   
encoding = [
            'utf-8',
            'windows-1251',
            ]
flag=0
for enc in encoding:
    try:
        df1 = pd.read_csv("data.csv",delimiter=";", index_col=False ,
                 encoding=enc)
    except (UnicodeDecodeError, LookupError):
        pass
    else:
        flag=1
        print('Данные считаны')
        break
df1=ComaToPoint(df1)    
df1["Скидка"]=df1["Скидка"].fillna(0)
#df1["Price"]=(df1["Сумма"]+df1["Скидка"])/df1["Количество"]
df1["Price"]=(df1["Сумма"])/df1["Количество"]
df1["NWD"]=1

df1["NWD"]=list(map(lambda g, m, d: date(g, m, d).isocalendar()[1], 
                   df1["Год"], df1["Месяц"], df1["День"]))
c=df1.groupby(['Год', "NWD", "SKU"])["Price"].mean()
ban=pd.DataFrame({"Price":c})
ban.to_csv("temp.csv")
ban=pd.read_csv("temp.csv")

c1=ban.groupby(["SKU"])["Price"].min()
c2=ban.groupby(["SKU"])["Price"].max()

ban=pd.DataFrame({"min_price":c1, "max_price":c2})
ban.to_csv("temp.csv")
ban=pd.read_csv("temp.csv")

d=df1["SKU"].value_counts()

d.to_csv("SKU.csv", header=True)
d=pd.read_csv("SKU.csv")
d.columns=["SKU", "Num"]

d=pd.merge(d, ban, how='left')
d["min_price"]=d["min_price"]*0.9
d["max_price"]=d["max_price"]*1.2
d.to_csv("SKU.csv", header=True,  sep=";")


