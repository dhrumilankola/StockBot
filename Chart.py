import os
from tokenize import Token
from tracemalloc import stop
import numpy as np
import pandas as pd
import telebot
import yfinance as yf



data = yf.download(tickers='dlf.ns', period='2d', interval='1d')
print(data)


if not os.path.exists("images"):
    os.mkdir("images")

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
import plotly.io as pio

#Interval required 1 minute
data = yf.download(tickers='reliance.ns', period='1d', interval='5m')

#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title='Reliance Chart',
    yaxis_title='Stock Price (INR)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
        dict(count=15, label="15m", step="minute", stepmode="backward"),
        dict(count=45, label="45m", step="minute", stepmode="backward"),
        dict(count=1, label="HTD", step="hour", stepmode="todate"),
        dict(count=3, label="3h", step="hour", stepmode="backward"),
        dict(step="all")    
        ])
        )
)

# @bot.message_handler(commands=['chart'])
def hello(message):
    pio.write_image(fig, "images/fig1.png")
    img = open('images/fig1.png', 'rb')
    # bot.send_photo(message.chat.id, img)

# bot.polling()
#Show
fig.show()