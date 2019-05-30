# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 22:45:53 2018

@author: Patrick
"""

"""
NOTE BT is using OPEN prices of day2 to do trade strategy because
https://community.backtrader.com/topic/15/convincing-strategy-to-buy-at-close-of-current-bar-in-backtest


"""
import backtrader as bt
import backtrader.feeds as btfeeds

import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import scipy as sp

#import API_KEY as KEY
from datetime import datetime

import strategy as strat
import analysis

def preprocess_pandasDatareader_quandl_df(df):
    """
    Rearrange pandas-datareader quandl source df to use
    adj. open prices instead of raw open prices.
    
    This adjustment makes the data same format as bt.feeds 
    original data format i.e. using adj. open of day 2.
    """
    df = df.reindex(index=df.index[::-1])
    df = df.drop(["Open", "High", "Low", "Close", "Volume", "ExDividend", "SplitRatio"], 1)
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    return df

def iexJSON2df(filename):
    #filename = "WTW_intraday_20181101-2019.json"
    df = pd.read_json(filename)
    
    #df_reform = pd.DataFrame(index = datetime.strptime(df.date.apply(str) + " " +df.minute.apply(str), '%Y%b%d %I:%M'))
    df_reform = pd.DataFrame(index = df.date.apply(str) + " " + df.minute.apply(str))
    df_reform.index = pd.to_datetime(df_reform.index)
    df_reform["Open"] = df["open"].values
    df_reform["Close"] = df["close"].values
    df_reform["Low"] = df["low"].values
    df_reform["High"] = df["high"].values
    df_reform["Volume"] = df["volume"].values
    df_reform = df_reform.dropna()
    return df_reform

def iexCSV2df(filename):
    """
    Takes output from getDailyDataIEX from getData.py and make it parseable for Backtrader adddata.
    """
    df = pd.read_csv(filename, sep = "\t", index_col = 0)
    dates = pd.to_datetime(df.index)
    df["Date"] = dates
    df = df.set_index("Date")
    return df

def Backtest(startCapital, strategy, data):
    """
    startCapital = starting capital
    strategy = a strategy from strategy.py
    
    """
    #Variable for our starting cash
    startcash = startCapital

    #Create an instance of cerebro
    cerebro = bt.Cerebro()
    
    #Add our strategy
    cerebro.addstrategy(strategy)
    
    #Add the data to Cerebro
    cerebro.adddata(data)
    
    # Set our desired cash start
    cerebro.broker.setcash(startcash)
    
    # Run over everything
    cerebro.run()
    
    #Get final portfolio Value
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash
    
    #Print out the final result
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))
    
    #Finally plot the end results
    cerebro.plot(style='candlestick')
    
if __name__ == "__main__":
    #API_KEY = KEY.quandlAPI_KEY()
    
    startcash = 10000
    
    #MyStrat = strat.GoldenCross(10)
    #MyStrat = strat.BuyAndHold(size = 1)
    #MyStrat = strat.RSI(size = 1, period = 21, rsi_low = 8, rsi_high = 80)
    MyStrat = strat.Bollingband(size = 10, period = 20, std = 2, debug = False)
    #MyStrat = strat.StochasticCrossOver(size = 5)
    #MyStrat = strat.Doji(size = 5)
    #MyStrat = strat.EveningStar(size = 10)
    #MyStrat = strat.GraveStoneDoji(size = 10)
    #MyStrat = strat.GraveStoneDoji_test(size = 10)

    
    #stock = "GS"
    #df = web.DataReader(stock, "quandl", "2013-08-05", "2018-08-05")
    
    # Rearrange data for bt.feeds readin of pandas-datareader format
    #df = preprocess_pandasDatareader_quandl_df(df)
    
    # Read in datafraem
    filename = "/home/ptruong/Projects/gamma6/data/WTW_intraday_20181101-2019.json"
    #filename = "ABMD_intraday_20181101-2019.json"
    #filename = "/home/ptruong/Projects/gamma6/data/JILL_intraday_20181101-2019.json"
    filename = "/home/ptruong/Projects/gamma6/data/WTW_daily_20150301-20190301.csv"
    filename = "/home/ptruong/Projects/gamma6/data/FPRX_daily_20150301-20190301.csv"

    #df = iexJSON2df(filename)
    df =  iexCSV2df(filename)
    df = data
    # Convert to bt-dataformat
    datap = bt.feeds.PandasData(dataname = df)
    #Backtest(startCapital = 10000, strategy = MyStrat, data = datap)

    #Create an instance of cerebro
    cerebro = bt.Cerebro()    

    #Add our strategy
    cerebro.addstrategy(MyStrat)

    #Add the data to Cerebro
    cerebro.adddata(datap)
    
    # Set our desired cash start
    cerebro.broker.setcash(startcash)
    
    # Add the analyzers we are interested in
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    # Run over everything
    strategies = cerebro.run()
    firstStrat = strategies[0]
        
    #Get final portfolio Value
    portvalue = cerebro.broker.getvalue()
    
    #Print out the final result
    print('Final Portfolio Value: ${}'.format(portvalue))
    
    #Finally plot the end results
    cerebro.plot(style='candlestick')
    
    # print the analyzers
    analysis.printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
    analysis.printSQN(firstStrat.analyzers.sqn.get_analysis())
    analysis.printSQNref()
