from email import header
from time import sleep
from matplotlib.pyplot import cla
import requests as rq
import backtrader as bt
# 要記得載入 Enum
from myapp.mods.TEnums import ProductPrice 

class SetData():
   def __init__(self):
      # super(SetData,self).__init__()
      # 買一口期貨的錢（原始保證金）
      self.doData = 0 
      # 買一口期貨的錢（原始保證金）（意義上和 doData 一樣，但功能不太一樣）
      self.buyMoney = 0 
      # 固定比率 計算公式的 delta
      self.delta = 0  
      # 假設最大買賣口數
      self.maxQuan = 0 
      
      self.sellprice = 0
      self.buyprice = 0

      self.long_short = 0
      self.in_strategy = 1
      self.out_strategy = 1
      self.stopstrategy = 1
      self.profit = 1
      self.loss = 1
      self.moneymanage = 1
      self.userName = ''
      self.stock = ''
      
   
   # 原始保證金
   def GetProductPrice(self):
      # doData = int(self.doData)
      # 代入 AllEnum.py 的保證金
      return ProductPrice[self.doData].value

   # 固定比率
   def GetList(self):
      # 帳戶權益需求（陣列）
      buyMonlist = []
      for i in range(1,self.maxQuan+1):
         if i == 1:
               # 買第一口的錢 ＝ 原始保證金
               buyCount = self.buyMoney
               buyMonlist.append(buyCount)
         else:
               buyCount = (i-1)*self.delta+buyCount
               buyMonlist.append(buyCount)
      return  buyMonlist 

# if __name__ == '__main__':
# # 把 enum 列進來
#    productPrice = ProductPrice
#    setData = SetData()
#    setData.doData = "P003"
#    setData.delta = 10000
#    setData.maxQuan = 10
#    for i in range(11,13):
#       setData.buyMoney = productPrice[f"P0{i}"].value
#       print(setData.GetList())
#    # print(productPrice['P001'].value)