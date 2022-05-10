from re import A
import backtrader as bt
import os
from pathlib import Path
import datetime
from matplotlib.pyplot import margins
from pandas import Period
from sklearn.metrics import log_loss, pair_confusion_matrix

from myapp.mods import bt_strategy 


'''
longshort '0':做多 '1':做空
instrategy進場策略 '0':ma '1':osc '2':rsi '3':kd '4':bias '5':william 
outstrategy出場策略 '0':ma '1':rsi '2':kd '3':bias '4':william  
stopstrategy停損停利 '1':比率 '2':點數 '3':移動
profit停利數字
loss停損數字
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
        # osc
        ('p1', 12),
        ('p2', 26),
        ('p3', 9),
        # william
        ('wperiod', 14),
        # bias
        ('smaperiod', 10),
    )


    def __init__(self, longshort, instrategy, outstrategy, stopstrategy, losspoint, profitpoint, tmp):
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
        self.in_strategy = instrategy
        self.out_strategy = outstrategy
        self.stopstrategy = stopstrategy
        self.loss = losspoint
        self.profit = profitpoint
        self.tmp = tmp

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

        if self.order:
            return

        if self.long_short == 0:
            if not self.position:
                if self.in_strategy == 0:
                    bt_strategy.long_in_ma(
                        self=self, crossover_MA=self.crossover_MA)
                elif self.in_strategy == 1:
                    bt_strategy.long_in_osc(self=self, macdhist=self.macdhist)
                elif self.in_strategy == 2:
                    bt_strategy.long_in_rsi(self=self, rsi=self.rsi)
                elif self.in_strategy == 3:
                    bt_strategy.long_in_kd(
                        self=self, crossover_KD=self.crossover_KD)
                elif self.in_strategy == 4:
                    bt_strategy.long_in_bias(self=self, bias=self.bias)
                else:
                    bt_strategy.long_in_william(
                        self=self, williams=self.williams)
            else:
                if self.out_strategy == 0:
                    bt_strategy.long_out_ma(
                        self=self, crossover_MA=self.crossover_MA)
                elif self.out_strategy == 1:
                    bt_strategy.long_out_rsi(self=self, rsi=self.rsi)
                elif self.out_strategy == 2:
                    bt_strategy.long_out_kd(
                        self=self, crossover_KD=self.crossover_KD)
                elif self.out_strategy == 3:
                    bt_strategy.long_out_bias(self=self, bias=self.bias)
                else:
                    bt_strategy.long_out_william(
                        self=self, williams=self.williams)

                if self.stopstrategy == 1:
                    self.loss = self.loss / 100
                    self.profit = self.profit / 100
                    bt_strategy.long_percentage(
                        self=self, loss=self.loss, profit=self.profit)
                elif self.stopstrategy == 2:
                    bt_strategy.long_point(
                        self=self, loss=self.loss, profit=self.profit)
                else:
                    bt_strategy.long_trailing(
                        self=self, tmpHigh=self.tmp, loss=self.loss)
        else:
            if not self.position:
                if self.in_strategy == 0:
                    bt_strategy.short_in_ma(
                        self=self, crossover_MA=self.crossover_MA)
                elif self.in_strategy == 1:
                    bt_strategy.short_in_osc(self=self, macdhist=self.macdhist)
                elif self.in_strategy == 2:
                    bt_strategy.short_in_rsi(self=self, rsi=self.rsi)
                elif self.in_strategy == 3:
                    bt_strategy.short_in_kd(
                        self=self, crossover_KD=self.crossover_KD)
                elif self.in_strategy == 4:
                    bt_strategy.short_in_bias(self=self, bias=self.bias)
                else:
                    bt_strategy.short_in_william(
                        self=self, williams=self.williams)
            else:
                if self.out_strategy == 0:
                    bt_strategy.short_out_ma(
                        self=self, crossover_MA=self.crossover_MA)
                elif self.out_strategy == 1:
                    bt_strategy.short_out_rsi(self=self, rsi=self.rsi)
                elif self.out_strategy == 2:
                    bt_strategy.short_out_kd(
                        self=self, crossover_KD=self.crossover_KD)
                elif self.out_strategy == 3:
                    bt_strategy.short_out_bias(self=self, bias=self.bias)
                else:
                    bt_strategy.short_out_william(
                        self=self, williams=self.williams)

                if self.stopstrategy == 1:
                    self.loss = self.loss / 100
                    self.profit = self.profit / 100
                    bt_strategy.short_percentage(
                        self=self, loss=self.loss, profit=self.profit)
                elif self.stopstrategy == 2:
                    bt_strategy.short_point(
                        self=self, loss=self.loss, profit=self.profit)
                #else:
                #    bt_strategy.short_trailing(
                #        self=self, tmpLow=self.tmp, loss=self.loss)

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print("{} {}".format(dt.isoformat(), txt))



    