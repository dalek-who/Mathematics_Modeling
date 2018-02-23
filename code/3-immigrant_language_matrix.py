# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 18:36:48 2018

@author: Administrator
"""

import pandas as pd
import numpy as np

sheets_immigrant = pd.read_excel('D:/数模美赛2018/B题/6建模/sim_data/predict_immigrant.xlsx',sheetname=None)

use_countries = pd.read_excel('D:/数模美赛2018/B题/6建模/washed_data/use_countries.xlsx',sheetname='Sheet1')
use_languages = pd.read_excel('D:/数模美赛2018/B题/6建模/washed_data/use_languages.xlsx',sheetname='Sheet1')

start_country_language_percent = pd.read_excel('D:/数模美赛2018/B题/6建模/run_data/start.xlsx',sheetname='country_language_mat_percent')
start_country_language_population = pd.read_excel('D:/数模美赛2018/B题/6建模/run_data/start.xlsx',sheetname='country_language_mat_population')

population_increase = pd.read_excel('D:/数模美赛2018/B题/6建模/washed_data/population_increase.xlsx',sheetname='increase')
population_total    = pd.read_excel('D:/数模美赛2018/B题/6建模/washed_data/population_increase.xlsx',sheetname='increase')

writer_A = pd.ExcelWriter('D:/数模美赛2018/B题/6建模/run_data/con_lan_population.xlsx')
writer_B = pd.ExcelWriter('D:/数模美赛2018/B题/6建模/run_data/con_lan_percent.xlsx')

n_con = 187
m_lan = 44

def get_values(df,remove_total=False,remove_code=False):
    if remove_total == True:
        df = df.iloc[:187,:]
    if remove_code == True:
        df = df.iloc[:,1:]
    return df.values

'''
Ai:人口增长后的 国家-语言-人口矩阵

df_inc:当年的人口增长比例(1+人口增长率)
df_A_pop:人口增长前的 国家-语言人口矩阵
'''
def get_Ai_con_lan_pop_inc(df_inc,df_A_pop):
    m_inc = np.diag(df_inc.tolist())
    m_A = get_values(df_A_pop,remove_code=True,remove_total=True)
    return m_inc.dot(m_A)

#Ai = get_Ai_con_lan_pop_inc(population_increase['1955'],start_country_language_population)

def get_B_con_lan_per_inc(df_pop,df_Ai):

'''
C:国家-语言移出人口矩阵

df_imm:国家-国家-移民人口矩阵（行：to，列：from）
df_B_dstb:国家-语言-百分比矩阵
'''
def get_C_con_lan_imm_out(df_imm,df_B_dstb):
    out = df_imm.sum()
    out = out[1:]
    m_imm_out = out.values
    m_imm_out  = np.diag(m_imm_out.tolist())
    m_B = get_values(df_B_dstb,remove_code=True,remove_total=True)
    return m_imm_out.dot(m_B)

#C = get_C_con_lan_imm_out(sheets_immigrant['1990'],start_country_language_percent)



'''
D:国家-语言移入人口矩阵

df_imm:国家-国家-移民人口矩阵（行：to，列：from）
df_B_dstb:国家-语言-百分比矩阵
'''
def get_D_con_lan_imm_in(df_imm,df_B_dstb):
    m_imm = get_values(df_imm ,remove_code=True)
    m_B = get_values(df_B_dstb,remove_code=True,remove_total=True)
    return m_imm.dot(m_B)
   
    

'''
D = get_D_con_lan_imm_in(sheets_immigrant['1990'],start_country_language_percent)

country_language_percent_no_total_no_code = get_values(country_language_percent,remove_total=True,remove_code=True)
country_country_immigrant_no_code=get_values(sheets_immigrant['1990'],remove_code=True)

m = country_country_immigrant_no_code.dot(country_language_percent_no_total_no_code)

'''    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    