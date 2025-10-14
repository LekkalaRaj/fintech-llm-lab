def get_financial_deep_dive_prompt(stock_name: str) -> str:
    """Prompt for Tab 1: Synthesis and qualitative analysis (QoQ, Shareholding)."""
    return (
        f"Act as a specialized Indian equity research analyst. For the stock "
        f"'{stock_name}', find and summarize the most recent Quarter-on-Quarter (QoQ) "
        f"Revenue and Profit change and detail the latest quarterly Shareholding Pattern. "
        f"Provide your findings in a clear, formatted text response."
    )
    
def get_data_extraction_prompt(stock_name: str) -> str:
    """Prompt for Tab 1: Structured Data Extraction for Visualization (JSON)."""
    return (
        f"You are a data extraction specialist. For the stock '{stock_name}', find the "
        f"latest Quarterly Financials (Revenue, Net Profit) and the latest Quarterly "
        f"Shareholding Pattern (Promoter, FII, DII, Public). "
        f"Output ONLY a single JSON object with the following structure. "
        f"Use the most recent available quarter (e.g., Q1 FY26) as 'Current Quarter' "
        f"and the previous quarter (e.g., Q4 FY25) as 'Previous Quarter'.\n\n"
        f"```json\n{{\n"
        f"  \"stock_name\": \"{stock_name}\",\n"
        f"  \"financial_data\": [\n"
        f"    {{\"metric\": \"Revenue\", \"current_q_value\": <Current Q Revenue in Crores>, \"previous_q_value\": <Previous Q Revenue in Crores>}},\n"
        f"    {{\"metric\": \"Net Profit\", \"current_q_value\": <Current Q Profit in Crores>, \"previous_q_value\": <Previous Q Profit in Crores>}}\n"
        f"  ],\n"
        f"  \"shareholding_data\": [\n"
        f"    {{\"category\": \"Promoter\", \"percentage\": <Latest Promoter %>, \"change_qoq\": <Change from Previous Q %>}},\n"
        f"    {{\"category\": \"FII\", \"percentage\": <Latest FII %>,\"change_qoq\": <Change from Previous Q %>}},\n"
        f"    {{\"category\": \"DII\", \"percentage\": <Latest DII %>,\"change_qoq\": <Change from Previous Q %>}},\n"
        f"    {{\"category\": \"Public\", \"percentage\": <Latest Public %>,\"change_qoq\": <Change from Previous Q %>}}\n"
        f"  ]\n"
        f"}}\n```"
    )

def get_risk_tone_prompt(stock_name: str) -> str:
    """NEW Prompt for Tab 3: Synthesizes management tone and risk."""
    return (
        f"Act as a cynical financial risk manager. For the stock '{stock_name}', search for "
        f"recent (last 3-6 months) Management Guidance, Earnings Call Transcripts, and Analyst Reports. "
        f"Based on this, perform two tasks: "
        f"1. Summarize the **Management's Tone** (e.g., 'Cautiously Optimistic', 'Highly Aggressive') with evidence. "
        f"2. Generate a **Risk Summary** detailing the top 3-4 specific, quantifiable risks (e.g., Margin pressure due to wage inflation, US recession impacting exports, specific regulatory changes). "
        f"Do not talk about generic risks like 'market volatility'. Provide your findings in separate, clearly labeled paragraphs."
    )
    
def get_news_guidance_prompt(stock_name: str) -> str:
    """Prompt for Tab 4: General news and market guidance."""
    return (
        f"Act as a professional market reporter. Find the most recent (last 30 days) "
        f"major news headlines, analyst guidance (target price changes), and significant "
        f"developments for '{stock_name}'. Synthesize this into a detailed, easy-to-read "
        f"report for a client."
    )