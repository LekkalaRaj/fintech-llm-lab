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
conda activate synthetic-financial-data-generator
```

**Or manually:**

```bash
conda create -n synthetic-financial-data-generator python=3.9
conda activate synthetic-financial-data-generator
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

## 📊 Performance

- **Generation Speed**: ~100-500 records/minute (depends on LLM response time)
- **Memory Usage**: ~50-100MB for 10K records
- **API Costs**: Gemini Pro is free for moderate usage (see Google AI Studio for limits)

## 🔐 Security & Privacy

- **Synthetic Data Only**: Never uses real customer data
- **API Key Security**: Store API keys in `.env`, never commit to version control
- **Compliance**: Generated data includes synthetic markers for clear identification
- **Rate Limiting**: Built-in rate limiting to prevent API abuse

**⚠️ Disclaimer**: This tool generates synthetic data for development and testing purposes only. Always ensure compliance with relevant regulations when using synthetic data in production environments.