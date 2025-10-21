"""
Capital Markets data generator.
"""
from typing import Optional
import pandas as pd
from loguru import logger
from src.generators.base_generator import BaseGenerator
from src.config.prompts import CAPITAL_MARKETS_PROMPTS


class CapitalMarketsGenerator(BaseGenerator):
    """Generator for capital markets datasets."""
    
    def generate(
        self,
        dataset_type: str,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate capital markets dataset."""
        
        logger.info(f"Generating {num_records} records for {dataset_type}")
        
        # Map dataset type to generation method
        dataset_map = {
            "Stock Prices (OHLCV)": self.generate_stock_prices,
            "Securities Master Data": self.generate_securities_master,
            "Trading Volumes": self.generate_trading_volumes,
            "Corporate Actions": self.generate_corporate_actions,
            "Market Indices": self.generate_market_indices
        }
        
        generator_func = dataset_map.get(dataset_type)
        if not generator_func:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
        
        return generator_func(num_records, start_date, end_date, **kwargs)
    
    def generate_stock_prices(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate stock price OHLCV data."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        records = self._generate_in_batches(
            CAPITAL_MARKETS_PROMPTS["stock_prices"],
            num_records,
            batch_size=100,
            start_date=start_date,
            end_date=end_date
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        
        # Add synthetic data marker
        df = self.add_metadata(df, is_synthetic=True, domain="capital_markets")
        
        return df
    
    def generate_securities_master(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate securities master data."""
        
        records = self._generate_in_batches(
            CAPITAL_MARKETS_PROMPTS["securities_master"],
            num_records,
            batch_size=50
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="capital_markets")
        
        return df
    
    def generate_trading_volumes(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate trading volume data."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        prompt = f"""Generate {num_records} trading volume records:
        
Required fields:
- ticker: Stock ticker
- date: Trading date between {start_date} and {end_date}
- volume: Total trading volume
- trade_count: Number of trades
- vwap: Volume weighted average price
- market_cap_mm: Market cap in millions

Return as JSON array of objects."""
        
        records = self._generate_in_batches(
            prompt,
            num_records,
            batch_size=100,
            start_date=start_date,
            end_date=end_date
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="capital_markets")
        
        return df
    
    def generate_corporate_actions(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate corporate actions data."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        records = self._generate_in_batches(
            CAPITAL_MARKETS_PROMPTS["corporate_actions"],
            num_records,
            batch_size=50,
            start_date=start_date,
            end_date=end_date
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="capital_markets")
        
        return df
    
    def generate_market_indices(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate market indices data."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        prompt = f"""Generate {num_records} market index records:
        
Required fields:
- index_name: Index name (S&P 500, NASDAQ, FTSE 100, etc.)
- date: Date between {start_date} and {end_date}
- value: Index value
- change: Daily change
- change_pct: Daily change percentage
- volume: Total market volume
- market_cap_trillion: Total market cap in trillions

Return as JSON array of objects."""
        
        records = self._generate_in_batches(
            prompt,
            num_records,
            batch_size=100,
            start_date=start_date,
            end_date=end_date
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="capital_markets")
        
        return df