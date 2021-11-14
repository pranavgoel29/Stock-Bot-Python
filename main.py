import discord
import os
import requests
import json
import random
import yfinance as yf
from replit import db


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

def send_price(pricec):
    # request = message.content.split()[1]
  request = pricec
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    return(data['Close'].to_string(header=False))
  else:
    return("No data!?")


# Function for some predefined Stocks.

def get_stock():
  response = ""
  stocks = ['gme', 'amc', 'nok']
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
  response += "\nStock Data"
  return(string(response))


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


    if msg.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if msg.startswith('!stock'):
        stock_data = get_stock()
        await message.channel.send(stock_data)
 
    if msg.startswith('Greet') or msg.startswith('greet'):
        await message.channel.send('Hey! Hows it going?')


    if msg.startswith('!price'):
    # request = message.content.split()
    # if len(request) < 2 or request[0].lower() not in "!price":
    #   return False
    # else:
      pricec = msg.split()[1]
      price_custom = send_price(pricec)
      await message.channel.send(price_custom)

client.run(os.getenv('TOKEN'))
