import yfinance as yf 
ticker_list = ['MSFT', 'AMZN']
for tkr in ticker_list:
	dat = yf.Ticker(tkr)
	tz = dat._fetch_ticker_tz(proxy=None, timeout=30)
	valid = yf.utils.is_valid_timezone(tz)
	print(f"{tkr}: tz='{tz}', valid={valid}")