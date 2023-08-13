from config import ALPACA_CONFIG
from lumibot.brokers import Alpaca
#from lumibot.strategies import Strategy
from lumibot.backtesting import YahooDataBacktesting
from lumibot.traders import Trader
import streamlit as st
import datetime as dt
from dateutil.relativedelta import relativedelta
import os
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import quantstats as qs
import webbrowser as web
import yfinance as yf


st.title("🦜🔗 Algorithmic Trading Framework using Lumibots API")
message =  "This project is intended for users with an intermediate knowledge of Finance"
st.warning(message)

def main():
    global stocks_all
    # Retrieve the tickers from the app state or initialize as an empty list
    if 'tickers' not in st.session_state:
        st.session_state.tickers = []

    #retrieve the empty quantity values for each ticker
    if 'quantities' not in st.session_state:
        st.session_state.quantities =[]

    # Create a form for the ticker input
    with st.form(key='ticker_form'):
        col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
        with col1:
            ticker_input = st.text_input("Enter a stock ticker:", key='ticker_input')
        with col2:
            add_ticker_button = st.form_submit_button(label="Add +")
            remove_ticker_button = st.form_submit_button(label="Remove -")
        with col3:
            quantities_input =st.number_input("Enter the Stock quantity")
        with col4:
            add_quantity_button = st.form_submit_button(label="Confirm")
            remove_quantity_button = st.form_submit_button(label="Reset -")

        # Check if the ticker is already in the list
        is_duplicate = ticker_input in st.session_state.tickers

        # Add the entered ticker to the list when the user clicks the "+" button
        if add_ticker_button and not is_duplicate:
            st.session_state.tickers.append(ticker_input)

        # Remove the last ticker from the list when the "-" button is clicked
        if remove_ticker_button:
            if st.session_state.tickers:
                st.session_state.tickers.pop()
        # Display the current list of tickers and benchmarks
        st.markdown("**Current ticker(s) and quantity**")
        st.write(st.session_state.tickers),st.write (st.session_state.quantities)


def time():
        # Add the Start Date and End Date
        with st.form(key='start_end_dates'):
            st.header("Backtesting Strategies using Lumibots API")
            st.warning("Read the documentation to understand what each platform does technically")
            portfolio_size = st.number_input("Enter the value of your portfolio in ($):")
            try:
                val = float(portfolio_size)
            except ValueError:
                print("That's not a number! \n Try again:")
                portfolio_size = input("Enter the value of your portfolio in ($):")
            option = st.radio(
                                'Please select the Strategy you would like to use;', (
                                'Buy & Hold' , "Swing High", ""
                                )
                            )
            col1, col2 = st.columns([2, 2])
            with col1:
                start_date = st.date_input("Start date:")
            with col2:
                end_date = st.date_input("End Date:")


main()
time()