#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 14:09:30 2019

@author: ptruong
"""



import pandas as pd


class cryptoDataDownload(object):
    """
    Parses data from cryptodatadownload.com
    """ 
    def krakenH(self, fileName):
        fileName = fileName
        df = pd.read_csv(fileName, sep = ",", skiprows = 1)
        df["Date"] = pd.to_datetime(df["Date"], format = '%Y-%m-%d %I-%p')
        df = df.set_index("Date")
        return df
    def krakenD(self, fileName):
        fileName = fileName
        df = pd.read_csv(fileName, sep = ",", skiprows = 1)
        df["Date"] = pd.to_datetime(df["Date"], format = '%Y-%m-%d')
        df = df.set_index("Date")
        return df

class iexParse(object):
    """
    Parse IEX data from pandas-datareader.
    """
    def iexJSON2df(self, filename):
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
    
    def iexCSV2df(self, filename):
        """
        Takes output from getDailyDataIEX from getData.py and make it parseable for Backtrader adddata.
        """
        df = pd.read_csv(filename, sep = "\t", index_col = 0)
        dates = pd.to_datetime(df.index)
        df["Date"] = dates
        df = df.set_index("Date")
        return df