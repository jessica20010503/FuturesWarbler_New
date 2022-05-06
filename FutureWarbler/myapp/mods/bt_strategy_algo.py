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


#------------------------------演算法進場策略-----------------------------------------
#演算法 做多進場
def long_in_algo(self):
    if self.datapredict[0] == 1:
            self.log("LONG IN CREATE, {}".format(self.dataclose[0]))
            self.order = self.buy()
#演算法 做空進場
def short_in_algo(self):
    if self.datapredict[0] == 1:
        self.log("SHORT IN CREATE. {}".format(self.dataclose[0]))
        self.log('Pos size %s' % self.position.size)
        self.order = self.sell()

