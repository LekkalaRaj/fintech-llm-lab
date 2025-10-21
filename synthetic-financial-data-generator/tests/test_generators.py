"""
Unit tests for data generators.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock
from src.generators.capital_markets import CapitalMarketsGenerator
from src.generators.banking import BankingGenerator
from src.llm.gemini_client import GeminiClient


@pytest.fixture
def mock_llm_client():
    """Mock LLM client for testing."""
    client = Mock(spec=GeminiClient)
    client.generate_json.return_value = [
        {
            "ticker": "AAPL",
            "date": "2024-01-01",
            "open": 150.0,
            "high": 155.0,
            "low": 149.0,
            "close": 154.0,
            "volume": 1000000,
            "adj_close": 154.0
        }
    ]
    return client


class TestCapitalMarketsGenerator:
    """Test Capital Markets generator."""
    
    def test_generate_stock_prices(self, mock_llm_client):
        """Test stock price generation."""
        generator = CapitalMarketsGenerator(mock_llm_client)
        
        df = generator.generate_stock_prices(
            num_records=10,
            start_date="2024-01-01",
            end_date="2024-12-31"
        )
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'ticker' in df.columns
        assert '_generated_at' in df.columns
    
    def test_generate_securities_master(self, mock_llm_client):
        """Test securities master generation."""
        mock_llm_client.generate_json.return_value = [
            {
                "ticker": "AAPL",
                "isin": "US0378331005",
                "company_name": "Apple Inc.",
                "sector": "Technology",
                "market_cap": 3000.0,
                "country": "USA",
                "currency": "USD",
                "exchange": "NASDAQ",
                "listing_date": "1980-12-12"
            }
        ]
        
        generator = CapitalMarketsGenerator(mock_llm_client)
        df = generator.generate_securities_master(num_records=5)
        
        assert isinstance(df, pd.DataFrame)
        assert 'ticker' in df.columns
        assert 'isin' in df.columns


class TestBankingGenerator:
    """Test Banking generator."""
    
    def test_generate_customer_profiles(self, mock_llm_client):
        """Test customer profile generation."""
        mock_llm_client.generate_json.return_value = [
            {
                "customer_id": "CUST0000000001",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-01",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "address": "123 Main St",
                "city": "New York",
                "country": "USA",
                "customer_since": "2020-01-01",
                "customer_segment": "Mass Market",
                "kyc_status": "Verified",
                "risk_rating": "Low"
            }
        ]
        
        generator = BankingGenerator(mock_llm_client)
        df = generator.generate_customer_profiles(num_records=5)
        
        assert isinstance(df, pd.DataFrame)
        assert 'customer_id' in df.columns
        assert '_meta_pii_removed' in df.columns


class TestBaseGenerator:
    """Test base generator functionality."""
    
    def test_validate_records(self, mock_llm_client):
        """Test record validation."""
        generator = CapitalMarketsGenerator(mock_llm_client)
        
        records = [
            {"ticker": "AAPL", "price": 150.0},
            {"ticker": "GOOGL"},  # Missing price
            {"ticker": "MSFT", "price": 300.0}
        ]
        
        validated = generator._validate_records(records)
        assert len(validated) == 3  # All records have ticker
    
    def test_to_dataframe(self, mock_llm_client):
        """Test DataFrame conversion."""
        generator = CapitalMarketsGenerator(mock_llm_client)
        
        records = [
            {"ticker": "AAPL", "date": "2024-01-01", "price": 150.0},
            {"ticker": "GOOGL", "date": "2024-01-02", "price": 140.0}
        ]
        
        df = generator._to_dataframe(records)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert pd.api.types.is_datetime64_any_dtype(df['date'])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])