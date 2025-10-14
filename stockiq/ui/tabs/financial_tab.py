import streamlit as st
import pandas as pd
import altair as alt
from prompts.prompts import get_data_extraction_prompt, get_financial_deep_dive_prompt
from services.llm_service import extract_structured_data, generate_llm_response
from ui.components import display_sources
from config.settings import PRIMARY_COLOR, SECONDARY_COLOR

def render_financial_tab(client, stock_name):
    st.subheader("Quarterly Performance and Ownership")

    if st.button(f"Generate/Refresh Deep Dive for {stock_name}"):
        st.session_state.pop(f"{stock_name}_data", None)
        st.session_state.pop(f"{stock_name}_text", None)

    data_key, text_key = f"{stock_name}_data", f"{stock_name}_text"

    if data_key not in st.session_state:
        with st.spinner("Extracting structured data..."):
            data, sources = extract_structured_data(client, get_data_extraction_prompt(stock_name))
            st.session_state[data_key] = {"data": data, "sources": sources}

    cache = st.session_state.get(data_key)
    if cache and cache["data"]:
        show_financial_charts(cache["data"])
        display_sources(cache["sources"])

    if text_key not in st.session_state:
        with st.spinner("Generating written analysis..."):
            text, sources = generate_llm_response(client, get_financial_deep_dive_prompt(stock_name))
            st.session_state[text_key] = {"text": text, "sources": sources}

    text_cache = st.session_state.get(text_key)
    if text_cache:
        st.markdown(text_cache["text"])
        display_sources(text_cache["sources"])

def show_financial_charts(data):
    df = pd.DataFrame(data["financial_data"])
    df_m = df.melt(id_vars="metric", var_name="Quarter", value_name="Value")
    chart = alt.Chart(df_m).mark_bar().encode(
        x="metric:N", y="Value:Q",
        color=alt.Color("Quarter:N", scale=alt.Scale(range=[PRIMARY_COLOR, SECONDARY_COLOR])),
        tooltip=["metric", "Quarter", "Value"]
    )
    st.altair_chart(chart, use_container_width=True)
