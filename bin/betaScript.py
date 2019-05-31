# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:31:02 2019

@author: Patrick
"""

import API_KEY
import datetime
import pandas as pd  
from binance.client import Client
import talib as ta
import mpl_finance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from statsmodels.tsa.seasonal import seasonal_decompose

def getBTC(interval = Client.KLINE_INTERVAL_30MINUTE):
    client = Client(API_KEY.binance.public, API_KEY.binance.private)
    
    symbol = 'BTCUSDT'
    BTC = client.get_historical_klines(symbol = symbol, interval = interval, start_str = "1 year ago UTC")
    
    BTC = pd.DataFrame(BTC, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
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
    BTC["BBMid"].plot(color = "r")
    BTC["BBUp"].plot(color = "b")
    BTC["BBLow"].plot(color = "b")
    plt.fill_between(BTC.index, BTC["BBUp"], BTC["BBLow"], alpha = 0.5)
    
if __name__ == "__main__":
    BTC = getBTC(interval = Client.KLINE_INTERVAL_30MINUTE)
    BTC_long = getBTC(interval = Client.KLINE_INTERVAL_1DAY)
    
    BTC_long["SMA25"] = ta.SMA(BTC["Close"], timeperiod = 200)
    
    BTC["SMA5"] = ta.SMA(BTC["Close"].values, timeperiod = 5)
    BTC["SMA20"] = ta.SMA(BTC["Close"].values, timeperiod = 20)
    BTC["SMA50"] = ta.SMA(BTC["Close"].values, timeperiod = 50)
    BTC["SMA200"] = ta.SMA(BTC["Close"].values, timeperiod = 200)

 

    BTC["ATR"] = ta.ATR(BTC["High"].values, BTC["Low"].values, BTC["Close"].values, timeperiod = 20)
    BTC["BBUp"], BTC["BBMid"], BTC["BBLow"] = ta.BBANDS(BTC["Close"].values, timeperiod=20, nbdevup=2, nbdevdn=2, matype=ta.MA_Type.SMA)
    
    
    BTC["SMA200"].plot()
    BTC_long["SMA25"].plot()

    decomp = seasonal_decompose(BTC["Close"], freq = 48*30)
    decomp.plot()
    decomp = seasonal_decompose(BTC["Close"], freq = 48*30, model = "multiplicative")
    decomp.plot()
    
    candlePlot(BTC)
    # trend finding
    BTC["TEMA50"] = ta.TEMA(BTC["Close"].values, timeperiod = 100)
    BTC["TEMA200"] = ta.TEMA(BTC["Close"].values, timeperiod = 400)
    BTC["TEMA50"].plot()
    BTC["TEMA200"].plot()
    BTC["Close"].plot()
    bollingerPlot(BTC)
    
    BTC["SMA50"].plot()
    BTC["SMA200"].plot()
    BTC["Close"].plot()
    bollingerPlot(BTC)
    

    BTC["SMA200"].plot()
    BTC["Close"].plot()
    bollingerPlot(BTC)
    