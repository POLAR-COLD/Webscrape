import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas_market_calendars as mcal

stock_symbol = input('Enter the stock symbol: ').upper()

def search_str(stock_symbol):
  with open('all_tickers.txt', 'r') as file:
      content = file.read()
      return stock_symbol in content

def market_is_open(date):
  result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
  return result.empty == False

def fetch_price(stock_symbol):
  url = f'https://finance.yahoo.com/quote/{stock_symbol}'

  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110    Safari/537.3'
  }

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')

  price = soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)').get_text()
  return price

is_open = market_is_open(datetime.now().strftime("%Y-%m-%d"))

if __name__ == '__main__':
  while True:
      current_price = fetch_price(stock_symbol)
      if search_str(stock_symbol) == False:
        if is_open == True:
          print(f'Current price of {stock_symbol}: current_price')
          time.sleep(10)
        else:
          print(f'Closing price of {stock_symbol}: {current_price}')
          print(f'The market is closed for {stock_symbol}.')
          break
      else:
        print(f'The ticker {stock_symbol} is not in the list.')
        break
