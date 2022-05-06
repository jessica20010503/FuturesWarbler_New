#-----------------------------停損停利策略------------------------------------------
#做多 固定點數停損停利
def long_point(self, loss, profit):
    if self.dataclose[0] < self.buyprice - loss:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.sell()
    if self.dataclose[0] > self.buyprice + profit:
        self.log('STOP PROFIT SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.sell()

#做空 固定點數停損停利
def short_point(self, loss, profit):
    if self.dataclose[0] > self.buyprice + loss:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()
    if self.dataclose[0] < self.buyprice - profit:
        self.log('STOP PROFIT SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

#做多 固定比例停損停利
def long_percentage(self, loss, profit):
    if self.dataclose[0] - self.buyprice < 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >loss:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.sell()
    if self.dataclose[0] - self.buyprice > 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >profit:
        self.log('STOP PROFIT SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.sell()

#做空 固定比例停損停利
def short_percentage(self, loss, profit):
    if self.dataclose[0] - self.buyprice > 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >loss:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()
    if self.dataclose[0] - self.buyprice < 0 and (self.dataclose[0]-self.buyprice)/self.buyprice >profit:
        self.log('STOP PROFIT SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

#做多 移動停損
def long_trailing(self, tmpHigh, loss):
    TrailingStop = tmpHigh - loss
    if self.datahigh > tmpHigh:
        tmpHigh = self.datahigh
        TrailingStop = tmpHigh - loss
    elif self.datahigh <= TrailingStop:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.sell()

#做空 移動停損 
def short_trailing(self, tmpLow, loss):
    TrailingStop = tmpLow + loss
    if self.datalow < tmpLow:
        tmpLow = self.datalow
        TrailingStop = tmpLow + loss
    elif self.datalow >= TrailingStop:
        self.log('STOP LOSS SELL CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()


#------------------------------進出場策略-----------------------------------------
#OSC 做多進場
def long_in_osc(self, macdhist):
    if macdhist > 0 and macdhist[-1] > 0 and macdhist[-2]<0:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

#OSC 做空進場
def short_in_osc(self, macdhist):
    if macdhist < 0:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()

#william 做多進場
def long_in_william(self,williams):
    if williams[0] > -80 and williams[-1] <= -20:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()
#william 做多出場
def long_out_william(self, williams):
    if williams[-1]>= -20 and williams[0] <-20:
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()
#william 做空進場
def short_in_william(self, williams):
    if williams[-1]>= -20 and williams[0] <-20:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()
#william 做空出場
def short_out_william(self,williams):
    if williams[0] > -80 and williams[-1] <= -20:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()
#bias 做多進場
def long_in_bias(self, bias):
    if bias <= -0.1:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()
#bias 做多出場
def long_out_bias(self, bias):
    if self.bias[-1] >= 0.1 and self.bias[0] < 0.1 :
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()
#bias 做空進場
def short_in_bias(self, bias):
    if self.bias[-1] >= 0.1 and self.bias[0] < 0.1 :
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()
#bias 做空出場
def short_out_bias(self, bias):
    if bias <= -0.1:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

# MA 做多進場
def long_in_ma(self, crossover_MA):
    if crossover_MA > 0:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

# MA 做多出場
def long_out_ma(self, crossover_MA):
    if crossover_MA < 0:
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()

# MA 做空進場
def short_in_ma(self, crossover_MA):
    if crossover_MA < 0:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()

# MA 做空出場
def short_out_ma(self, crossover_MA):
    if crossover_MA > 0:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

# RSI 做多進場
def long_in_rsi(self, rsi):
    if rsi > 50:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

# RSI 做多出場
def long_out_rsi(self, rsi):
    if rsi < 30 or rsi > 80:
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()

# RSI 做空進場
def short_in_rsi(self, rsi):
    if rsi < 20 or rsi > 70:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.order = self.sell()

# RSI 做空出場
def short_out_rsi(self, rsi):
    if rsi > 50:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

# KD 做多進場
def long_in_kd(self, crossover_KD):
    if crossover_KD > 0:
        self.log('LONG IN CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()

# KD 做多出場
def long_out_kd(self, crossover_KD):
    if crossover_KD < 0:
        self.log('LONG OUT CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()

# KD 做空進場
def short_in_kd(self, crossover_KD):
    if crossover_KD < 0:
        self.log('SHORT IN CREATE,{}'.format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()

# KD 做空出場
def short_out_kd(self, crossover_KD):
    if crossover_KD > 0:
        self.log('SHORT OUT CREATE,{}'.format(self.dataclose[0]))
        self.order = self.buy()
