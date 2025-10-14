import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import warnings

# Suppress yfinance warnings about data retrieval issues
warnings.filterwarnings("ignore", category=FutureWarning)

def get_ticker_object(ticker_symbol: str) -> Optional[yf.Ticker]:
    """Helper function to create a yfinance Ticker object."""
    try:
        return yf.Ticker(ticker_symbol)
    except Exception as e:
        print(f"Error creating Ticker object for {ticker_symbol}: {e}")
        return None

def get_realtime_price(ticker_symbol: str) -> float:
    """Fetches the current market price."""
    ticker = get_ticker_object(ticker_symbol)
    if ticker and ticker.info.get('currentPrice'):
        return ticker.info['currentPrice']
    
    # Fallback: Get last close price from history
    try:
        data = yf.download(ticker_symbol, period="1d", interval="1m", progress=False)
        return data['Close'].iloc[-1] if not data.empty else 0.0
    except:
        return 0.0

def calculate_dcf(ticker_symbol: str) -> Dict[str, Any]:
    """Uses yfinance to pull info for a simplified DCF calculation."""
    ticker = get_ticker_object(ticker_symbol)
    if not ticker:
        return {'current_price': 0, 'intrinsic_value': 0, 'margin_of_safety': 0, 'inputs': {}}

    info = ticker.info
    
    # --- Real Data Points ---
    current_price = info.get('currentPrice', 0.0)
    eps_ttm = info.get('trailingEps', 0.0)
    
    # --- Assumption Based (Cannot reliably pull from yfinance) ---
    # We use some heuristics/defaults since future growth and WACC are internal estimates
    # Use analyst growth estimates if available, otherwise default
    growth_rate = info.get('earningsGrowth', 0.10) # Analyst estimate or default 10%
    discount_rate = 0.12 # Standard WACC assumption 
    terminal_multiple = 15 

    if eps_ttm <= 0 or current_price == 0:
        return {'current_price': current_price, 'intrinsic_value': 0, 'margin_of_safety': 0, 'inputs': {}}

    # Simplified 5-year DCF projection (using EPS for proxy)
    projected_eps = [eps_ttm * (1 + growth_rate)**i for i in range(1, 6)]
    
    # Calculate Present Value (PV)
    pv_cash_flows = [eps / (1 + discount_rate)**i for i, eps in enumerate(projected_eps, 1)]
    
    # Terminal Value (Year 5 EPS * Terminal Multiple)
    terminal_value = projected_eps[-1] * terminal_multiple
    pv_terminal_value = terminal_value / (1 + discount_rate)**5
    
    intrinsic_value = round(sum(pv_cash_flows) + pv_terminal_value, 2)
    
    margin_of_safety = round(100 * (intrinsic_value - current_price) / intrinsic_value, 2)
    
    return {
        'current_price': current_price,
        'intrinsic_value': intrinsic_value,
        'margin_of_safety': margin_of_safety,
        'inputs': {
            'EPS (TTM)': f"₹{eps_ttm:.2f}", 
            'LT Growth': f"{growth_rate * 100:.1f}%",
            'Discount Rate': f"{discount_rate * 100:.0f}%"
        }
    }

def get_technical_data(ticker_symbol: str) -> pd.DataFrame:
    """Fetches 12 months of historical price data and calculates SMAs and RSI (using TA-Lib or simplified)."""
    #end_date = datetime.today()
    #start_date = end_date - timedelta(days=365)
    
    # Download data
    df_multi = yf.download(
        ticker_symbol, 
        period="5y", # <-- Set period to 5 years (recommended for 200-day SMA)
        interval="1d",
        progress=False
    )
    
    if df_multi.empty:
        return pd.DataFrame()
    
    # 2. Extract only the 'Price' level from the MultiIndex for the column names
    # The column names are currently a MultiIndex: ('Close', 'RELIANCE.NS')
    # We want to keep only the first level: 'Close', 'High', 'Low', 'Open', 'Volume'
    df_multi.columns = df_multi.columns.get_level_values(0)

    # 3. (Optional but recommended) Rename the 'Adj Close' column to simply 'Close' 
    # if you prefer a cleaner column name for the adjusted closing price
    if 'Adj Close' in df_multi.columns:
        df_multi = df_multi.rename(columns={'Adj Close': 'Close'})

    # The resulting DataFrame now has a single-level index showing only price metrics
    df = df_multi

    # Calculate SMAs
    df['SMA_50'] = df['Close'].rolling(window=50).mean().round(2)
    df['SMA_200'] = df['Close'].rolling(window=200).mean().round(2)
    
    # Simplified RSI (Note: A true RSI needs >14 periods of history)
    # This is a placeholder; for production, use 'ta' library.
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs)).round(2)
    
    # Drop rows where SMAs/RSI are NaN due to insufficient history (start of the DataFrame)
    df = df.dropna(subset=['SMA_50', 'SMA_200', 'RSI'])
    return df

def get_valuation_and_peer_data(ticker_symbol: str, peer_tickers: List[str]) -> Dict[str, Any]:
    """Fetches valuation metrics for the company and its peers."""
    ticker = get_ticker_object(ticker_symbol)
    if not ticker:
        return {}

    info = ticker.info
    
    # --- Company Valuation ---
    company_data = {
        'P/E (TTM)': info.get('trailingPE', np.nan),
        'P/B': info.get('priceToBook', np.nan),
        'EV/EBITDA': info.get('enterpriseToEbitda', np.nan),
        '5Y Avg P/E': info.get('fiftyDayAverage', np.nan) / info.get('trailingEps', 1) # Crude proxy, not actual 5Y avg
    }
    
    # --- Peer Valuation (for comparison chart) ---
    peer_metrics = []
    
    # Bulk fetch peer info
    #multi_ticker_data = yf.download(peer_tickers, period="1d", progress=False)
    
    for peer_ticker in peer_tickers:
        try:
            peer_info = yf.Ticker(peer_ticker).info
            peer_metrics.append({
                'Stock': peer_ticker,
                'P/E (TTM)': peer_info.get('trailingPE', np.nan),
                'P/B': peer_info.get('priceToBook', np.nan),
                'EV/EBITDA': peer_info.get('enterpriseToEbitda', np.nan),
            })
        except:
            peer_metrics.append({'Stock': peer_ticker, 'P/E (TTM)': np.nan, 'P/B': np.nan, 'EV/EBITDA': np.nan})

    # --- Financial Quality Ratios ---
    quality_ratios = {
        'ROE (%)': info.get('returnOnEquity', np.nan) * 100,
        'Debt/Equity': info.get('debtToEquity', np.nan) / 100,
        'Current Ratio': info.get('currentRatio', np.nan),
        'Interest Coverage': info.get('ebitda') / info.get('interestExpense') if info.get('interestExpense') else np.nan,
    }
    
    return {
        'company_valuation': {k: round(v, 2) if isinstance(v, (int, float)) and not np.isnan(v) else v for k, v in company_data.items()},
        'peer_comparison': peer_metrics,
        'quality_ratios': {k: round(v, 2) if isinstance(v, (int, float)) and not np.isnan(v) else v for k, v in quality_ratios.items()}
    }