# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:32:46 2022

@author: Tiffany
"""


# futures代表要選哪個資料集
# longshort代表要選作多還是做空的predict結果
# longshort 0 代表作多 1 代表作空


def bt_dataframe(futures, longshort, algo):
    # 如果是多
    if longshort == 0:
        name = "myapp\\mods\\algodata\\"+algo+"_bt_"+futures+"_long.csv"
        #file= pd.read_csv('data/rf_bt_mtx_short.csv')

    # 如果是空
    else:
        name = "myapp\\mods\\algodata\\"+algo+"_bt_"+futures+"_short.csv"

    return name

# 這邊演算法的結果顯示途徑接著寫
# 這邊檔名的部分 fall 等同做空(short)， rise 等同做多(long)


def bt_result_dataframe(futures, longshort, algo):
    # 如果是多
    if longshort == 0:
        name = "myapp\\mods\\algodata_result\\"+algo+"_"+futures+"_rise_result.csv"
        #file= pd.read_csv('myapp/mods/algodata_result/SVM_tf_fall_result.csv')

    # 如果是空
    else:
        name = "myapp\\mods\\algodata_result\\"+algo+"_"+futures+"_fall_result.csv"

    return name
