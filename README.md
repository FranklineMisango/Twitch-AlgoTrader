# Twitch-AlgoTrader
This Python project is quite complex and requires users to have at least basic understanding of Algorithmic Trading software structures and Finance. The project allows me to execute Novice Level Trades After considering recommendations from customized Algorithms modelled into web apps. I am a certified Financial Modelling Valuation Analyst (FMVA) from The Corporate Finance Institute & Intermediate Software Engineer that qualifies me to work on this project

## Project Updates and Goals
* Generate a live graph and allow users to trade with realtime observation of portfolio value and real-time cash
* Give Lumibots autonomy to keep trading on low stream days

## Software Development
#### Software Development Cycle Architecture 
![](images/Architecture_b.png)

#### Application Programming Interface (APIs)
* Twitch APIs - These APIs are creating the Intertwined Twitch bot that allows my followers to Trade
* Alpaca Markets APIs -  These APIs allowed me to link my Application with my Paper Trading Account.   
#### Twitch Trading Bot
* This is the Twitch chat
![](images/twitch.png)
* This is the response from terminal
![](images/terminal.png)
#### Live Trade in Action Demo
![](images/construction.jpg)

## Installation - Twitch Testing 
* You need to create your own Twitch, and Alpaca Trading API
* Clone this repo to your local Machine
* Run `pip install requirements.txt`
* Create a config.py and paste in that your `ALPACA API credentials` and `Twitch credentials` all specified in the twitch.py
* To start trading, run `python twitch.py` and observe `connected to bot` successfully
* Login to your own twitch account and in your chat, try `!buy STOCK_SYMBOL Number` replacing Stock symbol and the number
* To trade for my behalf lol, Follow me on Twitch `ATLien_ke` and join my message list when the chat & live stream opens, you can be allowed in

## Installation - Inhouse Testing 
* create your own config file and append your own APIs 
* Refer to my repo, Lumibots for automation 