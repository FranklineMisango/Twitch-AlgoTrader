import streamlit as st
import requests
import pandas as pd
import math
from statistics import mean
from scipy import stats 
from secrets_1 import IEX_CLOUD_API_TOKEN

def main():
    st.title("Level II : Quantitative Momentum Strategizer")
    message  = "This app helps in Strategizing which stocks to invest based on Highest price momentum, It builds so from Level I Equal Weight Optimizer : stock.py. Recommended for optimal selections of better stocks from voluminous stock input of particular echelon (i.e Technology Stocks)"
    st.success(message)
    st.warning("This project is intended for users with a basic understanding of Algorithmic Trading")
    st.image('/home/misango/code/Xpay_AlgoTrader/images/quantitative.jpeg')
    st.markdown("**Enter stock tickers and select a benchmark:**")

    if 'tickers' not in st.session_state:
        st.session_state.tickers = []

    if 'benchmark' not in st.session_state:
        st.session_state.benchmarks = []
    
    # Create a form for the ticker input
    with st.form(key='ticker_form'):
        col1, col2 = st.columns([2, 1])
        with col1:
            ticker_input = st.text_input("Enter a stock ticker:", key='ticker_input')
        with col2:
            add_ticker_button = st.form_submit_button(label="Add +")
            remove_ticker_button = st.form_submit_button(label="Remove -")

        # Check if the ticker is already in the list
        is_duplicate = ticker_input in st.session_state.tickers

        # Add the entered ticker to the list when the user clicks the "+" button
        if add_ticker_button and not is_duplicate:
            st.session_state.tickers.append(ticker_input)

        # Remove the last ticker from the list when the "-" button is clicked
        if remove_ticker_button:
            if st.session_state.tickers:
                st.session_state.tickers.pop()

    st.write(st.session_state.tickers)

    # Create a form for selecting the benchmark
    with st.form(key='benchmark_form'):
        col1, col2 = st.columns([2, 1])
        with col1:
            benchmark = st.selectbox("Select One benchmark (More will be added soon):", ["S&P 500", "DJIA", "HSI", "UKX", "SX5E", "SHCOMP", "N225", "STI", "NSEASI", "DFMGI", "ADXGI", "TASI"])
        with col2:
            add_benchmark_button = st.form_submit_button("Add +")
            remove_benchmark_button = st.form_submit_button("Remove -")

    # Add or remove the selected benchmark from the list when the user clicks the corresponding button
    if add_benchmark_button:
        st.session_state.benchmarks.append(benchmark)
    if remove_benchmark_button and benchmark in st.session_state.tickers:
        st.session_state.benchmarks.remove(benchmark)
    
    st.write(st.session_state.benchmarks)


    portfolio_size = st.number_input("Enter the value of your portfolio in ($):")
    try:
        val = float(portfolio_size)
    except ValueError:
        print("That's not a number! \n Try again:")
        portfolio_size = input("Enter the value of your portfolio in ($):")
    
    if st.button("Strategize"):
        # Blueprints for Showcasing the Final Data Frames
        symbol_groups = list(chunks(st.session_state.tickers, len(st.session_state.tickers)))
        symbol_strings = []
        for i in range(0, len(symbol_groups)):
            symbol_strings.append(','.join(symbol_groups[i]))


        hqm_columns = [
                'Ticker', 
                'Price', 
                'Recommended Number of shares to Buy', 
                'One-Year Price Return', 
                'One-Year Return Percentile',
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'Three-Month Price Return',
                'Three-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score'
                ]
        hqm_dataframe = pd.DataFrame(columns = hqm_columns)
        if benchmark == 'S&P 500' :
            for symbol_string in symbol_strings:
                batch_api_call_url = f'https://cloud.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
                data = requests.get(batch_api_call_url).json()
                for symbol in symbol_string.split(','):
                    hqm_dataframe = hqm_dataframe.append(
                                                    pd.Series([symbol, 
                                                            data[symbol]['quote']['latestPrice'],
                                                            'N/A',
                                                            data[symbol]['stats']['year1ChangePercent'],
                                                            'N/A',
                                                            data[symbol]['stats']['month6ChangePercent'],
                                                            'N/A',
                                                            data[symbol]['stats']['month3ChangePercent'],
                                                            'N/A',
                                                            data[symbol]['stats']['month1ChangePercent'],
                                                            'N/A',
                                                            'N/A'
                                                            ], 
                                                            index = hqm_columns), 
                                                    ignore_index = True)
                                 
        time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]

        for row in hqm_dataframe.index:
            for time_period in time_periods:
                hqm_dataframe.loc[row, f'{time_period} Return Percentile'] = stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'], hqm_dataframe.loc[row, f'{time_period} Price Return'])/100

        # Print each percentile score to make sure it was calculated properly
        for time_period in time_periods:
            print(hqm_dataframe[f'{time_period} Return Percentile'])
        for row in hqm_dataframe.index:
            momentum_percentiles = []
            for time_period in time_periods:
                momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
            hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)
        hqm_dataframe.sort_values(by = 'HQM Score', ascending = False)
        position_size = float(portfolio_size) / len(hqm_dataframe.index)
        for i in range(0, len(hqm_dataframe['Ticker'])):
            hqm_dataframe.loc[i, 'Recommended Number of shares to Buy'] = math.floor(position_size / hqm_dataframe['Price'][i])         
        st.write(hqm_dataframe)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    main()