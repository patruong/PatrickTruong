# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:31:02 2019

@author: Patrick
"""

import API_KEY
import parseModule as pm

import datetime
import pandas as pd  
import numpy as np
from sklearn.linear_model import LinearRegression
from binance.client import Client
import talib as ta
import mpl_finance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose



def getBTC(interval = Client.KLINE_INTERVAL_30MINUTE, start = None, end = None):
    client = Client(API_KEY.binance.public, API_KEY.binance.private)
    binance = pm.binance()
    symbol = 'BTCUSDT'
    #symbol = "NEOBTC"
    if (start == None) and (end == None):
        #BTC = client.get_historical_klines(symbol = symbol, interval = interval, start_str = "1 year ago UTC")
        klines = binance.get_historical_klines(symbol, interval, "1 Jan, 2017")
    elif end == None:
        klines = binance.get_historical_klines(symbol, interval, start_str = start)
    else:
        #BTC = client.get_historical_klines(symbol = symbol, interval = interval, start_str = start, end_str = end)
        klines = binance.get_historical_klines(symbol, interval, start_str = start, end_str = end)

    BTC = pd.DataFrame(klines, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                                       'Close time', 'Quote asset volume', 'Number of trades',
                                       'Taker buy base asset volume', 'Taker buy quote asset volume',
                                       'Ignore'])
    
    BTC["Open time"] = pd.to_datetime(BTC["Open time"], unit = "ms")
    BTC.set_index('Open time', inplace = True)
    BTC = BTC.apply(pd.to_numeric)
    return BTC


def candlePlot(BTC):
    fig,ax = plt.subplots()
    ohcl_form = pd.DataFrame(BTC.index).apply(mdates.date2num)
    ohcl_form["Open"] = BTC["Open"].values
    ohcl_form["High"] = BTC["High"].values
    ohcl_form["Low"] = BTC["Low"].values
    ohcl_form["Close"] = BTC["Close"].values
    quotes = [tuple(x) for x in ohcl_form.values]
    mpf.candlestick_ohlc(ax, quotes)

def bollingerPlot(BTC):
    BTC["Close"].plot(color = "k")
    BTC["BBMid"].plot(color = "b")
    BTC["BBUp"].plot(color = "b", alpha = 0.6)
    BTC["BBLow"].plot(color = "b", alpha = 0.6)
    plt.fill_between(BTC.index, BTC["BBUp"], BTC["BBLow"], alpha = 0.5)


def interpolateLine(df, startDate, endDate):
    startVal = df[startDate]
    endVal = df[endDate]
    nVals = len(df[startDate:endDate])
    line = np.linspace(startVal, endVal, nVals)    
    line = pd.DataFrame(line, index = df[startDate:endDate].index, columns = ["line"])
    return line

def linReg(df, startDate, endDate, normalize = True):
    y = BTC["RSI14"][startDate:endDate].values
    x = np.array(range(len(BTC["RSI14"][startDate:endDate]))).reshape(-1,1)
    model = LinearRegression()
    model = model.fit(x, y)
    r_sq = model.score(x, y)
    print("coefficient of determination:", r_sq)
    print("intercept: ", model.intercept_)    
    print("slope: ", model.coef_)
    line =  model.intercept_ + np.array(range(len(BTC["RSI14"][startDate:endDate])))*model.coef_
    return line, (r_sq, model.intercept_, model.coef_)

def standardize(df):
   # return df.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
   return (df - df.mean())/(df.max() - df.min())

if __name__ == "__main__":
    BTC = getBTC(interval = Client.KLINE_INTERVAL_30MINUTE)
    BTC = getBTC(interval = Client.KLINE_INTERVAL_1DAY, start = "1 Jan, 2017")
    BTC_long = getBTC(interval = Client.KLINE_INTERVAL_1DAY)
    
    BTC_long["SMA25"] = ta.SMA(BTC["Close"], timeperiod = 200)
    
    BTC["SMA5"] = ta.SMA(BTC["Close"].values, timeperiod = 5)
    BTC["SMA20"] = ta.SMA(BTC["Close"].values, timeperiod = 20)
    BTC["SMA50"] = ta.SMA(BTC["Close"].values, timeperiod = 50)
    BTC["SMA200"] = ta.SMA(BTC["Close"].values, timeperiod = 200)

    BTC["EMA20"] = ta.EMA(BTC["Close"].values, timeperiod = 20)
    BTC["EMA55"] = ta.EMA(BTC["Close"].values, timeperiod = 55)
    BTC["EMA50"] = ta.EMA(BTC["Close"].values, timeperiod = 50)
    BTC["EMA200"] = ta.EMA(BTC["Close"].values, timeperiod = 200)
    
    BTC["ATR"] = ta.ATR(BTC["High"].values, BTC["Low"].values, BTC["Close"].values, timeperiod = 20)
    BTC["BBUp"], BTC["BBMid"], BTC["BBLow"] = ta.BBANDS(BTC["Close"].values, timeperiod=20, nbdevup=2, nbdevdn=2, matype=ta.MA_Type.SMA)
    
    
    BTC["SMA200"].plot()
    BTC_long["SMA25"].plot()

    decomp = seasonal_decompose(BTC["Close"], freq = 48*30)
    decomp.plot()
    decomp = seasonal_decompose(BTC["Close"], freq = 48*30, model = "multiplicative")
    decomp.plot()
    
    candlePlot(BTC)
    # trend finding - should be found in higher time frame to reduce noise!
    BTC["TEMA20"] = ta.TEMA(BTC["Close"].values, timeperiod = 20)
    BTC["TEMA55"] = ta.TEMA(BTC["Close"].values, timeperiod = 55)
    BTC["TEMA20"].plot(color = "g")
    BTC["TEMA55"].plot(color = "r")
    BTC["Close"].plot()
    bollingerPlot(BTC)
    
    BTC["SMA50"].plot()
    BTC["SMA200"].plot()
    BTC["Close"].plot()
    bollingerPlot(BTC)
    

    BTC["SMA200"].plot()
    BTC["Close"].plot()
    bollingerPlot(BTC)
    
    BTC["EMA20"].plot()
    BTC["EMA55"].plot()
    BTC["Close"].plot()
    bollingerPlot(BTC)
    
    #############################
    # TREND MA50 > MA200 daily ##
    #############################
    
    BTC["SMA50"].plot()
    BTC["SMA200"].plot()
    BTC["Close"].plot()
    bollingerPlot(BTC)
    
    BTC["longTrend"] = BTC["SMA50"]>BTC["SMA200"]

    BTC["EMA50"].plot()
    BTC["EMA200"].plot()
    BTC["Close"].plot()
    bollingerPlot(BTC)
    
    BTC["longTrend"] = BTC["SMA50"]>BTC["SMA200"]
    
    
    ####################
    # Taking position ##
    ####################
    
    # RSI
    BTC["RSI14"] = ta.RSI(BTC["Close"].values, timeperiod = 14)
    BTC["RSI21"] = ta.RSI(BTC["Close"].values, timeperiod = 21)
    BTC["RSI14"].plot()
    
    # trend support functions
    BTC["RSI14"]["2018-11-24":].plot()
    
    startDate = "2018-11-24"
    startDate = "2019-01-01"
    endDate = "2019-02-01"
 
    BTC["RSI14"][startDate:endDate].plot()
    
    line, stats = linReg(BTC["RSI14"], startDate, endDate)
    tmp_df = pd.DataFrame(BTC["RSI14"][startDate:endDate])
    #tmp_df["lines"] = line.values
    tmp_df["lines"] = line
    tmp_df.plot()


    #################################
    # Price trend confirmation OBV ##
    #################################
    
    BTC["OBV"] = ta.OBV(BTC["Close"], BTC["Volume"])
    stdClose = standardize(BTC["Close"][startDate:endDate])
    