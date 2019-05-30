# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 22:03:44 2018

@author: Patrick
"""


import backtrader as bt

def BuyAndHold(size):
    size = size
    class MyStrategy(bt.Strategy):
        def __init__(self):
            pass
        def next(self):
            if not self.position:
                self.buy(size=size)
    return MyStrategy

def GoldenCross(size):
    size = size
    class MyStrategy(bt.Strategy):
        params = dict(period1=20,
                      period2=50,
                      period3 = 200)
        def __init__(self):
            self.sma_50 = bt.talib.SMA(self.data, timeperiod=self.params.period2)
            self.sma_200 = bt.talib.SMA(self.data, timeperiod=self.params.period3)
            #print(self.sma_50)
        def next(self):
            if not self.position:
                if self.sma_50 > self.sma_200:
                    self.buy(size=size)
            else:
                if self.sma_50 < self.sma_200:
                    self.sell(size=size)
    return MyStrategy

def RSI(size, period = 21, rsi_low = 30, rsi_high = 70):
    size = size
    period = period
    rsi_low = rsi_low
    rsi_high = rsi_high
    class firstStrategy(bt.Strategy):
    
        def __init__(self):
            self.rsi = bt.indicators.RSI_SMA(self.data.close, period=period)
    
        def next(self):
            if not self.position:
                if self.rsi < rsi_low:
                    self.buy(size=size)
            else:
                if self.rsi > rsi_high:
                    self.sell(size=size)
    return firstStrategy

def StochasticCrossOver(size):
    size = size
    class MyStrategy(bt.Strategy):
        params = dict(fastk_period=5,
                      slowk_period=3,
                      slowk_matype = 0,
                      slowd_period = 3,
                      slowd_matype = 0)
        def __init__(self):
            self.stoc = bt.indicators.Stochastic(self.data)
            self.slowd = self.stoc.lines.percD
            self.slowk = self.stoc.lines.percK
            self.delta = self.slowk - self.slowd
            self.above80 = None
            self.slowk_dropdown = None
            self.slowd_dropdown = None
        def next(self):
            if not self.position:
                if (self.slowk < 20) and (self.slowd < 20) and (self.delta == 0):
                   self.buy(size=size)
            else:          
                if (self.slowk > 80) and (self.slowd > 80):
                    self.above80 = True
                if self.above80 == True:
                    if self.slowk < 80:
                        self.slowk_dropdown = True
                    if self.slowd < 80:
                        self.slowd_dropdown = True
                if (self.slowk_dropdown == True) and (self.slowd_dropdown == True):
                    self.sell(size=size)
                    self.above80 = None
                    self.slowk_dropdown = None
                    self.slowd_dropdown = None
    return MyStrategy


def Bollingband(size, period = 20, std = 2, debug = False):
    class BOLLStrat(bt.Strategy):
     
        '''
        This is a simple mean reversion bollinger band strategy.
     
        Entry Critria:
            - Long:
                - Price closes below the lower band
                - Stop Order entry when price crosses back above the lower band
            - Short:
                - Price closes above the upper band
                - Stop order entry when price crosses back below the upper band
        Exit Critria
            - Long/Short: Price touching the median line
        '''
     
        params = (
            ("period", period),
            ("devfactor", std),
            ("size", size),
            ("debug", False)
            )
     
        def __init__(self):
            print(self.p)
            self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
            #self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
            #self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)
     
        def next(self):
     
            orders = self.broker.get_orders_open()
     
            # Cancel open orders so we can track the median line
            if orders:
                for order in orders:
                    self.broker.cancel(order)
     
            if not self.position:
     
                if self.data.close > self.boll.lines.top:
     
                    self.sell(exectype=bt.Order.Stop, price=self.boll.lines.top[0], size=self.p.size)
     
                if self.data.close < self.boll.lines.bot:
                    self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0], size=self.p.size)
     
     
            else:
     
     
                if self.position.size > 0:
                    self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)
     
                else:
                    self.buy(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)
     
            if self.p.debug:
                print('---------------------------- NEXT ----------------------------------')
                print("1: Data Name:                            {}".format(data._name))
                print("2: Bar Num:                              {}".format(len(data)))
                print("3: Current date:                         {}".format(data.datetime.datetime()))
                print('4: Open:                                 {}'.format(data.open[0]))
                print('5: High:                                 {}'.format(data.high[0]))
                print('6: Low:                                  {}'.format(data.low[0]))
                print('7: Close:                                {}'.format(data.close[0]))
                print('8: Volume:                               {}'.format(data.volume[0]))
                print('9: Position Size:                       {}'.format(self.position.size))
                print('--------------------------------------------------------------------')
     
        def notify_trade(self,trade):
            if trade.isclosed:
                dt = self.data.datetime.date()
     
                print('---------------------------- TRADE ---------------------------------')
                print("1: Data Name:                            {}".format(trade.data._name))
                print("2: Bar Num:                              {}".format(len(trade.data)))
                print("3: Current date:                         {}".format(dt))
                print('4: Status:                               Trade Complete')
                print('5: Ref:                                  {}'.format(trade.ref))
                print('6: PnL:                                  {}'.format(round(trade.pnl,2)))
                print('--------------------------------------------------------------------')
    return BOLLStrat

def GraveStoneDoji_test(size):
    size = size
    class MyStrategy(bt.Strategy):
        params = dict(period1=20)
        def __init__(self):
            self.doji = bt.talib.CDLDOJI(self.data.open, self.data.high, 
                             self.data.low, self.data.close)
            print(self.doji.__dict__)
        def next(self):
            if not self.position:
                if self.doji == 100:
                    self.buy(size=size)
            else:
                if self.doji == 100:
                    self.sell(size=size)
    return MyStrategy


######################
# Non-strats ########
#####################

def Doji(size):
    size = size
    class MyStrategy(bt.Strategy):
        params = dict(period1=20,
                      period2=50,
                      period3 = 200)
        def __init__(self):
            self.doji = bt.talib.CDLDOJI(self.data.open, self.data.high, 
                             self.data.low, self.data.close)
    return MyStrategy

def GraveStoneDoji(size):
    size = size
    class MyStrategy(bt.Strategy):
        params = dict(period1=20)
        def __init__(self):
            self.doji = bt.talib.CDLGRAVESTONEDOJI(self.data.open, self.data.high, 
                             self.data.low, self.data.close)
    return MyStrategy


def EveningStar(size):
    size = size
    class MyStrategy(bt.Strategy):
        params = dict(penetration=0.3)
        def __init__(self):
            self.doji = bt.talib.CDLEVENINGSTAR(self.data.open, self.data.high, 
                             self.data.low, self.data.close, penetration = self.params.penetration)
    """
            def next(self):
                if not self.position:
                    if self.sma_50 > self.sma_200:
                        self.buy(size=size)
                else:
                    if self.sma_50 < self.sma_200:
                        self.sell(size=size)
    """
    return MyStrategy


"""
def ATR(size, period):
    size = size
    class MyStrategy(bt.Strategy):
        params = dict(period = period)
        def __init__(self):
            self.ATR = bt.talib.ATR(self.data, period = params.period)
        def next(self):
            if not self.position:
                self.buy(size=size)
            else:
                self.sell(size=size)
    return MyStrategy


"""