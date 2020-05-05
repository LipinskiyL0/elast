# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:13:13 2020

@author: Леонид
"""
import pandas as pd
l=['Магазин',  "Чек ID", "Группа", "Код", "SKU", 
   "Ценовой сегмент", "Бренд", "Год", "Месяц", "День", "Количество", 
   "Сумма", "Скидка", "Тип чека"]
df=pd.read_csv("elast.csv", delimiter="	", encoding="windows-1251")
df.columns=l
df.to_csv("data.csv", index=False)
df=pd.read_csv("data.csv")