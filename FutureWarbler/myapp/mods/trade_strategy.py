from asyncio import futures
from myapp.models import History

#-----------------------------資金管理策略------------------------------------------
def FixedSizeStrategy(self,isBuy):
    if isBuy == True:
        price = self.doPrice
        # buy_qty
        # self.log("b1口")
        # print("買1口")
        # buy_mon
        # self.log("{}".format(price)) 
        # print(price)
        # buy_time
        # print(self.datas[0].datetime.date(0))
        self.order = self.buy(price=price)
        print(self.userName,self.stock)
        History.objects.create(member_id=self.userName,buy_qty=1,buy_mon=price,buy_time=self.datas[0].datetime.date(0),futures_id=self.stock)              

    else:
        # sell_qty
        # self.log("s{}口".format(abs(self.broker.getposition(self.data).size)))
        # print(abs(self.broker.getposition(self.data).size))
        # sell_mon
        # print(self.dataclose[0])
        # self.log("{}".format(self.dataclose[0])) 
        # sell_time
        self.order = self.sell()
        History.objects.create(member_id=self.userName,sell_qty=abs(self.broker.getposition(self.data).size),sell_mon=self.dataclose[0],sell_time=self.datas[0].datetime.date(0),futures_id=self.stock)              

def FixedAmountStrategy(self,isBuy):
    if isBuy == True:
        count = int(self.cerebro.broker.getvalue()/(self.doPrice*1.5))
        price = count*self.doPrice
        # buy_qty
        # self.log("{}口".format(count))
        # print(count)
        # buy_mon
        # self.log("{}".format(price)) 
        # print(price)
        # buy_time
        self.order = self.buy(price=price)
        History.objects.create(member_id=self.userName,buy_qty=count,buy_mon=price,buy_time=self.datas[0].datetime.date(0),futures_id=self.stock)              
    else:
        # sell_qty 
        # self.log("{}口".format(abs(self.broker.getposition(self.data).size)))
        # print(abs(self.broker.getposition(self.data).size))
        # sell_mon 
        # self.log("{}".format(self.dataclose[0])) 
        # print(self.dataclose[0])
        # sell_time
        self.order = self.sell()
        History.objects.create(member_id=self.userName,sell_qty=abs(self.broker.getposition(self.data).size),sell_mon=self.dataclose[0],sell_time=self.datas[0].datetime.date(0),futures_id=self.stock)              

def FixedRatioStrategy(self,isBuy):
    if isBuy == True:
        count = 0
        for i in self.buyMonlist:
            # 在 我的錢 < 帳戶權益需求的錢 的情況下
            if self.cerebro.broker.getvalue() < i:
                if count == 0:
                    price = self.buyMonlist[count+1]
                    break
                else:
                    price = self.buyMonlist[count-1]
                break
            # 在 我的錢 = 帳戶權益需求的錢 的情況下
            elif self.cerebro.broker.getvalue() == i:
                price = i
                break
            # 在 我的錢 > 帳戶權益需求的錢 的情況下
            else :
                if count == len(self.buyMonlist)-1:
                    price = i
                else:
                    count = count+1
        # buy_qty
        # self.log("{}口".format(count))
        # print(count)
        # buy_mon
        # self.log("{}".format(price)) 
        # print(price)
        # buy_time  
        self.order = self.buy(price=price)
        History.objects.create(member_id=self.userName,buy_qty=count,buy_mon=price,buy_time=self.datas[0].datetime.date(0),futures_id=self.stock)              

    else:
        # sell_qty 
        # self.log("{}口".format(abs(self.broker.getposition(self.data).size)))
        # print(abs(self.broker.getposition(self.data).size))
        # sell_mon 
        # self.log("{}".format(self.dataclose[0])) 
        # print(self.dataclose[0])
        # sell_time
        self.order = self.sell()
        History.objects.create(member_id=self.userName,sell_qty=abs(self.broker.getposition(self.data).size),sell_mon=self.dataclose[0],sell_time=self.datas[0].datetime.date(0),futures_id=self.stock)              


#-----------------------------停損停利策略------------------------------------------
#做多 固定點數停損停利 STOP LOSS SELL STOP PROFIT SELL
def long_point(self, loss, profit):
    if self.dataclose[0] < self.buyprice - loss:
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

    if self.dataclose[0] > self.buyprice + profit:
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#做空 固定點數停損停利 STOP LOSS SELL CREATE STOP PROFIT SELL CREATE
def short_point(self, loss, profit):
    if self.dataclose[0] > self.buyprice + loss:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

    if self.dataclose[0] < self.buyprice - profit:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#做多 固定比例停損停利 STOP LOSS SELL CREATE STOP PROFIT SELL CREATE
def long_percentage(self, loss, profit):
    if self.dataclose[0] - self.buyprice < 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >loss:
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

    if self.dataclose[0] - self.buyprice > 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >profit:
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#做空 固定比例停損停利 STOP LOSS SELL CREATE STOP PROFIT SELL CREATE
def short_percentage(self, loss, profit):
    if self.dataclose[0] - self.buyprice > 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >loss:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

    if self.dataclose[0] - self.buyprice < 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >profit:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)


#做多 移動停損 STOP LOSS SELL CREATE
def long_trailing(self, tmpHigh, loss):
    TrailingStop = tmpHigh - loss
    if self.datahigh > tmpHigh:
        tmpHigh = self.datahigh
        TrailingStop = tmpHigh - loss
        pass

    elif self.datahigh <= TrailingStop:
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)


#做空 移動停損 STOP LOSS SELL CREATE
def short_trailing(self, tmpLow, loss):
    TrailingStop = tmpLow + loss
    if self.datalow < tmpLow:
        tmpLow = self.datalow
        TrailingStop = tmpLow + loss
        pass

    elif self.datalow >= TrailingStop:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#------------------------------進出場策略-----------------------------------------
#OSC 做多進場 LONG IN CREATE
def long_in_osc(self, macdhist):
    if macdhist > 0 and macdhist[-1] > 0 and macdhist[-2]<0:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#OSC 做空進場 SHORT IN CREATE
def short_in_osc(self, macdhist):
    if macdhist < 0:
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)
        
#william 做多進場 LONG IN CREATE
def long_in_william(self,williams):
    if williams[0] > -80 and williams[-1] <= -20:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#william 做多出場 LONG OUT CREATE
def long_out_william(self, williams):
    if williams[-1]>= -20 and williams[0] <-20:
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#william 做空進場 SHORT IN CREATE
def short_in_william(self, williams):
    if williams[-1]>= -20 and williams[0] <-20:
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#william 做空出場 SHORT OUT CREATE
def short_out_william(self,williams):
    if williams[0] > -80 and williams[-1] <= -20:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#bias 做多進場 LONG IN CREATE
def long_in_bias(self, bias):
    if bias <= -0.1:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#bias 做多出場 LONG OUT CREATE
def long_out_bias(self, bias):
    if self.bias[-1] >= 0.1 and self.bias[0] < 0.1 :
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#bias 做空進場 SHORT IN CREATE
def short_in_bias(self, bias):
    if self.bias[-1] >= 0.1 and self.bias[0] < 0.1 :
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#bias 做空出場 SHORT OUT CREATE
def short_out_bias(self, bias):
    if bias <= -0.1:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# MA 做多進場 LONG IN CREATE
def long_in_ma(self, crossover_MA):
    if crossover_MA > 0:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# MA 做多出場 LONG OUT CREATE
def long_out_ma(self, crossover_MA):
    if crossover_MA < 0:
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# MA 做空進場 SHORT IN CREATE
def short_in_ma(self, crossover_MA):
    if crossover_MA < 0:
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# MA 做空出場 SHORT OUT CREATE
def short_out_ma(self, crossover_MA):
    if crossover_MA > 0:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# RSI 做多進場 LONG IN CREATE
def long_in_rsi(self, rsi):
    if rsi > 50:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# RSI 做多出場 LONG OUT CREATE
def long_out_rsi(self, rsi):
    if rsi < 30 or rsi > 80:
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# RSI 做空進場 SHORT IN CREATE
def short_in_rsi(self, rsi):
    if rsi < 20 or rsi > 70:
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# RSI 做空出場 SHORT OUT CREATE
def short_out_rsi(self, rsi):
    if rsi > 50:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# KD 做多進場 LONG IN CREATE
def long_in_kd(self, crossover_KD):
    if crossover_KD > 0:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# KD 做多出場 LONG OUT CREATE
def long_out_kd(self, crossover_KD):
    if crossover_KD < 0:
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# KD 做空進場 SHORT IN CREATE
def short_in_kd(self, crossover_KD):
    if crossover_KD < 0:
        # self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# KD 做空出場 SHORT OUT CREATE
def short_out_kd(self, crossover_KD):
    if crossover_KD > 0:
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)