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

