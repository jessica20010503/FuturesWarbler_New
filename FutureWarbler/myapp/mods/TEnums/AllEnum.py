from enum import Enum

# Enum 是列舉
# 以下為保證金（TWD\P004以後為USD）
class ProductPrice(Enum):
   #台指期
   tx = 	184000 
   #小台指
   mtx = 46000
   #電子期
   te = 	300000
   #金融期
   tf =	79000
   #小道瓊
   mini_dow =	9350
   #小那斯達克
   mini_nasdaq =	17600
   #小 S&P
   mini_sp =	12540
   #小羅素2000
   mini_russell =	6600
   #黃豆
   soy =	4180
   #小麥
   wheat =	4950
   #玉米
   corn =	2365