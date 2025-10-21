"""
LLM prompt templates for different financial domains and datasets.
"""

# Base system prompt
SYSTEM_PROMPT = """You are an expert financial data engineer specializing in generating realistic, 
compliant synthetic datasets for various financial domains. Your generated data must:

1. Follow industry standards and regulations
2. Maintain statistical validity and realistic distributions
3. Include appropriate correlations between fields
4. Be completely synthetic (no real customer data)
5. Follow the specified schema exactly
6. Return data in valid JSON format

Always ensure data quality, consistency, and compliance."""

# Capital Markets Prompts
CAPITAL_MARKETS_PROMPTS = {
    "stock_prices": """Generate {num_records} realistic stock price records (OHLCV data) with the following specifications:

Required fields:
- ticker: Stock ticker symbol (e.g., AAPL, GOOGL, MSFT)
- date: Trading date in YYYY-MM-DD format between {start_date} and {end_date}
- open: Opening price (reasonable range based on stock)
- high: Highest price (must be >= open and close)
- low: Lowest price (must be <= open and close)
- close: Closing price
- volume: Trading volume (realistic for stock size)
- adj_close: Adjusted closing price

Constraints:
- Prices should show realistic market movements (not random)
- Volume should correlate with price volatility
- Include some uptrends, downtrends, and consolidation periods
- High >= max(open, close) and Low <= min(open, close)

Return as JSON array of objects.""",

    "securities_master": """Generate {num_records} securities master data records:

Required fields:
- ticker: Unique ticker symbol
- isin: International Securities Identification Number (valid format)
- company_name: Realistic company name
- sector: Industry sector (Technology, Healthcare, Finance, Energy, Consumer, Industrial, etc.)
- market_cap: Market capitalization in billions (realistic distribution)
- country: Country of incorporation
- currency: Trading currency (USD, EUR, GBP, etc.)
- exchange: Stock exchange (NYSE, NASDAQ, LSE, etc.)
- listing_date: Date listed on exchange

Constraints:
- Ticker should be 1-5 uppercase letters
- ISIN format: 2-letter country code + 9 alphanumeric + 1 check digit
- Market cap distribution: many small-cap, fewer mid-cap, rare large-cap
- Sector distribution should be realistic

Return as JSON array of objects.""",

    "corporate_actions": """Generate {num_records} corporate action records:

Required fields:
- ticker: Stock ticker
- action_type: Type (Dividend, Stock Split, Merger, Acquisition, Spin-off)
- announcement_date: When announced
- effective_date: When effective
- value: Relevant value (dividend amount, split ratio, acquisition price)
- status: Status (Announced, Completed, Cancelled)

Constraints:
- Effective date should be after announcement date
- Dividend values typically $0.10 to $5.00 per share
- Split ratios like 2:1, 3:1, 3:2
- Actions should align with realistic corporate behavior

Return as JSON array of objects."""
}

# Private Equity Prompts
PRIVATE_EQUITY_PROMPTS = {
    "fund_information": """Generate {num_records} private equity fund records:

Required fields:
- fund_name: Fund name (e.g., "ABC Capital Fund III")
- vintage_year: Year fund was established
- fund_size_mm: Fund size in millions USD
- strategy: Strategy (Buyout, Growth, Distressed, Secondary, etc.)
- geography: Geographic focus (North America, Europe, Asia, Global)
- target_irr: Target IRR percentage
- management_fee: Management fee percentage (typically 1.5-2.5%)
- carried_interest: Carried interest percentage (typically 20%)
- gp_name: General Partner name
- fund_term_years: Fund term in years (typically 10-12)

Constraints:
- Vintage year between 2010 and 2024
- Fund size realistic for strategy (Buyout largest, Growth/Venture smaller)
- Target IRR typically 15-30%
- Larger funds typically have lower fee percentages

Return as JSON array of objects.""",

    "portfolio_companies": """Generate {num_records} portfolio company investment records:

Required fields:
- company_name: Portfolio company name
- fund_name: Investing fund
- sector: Industry sector
- investment_date: Date of investment
- entry_valuation_mm: Entry valuation in millions
- ownership_pct: Ownership percentage acquired
- investment_amount_mm: Investment amount in millions
- ebitda_at_entry_mm: EBITDA at entry in millions
- entry_multiple: Entry EV/EBITDA multiple
- status: Investment status (Active, Exited, Written-off)

Constraints:
- Investment date after fund vintage year
- Ownership typically 20% to 100% for PE
- Entry multiples typically 6x to 15x EBITDA
- Investment amount = ownership% * entry valuation

Return as JSON array of objects.""",

    "deal_metrics": """Generate {num_records} private equity deal performance records:

Required fields:
- deal_id: Unique deal identifier
- company_name: Company name
- entry_date: Investment date
- exit_date: Exit date (null if still active)
- hold_period_years: Years held
- entry_ev_mm: Entry enterprise value in millions
- exit_ev_mm: Exit enterprise value in millions (null if active)
- moic: Multiple on Invested Capital
- irr_pct: Internal Rate of Return percentage
- exit_type: Exit type (IPO, Strategic Sale, Secondary Sale, Still Held)

Constraints:
- Exit date after entry date if exited
- Hold period typically 3-7 years
- MOIC typically 1.5x to 5.0x
- IRR typically 15% to 40% for successful deals
- MOIC and IRR should be mathematically consistent

Return as JSON array of objects."""
}

# Venture Capital Prompts
VENTURE_CAPITAL_PROMPTS = {
    "startup_profiles": """Generate {num_records} startup profile records:

Required fields:
- startup_name: Company name
- founded_year: Year founded
- sector: Sector (SaaS, FinTech, HealthTech, E-commerce, AI/ML, etc.)
- stage: Current stage (Pre-seed, Seed, Series A, B, C, D, E)
- geography: Location (Silicon Valley, NYC, London, Berlin, Singapore, etc.)
- employee_count: Number of employees
- total_funding_mm: Total funding raised in millions
- valuation_mm: Current valuation in millions
- revenue_mm: Annual revenue in millions (null if pre-revenue)
- growth_rate_pct: YoY revenue growth percentage

Constraints:
- Founded year between 2015 and 2024
- Employee count should correlate with stage and funding
- Later stages have higher valuations and funding
- Growth rates typically 50% to 300% for early stage

Return as JSON array of objects.""",

    "funding_rounds": """Generate {num_records} funding round records:

Required fields:
- startup_name: Company receiving funding
- round_type: Round type (Pre-seed, Seed, Series A, B, C, D, E)
- round_date: Date of funding round
- amount_mm: Amount raised in millions
- valuation_mm: Post-money valuation in millions
- lead_investor: Lead investor name
- investor_count: Number of participating investors
- equity_sold_pct: Percentage of equity sold
- use_of_funds: Primary use (Product Development, Sales & Marketing, Hiring, Expansion)

Constraints:
- Round amounts and valuations should increase with stage
- Seed: $0.5-3M, Series A: $2-15M, B: $10-50M, C+: $25M+
- Equity sold typically 15-25% per round
- Amount = equity_sold% * valuation

Return as JSON array of objects.""",

    "cap_tables": """Generate {num_records} cap table snapshot records:

Required fields:
- startup_name: Company name
- as_of_date: Snapshot date
- investor_name: Investor or founder name
- investor_type: Type (Founder, Angel, VC, Corporate, Employee)
- shares_held: Number of shares held
- ownership_pct: Ownership percentage
- share_class: Share class (Common, Preferred A, B, C, etc.)
- fully_diluted: Fully diluted ownership percentage

Constraints:
- Total ownership should sum to 100% per company/date
- Founders typically 40-70% at seed, diluting over time
- VCs get Preferred shares, employees get Common
- Later round investors have later Preferred series

Return as JSON array of objects."""
}

# Banking Prompts
BANKING_PROMPTS = {
    "customer_profiles": """Generate {num_records} bank customer profile records:

Required fields:
- customer_id: Unique customer identifier
- first_name: First name
- last_name: Last name
- date_of_birth: Date of birth (age 18-85)
- email: Email address
- phone: Phone number
- address: Street address
- city: City
- country: Country
- customer_since: Account opening date
- customer_segment: Segment (Mass Market, Affluent, High Net Worth, Business)
- kyc_status: KYC status (Verified, Pending, Expired)
- risk_rating: Risk rating (Low, Medium, High)

Constraints:
- Customer_id format: CUST followed by 10 digits
- Age between 18 and 85
- Customer_since within last 20 years
- Segment distribution: 70% Mass, 20% Affluent, 8% HNW, 2% Business
- 95% should have Verified KYC status

Return as JSON array of objects.""",

    "casa_accounts": """Generate {num_records} CASA (Current Account Savings Account) records:

Required fields:
- account_number: Unique account number
- customer_id: Customer identifier
- account_type: Type (Savings, Current, Salary, Fixed Deposit)
- opening_date: Account opening date
- currency: Currency (USD, EUR, GBP, SGD, etc.)
- balance: Current balance
- interest_rate: Annual interest rate percentage
- status: Account status (Active, Dormant, Closed)
- branch_code: Branch code
- last_transaction_date: Last transaction date

Constraints:
- Account number format: 4 digit branch + 10 digit account
- Balance distribution: most accounts $100-$50K, some higher
- Savings accounts: 0.5-3% interest
- Current accounts: 0% interest
- 90% Active, 8% Dormant, 2% Closed

Return as JSON array of objects.""",

    "loan_products": """Generate {num_records} loan product records:

Required fields:
- loan_id: Unique loan identifier
- customer_id: Customer identifier
- loan_type: Type (Personal, Home, Auto, Education, Business)
- loan_amount: Loan principal amount
- interest_rate: Annual interest rate percentage
- tenure_months: Loan tenure in months
- emi: Monthly EMI amount
- disbursement_date: Loan disbursement date
- outstanding_balance: Current outstanding balance
- status: Loan status (Active, Paid, Defaulted, Written-off)
- credit_score: Credit score at origination (300-850)
- ltv_ratio: Loan to value ratio for secured loans

Constraints:
- Personal: $1K-$50K, 12-60 months, 8-18% interest
- Home: $50K-$1M, 120-360 months, 3-7% interest
- Auto: $5K-$100K, 24-84 months, 4-10% interest
- EMI calculation should be accurate
- 92% Active, 5% Paid, 2% Defaulted, 1% Written-off

Return as JSON array of objects.""",

    "transactions": """Generate {num_records} bank transaction records:

Required fields:
- transaction_id: Unique transaction identifier
- account_number: Account number
- transaction_date: Date and time of transaction
- transaction_type: Type (Debit, Credit)
- category: Category (ATM Withdrawal, Online Transfer, POS Purchase, Salary Credit, Bill Payment, etc.)
- amount: Transaction amount
- balance_after: Account balance after transaction
- description: Transaction description
- merchant_name: Merchant name (for purchases)
- status: Status (Completed, Pending, Failed)

Constraints:
- Multiple transactions per account over time period
- Balance should be mathematically consistent
- Common patterns: salary on month-end, regular bills, varied shopping
- 95% Completed, 4% Pending, 1% Failed
- Amounts realistic for category (ATM: $20-$500, Salary: $2K-$10K)

Return as JSON array of objects."""
}

def get_prompt(domain: str, dataset_type: str, **kwargs) -> str:
    """
    Get the appropriate prompt template for a domain and dataset type.
    
    Args:
        domain: Financial domain
        dataset_type: Type of dataset
        **kwargs: Variables to inject into prompt
    
    Returns:
        Formatted prompt string
    """
    domain_key = domain.lower().replace(" ", "_")
    dataset_key = dataset_type.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    
    prompt_map = {
        "capital_markets": CAPITAL_MARKETS_PROMPTS,
        "private_equity": PRIVATE_EQUITY_PROMPTS,
        "venture_capital": VENTURE_CAPITAL_PROMPTS,
        "banking": BANKING_PROMPTS
    }
    
    prompts = prompt_map.get(domain_key, {})
    
    # Find matching prompt key
    for key in prompts.keys():
        if key in dataset_key or dataset_key in key:
            template = prompts[key]
            return template.format(**kwargs)
    
    # Default generic prompt if no match
    return f"""Generate {kwargs.get('num_records', 100)} realistic {dataset_type} records for the {domain} domain.
    
    Return data as a JSON array of objects with appropriate fields for this dataset type.
    Ensure data is realistic, follows industry standards, and maintains consistency."""