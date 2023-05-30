import alpaca_trade_api as tradeapi
from config import ALPACA_SECRET_KEY
from config import ALPACA_KEY
from twitchio.ext import commands

# Alpaca API credentials
API_KEY = ALPACA_KEY
SECRET_KEY = ALPACA_SECRET_KEY
BASE_URL = 'https://paper-api.alpaca.markets'

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
