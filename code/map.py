# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:48:01 2018

@author: Administrator
"""
import cairosvg
import pygal
import pygal_maps_world
import pandas as pd
import matplotlib.pyplot  as plt

loc = '../pic/'
sheets = pd.read_excel('../run_data/con_lan_population.xlsx',sheetname=None)
countries=pd.read_excel('countries.xlsx',sheetname='Sheet1')
countries.index = countries['3code']

print('handle language-pop excel......')
for year in sheets:
    sheets[year].index = countries['2code'].tolist()
    sheets[year]=sheets[year].iloc[:,1:]
    
pa = pd.Panel(sheets)
df_tot = pa.major_xs('Total')

languages = df_tot.index.tolist()

writer = pd.ExcelWriter(loc+'language_pop.xlsx')
for language in languages:
    pa.minor_xs(language).to_excel(writer,sheet_name=language)

writer.save()
print('language-pop excel finish !!!')

sheets_lpmap=pd.read_excel(loc+'language_pop.xlsx',sheetname=None)
wm_style=pygal.style.RotateStyle('#3399AA',base_style=pygal.style.LightColorizedStyle)  
ct = 5 #分组数量
#按人数编组]
num = 0
for language in languages[:10]:
    mx=int(sheets_lpmap[language]['2015']['Max'])
    cutter = list(map(lambda x:mx/10**x,range(ct,0,-1)))
    num+=1
    for year in sheets_lpmap[language].columns:
        c=[]
        s = sheets_lpmap[language][year][:-2]
        for i in range(0,ct):
            if i != ct-1:
                group = s.loc[(s>cutter[i]) & (s<=cutter[i+1])].index.tolist()
            else:
                group = s.loc[s>cutter[i]].index.tolist()
            c.append(group)
       
        #绘图
        wm = pygal_maps_world.maps.World(style=wm_style)
        wm.title = language+'-'+year
        for i in range(1,ct):
            wm.add('> '+str(cutter[i]),c[i])
        wm.render_to_file(loc+'maps/'+str(num)+'-'+language+'-'+str(year)+'.svg')
        print(str(num)+'-'+language+'-'+str(year))


            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    