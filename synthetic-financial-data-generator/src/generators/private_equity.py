"""
Private Equity data generator.
"""
from typing import Optional
import pandas as pd
from loguru import logger
from src.generators.base_generator import BaseGenerator
from src.config.prompts import PRIVATE_EQUITY_PROMPTS


class PrivateEquityGenerator(BaseGenerator):
    """Generator for private equity datasets."""
    
    def generate(
        self,
        dataset_type: str,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate private equity dataset."""
        
        logger.info(f"Generating {num_records} records for {dataset_type}")
        
        dataset_map = {
            "Fund Information": self.generate_fund_information,
            "Portfolio Companies": self.generate_portfolio_companies,
            "Deal Metrics": self.generate_deal_metrics,
            "Capital Calls & Distributions": self.generate_capital_flows,
            "Valuations": self.generate_valuations
        }
        
        generator_func = dataset_map.get(dataset_type)
        if not generator_func:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
        
        return generator_func(num_records, start_date, end_date, **kwargs)
    
    def generate_fund_information(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate private equity fund information."""
        
        records = self._generate_in_batches(
            PRIVATE_EQUITY_PROMPTS["fund_information"],
            num_records,
            batch_size=50
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="private_equity")
        
        return df
    
    def generate_portfolio_companies(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate portfolio company investment records."""
        
        records = self._generate_in_batches(
            PRIVATE_EQUITY_PROMPTS["portfolio_companies"],
            num_records,
            batch_size=50
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="private_equity")
        
        return df
    
    def generate_deal_metrics(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate deal performance metrics."""
        
        records = self._generate_in_batches(
            PRIVATE_EQUITY_PROMPTS["deal_metrics"],
            num_records,
            batch_size=50
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="private_equity")
        
        return df
    
    def generate_capital_flows(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate capital calls and distributions."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        prompt = f"""Generate {num_records} capital call and distribution records:
        
Required fields:
- fund_name: Fund name
- transaction_type: Type (Capital Call, Distribution)
- transaction_date: Date between {start_date} and {end_date}
- amount_mm: Amount in millions
- investor_name: Investor name
- percentage_of_commitment: Percentage of total commitment
- cumulative_called_pct: Cumulative capital called percentage
- cumulative_distributed_pct: Cumulative distributions percentage

Return as JSON array of objects."""
        
        records = self._generate_in_batches(
            prompt,
            num_records,
            batch_size=50,
            start_date=start_date,
            end_date=end_date
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="private_equity")
        
        return df
    
    def generate_valuations(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate portfolio company valuations."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        prompt = f"""Generate {num_records} portfolio company valuation records:
        
Required fields:
- company_name: Portfolio company name
- valuation_date: Valuation date between {start_date} and {end_date}
- enterprise_value_mm: Enterprise value in millions
- equity_value_mm: Equity value in millions
- ebitda_mm: EBITDA in millions
- revenue_mm: Revenue in millions
- ev_ebitda_multiple: EV/EBITDA multiple
- ev_revenue_multiple: EV/Revenue multiple
- net_debt_mm: Net debt in millions
- valuation_method: Method (DCF, Comparable Companies, Precedent Transactions)

Constraints:
- EV/EBITDA typically 8x to 15x
- EV/Revenue typically 1x to 5x
- Enterprise Value = Equity Value + Net Debt

Return as JSON array of objects."""
        
        records = self._generate_in_batches(
            prompt,
            num_records,
            batch_size=50,
            start_date=start_date,
            end_date=end_date
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="private_equity")
        
        return df