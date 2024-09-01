from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from twitchio.ext import commands
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Retrieve environment variables
API_KEY = os.getenv('ALPACA_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = os.getenv('ALPACA_API_BASE_URL')

# Twitch environment variables
TWITCH_TOKEN = os.getenv('access_token')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')

# Log the loaded environment variables (excluding sensitive information)
logging.info(f"API_KEY: {API_KEY[:4]}****")
logging.info(f"SECRET_KEY: {SECRET_KEY[:4]}****")
logging.info(f"BASE_URL: {BASE_URL}")
logging.info(f"TWITCH_TOKEN: {TWITCH_TOKEN[:4]}****")
logging.info(f"TWITCH_CLIENT_ID: {TWITCH_CLIENT_ID}")

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

class TradingBot(commands.Bot):
    def __init__(self):
        super().__init__(
            client_id=TWITCH_CLIENT_ID,
            nick="ATLien_Ke",
            prefix="!",
            initial_channels=["atlien_ke"],
            token=TWITCH_TOKEN
        )
        self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

    async def event_ready(self):
        logging.info("Bot connected to Twitch chat.")
    
    async def event_message(self, message):
        if message is None or message.author is None:
            return
        
        if message.author.name.lower() == self.nick.lower():
            return await message.channel.send("Message well received")

        if message.content.startswith('!'):
            await self.handle_commands(message)
        else:
            user_name = message.author.name
            response = f"@{user_name}, this is a trading bot. Please use the !buy or !sell command to trade."
            await message.channel.send(response)
            logging.info("Sent response: %s", response)

    async def handle_commands(self, message):
        command = message.content.split()
        if command[0] == '!buy':
            await self.buy_stock(message, command[1], command[2])

    async def buy_stock(self, message, symbol, amount):
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=amount,
                side='buy',
                type='market',
                time_in_force='GTC'
            )
            response = f"Successfully placed order to buy {amount} shares of {symbol}."
        except tradeapi.rest.APIError as e:
            response = f"Error occurred while buying {symbol}: {e}"
            logging.error("Error occurred while buying %s: %s", symbol, e)
        
        await message.channel.send(response)
        logging.info("Sent response: %s", response)

    async def sell_stock(self, message, symbol, amount):
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=amount,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            response = f'Sold {amount} shares of {symbol}'
        except tradeapi.rest.APIError as e:
            response = f'Error occurred while selling {symbol}: {e}'
            logging.error("Error occurred while selling %s: %s", symbol, e)
        
        await message.channel.send(response)
        logging.info("Sent response: %s", response)

if __name__ == '__main__':
    bot = TradingBot()
    bot.run()