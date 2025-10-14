import streamlit as st
import altair as alt
from services.yfinance_service import get_technical_data
from config.settings import TICKER_TO_NAME, PRIMARY_COLOR, SECONDARY_COLOR

def render_technical_tab(ticker):
    stock_name = TICKER_TO_NAME.get(ticker, ticker)
    st.subheader(f"Technical Analysis for {stock_name}")

    df = get_technical_data(ticker)
    if df.empty:
        st.warning("Could not fetch data.")
        return

    chart = alt.Chart(df.reset_index()).transform_fold(
        ['Close', 'SMA_50', 'SMA_200'], as_=['Metric', 'Value']
    ).mark_line().encode(
        x='Date:T', y='Value:Q', color='Metric:N'
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)
