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
    # Conglomerate / Energy
    "RELIANCE.NS": ["BPCL.NS", "IOC.NS", "ONGC.NS", "TATAPOWER.NS"],

    # Financial Services / NBFC
    "JIOFIN.NS": ["BAJFINANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS"],

    # Capital Goods / Auto Components
    "TIINDIA.NS": ["CUMMINSIND.NS", "SKFINDIA.NS", "BOSCHLTD.NS", "MOTHERSON.NS"],

    # Beverages / FMCG
    "VBL.NS": ["NESTLEIND.NS", "JUBLFOOD.NS", "BRITANNIA.NS", "UBL.NS"],

    # IT / Engineering Design
    "TATATECH.NS": ["LTTS.NS", "KPITTECH.NS", "TATAELXSI.NS", "CYIENT.NS"],

    # Automobile / EV
    "TATAMOTORS.NS": ["MARUTI.NS", "M&M.NS", "ASHOKLEY.NS", "BAJAJ-AUTO.NS"],

    # Process Engineering / Bioenergy
    "PRAJIND.NS": ["CUMMINSIND.NS", "BEML.NS", "THERMAX.NS", "ELECON.NS"],

    # Defence / Electronics
    "ZENTEC.NS": ["BEL.NS", "HAL.NS", "SOLARINDS.NS", "DATA-PATTERN.NS"],

    # Tyres / Auto Ancillary
    "BALKRISIND.NS": ["MRF.NS", "APOLLOTYRE.NS", "JKTYRE.NS", "CEATLTD.NS"],

    # Ports / Infrastructure
    "ADANIPORTS.NS": ["CONCOR.NS", "GMDCLTD.NS", "GMRINFRA.NS", "NHPC.NS"],

    # Electronics Manufacturing / EMS
    "PGELETRO.NS": ["DIXON.NS", "AMBER.NS", "ELIN.NS", "SYRMA.NS"],

    # Textile / Export
    "GOKEX.NS": ["KPRMILL.NS", "PAGEIND.NS", "WELSPUNIND.NS", "VARDMNPOLY.NS"],

    # Auto Tech / Engineering IT
    "KPITTECH.NS": ["TATAELXSI.NS", "LTTS.NS", "CYIENT.NS", "PERSISTENT.NS"],

    # Shipbuilding / Defense PSU
    "MAZDA.BO": ["COCHINSHIP.NS", "GRSE.NS", "GARDENSILK.NS"],

    # Healthcare / Insurance Tech
    "MEDIASSIST.NS": ["HDFCLIFE.NS", "ICICIPRULI.NS", "STARHEALTH.NS", "MAXHEALTH.NS"],

    # Mapping / Tech SaaS
    "MAPMYINDIA.NS": ["INFOEDGE.NS", "ZOMATO.NS", "NAUKRI.NS", "PAYTM.NS"],

    # Depository / Financial Infrastructure
    "CDSL.NS": ["ICICIBANK.NS", "HDFCBANK.NS", "KOTAKBANK.NS", "SBICARD.NS"],

    # Default fallback
    "DEFAULT": ["NIFTYBEES.NS"]
}
