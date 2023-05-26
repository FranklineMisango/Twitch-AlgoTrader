import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit import pyplot as st_plt

def main():
    st.title("Level I Stock Risk + Reward Visualizer")
    st.warning("This project is intended for users with a basic understanding of Algorithmic Trading")
    st.image('/home/misango/code/Xpay_AlgoTrader/images/stock_visual.jpg')
    st.markdown("**Enter stock tickers and select a benchmark:**")

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
        st.header("Add/End Date Fetching & Price Frame + Graph")
        col1, col2 = st.columns([2, 1])
        with col1:
            start_date = st.date_input("Start date:")
        with col2:
            end_date = st.date_input("End Date:")
        if start_date and end_date and st.form_submit_button("Closing Price Data"):
            # Perform download on all stocks
            stocks_all = yf.download(st.session_state.tickers, start=start_date, end=end_date)
            if not stocks_all.empty:
                st.success("Data downloaded successfully! Analyst Can Now Investigate A Stock's perfomance against selected Benchmark")
                close_all = stocks_all.loc[:, "Close"].copy()
                plt.figure(figsize=(15, 8))
                for ticker in close_all.columns:
                    plt.plot(close_all.index, close_all[ticker], label=ticker)
                plt.xlabel('Date', fontsize=12)
                plt.ylabel('Close Price', fontsize=12)
                plt.title('Closing Prices($)', fontsize=14)
                plt.grid(True)
                plt.legend(loc='upper left')
                plt.tight_layout()
                fig = plt.gcf()  # Get the current figure
                st.pyplot(fig)

                # Use the normalized_close_all DataFrame as needed
                st.header("Normalization for Benchmark Comparison [100 used]")
                normalized_close_all = close_all.div(close_all.iloc[0]).mul(100)
                plt.figure(figsize=(15, 8))
                for ticker in normalized_close_all.columns:
                    plt.plot(normalized_close_all.index, normalized_close_all[ticker], label=ticker)
                plt.xlabel('Date', fontsize=12)
                plt.ylabel('Closing price ($)', fontsize=12)
                plt.title('Normalized Closing Prices($)', fontsize=14)
                plt.grid(True)
                plt.legend(loc='upper left')
                plt.tight_layout()
                normalized_figure = plt.gcf()
                st.pyplot(normalized_figure)
                
                st.header("Annual Risk & Return / Year using Mean & Stdev")
                return_all_close = close_all.pct_change().dropna()
                summary_close_all = return_all_close.describe().T.loc[:, ["mean", "std"]]
                summary_close_all["mean"] = summary_close_all["mean"] * 252
                summary_close_all["std"] = summary_close_all["std"] * np.sqrt(252)
                plt.figure(figsize=(12,8))
                for i in summary_close_all.index:
                    plt.scatter(summary_close_all.loc[i, "std"] + 0.002, summary_close_all.loc[i, "mean"]+0.002, s=15)
                    plt.text(summary_close_all.loc[i, "std"] + 0.002, summary_close_all.loc[i, "mean"]+0.002, i)  # Add label using plt.text()
                plt.xlabel('Annual Risk Promise(%)', fontsize=12)
                plt.ylabel('Annual Return Promise(%)', fontsize=12)
                plt.title('Annual Risk/Return Portfolio for Each Ticker', fontsize=14)
                plt.grid(True)
                plt.legend(loc='upper left')
                plt.tight_layout()
                normalized_figure_final = plt.gcf()
                st.pyplot(normalized_figure_final)              
                max_mean = summary_close_all["mean"].max()
                max_std = summary_close_all["std"].max()
                high_mean_std_rows = summary_close_all[(summary_close_all["mean"] == max_mean) & (summary_close_all["std"] == max_std)]
                st.write("For instance, Our graph depicts", high_mean_std_rows.index[0], "has higher Annual returns but Also a higher risk.")
                st.warning("It is Recommended for short term Investment, But such should be proceeded with caution")

                st.header("Volatility in Return Margins (%) For All Business Days till Aforementioned End Date")
                # Extract the tickers (column names excluding the first column)
                data_columns = return_all_close.columns[0:-1]

                # Define a color palette with desired colors
                color_palette = sns.color_palette("Set2", len(data_columns))

                # Create a histogram for each ticker
                for i, column in enumerate(data_columns):
                    fig, ax = plt.subplots(figsize=(12, 8))
                    ax.set_xlabel("Volatility in Return Margins")
                    ax.set_ylabel("Frequency of Return Change")
                    return_all_close.loc[:, column].plot(kind="hist", bins=100, ax=ax, color=color_palette[i], label=column)
                    ax.legend()
                    st.pyplot(fig)
                st.header("Correlation & Covariance Analysis Per stock & Against Benchmark Referencing Annual Returns(%)")
                plt.figure(figsize = (12,8))
                sns.set(font_scale = 1.4)
                plt.title("Correlation Heatmap ")
                sns.heatmap(return_all_close.corr(), cmap="Reds", annot=True, annot_kws={"size":15}, vmax=0.6)
                correlation_graph = plt.gcf()
                st.pyplot(correlation_graph)

                #The covariance graph
                
                plt.figure(figsize = (12,8))
                sns.set(font_scale = 1.4)
                plt.title("Correlation Heatmap ")
                sns.heatmap(return_all_close.cov(), cmap="Greens", annot=True, annot_kws={"size":15}, vmax=0.6)
                covariance_graph = plt.gcf()
                st.pyplot(covariance_graph)
            else:
                st.error("Failed to download data.")
    if st.button('Reset'):
    # Clear the session state
        st.session_state.clear()
    # Refresh the page
        raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

if __name__ == "__main__":
    main()
