import alpaca_trade_api as tradeapi
from twitchio.ext import commands
import os

# Retrieve environment variables
API_KEY = os.getenv('ALPACA_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = os.getenv('ALPACA_API_BASE_URL')
TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')

# Create Alpaca API client
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

# Function to execute a buy order
def buy_stock(symbol, quantity):
    try:
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        return f"Bought {quantity} shares of {symbol}"
    except Exception as e:
        return f"Error occurred while buying {symbol}: {str(e)}"

# Function to execute a sell order
def sell_stock(symbol, quantity):
    try:
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        return f"Sold {quantity} shares of {symbol}"
    except Exception as e:
        return f"Error occurred while selling {symbol}: {str(e)}"

#TODO - add function to backtest strategies