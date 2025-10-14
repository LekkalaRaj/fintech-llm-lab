import streamlit as st
import altair as alt

def display_sources(sources):
    if not sources:
        st.info("No source URLs found.")
        return
    with st.expander("🔗 Data Traceability (Source URLs)"):
        for i, url in enumerate(sources, 1):
            st.markdown(f"{i}. [{url}]({url})")

def colorize_change(val):
    color = "green" if val > 0 else "red"
    return f'<span style="color:{color};font-weight:bold;">{val:.2f}%</span>'