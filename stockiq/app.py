import streamlit as st
from config.settings import INDIAN_PORTFOLIO, MOCK_USER_ID, MODEL_NAME, TICKER_TO_NAME
from services.llm_service import initialize_client
from ui.tabs.financial_tab import render_financial_tab
from ui.tabs.valuation_tab import render_valuation_tab
from ui.tabs.technical_tab import render_technical_tab
from ui.tabs.news_tab import render_news_tab

def main():
    st.set_page_config(
        page_title="StockIQ: Fund Manager Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    client = initialize_client()
    if not client:
        st.stop()

    with st.sidebar:
        st.title("📈 StockIQ Fund Manager")
        selected_ticker = st.selectbox(
            "Choose a Stock to Analyze:",
            options=INDIAN_PORTFOLIO,
            format_func=lambda x: f"{TICKER_TO_NAME.get(x, x)} ({x})"
        )
        st.caption(f"LLM Model: `{MODEL_NAME}`")
        st.caption(f"User ID: `{MOCK_USER_ID}`")

    stock_name = TICKER_TO_NAME.get(selected_ticker, selected_ticker)
    st.header(f"Intelligence Dashboard for: **{stock_name} ({selected_ticker})**")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Financial Deep Dive (LLM)",
        "💰 Valuation & Quality (YF)",
        "📉 Technical & Trend (YF)",
        "📰 Management Tone & News (LLM)"
    ])

    with tab1:
        render_financial_tab(client, selected_ticker)

    with tab2:
        render_valuation_tab(selected_ticker)

    with tab3:
        render_technical_tab(selected_ticker)

    with tab4:
        render_news_tab(client, selected_ticker)

if __name__ == "__main__":
    main()