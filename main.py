import discord
import os
import requests
import json
import random
import yfinance as yf
from replit import db
from keep_alive import keep_alive

#Solution for .env file import
from dotenv import load_dotenv

load_dotenv()       #The load_dotenv() function looks for any .env file present in the current directory. After finding it will load them for use in your project

#upto this

client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

# Function for custom stock

def send_price(price):
  request = price
  data = yf.download(tickers=request, period='10m', interval='2m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d   %I:%M  %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    return("Date    Time       Price($)\n" + data['Close'].to_string(header=False) + "\n \n stock data (amount in $)")
  else:
    return("No data!?")


# Function for some predefined Stocks.

def get_stock():
  response = ""
  stocks = ['msft', 'googl', 'fb', 'tsla', 'adbe']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    response += f"--------{stock}--------\n"
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
  response += "\nStock Data (amount in $)"
  return(response)


# Server login message function.

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

# Function for commands from message of Discord.

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!commands'):
      await message.channel.send('Include "!" before every command.\n\n1. inspire - To get inspirational quotes.\n\n2. stock - To get data about some predefined tech companies.\n\n3. price stock_name - To get data of custom stock provided by user. (Type stock name in place of "stock_name") \n')

    if msg.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if msg.startswith('!stock'):
        stock_data = get_stock()
        await message.channel.send(stock_data)
 
    if msg.startswith('Greet') or msg.startswith('greet'):
        await message.channel.send('Hey! Hows it going?')


    if msg.startswith('!price'):
      price = msg.split()[1]
      price_custom = send_price(price)
      await message.channel.send(price_custom)

keep_alive()
client.run(os.getenv('TOKEN'))
