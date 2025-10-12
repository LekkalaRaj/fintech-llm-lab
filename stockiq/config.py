# config.py

from google.genai import types

# --- LLM CONFIG ---
MODEL_NAME = "gemini-2.5-flash" 
GROUNDING_TOOL = [types.Tool(google_search=types.GoogleSearch())]
MOCK_USER_ID = "FM_101_INDIA_CUSTOM"

# --- PORTFOLIO & PEERS ---

# Use Yahoo Finance Ticker Symbols for accurate data retrieval.
INDIAN_PORTFOLIO = [
    "RELIANCE.NS",      # Reliance Industries
    "JIOFIN.NS",        # Jio Financial Services (listed as JIOFIN)
    "TIINDIA.NS",       # Tube Investments of India
    "VBL.NS",           # Varun Beverages Ltd
    "TATATECH.NS",      # Tata Technologies Ltd
    "TATAMOTORS.NS",    # Tata Motors Ltd
    "PRAJIND.NS",       # Praj Industries Ltd
    "ZENTEC.NS",        # Zen Technologies Ltd
    "BALKRISIND.NS",    # Balkrishna Industries Ltd (tyres)
    "ADANIPORTS.NS",    # Adani Ports & SEZ Ltd
    "PGELETRO.NS",      # PG Electroplast Ltd (Approximate, ticker varies)
    "GOKEX.NS",         # Gokaldas Exports Ltd
    "KPITTECH.NS",      # KPIT Technologies Ltd
    "MAZDA.BO",         # Mazagon Dock Shipbuilders Ltd (Using .BO as MAZGAON.NS sometimes fails)
    "MEDIASSIST.NS",    # Medi Assist Healthcare Services Ltd
    "MAPMYINDIA.NS",    # CE Info Systems Ltd (MapmyIndia)
    "CDSL.NS"           # Central Depository Services Ltd
]

# Ticker-to-Name Mapping (for display)
TICKER_TO_NAME = {
    "RELIANCE.NS": "Reliance Industries",
    "JIOFIN.NS": "Jio Financial Services",
    "TIINDIA.NS": "Tube Investments India",
    "VBL.NS": "Varun Beverages",
    "TATATECH.NS": "Tata Technologies",
    "TATAMOTORS.NS": "Tata Motors",
    "PRAJIND.NS": "Praj Industries",
    "ZENTEC.NS": "Zen Technologies",
    "BALKRISIND.NS": "Balkrishna Tyres",
    "ADANIPORTS.NS": "Adani Ports",
    "PGELETRO.NS": "PG Electroplasts",
    "GOKEX.NS": "Gokaldas Exports",
    "KPITTECH.NS": "KPIT Technologies",
    "MAZDA.BO": "Mazagon Dock Shipbuilders",
    "MEDIASSIST.NS": "Medi Assist",
    "MAPMYINDIA.NS": "MapmyIndia",
    "CDSL.NS": "CDSL"
}

# Simplified Peer Grouping (for the valuation comparison tab)
PEER_TICKERS = {
    # IT/Tech/Software
    "KPITTECH.NS": ["TCS.NS", "INFY.NS", "PERSISTENT.NS"],
    "ZENTEC.NS": ["DATAPATNS.NS", "BEL.NS"], 
    "TATATECH.NS": ["LTTS.NS", "KPITTECH.NS"],
    "MAPMYINDIA.NS": ["INFOEDGE.NS", "ZOMATO.NS"],
    
    # Auto & Ancillary
    "TATAMOTORS.NS": ["MARUTI.NS", "M&M.NS"],
    "BALKRISIND.NS": ["MRF.NS", "APOLLOTYRE.NS"],
    
    # Financial Services
    "JIOFIN.NS": ["BAJFINANCE.NS", "HDFCBANK.NS"],
    "CDSL.NS": ["NSDL.NS", "ICICIBANK.NS"], # NSDL is not public, using proxies
    "MEDIASSIST.NS": ["HDFCLIFE.NS", "ICICIPRULI.NS"], # Health proxy
    
    # Capital Goods / Infrastructure
    "MAZDA.BO": ["GRSE.NS", "COCHINSHIP.NS"],
    "ADANIPORTS.NS": ["GMDCLTD.NS", "CONCOR.NS"],
    "TIINDIA.NS": ["CUMMINSIND.NS", "SKFINDIA.NS"],
    "PRAJIND.NS": ["ISGEC.NS", "TRIDENT.NS"],
    
    # FMCG/Consumer
    "VBL.NS": ["JUBLFOOD.NS", "NESTLEIND.NS"],
    "GOKEX.NS": ["KPRMILL.NS", "WELSPUNIND.NS"],
    "RELIANCE.NS": ["TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS"], # Conglomerate, using diversified
    "PGELETRO.NS": ["DIXON.NS", "AMBER.NS"], # Electronics Manufacturing
    
    # Default for any missing entry
    "DEFAULT": ["NIFTYBEES.NS"] 
}

# --- VISUALIZATION CONFIG ---
PRIMARY_COLOR = "#00B0FF" 
SECONDARY_COLOR = "#FF9900"