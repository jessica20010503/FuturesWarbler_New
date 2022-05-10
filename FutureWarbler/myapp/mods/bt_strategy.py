#-----------------------------資金管理策略------------------------------------------
def FixedSizeStrategy(self,isBuy):
    if isBuy == True:
        price = self.doPrice
        self.log("BUY FIXEDSIZE CREATE,{}".format(price))
        self.order = self.buy(price=price)
    else:
        self.log("SELL FIXEDSIZE CREATE,{}".format(self.dataclose[0]))
        self.order = self.sell()

def FixedAmountStrategy(self,isBuy):
    if isBuy == True:
        count = int(self.cerebro.broker.getvalue()/(self.doPrice*1.5))
        price = count*self.doPrice
        self.log("BUY FIXEDAMOUNT CREATE,{}".format(price))
        self.order = self.buy(price=price)
    else:
        self.log("SELL FIXEDAMOUNT CREATE,{}".format(self.dataclose[0]))
        self.order = self.sell()

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
        self.log("BUY FIXEDRATIO CREATE,{}".format(price))
        self.order = self.buy(price=price)
    else:
        self.log("SELL FIXEDRATIO CREATE,{}".format(self.dataclose[0]))
        self.order = self.sell()

#-----------------------------停損停利策略------------------------------------------
#做多 固定點數停損停利
def long_point(self, loss, profit):
    if self.dataclose[0] < self.buyprice - loss:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

    if self.dataclose[0] > self.buyprice + profit:
        self.log('STOP PROFIT SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#做空 固定點數停損停利
def short_point(self, loss, profit):
    if self.dataclose[0] > self.buyprice + loss:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

    if self.dataclose[0] < self.buyprice - profit:
        self.log('STOP PROFIT SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#做多 固定比例停損停利
def long_percentage(self, loss, profit):
    if self.dataclose[0] - self.buyprice < 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >loss:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

    if self.dataclose[0] - self.buyprice > 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >profit:
        self.log('STOP PROFIT SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#做空 固定比例停損停利
def short_percentage(self, loss, profit):
    if self.dataclose[0] - self.buyprice > 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >loss:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

    if self.dataclose[0] - self.buyprice < 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >profit:
        self.log('STOP PROFIT SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#做多 移動停損
def long_trailing(self, tmpHigh, loss):
    TrailingStop = tmpHigh - loss
    if self.datahigh > tmpHigh:
        tmpHigh = self.datahigh
        TrailingStop = tmpHigh - loss
        pass

    elif self.datahigh <= TrailingStop:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#做空 移動停損 
def short_trailing(self, tmpLow, loss):
    TrailingStop = tmpLow + loss
    if self.datalow < tmpLow:
        tmpLow = self.datalow
        TrailingStop = tmpLow + loss
        pass

    elif self.datalow >= TrailingStop:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#------------------------------進出場策略-----------------------------------------
#OSC 做多進場
def long_in_osc(self, macdhist):
    if macdhist > 0 and macdhist[-1] > 0 and macdhist[-2]<0:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#OSC 做空進場
def short_in_osc(self, macdhist):
    if macdhist < 0:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)
        
#william 做多進場
def long_in_william(self,williams):
    if williams[0] > -80 and williams[-1] <= -20:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#william 做多出場
def long_out_william(self, williams):
    if williams[-1]>= -20 and williams[0] <-20:
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#william 做空進場
def short_in_william(self, williams):
    if williams[-1]>= -20 and williams[0] <-20:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#william 做空出場
def short_out_william(self,williams):
    if williams[0] > -80 and williams[-1] <= -20:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#bias 做多進場
def long_in_bias(self, bias):
    if bias <= -0.1:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#bias 做多出場
def long_out_bias(self, bias):
    if self.bias[-1] >= 0.1 and self.bias[0] < 0.1 :
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#bias 做空進場
def short_in_bias(self, bias):
    if self.bias[-1] >= 0.1 and self.bias[0] < 0.1 :
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

#bias 做空出場
def short_out_bias(self, bias):
    if bias <= -0.1:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# MA 做多進場
def long_in_ma(self, crossover_MA):
    if crossover_MA > 0:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# MA 做多出場
def long_out_ma(self, crossover_MA):
    if crossover_MA < 0:
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# MA 做空進場
def short_in_ma(self, crossover_MA):
    if crossover_MA < 0:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# MA 做空出場
def short_out_ma(self, crossover_MA):
    if crossover_MA > 0:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# RSI 做多進場
def long_in_rsi(self, rsi):
    if rsi > 50:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# RSI 做多出場
def long_out_rsi(self, rsi):
    if rsi < 30 or rsi > 80:
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# RSI 做空進場
def short_in_rsi(self, rsi):
    if rsi < 20 or rsi > 70:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# RSI 做空出場
def short_out_rsi(self, rsi):
    if rsi > 50:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# KD 做多進場
def long_in_kd(self, crossover_KD):
    if crossover_KD > 0:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# KD 做多出場
def long_out_kd(self, crossover_KD):
    if crossover_KD < 0:
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# KD 做空進場
def short_in_kd(self, crossover_KD):
    if crossover_KD < 0:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        isBuy = False
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)

# KD 做空出場
def short_out_kd(self, crossover_KD):
    if crossover_KD > 0:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        isBuy = True
        if self.moneymanage == 1:
            FixedSizeStrategy(self,isBuy)
        elif self.moneymanage == 2:
            FixedAmountStrategy(self,isBuy)
        else:
            FixedRatioStrategy(self,isBuy)