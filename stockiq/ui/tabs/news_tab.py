import streamlit as st
from prompts.prompts import get_risk_tone_prompt, get_news_guidance_prompt
from services.llm_service import generate_llm_response
from ui.components import display_sources

def render_news_tab(client, stock_name):
    st.subheader("Management Tone & Real-Time News")

    if st.button(f"Generate/Refresh Insights for {stock_name}"):
        st.session_state.pop(f"{stock_name}_tone", None)
        st.session_state.pop(f"{stock_name}_news", None)

    tone_key, news_key = f"{stock_name}_tone", f"{stock_name}_news"

    if tone_key not in st.session_state:
        with st.spinner("Analyzing management tone and risk..."):
            text, src = generate_llm_response(client, get_risk_tone_prompt(stock_name))
            st.session_state[tone_key] = {"text": text, "sources": src}

    tone_cache = st.session_state.get(tone_key)
    if tone_cache:
        st.markdown(tone_cache["text"])
        display_sources(tone_cache["sources"])

    st.markdown("---")

    if news_key not in st.session_state:
        with st.spinner("Fetching latest news and guidance..."):
            text, src = generate_llm_response(client, get_news_guidance_prompt(stock_name))
            st.session_state[news_key] = {"text": text, "sources": src}

    news_cache = st.session_state.get(news_key)
    if news_cache:
        st.markdown(news_cache["text"])
        display_sources(news_cache["sources"])
