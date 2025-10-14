from google.genai import types

MODEL_NAME = "gemini-2.5-flash"
GROUNDING_TOOL = [types.Tool(google_search=types.GoogleSearch())]
MOCK_USER_ID = "FM_101_INDIA_CUSTOM"

INDIAN_PORTFOLIO = [
    "RELIANCE.NS", "JIOFIN.NS", "TIINDIA.NS", "VBL.NS",
    "TATATECH.NS", "TATAMOTORS.NS", "PRAJIND.NS", "ZENTEC.NS",
    "BALKRISIND.NS", "ADANIPORTS.NS", "PGELETRO.NS", "GOKEX.NS",
    "KPITTECH.NS", "MAZDA.BO", "MEDIASSIST.NS", "MAPMYINDIA.NS", "CDSL.NS"
]

TICKER_TO_NAME = {
    "RELIANCE.NS": "Reliance Industries", "JIOFIN.NS": "Jio Financial Services",
    "TIINDIA.NS": "Tube Investments India", "VBL.NS": "Varun Beverages",
    "TATATECH.NS": "Tata Technologies", "TATAMOTORS.NS": "Tata Motors",
    "PRAJIND.NS": "Praj Industries", "ZENTEC.NS": "Zen Technologies",
    "BALKRISIND.NS": "Balkrishna Tyres", "ADANIPORTS.NS": "Adani Ports",
    "PGELETRO.NS": "PG Electroplasts", "GOKEX.NS": "Gokaldas Exports",
    "KPITTECH.NS": "KPIT Technologies", "MAZDA.BO": "Mazagon Dock Shipbuilders",
    "MEDIASSIST.NS": "Medi Assist", "MAPMYINDIA.NS": "MapmyIndia", "CDSL.NS": "CDSL"
}

PRIMARY_COLOR = "#00B0FF"
SECONDARY_COLOR = "#FF9900"

PEER_TICKERS = {
    "KPITTECH.NS": ["TCS.NS", "INFY.NS"],
    "TATAMOTORS.NS": ["MARUTI.NS", "M&M.NS"],
    "RELIANCE.NS": ["TCS.NS", "HDFCBANK.NS"],
    "DEFAULT": ["NIFTYBEES.NS"]
}