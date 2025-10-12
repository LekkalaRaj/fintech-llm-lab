import streamlit as st
import time
import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from typing import Optional, Dict, Any, Tuple, List

from config import MODEL_NAME, GROUNDING_TOOL

@st.cache_resource(show_spinner=False)
def initialize_client() -> Optional[genai.Client]:
    """Initializes the Gemini API client."""
    try:
        # Use GEMINI_API_KEY in the .env file
        load_dotenv(override=True)
        GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")
        
        # Initialize the native Google GenAI client
        client = genai.Client(api_key=GEMINI_API_KEY)
        return client
    except Exception as e:
        st.error(f"Error initializing Gemini client: {e}")
        st.info("Please ensure the GEMINI_API_KEY environment variable is set.")
        return None

def _extract_sources(response: types.GenerateContentResponse) -> List[str]:
    """Helper function to extract unique source URLs from the grounding metadata (robustly)."""
    sources = set()
    
    if (response.candidates and 
        response.candidates[0].grounding_metadata):
        
        grounding = response.candidates[0].grounding_metadata
        
        # Check if grounding_chunks is NOT None before iterating
        if grounding.grounding_chunks is not None:
            for chunk in grounding.grounding_chunks:
                # Use hasattr for safety, though standard in the SDK
                if hasattr(chunk, 'web') and chunk.web and hasattr(chunk.web, 'uri') and chunk.web.uri:
                    sources.add(chunk.web.uri)

    return sorted(list(sources))

def generate_llm_response(
    client: genai.Client,
    prompt: str,
    max_retries: int = 3,
) -> Tuple[str, List[str]]:
    """Calls Gemini API, returns the text content and a list of source URLs."""
    if client is None:
        return ("LLM Client failed to initialize. Check API key.", [])

    try:
        for attempt in range(max_retries):
            # ... (API call logic remains the same) ...
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=GROUNDING_TOOL,
                        temperature=0.2, 
                    ),
                )
                
                sources = _extract_sources(response)
                source_note = f"\n\n---\n*Data Grounded via Google Search. Model: {MODEL_NAME}*"
                return response.text + source_note, sources # SUCCESS RETURN

            except APIError as e:
                # ... (API error handling remains the same) ...
                if attempt < max_retries - 1:
                    st.warning(f"API call failed (Attempt {attempt + 1}/{max_retries}). Retrying with backoff...")
                    time.sleep(2 ** attempt) 
                else:
                    st.error(f"LLM API failed after {max_retries} attempts: {e}")
                    return ("Analysis could not be generated due to a persistent API error.", [])
            except Exception as e:
                # Catch unexpected errors within the retry loop
                st.error(f"An unexpected error occurred during LLM call in retry loop: {e}")
                time.sleep(1) # Wait a second before next attempt (optional)
        
        st.error("Text generation failed after all retries.")
        return ("Analysis failed to generate after multiple retries.", [])

    except Exception as e:
        # Final Catch-All for critical errors outside the retry loop
        st.error(f"A final critical error occurred during text LLM call: {e}")
        return ("Analysis failed due to a critical setup error.", [])


def extract_structured_data(
    client: genai.Client,
    prompt: str,
    max_retries: int = 3,
) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    """Calls Gemini API to extract data, returns parsed JSON dictionary and source URLs."""
    if client is None:
        return (None, [])

    try:
        for attempt in range(max_retries):
            # ... (API call and JSON parsing logic remains the same, ensuring robustness) ...
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=GROUNDING_TOOL,
                        temperature=0.01,
                    ),
                )
                
                sources = _extract_sources(response)
                
                raw_json_text = response.text.strip()
                if raw_json_text.startswith("```json"):
                    raw_json_text = raw_json_text[7:]
                if raw_json_text.endswith("```"):
                    raw_json_text = raw_json_text[:-3]

                data = json.loads(raw_json_text.strip())
                return data, sources # SUCCESS RETURN

            except json.JSONDecodeError as e:
                st.warning(f"Failed to parse JSON (Attempt {attempt + 1}/{max_retries}). LLM output was non-compliant.")
                time.sleep(1 ** attempt)
            except APIError as e:
                if attempt < max_retries - 1:
                    st.warning(f"API call failed (Attempt {attempt + 1}/{max_retries}). Retrying with backoff...")
                    time.sleep(2 ** attempt)
                else:
                    st.error(f"LLM API failed after {max_retries} attempts: {e}")
                    return (None, [])
            except Exception as e:
                st.error(f"An unexpected error occurred during LLM call in retry loop: {e}")
                time.sleep(1) 
        
        st.error("Data extraction failed after all retries.")
        return (None, [])

    except Exception as e:
        st.error(f"A final critical error occurred during data LLM call: {e}")
        return (None, [])