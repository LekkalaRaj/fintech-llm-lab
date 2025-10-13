# app.py (Updated for yfinance)

import streamlit as st
import pandas as pd
import json
import os
from typing import Dict, Any, List
import altair as alt
from datetime import datetime

# Import components from our modular files
from config import INDIAN_PORTFOLIO, MOCK_USER_ID, MODEL_NAME, PEER_TICKERS, TICKER_TO_NAME, PRIMARY_COLOR, SECONDARY_COLOR
from prompts import (
    get_financial_deep_dive_prompt, 
    get_news_guidance_prompt, 
    get_data_extraction_prompt,
    get_risk_tone_prompt
)
from llm_service import (
    initialize_client, 
    generate_llm_response, 
    extract_structured_data 
)
from yfinance_data_service import ( # UPDATED IMPORT
    get_technical_data, 
    get_valuation_and_peer_data, 
    calculate_dcf, 
    get_realtime_price
)


# --- Reusable Utility Functions ---

def display_sources(sources: List[str]):
    """Displays the list of source URLs in an expandable element."""
    if sources:
        with st.expander("🔗 Data Traceability (Source URLs)"):
            st.markdown("The following sources were used to ground this analysis:")
            for i, url in enumerate(sources, 1):
                st.markdown(f"{i}. [{url}]({url})")
    else:
        st.info("No explicit source URLs were retrieved for this query.")

def create_financial_visualizations(data: Dict[str, Any]):
    """Creates and displays charts based on the extracted JSON data (Tab 1)."""
    
    # 1. QoQ Financial Bar Chart
    st.markdown("### 📈 QoQ Financial Performance")
    financial_df = pd.DataFrame(data['financial_data'])
    financial_df_melted = financial_df.melt(
        id_vars='metric',
        var_name='Quarter',
        value_name='Value (Crores)'
    ).rename(columns={'metric': 'Metric'})
    
    financial_df_melted['Quarter'] = financial_df_melted['Quarter'].replace({
        'current_q_value': 'Current Quarter',
        'previous_q_value': 'Previous Quarter'
    })
    
    chart = alt.Chart(financial_df_melted).mark_bar().encode(
        x=alt.X('Metric:N'),
        y=alt.Y('Value (Crores):Q'),
        color=alt.Color('Quarter:N', scale=alt.Scale(range=[PRIMARY_COLOR, SECONDARY_COLOR])),
        column=alt.Column('Metric:N', header=alt.Header(titleOrient="bottom", labelOrient="bottom")),
        tooltip=['Metric', 'Quarter', 'Value (Crores)']
    ).properties(title="QoQ Revenue & Net Profit (in Crores)").interactive()
    
    st.altair_chart(chart, use_container_width=True)

    # 2. Shareholding Pie Chart and Table
    st.markdown("### 📊 Latest Shareholding Pattern")
    shareholding_data = [
        {'category': item['category'], 'percentage': item['percentage'], 'change_qoq': item['change_qoq']}
        for item in data['shareholding_data']
    ]
    shareholding_df = pd.DataFrame(shareholding_data)

    col_chart, col_table = st.columns([1, 1])
    
    with col_chart:
        st.subheader("Composition (%)")
        pie = alt.Chart(shareholding_df).mark_arc(outerRadius=120).encode(
            theta=alt.Theta("percentage", stack=True),
            color=alt.Color("category"),
            order=alt.Order("percentage", sort="descending"),
            tooltip=["category", "percentage"]
        ).properties(height=300)
        st.altair_chart(pie, use_container_width=True)

    with col_table:
        st.subheader("QoQ Change (Points)")
        def color_change(val):
            return f'<span style="color: {"green" if val > 0 else "red"}; font-weight: bold;">{val:.2f}%</span>'
            
        styled_df = shareholding_df[['category', 'change_qoq']].set_index('category')
        styled_df.columns = ['QoQ Change (pp)']
        st.markdown(styled_df.to_html(formatters={'QoQ Change (pp)': color_change}, escape=False), unsafe_allow_html=True)
        st.caption("pp = percentage points. Positive change means the holder increased their stake.")

# --- Tab 2: Valuation and Quality ---

def render_valuation_tab(ticker_symbol: str):
    """Renders the Valuation and Quality Analysis tab (Tab 2)."""
    stock_name = TICKER_TO_NAME.get(ticker_symbol, ticker_symbol)
    st.subheader(f"Valuation and Financial Quality for {stock_name} ({ticker_symbol})")
    
    # 1. Fetch REAL Data from yfinance
    peers = PEER_TICKERS.get(ticker_symbol, [])
    data_metrics = get_valuation_and_peer_data(ticker_symbol, peers)
    dcf_data = calculate_dcf(ticker_symbol)
    
    # Check for empty data
    if not data_metrics or not dcf_data:
        st.error("Could not fetch real-time financial data from Yahoo Finance. Please check the ticker symbol and your internet connection.")
        return

    # --- DCF and Margin of Safety ---
    st.markdown("### 🎯 Discounted Cash Flow (DCF) Analysis")
    col1, col2, col3 = st.columns(3)
    
    # Margin of Safety Indicator
    mos = dcf_data.get('margin_of_safety', 0)
    color = "green" if mos > 0 else ("red" if mos < 0 else "gray")
    col1.metric(
        "Intrinsic Value (DCF)", 
        f"₹{dcf_data['intrinsic_value']:,.2f}", 
        f"{mos:.2f}% Margin of Safety", 
        delta_color="normal"
    )
    col2.metric("Current Market Price", f"₹{dcf_data['current_price']:,.2f}")
    
    with col3:
        st.markdown("#### DCF Inputs (Assumptions)")
        st.dataframe(pd.DataFrame(dcf_data['inputs'].items(), columns=['Metric', 'Value']).set_index('Metric'))
    
    st.markdown("---")

    # --- Relative Valuation (P/E Comparison) ---
    st.markdown("### ⚖️ Relative Valuation (Peer Comparison)")
    
    # Add company data to the peer list for comparison
    rel_df = pd.DataFrame(data_metrics['peer_comparison'])
    company_row = {
        'Stock': ticker_symbol, 
        'P/E (TTM)': data_metrics['company_valuation'].get('P/E (TTM)'), 
        'P/B': data_metrics['company_valuation'].get('P/B'),
        'EV/EBITDA': data_metrics['company_valuation'].get('EV/EBITDA'),
    }
    rel_df = pd.concat([pd.DataFrame([company_row]), rel_df], ignore_index=True)
    
    # Chart
    pe_chart = alt.Chart(rel_df).mark_bar(color=PRIMARY_COLOR).encode(
        x=alt.X('Stock:N', sort=alt.EncodingSortField(field="P/E (TTM)", op="average", order='descending')),
        y=alt.Y('P/E (TTM):Q', title='P/E Ratio (TTM)'),
        color=alt.condition(
            alt.datum.Stock == ticker_symbol, 
            alt.value(SECONDARY_COLOR), 
            alt.value(PRIMARY_COLOR)
        ),
        tooltip=['Stock', 'P/E (TTM)']
    ).properties(title="P/E Ratio: Company vs. Peers").interactive()
    
    st.altair_chart(pe_chart, use_container_width=True)
    
    # Table and Historical P/E
    col_table, col_hist = st.columns(2)
    with col_table:
        st.markdown("##### Valuation Metrics Table (TTM)")
        st.dataframe(rel_df.set_index('Stock').fillna('N/A'))
    with col_hist:
        st.markdown("##### Historical Context")
        val_df = pd.DataFrame({
            'Metric': ['Current P/E', '5Y Avg P/E (Proxy)'],
            'Value': [
                data_metrics['company_valuation'].get('P/E (TTM)'), 
                data_metrics['company_valuation'].get('5Y Avg P/E')
            ]
        })
        st.dataframe(val_df.set_index('Metric').fillna('N/A'))
        st.caption("5Y Avg P/E is a crude approximation using yfinance data; use actual long-term data for precision.")
        
    st.markdown("---")
    
    # --- Financial Quality Ratios ---
    st.markdown("### 🛡️ Financial Quality and Risk Ratios")
    ratios_df = pd.DataFrame(data_metrics['quality_ratios'].items(), columns=['Ratio', 'Value'])
    st.dataframe(ratios_df.fillna('N/A'), width='stretch')
    st.caption("Key Ratios: ROE (Return on Equity), Debt/Equity (Leverage), Current Ratio (Liquidity).")


# --- Tab 3: Technical Analysis ---

def render_technical_tab(ticker_symbol: str):
    """Renders the Technical and Trend Analysis tab (Tab 3)."""
    stock_name = TICKER_TO_NAME.get(ticker_symbol, ticker_symbol)
    st.subheader(f"Technical and Momentum Analysis for {stock_name} ({ticker_symbol})")

    # Fetch REAL Data
    tech_df = get_technical_data(ticker_symbol)
    
    if tech_df.empty:
        st.error(f"Could not fetch historical price data for {ticker_symbol} from Yahoo Finance.")
        return
    
    # 1. Price and Volume Chart
    st.markdown("### 📈 Price and Moving Averages")
    
    # Calculate current values and comparison
    current_close = tech_df['Close'].iloc[-1].item()
    sma_50 = tech_df['SMA_50'].iloc[-1].item()
    sma_200 = tech_df['SMA_200'].iloc[-1].item()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"₹{current_close:,.2f}")
    col2.metric("50-Day SMA", f"₹{sma_50:,.2f}", delta=f"{current_close - sma_50:,.2f}", delta_color="normal")
    col3.metric("200-Day SMA", f"₹{sma_200:,.2f}", delta=f"{current_close - sma_200:,.2f}", delta_color="normal")

    # Altair Chart for Price and SMAs
    tech_df.columns.name = None

    price_chart = alt.Chart(tech_df.reset_index()).transform_fold(
            ['Close', 'SMA_50', 'SMA_200'],
            as_=['Metric', 'Value']
        ).mark_line().encode(
            x=alt.X('Date:T', title="Date"),
            y=alt.Y('Value:Q', title="Price (₹)"),
            color=alt.Color('Metric:N', scale=alt.Scale(range=['green', PRIMARY_COLOR, SECONDARY_COLOR])),
            tooltip=['Date:T', 'Metric:N', alt.Tooltip('Value:Q', format=".2f")]
        ).properties(height=400)
    
    st.altair_chart(price_chart, use_container_width=True)
    
    st.markdown("---")
    
    # 2. Momentum and Volume Analysis
    col_rsi, col_vol = st.columns(2)
    
    with col_rsi:
        st.markdown("### Momentum (RSI)")
        current_rsi = tech_df['RSI'].iloc[-1]
        
        st.metric(
            "Current RSI (14-Day)", 
            f"{current_rsi:.2f}",
            "Overbought (>70) / Oversold (<30)", 
            delta_color="off"
        )
        
        # Simple RSI chart
        rsi_chart = alt.Chart(tech_df.reset_index()).mark_line(color=SECONDARY_COLOR).encode(
            x='Date:T',
            y=alt.Y('RSI:Q', scale=alt.Scale(domain=[20, 80])),
            tooltip=['Date', 'RSI']
        ).properties(height=200).interactive()
        
        # Add 70 and 30 lines
        line_70 = alt.Chart(pd.DataFrame({'y': [70]})).mark_rule(color='red').encode(y='y')
        line_30 = alt.Chart(pd.DataFrame({'y': [30]})).mark_rule(color='green').encode(y='y')
        
        st.altair_chart(rsi_chart + line_70 + line_30, use_container_width=True)

    with col_vol:
        st.markdown("### Volume")
        current_vol = tech_df['Volume'].iloc[-1]
        avg_vol = tech_df['Volume'].iloc[-50:-1].mean()
        
        vol_delta = f"{current_vol - avg_vol:,.0f}"
        
        st.metric("Today's Volume", f"{current_vol:,.0f}", delta=vol_delta, delta_color="off")
        
        # Volume Chart
        volume_chart = alt.Chart(tech_df.reset_index()).mark_bar(color=PRIMARY_COLOR).encode(
            x='Date:T',
            y='Volume:Q',
            tooltip=['Date', 'Volume']
        ).properties(height=200)
        st.altair_chart(volume_chart, use_container_width=True)


# --- Main Application Logic ---

def st_app():
    """Main Streamlit application function."""
    st.set_page_config(
        page_title="StockIQ: Fund Manager Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    client = initialize_client()
    if client is None:
        st.stop()

    # --- Sidebar and State Management ---
    with st.sidebar:
        st.title("📈 StockIQ Fund Manager")
        
        if 'selected_stock' not in st.session_state:
            st.session_state['selected_stock'] = INDIAN_PORTFOLIO[0]
        if 'analysis_cache' not in st.session_state:
            st.session_state['analysis_cache'] = {}
            
        selected_ticker = st.selectbox(
            "Choose a Stock to Analyze:",
            options=INDIAN_PORTFOLIO,
            format_func=lambda x: f"{TICKER_TO_NAME.get(x, x)} ({x})",
            key='stock_select_widget'
        )
        st.session_state['selected_stock'] = selected_ticker # Store the ticker
        selected_name = TICKER_TO_NAME.get(selected_ticker, selected_ticker)

        st.markdown("---")
        st.caption(f"LLM Model: `{MODEL_NAME}`")
        st.caption(f"User ID: `{MOCK_USER_ID}`")
        st.caption("Valuation/Technical Data is live via **yfinance**.")

    # --- Main Panel Header ---
    st.header(f"Intelligence Dashboard for: **{selected_name}** ({selected_ticker})")
    
    # --- Tabbed Analysis (Now 4 Tabs) ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Financial Deep Dive (LLM)", 
        "💰 Valuation & Quality (YF)", 
        "📉 Technical & Trend (YF)", 
        "📰 Management Tone & News (LLM)"
    ])
    
    # --- Tab 1: Financial Deep Dive (QoQ & Shareholding) ---
    with tab1:
        st.subheader("Quarterly Performance and Ownership (LLM-Grounded)")
        
        # Use the name for the LLM prompt as it grounds better with Google Search
        llm_search_query = selected_name 
        
        cache_key_data = f"t1_data_{llm_search_query}"
        cache_key_text = f"t1_text_{llm_search_query}"
        
        if st.button(f"Generate/Refresh Deep Dive for {llm_search_query}", key="btn_t1"):
            st.session_state['analysis_cache'][cache_key_data] = None 
            st.session_state['analysis_cache'][cache_key_text] = None
        
        # A. Data Extraction (for Plots)
        if st.session_state['analysis_cache'].get(cache_key_data) is None:
            with st.spinner(f"STEP 1/2: Extracting structured data for plots for {llm_search_query}..."):
                prompt_data = get_data_extraction_prompt(llm_search_query)
                data_response, data_sources = extract_structured_data(client, prompt_data)
                st.session_state['analysis_cache'][cache_key_data] = {"data": data_response, "sources": data_sources}

        # B. Data Visualization
        data_cache = st.session_state['analysis_cache'].get(cache_key_data)
        if data_cache and data_cache.get('data'): 
            create_financial_visualizations(data_cache['data'])
            st.markdown("---")
            display_sources(data_cache.get('sources', [])) 
        else:
            st.warning("Structured data extraction failed. Click 'Generate/Refresh Deep Dive' to try again.")

        # C. Text Synthesis (Original Report)
        st.markdown("### 📝 Detailed Written Analysis")
        if st.session_state['analysis_cache'].get(cache_key_text) is None:
            with st.spinner(f"STEP 2/2: Generating detailed written report for {llm_search_query}..."):
                prompt_text = get_financial_deep_dive_prompt(llm_search_query)
                text_content, text_sources = generate_llm_response(client, prompt_text)
                st.session_state['analysis_cache'][cache_key_text] = {"content": text_content, "sources": text_sources}
        
        text_cache = st.session_state['analysis_cache'].get(cache_key_text)
        if text_cache and text_cache.get('content'):
            st.markdown(text_cache['content'])
            display_sources(text_cache.get('sources', []))

    # --- Tab 2: Valuation & Quality (yfinance) ---
    with tab2:
        render_valuation_tab(selected_ticker)

    # --- Tab 3: Technical & Trend (yfinance) ---
    with tab3:
        render_technical_tab(selected_ticker)

    # --- Tab 4: Management Tone & News (Two LLM Calls) ---
    with tab4:
        st.subheader("Management's View and Real-Time Events (LLM-Grounded)")

        cache_key_t4_tone = f"t4_tone_{llm_search_query}"
        cache_key_t4_news = f"t4_news_{llm_search_query}"

        if st.button(f"Generate/Refresh Qualitative Intelligence for {llm_search_query}", key="btn_t4"):
            st.session_state['analysis_cache'][cache_key_t4_tone] = None
            st.session_state['analysis_cache'][cache_key_t4_news] = None

        # 1. Management Tone & Risk Analysis
        st.markdown("### 🛑 Management Tone and Critical Risk Analysis")
        if st.session_state['analysis_cache'].get(cache_key_t4_tone) is None:
            with st.spinner(f"STEP 1/2: Synthesizing management tone and specific risks for {llm_search_query}..."):
                prompt_tone = get_risk_tone_prompt(llm_search_query)
                tone_content, tone_sources = generate_llm_response(client, prompt_tone)
                st.session_state['analysis_cache'][cache_key_t4_tone] = {"content": tone_content, "sources": tone_sources}
        
        tone_cache = st.session_state['analysis_cache'].get(cache_key_t4_tone)
        if tone_cache and tone_cache.get('content'):
            st.markdown(tone_cache['content'])
            display_sources(tone_cache.get('sources', []))
        
        st.markdown("---")
        
        # 2. Real-Time News & Guidance
        st.markdown("### 📰 Real-Time News and Analyst Guidance")
        if st.session_state['analysis_cache'].get(cache_key_t4_news) is None:
            with st.spinner(f"STEP 2/2: Searching and synthesizing latest news for {llm_search_query}..."):
                prompt_news = get_news_guidance_prompt(llm_search_query)
                news_content, news_sources = generate_llm_response(client, prompt_news)
                st.session_state['analysis_cache'][cache_key_t4_news] = {"content": news_content, "sources": news_sources}
        
        news_cache = st.session_state['analysis_cache'].get(cache_key_t4_news)
        if news_cache and news_cache.get('content'):
            st.markdown(news_cache['content'])
            display_sources(news_cache.get('sources', []))


if __name__ == "__main__":
    st_app()