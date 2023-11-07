from distutils import command
import os
from turtle import clear
import telebot
import yfinance as yf
import plotly.graph_objs as go
import plotly.io as pio
from tokenize import Token
from tracemalloc import stop
import numpy as np
import pandas as pd

API_KEY = '5021308347:AAFayy20PDMUSdxXxZ9YOx4qkHt7rCUNK1c'
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['Greet'])
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['wsb'])
def get_stocks(message):
  response = ""
  stocks = ['gme', 'amc', 'nok']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 2)
      format_date = row['Date'].strftime('%m/%d')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  response += "\nStock Data"
  print(response)
  bot.send_message(message.chat.id, response)

# def stock_request(message):
#   request = message.text.split()
#   if len(request) < 2 or request[0].lower() not in "price":
#     return False
#   else:
#     return True

@bot.message_handler(commands=['price'])
def send_price(message):
  request = message.text.split()[1]
  company_name = request.split('.')
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, company_name[0].capitalize())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")


@bot.message_handler(commands=['chart'])
def send_chart(message):
  req_company = message.text.split()
  main_company = req_company[1].lower()
  company_title = main_company.split('.')
  
  if not os.path.exists("images"):
      os.mkdir("images")

  #Interval required 1 minute
  data = yf.download(tickers=main_company, period='1d', interval='5m')

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
      title=company_title[0].capitalize(),
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
  pio.write_image(fig, "images/fig1.png")
  img = open('images/fig1.png', 'rb')
  bot.send_photo(message.chat.id, img)
  os.remove('images/fig1.png')

bot.polling()
# #Show