# 🏦 Synthetic Financial Dataset Generator

A production-ready, modular Python application for generating realistic synthetic financial datasets across multiple domains using Google Gemini LLM with Google Search validation and grounding.

## 📋 Table of Contents

- [Features](#features)
- [Supported Domains](#supported-domains)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Multi-Domain Support**: Capital Markets, Private Equity, Venture Capital, Banking
- **LLM-Powered Generation**: Uses Google Gemini for intelligent, context-aware data generation
- **Google Search Validation**: Cross-references generated data with real-world patterns
- **Multiple Export Formats**: CSV, JSON, XML, Parquet, Excel
- **Interactive UI**: Gradio-based web interface
- **Quality Metrics**: Comprehensive data quality analysis
- **Modular Architecture**: Easy to extend and maintain
- **Compliance-Aware**: Generates synthetic data with privacy considerations

## 🎯 Supported Domains

### 1. Capital Markets
- Securities master data (stocks, bonds, derivatives)
- Price/OHLCV historical data
- Trading volumes and market indicators
- Corporate actions (dividends, splits)

### 2. Private Equity
- Fund information and structures
- Portfolio company data
- Deal metrics (IRR, MOIC, multiples)
- Capital calls and distributions

### 3. Venture Capital
- Startup profiles and metrics
- Funding rounds (Seed to Series E)
- Cap table management
- Investor syndicate data

### 4. Banking
- Customer profiles (KYC compliant)
- CASA accounts (Current & Savings)
- Loan products and credit scores
- Transaction histories

## 🏗️ Architecture

```
┌─────────────────┐
│   Gradio UI     │
└────────┬────────┘
         │
┌────────▼────────┐
│  App Controller │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼────┐
│ LLM  │  │Search │
│Client│  │Validator│
└───┬──┘  └──┬────┘
    │        │
┌───▼────────▼───┐
│   Generators   │
│  (Domain-Specific) │
└────────┬────────┘
         │
┌────────▼────────┐
│ Data Exporter   │
└─────────────────┘
```

## 💻 Installation

### Prerequisites

- Python 3.9 or higher
- Conda (Miniconda or Anaconda)
- Google Gemini API Key
- Google Search API Key (optional, for validation)

### Step 1: Clone the Repository

```bash
git clone https://github.com/LekkalaRaj/fintech-llm-lab.git
cd synthetic-financial-data-generator
```

### Step 2: Create Conda Environment

```bash
conda env create -f environment.yml
conda activate findata-gen
```

**Or manually:**

```bash
conda create -n findata-gen python=3.9
conda activate findata-gen
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_SEARCH_API_KEY=your_search_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
LOG_LEVEL=INFO
OUTPUT_DIR=data/output
```

### Step 4: Install Package

```bash
pip install -e .
```

## ⚙️ Configuration

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

#### Google Search API (Optional)
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Custom Search API
3. Create credentials (API Key)
4. Set up a Custom Search Engine
5. Copy both API key and Search Engine ID to `.env`

### Configuration Files

- `src/config/settings.py`: Application settings
- `src/config/prompts.py`: LLM prompt templates
- `.env`: Environment variables and API keys

## 🚀 Usage

### Running the Application

```bash
python src/app.py
```

The Gradio interface will launch at `http://localhost:7860`

### Using the Web Interface

1. **Select Financial Domain**: Choose from Capital Markets, Private Equity, VC Fund, or Banking
2. **Select Dataset Type**: Based on the domain (e.g., Stock Prices, Customer Accounts)
3. **Configure Parameters**:
   - Number of records (10 - 100,000)
   - Date range
   - Additional options (include nulls, outliers, seasonality)
4. **Choose Output Format**: CSV, JSON, XML, Parquet, or Excel
5. **Click "Generate Dataset"**
6. **Review Results**:
   - Preview data in the table
   - Check quality metrics
   - View validation sources
7. **Download**: Click download button to get your dataset

### Programmatic Usage

```python
from src.generators.capital_markets import CapitalMarketsGenerator
from src.llm.gemini_client import GeminiClient
from src.utils.data_exporter import DataExporter

# Initialize
gemini = GeminiClient()
generator = CapitalMarketsGenerator(gemini)

# Generate data
df = generator.generate_stock_prices(
    num_records=1000,
    start_date="2023-01-01",
    end_date="2024-12-31"
)

# Export
exporter = DataExporter()
exporter.export(df, format="csv", filename="stock_prices.csv")
```

## 📁 Project Structure

```
synthetic-financial-data-generator/
├── src/
│   ├── __init__.py
│   ├── app.py                      # Main Gradio application
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Configuration settings
│   │   └── prompts.py             # LLM prompt templates
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── base_generator.py     # Abstract base class
│   │   ├── capital_markets.py    # Capital markets generator
│   │   ├── private_equity.py     # Private equity generator
│   │   ├── venture_capital.py    # VC generator
│   │   └── banking.py            # Banking generator
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── data_validator.py     # Data quality validation
│   │   └── search_validator.py   # Google Search validation
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_exporter.py      # Export to various formats
│   │   ├── metrics_calculator.py # Quality metrics
│   │   └── logger.py             # Logging configuration
│   └── llm/
│       ├── __init__.py
│       └── gemini_client.py      # Gemini API wrapper
├── tests/
│   ├── __init__.py
│   ├── test_generators.py
│   └── test_validators.py
├── data/
│   ├── output/                    # Generated datasets
│   └── templates/                 # Template files
├── requirements.txt               # Python dependencies
├── environment.yml                # Conda environment
├── setup.py                       # Package setup
├── README.md                      # This file
├── .env.example                   # Environment variables template
└── .gitignore
```

## 📚 API Reference

### Generators

#### BaseGenerator

Abstract base class for all domain-specific generators.

```python
class BaseGenerator(ABC):
    def __init__(self, llm_client: GeminiClient)
    
    @abstractmethod
    def generate(self, **kwargs) -> pd.DataFrame
    
    def validate(self, df: pd.DataFrame) -> dict
```

#### CapitalMarketsGenerator

```python
generator = CapitalMarketsGenerator(gemini_client)

# Generate stock prices
df = generator.generate_stock_prices(
    num_records=1000,
    start_date="2023-01-01",
    end_date="2024-12-31",
    tickers=["AAPL", "GOOGL", "MSFT"]
)

# Generate securities master
df = generator.generate_securities_master(num_records=500)
```

### Validators

#### DataValidator

```python
from src.validators.data_validator import DataValidator

validator = DataValidator()
metrics = validator.calculate_metrics(df)
issues = validator.find_issues(df)
```

#### SearchValidator

```python
from src.validators.search_validator import SearchValidator

validator = SearchValidator()
sources = validator.validate_ranges(
    domain="capital_markets",
    field="stock_price",
    values=[100, 150, 200]
)
```

### Utilities

#### DataExporter

```python
from src.utils.data_exporter import DataExporter

exporter = DataExporter()

# Export to CSV
exporter.to_csv(df, "output.csv")

# Export to JSON
exporter.to_json(df, "output.json", orient="records")

# Export to Excel with multiple sheets
exporter.to_excel(df, "output.xlsx", sheet_name="Data")
```

## 🧪 Testing

Run all tests:

```bash
pytest tests/
```

Run specific test file:

```bash
pytest tests/test_generators.py -v
```

Run with coverage:

```bash
pytest --cov=src tests/
```

## 🔧 Development

### Adding a New Domain

1. Create a new generator in `src/generators/`:

```python
# src/generators/insurance.py
from src.generators.base_generator import BaseGenerator

class InsuranceGenerator(BaseGenerator):
    def generate_policies(self, num_records: int) -> pd.DataFrame:
        # Implementation
        pass
```

2. Add prompts in `src/config/prompts.py`
3. Update `src/app.py` to include new domain in UI
4. Add tests in `tests/test_generators.py`

### Code Style

This project follows PEP 8 guidelines. Format code using:

```bash
black src/
flake8 src/
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'google.generativeai'`
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: `API key not valid`
**Solution**: Check your `.env` file and ensure GEMINI_API_KEY is set correctly

**Issue**: `Rate limit exceeded`
**Solution**: Reduce the number of records or add delays between API calls

**Issue**: `No validation sources found`
**Solution**: Check your GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID

## 📊 Performance

- **Generation Speed**: ~100-500 records/minute (depends on LLM response time)
- **Memory Usage**: ~50-100MB for 10K records
- **API Costs**: Gemini Pro is free for moderate usage (see Google AI Studio for limits)

## 🔐 Security & Privacy

- **Synthetic Data Only**: Never uses real customer data
- **API Key Security**: Store API keys in `.env`, never commit to version control
- **Compliance**: Generated data includes synthetic markers for clear identification
- **Rate Limiting**: Built-in rate limiting to prevent API abuse

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **Project**: [GitHub Repository](https://github.com/yourusername/synthetic-financial-data-generator)

## 🙏 Acknowledgments

- Google Gemini for LLM capabilities
- Gradio for the excellent UI framework
- The open-source community

---

**⚠️ Disclaimer**: This tool generates synthetic data for development and testing purposes only. Always ensure compliance with relevant regulations when using synthetic data in production environments.