import streamlit as st
import pandas as pd
import altair as alt
from services.yfinance_service import calculate_dcf, get_valuation_and_peer_data
from config.settings import TICKER_TO_NAME, PEER_TICKERS, PRIMARY_COLOR, SECONDARY_COLOR

def render_valuation_tab(ticker):
    stock_name = TICKER_TO_NAME.get(ticker, ticker)
    st.subheader(f"Valuation & Quality for {stock_name} ({ticker})")

    peers = PEER_TICKERS.get(ticker, ["NIFTYBEES.NS"])
    metrics = get_valuation_and_peer_data(ticker, peers)
    dcf = calculate_dcf(ticker)

    if not metrics or not dcf:
        st.error("Failed to fetch Yahoo Finance data.")
        return

    st.metric("Intrinsic Value (DCF)", f"₹{dcf['intrinsic_value']}", f"{dcf['margin_of_safety']}% MoS")
    st.metric("Current Market Price", f"₹{dcf['current_price']}")

    df = pd.DataFrame(metrics["peer_comparison"])
    chart = alt.Chart(df).mark_bar().encode(
        x="Stock:N", y="P/E (TTM):Q",
        color=alt.condition(alt.datum.Stock == ticker, alt.value(SECONDARY_COLOR), alt.value(PRIMARY_COLOR)),
        tooltip=["Stock", "P/E (TTM)"]
    ).properties(title="P/E Comparison").interactive()
    st.altair_chart(chart, use_container_width=True)

    st.dataframe(pd.DataFrame(metrics["quality_ratios"].items(), columns=["Ratio", "Value"]))
