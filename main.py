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

sad_words = ["sad", "depressed", "unhappy", "miserable", "depressing"]

starter_encouragements = ["Cheerup!", "I will be ok.", "Stay strong."]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)
 
client.run(os.getenv('TOKEN'))



# Stock part

# API_KEY = os.getenv('TOKEN')
# bot = client.run(API_KEY)

if message.content('Greet'):
    def greet(message):
        message.channel.send("Hey! Hows it going?")

# @bot.message_handler(commands=['hello'])
# def hello(message):
#   bot.send_message(message.chat.id, "Hello!")

# @bot.message_handler(commands=['wsb'])
# def get_stocks(message):
#   response = ""
#   stocks = ['gme', 'amc', 'nok']
#   stock_data = []
#   for stock in stocks:
#     data = yf.download(tickers=stock, period='2d', interval='1d')
#     data = data.reset_index()
#     response += f"-----{stock}-----\n"
#     stock_data.append([stock])
#     columns = ['stock']
#     for index, row in data.iterrows():
#       stock_position = len(stock_data) - 1
#       price = round(row['Close'], 2)
#       format_date = row['Date'].strftime('%m/%d')
#       response += f"{format_date}: {price}\n"
#       stock_data[stock_position].append(price)
#       columns.append(format_date)
#     print()

#   response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
#   for row in stock_data:
#     response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
#   response += "\nStock Data"
#   print(response)
#   bot.send_message(message.chat.id, response)

# def stock_request(message):
#   request = message.text.split()
#   if len(request) < 2 or request[0].lower() not in "price":
#     return False
#   else:
#     return True

# @bot.message_handler(func=stock_request)
# def send_price(message):
#   request = message.text.split()[1]
#   data = yf.download(tickers=request, period='5m', interval='1m')
#   if data.size > 0:
#     data = data.reset_index()
#     data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
#     data.set_index('format_date', inplace=True)
#     print(data.to_string())
#     bot.send_message(message.chat.id, data['Close'].to_string(header=False))
#   else:
#     bot.send_message(message.chat.id, "No data!?")

# bot.polling()