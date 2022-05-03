# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 22:54:14 2022

@author: Tiffany
"""
import pandas as pd

def futuresDateTime(futures,start,end,freq):
    if futures =="tf":
        df = pd.read_csv("./myapp/mods/2017-2021-tf-1min.csv")
    elif futures =="te":
        df = pd.read_csv("./myapp/mods/2017-2022-te-1min.csv")
    elif futures =="tx":
        df = pd.read_csv("./myapp/mods/2017-2022-tx-1min.csv")
    elif futures =="mtx":
        df = pd.read_csv("./myapp/mods/2017-2022-mtx-1min.csv")
    elif futures =="corn":
        df = pd.read_csv("./myapp/mods/2017-2022-corn-1min.csv")
    elif futures =="mini_nasdaq":
        df = pd.read_csv("./myapp/mods/2017-2022-E-mini-nasdaq-1min.csv")  
    elif futures =="mini_russell":
        df = pd.read_csv("./myapp/mods/2017-2022-E-mini-russell-1min.csv")  
    elif futures =="mini_sp":
        df = pd.read_csv("./myapp/mods/2017-2022-E-mini-s&p-1min.csv") 
    elif futures =="mini_dow" :
        df = pd.read_csv("./myapp/mods/2017-2022-mini_dow_1min.csv") 
    elif futures =="soybean" :
        df = pd.read_csv("./myapp/mods/2017-2022-soybean-1min.csv") 
    elif futures =="wheat":
        df = pd.read_csv("./myapp/mods/2017-2022-wheat-1min.csv") 
    else:
        df = pd.read_csv("./myapp/mods/2021-2022-a_debt-1min.csv") 
        
    df['DateTime'] =pd.to_datetime(df[futures+'_date'] + df[futures+'_time'], format='%Y-%m-%d%H:%M:%S')
    df[futures+'_date'] = pd.to_datetime(df[futures+'_date'])
    df[futures+'_time'] = pd.to_datetime(df[futures+'_time'])
    mask = (df[futures+'_date'] >= start) & (df[futures+'_date'] <= end)
    filtered_df=df.loc[mask]
    filtered_df = filtered_df.set_index("DateTime")
    df_final = filtered_df.groupby(pd.Grouper(freq=freq)).agg({
        futures+"_open" : "first",
        futures+"_close" : "last",
        futures+"_low": "min",
        futures+"_high": "max",
        futures+"_volume": "sum"
    })
    df_final = df_final.dropna()
    return df_final


