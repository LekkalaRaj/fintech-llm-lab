import time
import streamlit as st

def retry_operation(func, retries=3, delay=1):
    """Generic retry decorator for transient API issues."""
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            if attempt < retries - 1:
                st.warning(f"Retry {attempt+1}/{retries} failed: {e}")
                time.sleep(delay)
            else:
                st.error(f"Operation failed after {retries} attempts.")
                raise
