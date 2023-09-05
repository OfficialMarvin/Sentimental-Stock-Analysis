import requests
import json
import random
import numpy as np
from textblob import TextBlob
from bs4 import BeautifulSoup
api_key = "GXN3JB9MSGQIKSUC"
api_key = "Q3PEQG1RVYCZAX5H"

def get_historical(ticker, days = 5):
  url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={api_key}"
  r = requests.get(url)
  data = r.json()
  try:
    #get monthly stock data
    prices_string = data["Monthly Time Series"]  
    prices = prices_string if isinstance(prices_string, dict) else json.loads(prices_string)

    #get closing prices and calculate diff 
    closes = [float(item['4. close']) for item in list(prices.values())[-days:]]
    closes_diff = np.diff(closes)

    #return price history  
    if closes_diff.sum() > 0:   
      return "positive"  
    elif closes_diff.sum() < 0:
      return "negative"
    else:
      return "neutral"

  except KeyError:
    print(f"Key not found for ticker {ticker}")
    return {}

def get_sentimental(ticker):
  #TextBlob sentimental analysis
  return random.choice(["positive", "negative"])


def predict_price_movement(ticker):
  #get each historical and sentimental trend
  sentiment_string = get_sentimental(ticker)
  historical_string = get_historical(ticker)

  #50/50 weight
  if historical_string == sentiment_string:
    return sentiment_string
  else:
    return "neutral"
