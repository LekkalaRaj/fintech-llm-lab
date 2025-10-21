"""
Venture Capital data generator.
"""
from typing import Optional
import pandas as pd
from loguru import logger
from src.generators.base_generator import BaseGenerator
from src.config.prompts import VENTURE_CAPITAL_PROMPTS


class VentureCapitalGenerator(BaseGenerator):
    """Generator for venture capital datasets."""
    
    def generate(
        self,
        dataset_type: str,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate venture capital dataset."""
        
        logger.info(f"Generating {num_records} records for {dataset_type}")
        
        dataset_map = {
            "Startup Profiles": self.generate_startup_profiles,
            "Funding Rounds": self.generate_funding_rounds,
            "Cap Tables": self.generate_cap_tables,
            "Investor Syndicates": self.generate_investor_syndicates,
            "Exit Scenarios": self.generate_exit_scenarios
        }
        
        generator_func = dataset_map.get(dataset_type)
        if not generator_func:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
        
        return generator_func(num_records, start_date, end_date, **kwargs)
    
    def generate_startup_profiles(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate startup profile data."""
        
        records = self._generate_in_batches(
            VENTURE_CAPITAL_PROMPTS["startup_profiles"],
            num_records,
            batch_size=50
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="venture_capital")
        
        return df
    
    def generate_funding_rounds(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate funding round data."""
        
        records = self._generate_in_batches(
            VENTURE_CAPITAL_PROMPTS["funding_rounds"],
            num_records,
            batch_size=50
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="venture_capital")
        
        return df
    
    def generate_cap_tables(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate cap table data."""
        
        records = self._generate_in_batches(
            VENTURE_CAPITAL_PROMPTS["cap_tables"],
            num_records,
            batch_size=50
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="venture_capital")
        
        return df
    
    def generate_investor_syndicates(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate investor syndicate data."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        prompt = f"""Generate {num_records} investor syndicate records:
        
Required fields:
- deal_name: Deal/company name
- round_type: Round type (Seed, Series A, B, C, etc.)
- round_date: Date between {start_date} and {end_date}
- lead_investor: Lead investor name
- co_investors: List of co-investor names (comma-separated)
- total_investors: Total number of investors
- lead_investment_mm: Lead investor amount in millions
- total_round_mm: Total round size in millions
- lead_ownership_pct: Lead investor ownership percentage

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
        df = self.add_metadata(df, is_synthetic=True, domain="venture_capital")
        
        return df
    
    def generate_exit_scenarios(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate exit scenario data."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        prompt = f"""Generate {num_records} startup exit records:
        
Required fields:
- startup_name: Company name
- exit_date: Exit date between {start_date} and {end_date}
- exit_type: Type (IPO, Acquisition, Merger, Secondary Sale, Shutdown)
- exit_valuation_mm: Exit valuation in millions
- total_funding_mm: Total funding raised in millions
- return_multiple: Multiple on invested capital
- years_to_exit: Years from founding to exit
- acquirer_name: Acquirer name (for acquisitions)
- outcome: Outcome (Unicorn Exit, Successful, Modest, Failed)

Constraints:
- Successful exits typically 3-10 years
- Return multiples 2x to 100x for successful, <1x for failed
- IPO valuations typically $500M+

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
        df = self.add_metadata(df, is_synthetic=True, domain="venture_capital")
        
        return df