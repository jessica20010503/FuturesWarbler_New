import django
from myapp.models import Member
import backtrader as bt
import os
from pathlib import Path
from matplotlib.pyplot import margins
from pandas import Period
from sklearn.metrics import log_loss, pair_confusion_matrix
from myapp.mods import trade_strategy
from myapp.mods.TComponentFacade import SetData
from datetime import date, datetime

# 建構SetData變成全域
setData = SetData()
# 建構Cerebro變成全域
cerebro = bt.Cerebro()

'''
longshort '0':做多 '1':做空
instrategy進場策略 '0':ma '1':osc '2':rsi '3':kd '4':bias '5':william 
outstrategy出場策略 '0':ma '1':rsi '2':kd '3':bias '4':william  
stopstrategy停損停利 '1':比率 '2':點數 '3':移動
profit停利數字
loss停損數字
moneymanage資金管理 '1':口數 '2':金額 '3':比率
'''


class Strategy(bt.Strategy):
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

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.order = None
        self.macdhist = bt.ind.MACDHisto(
            self.datas[0], period_me1=self.params.p1, period_me2=self.params.p2, period_signal=self.params.p3)
        self.williams = bt.ind.WilliamsR(
            self.datas[0], period=self.params.wperiod)
        self.sma10 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.smaperiod)
        self.bias = (self.datas[0]-self.sma10)/self.sma10 * 100
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
            self.datas[0], period=self.params.K_period)
        self.d = bt.indicators.StochasticSlow(
            self.datas[0], period=self.params.D_period)
        self.crossover_KD = bt.indicators.CrossOver(self.k, self.d)

        self.sellprice = setData.sellprice
        self.buyprice = 0
        self.long_short = 0
        self.in_strategy = 1
        self.out_strategy = 1
        self.stopstrategy = 1
        self.loss = 1
        self.profit = 1
        self.moneymanage = 1
        self.doData = ''

        self.doPrice = setData.GetProductPrice()
        self.buyMonlist = setData.GetList()

        self.tobuy = setData.tobuy
        self.tosell = setData.tosell

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
        # self.log("Close {}".format(self.dataclose[0]))
        self.userName = setData.userName
        self.doData = setData.doData
        if self.order:
            return

        # 作多
        if self.long_short == 0:
            # 買入
            if not self.position:
                # if self.long_short =="0":
                if self.in_strategy == 0:
                    trade_strategy.long_in_ma(
                        self=self, crossover_MA=self.crossover_MA)
                elif self.in_strategy == 1:
                    trade_strategy.long_in_osc(
                        self=self, macdhist=self.macdhist)

                elif self.in_strategy == 2:
                    trade_strategy.long_in_rsi(self=self, rsi=self.rsi)
                elif self.in_strategy == 3:
                    trade_strategy.long_in_kd(
                        self=self, crossover_KD=self.crossover_KD)
                elif self.in_strategy == 4:
                    trade_strategy.long_in_bias(self=self, bias=self.bias)
                elif self.in_strategy == 5:
                    trade_strategy.long_in_william(
                        self=self, williams=self.williams)

            # 賣出
            else:
                if self.out_strategy == 0:
                    trade_strategy.long_out_ma(
                        self=self, crossover_MA=self.crossover_MA)
                elif self.out_strategy == 1:
                    trade_strategy.long_out_rsi(self=self, rsi=self.rsi)
                elif self.out_strategy == 2:
                    trade_strategy.long_out_kd(
                        self=self, crossover_KD=self.crossover_KD)
                elif self.out_strategy == 3:
                    trade_strategy.long_out_bias(self=self, bias=self.bias)
                elif self.out_strategy == 4:
                    trade_strategy.long_out_william(
                        self=self, williams=self.williams)

                if self.stopstrategy == 1:
                    trade_strategy.long_percentage(
                        self=self, loss=self.loss, profit=self.profit)
                elif self.stopstrategy == 2:
                    trade_strategy.long_point(
                        self=self, loss=self.loss, profit=self.profit)
                else:
                    trade_strategy.long_trailing(
                        self=self, tmpHigh=cerebro.broker.getvalue(), loss=self.loss)

        # 作空
        else:
            # 買入
            if not self.position:
                if self.in_strategy == 6:
                    trade_strategy.short_in_ma(
                        self=self, crossover_MA=self.crossover_MA)
                elif self.in_strategy == 7:
                    trade_strategy.short_in_osc(
                        self=self, macdhist=self.macdhist)
                elif self.in_strategy == 8:
                    trade_strategy.short_in_rsi(self=self, rsi=self.rsi)
                elif self.in_strategy == 9:
                    trade_strategy.short_in_kd(
                        self=self, crossover_KD=self.crossover_KD)
                elif self.in_strategy == 10:
                    trade_strategy.short_in_bias(self=self, bias=self.bias)
                else:
                    trade_strategy.short_in_william(
                        self=self, williams=self.williams)

            # 賣出
            else:
                if self.out_strategy == 5:
                    trade_strategy.short_out_ma(
                        self=self, crossover_MA=self.crossover_MA)
                elif self.out_strategy == 6:
                    trade_strategy.short_out_rsi(self=self, rsi=self.rsi)
                elif self.out_strategy == 7:
                    trade_strategy.short_out_kd(
                        self=self, crossover_KD=self.crossover_KD)
                elif self.out_strategy == 8:
                    trade_strategy.short_out_bias(self=self, bias=self.bias)
                else:
                    trade_strategy.short_out_william(
                        self=self, williams=self.williams)

                if self.stopstrategy == 1:
                    trade_strategy.short_percentage(
                        self=self, loss=self.loss, profit=self.profit)
                elif self.stopstrategy == 2:
                    trade_strategy.short_point(
                        self=self, loss=self.loss, profit=self.profit)
                else:
                    trade_strategy.short_trailing(
                        self=self, tmpLow=cerebro.broker.getvalue(), loss=self.loss)

        setData.tobuy = self.tobuy
        setData.tosell = self.tosell

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print("{} {}".format(dt.isoformat(), txt))


class SetStrategy():
    def __init__(self) -> None:
        self.sellprice = 0
        self.buyprice = 0
        self.useData = ""
        self.long_short = 0
        self.in_strategy = 1
        self.out_strategy = 1
        self.stopstrategy = 1
        self.profit = 1
        self.loss = 1
        self.moneymanage = 1
        self.userName = ''
        self.doData = ''
        self.startTime = ''
        self.endTime = ''
        self.memberid = ''
        self.cashtype = 0

    def SetValue(self):
        # django.db.connections.close_all()
        print("IN")
        print(self.maxQuan)
        print(self.delta)
        print(self.doData)
        print(self.maxQuan)
        setData.maxQuan = self.maxQuan
        setData.delta = self.delta
        setData.doData = self.doData
        setData.buyMoney = setData.GetProductPrice()

        setData.long_short = self.long_short
        setData.in_strategy = self.in_strategy
        setData.out_strategy = self.out_strategy
        setData.stopstrategy = self.stopstrategy
        setData.profit = self.profit
        setData.loss = self.loss
        setData.moneymanage = self.moneymanage
        setData.userName = self.userName

        setData.tobuy = 0
        setData.tosell = 0

        cerebro.broker.setcash(self.cash)
        cerebro.broker.setcommission(commission=0.001, margin=18400)

        cerebro.addstrategy(Strategy)
        data_path = self.useData
        print(data_path)
        print(self.startTime, type(self.startTime), type(str(self.startTime)))
        print(self.endTime, type(self.endTime), type(str(self.endTime)))
        data = bt.feeds.GenericCSVData(dataname=data_path,
                                       fromdate=datetime.strptime(
                                           str(self.startTime), '%Y-%m-%d'),
                                       todate=datetime.strptime(
                                           str(self.endTime), '%Y-%m-%d'),
                                       nullvalue=0.0,
                                       dtformat=('%Y-%m-%d'),
                                       tmformat=('%H:%M:%S'),
                                       date=1,
                                       time=1,
                                       high=3,
                                       low=4,
                                       open=2,
                                       close=5,
                                       volume=6,
                                       openinterest=-1)
        print(data)
        cerebro.adddata(data)
        # print("Start Portfolio {}".format(cerebro.broker.getvalue()))
        cerebro.run()
        memberdate = Member.objects.filter(member_id=self.userName)
        for i in memberdate:
            twd = int(i.member_twd) - int(setData.tobuy) + int(setData.tosell)
            usd = int(i.member_usd) - int(setData.tobuy) + int(setData.tosell)
            # usd = int(i.member_usd) + int(member_usd)
        print(self.cashtype)
        if self.cashtype == 0:
            Member.objects.filter(member_id=self.userName).update(
                member_twd=int(twd))
            print("原本的錢")
            print(self.cash)
            print("看下面")
            print(setData.tobuy)
            print(setData.tosell)
            print("最後的錢")
            print(twd)
        else:
            Member.objects.filter(member_id=self.userName).update(
                member_usd=int(usd))
            print("原本的錢")
            print(self.cash)
            print("看下面")
            print(setData.tobuy)
            print(setData.tosell)
            print("最後的錢")
            print(usd)

        # print("Final Portfolio {}".format(cerebro.broker.getvalue()))
        # cerebro.plot()


# if __name__ == '__main__':
#     #@
#     setData = SetData()
#     setData.maxQuan  = 10
#     setData.delta = 50000
#     setData.doData = "P002"
#     setData.buyMoney = setData.GetProductPrice()

#     cerebro = bt.Cerebro()
#     cerebro.broker.setcash(10000000)
#     cerebro.broker.setcommission(commission=0.001, margin=18400)
#     cerebro.addstrategy(Strategy)

#     # 載入資料集
#     data_path = Path(os.getcwd()) / \
#         'Data/MXF1-Minute-Trade(小台指分鐘-2016-1-1至2021--12-22).csv'
#     data = bt.feeds.GenericCSVData(dataname=data_path,
#                                    fromdate=datetime.datetime(2016, 1, 4),
#                                    todate=datetime.datetime(2017, 2, 18),
#                                    nullvalue=0.0,

#                                    dtformat=('%Y/%m/%d'),
#                                    tmformat=('%H:%M:%S'),
#                                    date=0,
#                                    time=1,
#                                    high=3,
#                                    low=4,
#                                    open=2,
#                                    close=5,
#                                    volume=6,
#                                    openinterest=-1)
#     cerebro.adddata(data)
#     print("Start Portfolio {}".format(cerebro.broker.getvalue()))
#     start_value = cerebro.broker.getvalue()
#     # 當執行 cerebro 這個方法時，cerebro 就會去迭代所有資料，並且計算我們策略回測出來的績效
#     # 加入績效分析
#     cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
#     cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
#     cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SR')
#     cerebro.addanalyzer(bt.analyzers.Returns, _name='RS')
#     cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')
#     cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
#     results = cerebro.run()
#     start = results[0]
#     end_value = cerebro.broker.getvalue()

#     # 看最後資產的總價值是多少
#     print("Final Portfolio {}".format(cerebro.broker.getvalue()))
#     print('收益:{:,.2f}'.format(end_value-start_value))
#     print('年利潤:', start.analyzers.AnnualReturn.get_analysis())
#     print('最大策略虧損:', start.analyzers.DW.get_analysis()["max"]["drawdown"])
#     print('夏普指數:', start.analyzers.SR.get_analysis()["sharperatio"])
#     print('總收益率:', start.analyzers.RS.get_analysis()["rtot"])
#     print('贏交易分析:', start.analyzers.TradeAnalyzer.get_analysis()['won'])
#     print('輸交易分析:', start.analyzers.TradeAnalyzer.get_analysis()['lost'])
#     # 注意:以下有用到 format(start.analyzers.TradeAnalyzer.get_analysis() 的都只有做多時才有值喔!!!
#     # 賺賠比 = 平均賺 / 平均賠
#     print('賺賠比:{:,.2f}'.format(start.analyzers.TradeAnalyzer.get_analysis()[
#           'won']['pnl']['average'] / (-1 * start.analyzers.TradeAnalyzer.get_analysis()['lost']['pnl']['average'])))
#     # 獲利因子 = 賺得和 / |賠的和|
#     print('總交易次數:', start.analyzers.TradeAnalyzer.get_analysis()
#           ['total']['total'])
#     print('盈利次數:', start.analyzers.TradeAnalyzer.get_analysis()
#           ['won']['total'])
#     print('虧損次數:', start.analyzers.TradeAnalyzer.get_analysis()
#           ['lost']['total'])
#     print('勝率: {:,.2f}'.format(start.analyzers.TradeAnalyzer.get_analysis()[
#           'won']['total'] / start.analyzers.TradeAnalyzer.get_analysis()['total']['total']))
#     # SNQ 1.6~1.9凑合用，2.0~2.4普通，2.5~2.9好，3.0~5.0杰出，5.1~6.0一流，7.0以上极好，SNQ=（平均获利/标准差）*年交易次数的平方根
#     print("SQN:{}".format(start.analyzers.SQN.get_analysis()["sqn"]))
#     # 在 cerebro 把所有回測結果 run 完後，就能使用內建的繪圖功能來製作圖表(損益圖，內還會有資產、買點賣點等損益的情況)
#     cerebro.plot()
