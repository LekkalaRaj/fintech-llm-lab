"""
Configuration settings for the Synthetic Financial Dataset Generator.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    from pydantic import BaseSettings, Field

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash", env="GEMINI_MODEL")
    google_search_api_key: str = Field(default="", env="GOOGLE_SEARCH_API_KEY")
    google_search_engine_id: str = Field(default="", env="GOOGLE_SEARCH_ENGINE_ID")
    
    # Application Settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    output_dir: Path = Field(default=Path("data/output"), env="OUTPUT_DIR")
    max_records: int = Field(default=100000, env="MAX_RECORDS")
    default_records: int = Field(default=1000, env="DEFAULT_RECORDS")
    
    # Rate Limiting
    gemini_requests_per_minute: int = Field(default=60, env="GEMINI_REQUESTS_PER_MINUTE")
    search_requests_per_day: int = Field(default=100, env="SEARCH_REQUESTS_PER_DAY")
    
    # Data Generation Settings
    include_nulls: bool = Field(default=False, env="INCLUDE_NULLS")
    include_outliers: bool = Field(default=True, env="INCLUDE_OUTLIERS")
    apply_seasonality: bool = Field(default=True, env="APPLY_SEASONALITY")
    
    # UI Configuration
    gradio_server_name: str = Field(default="0.0.0.0", env="GRADIO_SERVER_NAME")
    gradio_server_port: int = Field(default=7860, env="GRADIO_SERVER_PORT")
    gradio_share: bool = Field(default=False, env="GRADIO_SHARE")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate_api_keys(self) -> bool:
        """Validate that required API keys are present."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required. Please set it in .env file")
        return True
    
    def create_output_dir(self):
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Domain configurations
DOMAINS = {
    "Capital Markets": {
        "datasets": [
            "Stock Prices (OHLCV)",
            "Securities Master Data",
            "Trading Volumes",
            "Corporate Actions",
            "Market Indices"
        ],
        "description": "Generate capital markets data including stocks, bonds, and derivatives"
    },
    "Private Equity": {
        "datasets": [
            "Fund Information",
            "Portfolio Companies",
            "Deal Metrics",
            "Capital Calls & Distributions",
            "Valuations"
        ],
        "description": "Generate private equity fund and investment data"
    },
    "Venture Capital": {
        "datasets": [
            "Startup Profiles",
            "Funding Rounds",
            "Cap Tables",
            "Investor Syndicates",
            "Exit Scenarios"
        ],
        "description": "Generate venture capital and startup ecosystem data"
    },
    "Banking": {
        "datasets": [
            "Customer Profiles",
            "CASA Accounts",
            "Loan Products",
            "Transactions",
            "Credit Scores"
        ],
        "description": "Generate banking and retail finance data"
    }
}

# Export format configurations
EXPORT_FORMATS = {
    "CSV": {"extension": ".csv", "description": "Comma-separated values"},
    "JSON": {"extension": ".json", "description": "JavaScript Object Notation"},
    "XML": {"extension": ".xml", "description": "Extensible Markup Language"},
    "Parquet": {"extension": ".parquet", "description": "Apache Parquet columnar format"},
    "Excel": {"extension": ".xlsx", "description": "Microsoft Excel format"}
}

# Data quality thresholds
QUALITY_THRESHOLDS = {
    "completeness": 0.95,  # 95% non-null values
    "uniqueness": 0.90,    # 90% unique where expected
    "validity": 0.98,      # 98% within valid ranges
    "consistency": 0.99    # 99% referential integrity
}