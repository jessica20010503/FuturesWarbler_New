from re import A
from myapp.mods import trade_algo_strategy
import backtrader as bt
import os
from pathlib import Path
import datetime
from matplotlib.pyplot import margins
from pandas import Period
from sklearn.metrics import log_loss, pair_confusion_matrix
from backtrader.feeds import GenericCSVData #導入的原因是:要修改用成有predict的data
from myapp.mods.TComponentFacade import SetData
from myapp.mods.bt_dataframe import bt_dataframe
from myapp.models import Member

'''
longshort '0':做多 '1':做空
instrategy進場策略 '0':ma '1':osc '2':rsi '3':kd '4':bias '5':william 
outstrategy出場策略 '0':ma '1':rsi '2':kd '3':bias '4':william  
stopstrategy停損停利 '1':比率 '2':點數 '3':移動
profit停利數字
loss停損數字
'''
#建構SetData變成全域
setData = SetData()
#建構Cerebro變成全域
cerebro = bt.Cerebro()

class Strategy_algo(bt.Strategy):
    #停損停利會要用到的東西
    params = (
        # MA
        ('MA_period_fast', 5),
        ('MA_period_slow', 15),
        # RSI
        ('RSI_period', 12),
        # KD
        ('K_period', 14),
        ('D_period', 3),
        # 移動停損點數，這邊先寫死，之後需接使用者填入的
        ('Trailing_stop', 20),
        # osc
        ('p1', 12),
        ('p2', 26),
        ('p3', 9),
        # william
        ('wperiod', 14),
        # bias
        ('smaperiod', 10),
    )


    def __init__(self, longshort, algostrategy, stopstrategy, losspoint, profitpoint, tmp, moneymanage, doData, delta, maxQuan, buyMoney, setdata):
        #初始化
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        #我們自己的predict 
        self.datapredict = self.datas[0].predict
        #一開始是沒有單子的
        self.order = None

        #以下為指標
        self.macdhist = bt.ind.MACDHisto(
            self.datas[0], period_me1=self.params.p1, period_me2=self.params.p2, period_signal=self.params.p3)
        self.williams = bt.ind.WilliamsR(
            self.datas[0],period=self.params.wperiod)
        self.sma10 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.smaperiod)
        #self.bias = (self.datas[0]-self.sma10)/self.sma10 * 100
        # MA
        self.ma1 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.MA_period_fast)
        self.ma2 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.MA_period_slow)
        self.crossover_MA = bt.indicators.CrossOver(self.ma1, self.ma2)
        # RSI
        self.rsi = bt.indicators.RSI(
            self.datas[0], period=self.params.RSI_period)
        # KD
        self.k = bt.indicators.StochasticSlow(
            self.datas[0], safediv = True, period=self.params.K_period)
        self.d = bt.indicators.StochasticSlow(
            self.datas[0], safediv = True, period=self.params.D_period)
        self.crossover_KD = bt.indicators.CrossOver(self.k, self.d)

        self.sellprice = 0
        self.buyprice = 0

        self.long_short = longshort
        self.algo_strategy = algostrategy
        self.stopstrategy = stopstrategy
        self.loss = losspoint
        self.profit = profitpoint
        self.tmp = tmp
        self.moneymanage = moneymanage

        self.doData = doData
        self.delta = delta
        self.maxQuan = maxQuan
        self.buyMoney = buyMoney
        self.doPrice = setdata.GetProductPrice()
        self.buyMonlist = setdata.GetList()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("Buy Executed {}".format(order.executed.price))
                self.buyprice = order.executed.price
            elif order.issell():
                self.log("Sell Executed {}".format(order.executed.price))
                self.sellprice = order.executed.price
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def next(self):
        self.log("Close {}".format(self.dataclose[0]))
        # @
        self.userName =  setData.userName
        self.doData = setData.doData
        if self.order:
            return

        #若是做多
        if self.long_short == 0:
            #且目前沒有提交買單
            if not self.position:
                
                #則判斷是否符合演算法進場邏輯
                if self.algo_strategy == 0:
                   trade_algo_strategy.long_in_algo(self)
            else:
            #若目前有商品在手中了    
            #則判斷停損停利
                if self.stopstrategy == 1:
                    trade_algo_strategy.long_percentage(
                        self=self, loss=self.loss, profit=self.profit)
                elif self.stopstrategy == 2:
                    trade_algo_strategy.long_point(
                        self=self, loss=self.loss, profit=self.profit)
                else:
                    trade_algo_strategy.long_trailing(
                        self=self, tmpHigh=self.tmp, loss=self.loss)

        #若是做空
        else:
            #且手上無任何單子
            if not self.position:
                #則使用演算法進場策略
                if self.algo_strategy == 0:
                    trade_algo_strategy.short_in_algo(self)
            else:
            #若手上已商品在手上
            # 則判斷停損停利
                if self.stopstrategy == 1:
                    trade_algo_strategy.short_percentage(
                        self=self, loss=self.loss, profit=self.profit)
                elif self.stopstrategy == 2:
                    trade_algo_strategy.short_point(
                        self=self, loss=self.loss, profit=self.profit)
                #else:
                #    bt_strategy_algo.short_trailing(
                #        self=self, tmpLow=self.tmp, loss=self.loss)
        # @
        setData.tobuy = self.tobuy
        setData.tosell = self.tosell

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print("{} {}".format(dt.isoformat(), txt))


#因為我們的回測這次需要用到predict這個欄位，然而GenericCSVData裡面沒有這個參數，所以我們要自己去重做一個可以包含predict的feeder
#參考文章:https://blog.csdn.net/m0_46603114/article/details/105937213
class GenericCSVData_Predict(GenericCSVData):
    lines = ('predict',)
    params = (('predict', 8),)


class SetStrategy() :
    def __init__(self)-> None:
        self.sellprice = 0
        self.buyprice = 0
        self.useData = ""
        self.long_short = 0
        self.stopstrategy = 1
        self.profit = 1
        self.loss = 1
        self.moneymanage = 1
        self.userName = ''
        self.doData = ''
        self.memberid = ''
        self.cashtype=0
        self.algo_strategy = 0


    def SetValue(self):
        # django.db.connections.close_all()
        print("IN")
        print(self.maxQuan)
        print(self.delta)
        print(self.doData)
        print(self.maxQuan)
        setData.maxQuan  = self.maxQuan
        setData.delta = self.delta
        setData.doData = self.doData
        setData.buyMoney = setData.GetProductPrice()

        setData.long_short = self.long_short
        setData.stopstrategy = self.stopstrategy
        setData.profit = self.profit
        setData.loss = self.loss
        setData.moneymanage = self.moneymanage
        setData.userName = self.userName

        setData.tobuy = 0
        setData.tosell = 0


        cerebro = bt.Cerebro()
        cerebro.broker.setcash(10000000)
        #券商保證金以及手續費設定
        cerebro.broker.setcommission(commission=0.001, margin=2063)
        value = cerebro.broker.getvalue()

        cerebro.addstrategy(Strategy_algo,longshort=0, algostrategy=0, stopstrategy=1, losspoint=10, profitpoint=10, tmp=value, moneymanage=3, doData=setData.doData, delta=setData.delta, maxQuan=setData.maxQuan, buyMoney=setData.buyMoney, setdata=setData)

        #加入資料集 先用mtx並且先假裝做"多"
        filename = bt_dataframe("mtx",0,"rf")
        #載入資料集
        data = GenericCSVData_Predict(dataname=filename,
                                    fromdate=datetime.datetime(2018, 1, 1),
                                    todate=datetime.datetime(2018, 12, 31),
                                    nullvalue=0.0,
                                    dtformat=('%Y-%m-%d'),
                                    tmformat=('%H:%M:%S'),
                                    date=0,
                                    time=1,
                                    high=3,
                                    low=5,
                                    open=2,
                                    close=4,
                                    volume=6,
                                    predict=7,
                                    openinterest=-1)



        cerebro.adddata(data)
        cerebro.run()

        memberdate = Member.objects.filter(member_id=self.userName)
        for i in memberdate:
            twd = int(i.member_twd) - int(setData.tobuy) + int(setData.tosell)
            usd = int(i.member_usd) - int(setData.tobuy) + int(setData.tosell)
            # usd = int(i.member_usd) + int(member_usd)
        print(self.cashtype)    
        if self.cashtype == 0:
            Member.objects.filter(member_id=self.userName).update(member_twd=int(twd))
            print("原本的錢")
            print(self.cash)
            print("看下面")
            print(setData.tobuy)
            print(setData.tosell)
            print("最後的錢")
            print(twd)
        else:
            Member.objects.filter(member_id=self.userName).update(member_usd=int(usd))
            print("原本的錢")
            print(self.cash)
            print("看下面")
            print(setData.tobuy)
            print(setData.tosell)
            print("最後的錢")
            print(usd)

        # print("final profolio {}".format(cerebro.broker.getvalue()))
        # cerebro.plot()