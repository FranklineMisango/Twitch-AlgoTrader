import alpaca_trade_api as tradeapi
import requests
from twitchio.ext import commands
from config import APCA_API_BASE_URL
from config import CLIENT_ID
from config import ALPACA_KEY
from config import ALPACA_SECRET_KEY
from config import APCA_API_BASE_URL
import logging

# Import basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Alpaca API credentials
API_KEY = ALPACA_KEY
SECRET_KEY = ALPACA_SECRET_KEY
BASE_URL = APCA_API_BASE_URL

# Twitch bot credentials
BOT_USERNAME = "ATLien_Ke"
OAUTH_TOKEN = "zofcsbz4ogu2om0hmiwuitq7l3xq5f"
CLIENT_ID = "0vg1kmlbt52sp3szxv15zzlel3k1kz"
CHANNEL = "atlien_ke"

# Create Alpaca API client
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

# Create Twitch bot instance
class TwitchBot(commands.Bot):
    def __init__(self, username, irc_token, client_id, channel):
        super().__init__(
            irc_token=irc_token,
            client_id=client_id,
            nick=username,
            initial_channels=[channel]
        )
        self.channel = channel

        # Get the channel id, we will need this for Helix API calls
        url = f'https://api.twitch.tv/helix/users?login={username}'
        headers = {
            'Client-ID': client_id,
            'Authorization': f'Bearer {irc_token}',
            'Accept': 'application/vnd.twitchtv.v5+json'
        }
        r = requests.get(url, headers=headers).json()
        print(r)
        self.channel_id = r['data'][0]['id']

    async def event_ready(self):
        logging.info(f'Connected to Twitch chat: #{self.channel}')

    async def event_message(self, message):
        if message.author.name.lower() == BOT_USERNAME.lower():
            return  # Ignore messages sent by the bot itself

        if message.content.startswith('!buy') or message.content.startswith('!sell'):
            command, *params = message.content.split(' ')
            response = self.execute_alpaca_command(command[1:], *params)
            await message.channel.send_message(response)
        elif message.content.lower() == 'hello':
            response = f'Hello, {message.author.name}!'
            await message.channel.send_message(response)
        else:
            await message.channel.send_message(f'Unrecognized command: {message.content}')

    def execute_alpaca_command(self, command, *params):
        if command == 'buy' and len(params) == 2:
            symbol, quantity = params
            return self.buy_stock(symbol, int(quantity))
        elif command == 'sell' and len(params) == 2:
            symbol, quantity = params
            return self.sell_stock(symbol, int(quantity))
        else:
            return f'Invalid command: {command}'

    def buy_stock(self, symbol, quantity):
        try:
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            return f'Bought {quantity} shares of {symbol}'
        except Exception as e:
            return f'Error occurred while buying {symbol}: {str(e)}'

    def sell_stock(self, symbol, quantity):
        try:
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            return f'Sold {quantity} shares of {symbol}'
        except Exception as e:
            return f'Error occurred while selling {symbol}: {str(e)}'

# Start the Twitch bot
def start_twitch_bot():
    bot = TwitchBot(BOT_USERNAME, OAUTH_TOKEN, CLIENT_ID, CHANNEL)
    bot.run()

# Start the Twitch bot and connect to the Alpaca API
if __name__ == '__main__':
    start_twitch_bot()