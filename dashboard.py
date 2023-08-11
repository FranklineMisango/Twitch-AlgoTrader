import streamlit as st
import requests
import pandas as pd
import math
import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit import pyplot as st_plt
from statistics import mean
from scipy import stats 
#from secrets_1 import IEX_CLOUD_API_TOKEN

st.title("Xpay Recommendation Algorithms - Level I to III")
message =  "This project is intended for users with an intermediate level of Finance"
st.warning(message)
st.image('images/finance.jpg')
def main():
    # Retrieve the tickers from the app state or initialize as an empty list
    if 'tickers' not in st.session_state:
        st.session_state.tickers = []

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

    # Create a dropdown menu for selecting a benchmark
    with st.form(key='benchmark_form'):
        col1, col2 = st.columns([2, 1])
        with col1:
            benchmark = st.selectbox("Select One benchmark (More will be added soon):", ["SPY", "DJIA", "HSI", "UKX", "SX5E", "SHCOMP", "N225", "STI", "NSEASI", "DFMGI", "ADXGI", "TASI"])
        with col2:
            add_benchmark_button = st.form_submit_button("Add +")
            remove_benchmark_button = st.form_submit_button("Remove -")

    # Add or remove the selected benchmark from the list when the user clicks the corresponding button
    if add_benchmark_button:
        st.session_state.tickers.append(benchmark)
    if remove_benchmark_button and benchmark in st.session_state.tickers:
        st.session_state.tickers.remove(benchmark)

    # Display the current list of tickers and benchmarks
    st.markdown("**Current tickers and benchmarks:**")
    st.write(st.session_state.tickers)

    # Add the Start Date and End Date
    with st.form(key='start_end_dates'):
        st.header("Add/End Date for Data Fetching using IEX cloud")
        col1, col2 = st.columns([2, 1])
        with col1:
            start_date = st.date_input("Start date:")
        with col2:
            end_date = st.date_input("End Date:")
        if start_date and end_date and st.form_submit_button("Submit"):
            # Perform download on all stocks
            stocks_all = yf.download(st.session_state.tickers, start=start_date, end=end_date)      
            if not stocks_all.empty:
                st.success("Data downloaded successfully! Analyst Can Now Investigate A Stock's perfomance against the selected Benchmark")
    option = st.selectbox(
                'Please select the platform you would like to use', (
                'Level I : Stock & Reward visualizer', 'Level II : Equal-Weight Optimizer', 'Level III: Quantitative momentum Strategizer' , 'Level IV : Value Investing Strategizer'
                )
            )
def stock():
    pass
def equal():
    pass
def quantitative():
    pass
def value():
    pass


main()