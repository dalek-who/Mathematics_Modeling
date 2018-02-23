# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 22:00:15 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 18:36:48 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
import os

sheets_immigrant = pd.read_excel('../sim_data/predict_immigrant.xlsx',sheetname=None)
sheets_trade     = pd.read_excel('../sim_data/predict_trade.xlsx',sheetname=None)

use_countries = pd.read_excel('../washed_data/use_countries.xlsx',sheetname='Sheet1')
use_languages = pd.read_excel('../washed_data/use_languages.xlsx',sheetname='Sheet1')

start_country_language_percent = pd.read_excel('../run_data/start.xlsx',sheetname='country_language_mat_percent')
start_country_language_population = pd.read_excel('../run_data/start.xlsx',sheetname='country_language_mat_population')

population_increase = pd.read_excel('../washed_data/population_increase.xlsx',sheetname='increase')
population_total    = pd.read_excel('../washed_data/population_increase.xlsx',sheetname='total')

writer_A = pd.ExcelWriter('../run_data/con_lan_population.xlsx')
writer_B = pd.ExcelWriter('../run_data/con_lan_percent.xlsx')

internet_lan = pd.read_excel('../washed_data/internet_language.xls',sheetname='Sheet1')
internet     = pd.read_excel('../washed_data/internet.xls',sheetname='Sheet1')

n_con = 187
m_lan = 44

def get_values(df,remove_total=False,remove_code=False):
    if remove_total == True:
        df = df.iloc[:187,:]
    if remove_code == True:
        df = df.iloc[:,2:]
    return df.values

'''
Ai:人口增长后的 国家-语言-人口矩阵

df_inc:当年的人口增长比例(1+人口增长率)
df_A_pop:人口增长前的 国家-语言人口矩阵
'''
def get_Ai_con_lan_pop_inc(df_inc,m_A):
    m_inc = np.diag(df_inc.tolist())
    return m_inc.dot(m_A)

'''
m_A = start_country_language_population.iloc[:187,2:].values
Ai = get_Ai_con_lan_pop_inc(population_increase['1955'],m_A)
'''

def get_B_con_lan_per_inc(df_pop,m_Ai):
    v_tot = df_pop.values.reshape((n_con,1)) * 1000
    return m_Ai / v_tot    
    #return m_Ai / m_total_pop.T
    
'''
B = get_B_con_lan_per_inc(population_total['1955'],Ai)
'''

'''
C:国家-语言移出人口矩阵

df_imm:国家-国家-移民人口矩阵（行：to，列：from）
df_B_dstb:国家-语言-百分比矩阵
'''
def get_C_con_lan_imm_out(df_imm,m_B):
    out = df_imm.sum()
    out = out[1:]
    m_imm_out = out.values
    m_imm_out  = np.diag(m_imm_out.tolist())
    return m_imm_out.dot(m_B)

#C = get_C_con_lan_imm_out(sheets_immigrant['1990'],start_country_language_percent)



'''
D:国家-语言移入人口矩阵

df_imm:国家-国家-移民人口矩阵（行：to，列：from）
df_B_dstb:国家-语言-百分比矩阵
'''
def get_D_con_lan_imm_in(df_imm,m_B):
    m_imm = df_imm.iloc[:,1:].values
    return m_imm.dot(m_B)
   
    

'''
D = get_D_con_lan_imm_in(sheets_immigrant['1990'],start_country_language_percent)

country_language_percent_no_total_no_code = get_values(country_language_percent,remove_total=True,remove_code=True)
country_country_immigrant_no_code=get_values(sheets_immigrant['1990'],remove_code=True)

m = country_country_immigrant_no_code.dot(country_language_percent_no_total_no_code)

'''    

'''
M: 国家-语言贸易额矩阵

df_M: 国家-国家贸易额矩阵
m_B: 国家-语言百分比矩阵
'''
def get_M_trade(df_td,m_B):
    m_td = df_td.iloc[:,1:].values
    m_M1 = m_td.dot(m_B)
    v_tot = np.sum(m_M1,axis=1)
    v_tot = v_tot.reshape((n_con,1))
    return m_M1 / v_tot
'''
M = get_M_trade(sheets_trade['2005'],B)
'''

'''
N:国家-语言 互联网影响因子矩阵

m_pop:各国互联网普及率对角阵
m_lan: 互联网使用语言百分比（行向量）扩展成 n_con行 的矩阵
'''    
def get_N_internet():
        m_pop = np.diag(internet['Internet_Per'].tolist())
        li = internet_lan['percent'].tolist()
        li = [li]*n_con
        m_lan = np.array(li)
        return m_pop.dot(m_lan)
    
def write_excel(m_array,year,writer):
    tot    = np.sum(m_array,axis=0).tolist()
    maxium = np.max(m_array,axis=0).tolist()
    df = pd.DataFrame(m_array,columns=use_languages['languages'],index=use_countries['countries'])
    df = df.T
    df['Total'] = tot
    df['Max']   = maxium
    df = df.T
    df.to_excel(writer,sheet_name=str(year))
'''    #绘图
    pic = df.cumsum() 
    pic.plot()
    plt.show()
'''
    
def module(a,b,rand_trade=False,rand_tot=False):
    print('running module...')
    A = start_country_language_population.iloc[:187,2:].values
    N = get_N_internet()
    for year in range(2015,2075,5):
        print(year)
        
        Ai = get_Ai_con_lan_pop_inc(population_increase[str(year)],A)
        B  = get_B_con_lan_per_inc(population_total[str(year)],Ai)
        
        write_excel(A,year,writer_A)
        write_excel(B,year,writer_B)
        
        C  = get_C_con_lan_imm_out(sheets_immigrant[str(year)],B)
        D  = get_D_con_lan_imm_in(sheets_immigrant[str(year)],B)
        E  = Ai + D - C
        M  = get_M_trade(sheets_trade[str(year)],B)
        
        if rand_trade:
            trade_random = np.random.randint(0,a)+np.random.random()
            F = trade_random*M + b*N
        else:
            F  = a*M + b*N
        tot = np.diag(population_total[str(year)])*1000
        
        R = E + tot.dot(F)
        if rand_tot:
            R = R + np.random.randint(-rand_tot,rand_tot+1,R.shape)
        R[R<1000] = 0   #参数
        A = R
        
    writer_A.save()
    writer_B.save()
    print('module finish !!!')
    
def draw(a,b,rand_tot,lans=m_lan):
    print('drawing lines...')
    loc = '../pic/'
    sheets = pd.read_excel('../run_data/con_lan_population.xlsx',sheetname=None)
    #df_total:columns:语言，index:年 values:人口
    df_total = pd.DataFrame()
    for year in range(2015,2075,5):
        sheets[str(year)].index = sheets[str(year)]['countries']
        df_total[str(year)] = sheets[str(year)].T['Total']
    df_total = df_total.iloc[1:,:].T
    df_total = df_total.iloc[:,:lans]

    #df_order:columns:年 index:123456 values:语言
    order = {}
    for year in range(2015,2075,5):
        order[str(year)]=df_total.T[str(year)].sort_values(ascending=False).index
    df_order=pd.DataFrame(order)
    df_order.index = range(1,lans+1)
    
    order_num = {}
    for year in range(2015,2075,5):
        li = []
        for country in df_total.columns:
            sr=df_order[str(year)]
            li.append(sr[sr==country].index[0])
        order_num[str(year)]=li
    df_order_num = pd.DataFrame(order_num,index=df_total.columns.tolist())
    df_order_num = df_order_num.T
    
    #存入excel
    writer = pd.ExcelWriter(loc+'predict.xlsx')
    df_total.to_excel(writer,sheet_name='Total')
    df_order.to_excel(writer,sheet_name='order')
    df_order_num.to_excel(writer,sheet_name='order_num')
    writer.save()

    #绘图

    legend_loc=(1.01,1.4) #图例位置
    size = (10,5)

    df_total.plot(kind='line',title='language user population per year')
    plt.legend(bbox_to_anchor=legend_loc, loc=2, borderaxespad=0., handleheight=0.6)
    plt.savefig(loc+str(lans)+'-lans_tot-rt-'+str(rand_tot)+'.png')

    df_order_num.applymap(lambda x:-x).plot(kind='line',title='order of language user population per year')
    plt.legend(bbox_to_anchor=legend_loc, loc=2, borderaxespad=0., handleheight=0.6)
    plt.savefig(loc+str(lans)+'-lans_order_num-rt-'+str(rand_tot)+'.png')
    
    print('drawing finish !!!')
    return df_total
    


def running(a,b,rand_tot):
    module(a,b,rand_trade=False,rand_tot=rand_tot) #1700000
    df = draw(a,b,rand_tot,20)
    #os.system("python map.py")
    
    
if __name__ == '__main__':
    a = 0.1
    b = 0.01
    for rand_tot in map(lambda x:10**x,range(4,11)):
        print('rand_tot=',rand_tot)
        running(a,b,rand_tot)
        
    
    
    
    
    
    
    
    