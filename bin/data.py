!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:31:49 2019

@author: ptruong
"""

API_KEY = "M4LLJCZFCV10Y82G"

from alpha_vantage.cryptocurrencies import CryptoCurrencies
import matplotlib.pyplot as plt

cc = CryptoCurrencies(key=API_KEY, output_format='pandas')
data, meta_data = cc.get_digital_currency_daily(symbol='BTC', market = 'SEK')
data['1b. open (USD)'].plot()
plt.tight_layout()
plt.title('Intraday value for bitcoin (BTC)')
plt.grid()
plt.show()


from parser import *

cdd = cryptoDataDownload()
df_h = cdd.krakenH("Kraken_BTCUSD_1h.csv")
df_d = cdd.krakenD("Kraken_BTCUSD_d.csv")
