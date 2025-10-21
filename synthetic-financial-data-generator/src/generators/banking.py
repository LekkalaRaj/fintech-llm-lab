"""
Banking data generator.
"""
from typing import Optional
import pandas as pd
from loguru import logger
from src.generators.base_generator import BaseGenerator
from src.config.prompts import BANKING_PROMPTS


class BankingGenerator(BaseGenerator):
    """Generator for banking datasets."""
    
    def generate(
        self,
        dataset_type: str,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate banking dataset."""
        
        logger.info(f"Generating {num_records} records for {dataset_type}")
        
        dataset_map = {
            "Customer Profiles": self.generate_customer_profiles,
            "CASA Accounts": self.generate_casa_accounts,
            "Loan Products": self.generate_loan_products,
            "Transactions": self.generate_transactions,
            "Credit Scores": self.generate_credit_scores
        }
        
        generator_func = dataset_map.get(dataset_type)
        if not generator_func:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
        
        return generator_func(num_records, start_date, end_date, **kwargs)
    
    def generate_customer_profiles(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate customer profile data."""
        
        records = self._generate_in_batches(
            BANKING_PROMPTS["customer_profiles"],
            num_records,
            batch_size=100
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="banking", pii_removed=True)
        
        return df
    
    def generate_casa_accounts(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate CASA account data."""
        
        records = self._generate_in_batches(
            BANKING_PROMPTS["casa_accounts"],
            num_records,
            batch_size=100
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="banking")
        
        return df
    
    def generate_loan_products(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate loan products data."""
        
        records = self._generate_in_batches(
            BANKING_PROMPTS["loan_products"],
            num_records,
            batch_size=100
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="banking")
        
        return df
    
    def generate_transactions(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate transaction data."""
        
        start_date, end_date = self.get_date_range(start_date, end_date)
        
        records = self._generate_in_batches(
            BANKING_PROMPTS["transactions"],
            num_records,
            batch_size=100,
            start_date=start_date,
            end_date=end_date
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="banking")
        
        return df
    
    def generate_credit_scores(
        self,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Generate credit score data."""
        
        prompt = f"""Generate {num_records} credit score records:
        
Required fields:
- customer_id: Customer identifier
- score_date: Date of score calculation
- credit_score: Score (300-850)
- score_model: Model used (FICO, VantageScore, Custom)
- payment_history: Payment history score (0-100)
- credit_utilization_pct: Credit utilization percentage
- credit_age_months: Age of oldest account in months
- total_accounts: Total number of accounts
- recent_inquiries: Hard inquiries in last 12 months
- derogatory_marks: Number of derogatory marks
- risk_category: Category (Excellent, Good, Fair, Poor)

Constraints:
- Excellent: 750-850
- Good: 700-749
- Fair: 650-699
- Poor: 300-649
- Utilization typically 0-100%
- Age 1-360 months

Return as JSON array of objects."""
        
        records = self._generate_in_batches(
            prompt,
            num_records,
            batch_size=100
        )
        
        records = self._validate_records(records)
        df = self._to_dataframe(records)
        df = self.add_metadata(df, is_synthetic=True, domain="banking")
        
        return df