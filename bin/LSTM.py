# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:37:52 2019

@author: Patrick
"""

import API_KEY
import datetime
import pandas as pd  
from binance.client import Client

client = Client(API_KEY.binance.public, API_KEY.binance.private)

symbol = 'BTCUSDT'
BTC = client.get_historical_klines(symbol = symbol, interval = Client.KLINE_INTERVAL_30MINUTE, start_str = "1 year ago UTC")

BTC = pd.DataFrame(BTC, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                                   'Close time', 'Quote asset volume', 'Number of trades',
                                   'Taker buy base asset volume', 'Taker buy quote asset volume',
                                   'Ignore'])

BTC["Open time"] = pd.to_datetime(BTC["Open time"], unit = "ms")
BTC.set_index('Open time', inplace = True)

BTC['Close'] = BTC['Close'].astype(float)
BTC['Close'].plot(figsize=(20,10), title = '1 year Bitcoin price')

data = BTC.iloc[:, 3:4].astype(float).values #Close prices

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
data = scaler.fit_transform(data)

training_set = data[:10000]
test_set = data[10000:]

steps_ahead = 1
X_train = training_set[0:len(training_set)-steps_ahead]
y_train = training_set[steps_ahead:len(training_set)] # because LSTM predict one step ahead

X_test = test_set[0:len(test_set)-steps_ahead]
y_test = test_set[steps_ahead:len(test_set)]

import numpy as np

X_train = np.reshape(X_train, (len(X_train), 1, X_train.shape[1]))
X_test = np.reshape(X_test, (len(X_test), 1, X_test.shape[1]))

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

model = Sequential()
model.add(LSTM(256, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2)) # dropout
model.add(LSTM(256))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer = 'adam')
model.fit(X_train, y_train, epochs=50, batch_size = 16, shuffle=False)

predicted_price = model.predict(X_test)
predicted_price = scaler.inverse_transform(predicted_price)
real_price = scaler.inverse_transform(y_test)

import matplotlib.pyplot as plt

plt.figure(figsize=(20,8))
plt.plot(predicted_price, color = "red", label = "Predicted Price of Bitcoin")
plt.plot(real_price, color = "blue", label = "Real Price of Bitcoin")
plt.title("Predicted vs. Real Price")
plt.xlabel("Time")
plt.ylabel("Price")
plt.show()

# DROPOUT?