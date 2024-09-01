from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from twitchio.ext import commands
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
API_KEY = os.getenv('ALPACA_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = os.getenv('ALPACA_API_BASE_URL')
TWITCH_TOKEN = os.getenv('access_token')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

class TradingBot(commands.Bot):
    def __init__(self):
        super().__init__(
            client_id= TWITCH_CLIENT_ID,
            nick="ATLien_Ke",
            prefix="!",
            initial_channels=["atlien_ke"],
            token= TWITCH_TOKEN
        )

    async def event_ready(self):
        print(f"Bot connected to Twitch chat.")
    
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
            print("Sent response:", response)

    async def handle_commands(self, message):
        print("Handling command:", message.content)
        ctx = await self.get_context(message)
        await self.invoke(ctx)
    
    @commands.command(name='buy')
    async def buy_command(self, ctx):
        params = ctx.message.content.split(' ')[1:]
        if len(params) != 2:
            await ctx.send("Invalid command. Usage: !buy [symbol] [quantity]")
            return

        symbol, quantity = params
        response = self.buy_stock(symbol, int(quantity))
        await ctx.send(response)
        print("Sent response:", response)

    @commands.command(name='sell')
    async def sell_command(self, ctx):
        params = ctx.message.content.split(' ')[1:]
        if len(params) != 2:
            await ctx.send("Invalid command. Usage: !sell [symbol] [quantity]")
            return

        symbol, quantity = params
        response = self.sell_stock(symbol, int(quantity))
        await ctx.send(response)
        print("Sent response:", response)

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

if __name__ == '__main__':
    bot = TradingBot()
    bot.run()