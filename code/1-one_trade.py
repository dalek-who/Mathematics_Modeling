# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 17:04:26 2018

@author: Administrator
"""

import pandas as pd


writer = pd.ExcelWriter('D:/数模美赛2018/B题/6建模/washed_data/trade.xlsx')

for i in range(2000,2017):
    filename='trade-'+str(i)+'.xls'
    df = pd.read_excel('D:/数模美赛2018/B题/6建模/washed_data/'+filename,sheetname='Sheet1')
    df.to_excel(writer,sheet_name=str(i))
    print(i)
    
writer.save()