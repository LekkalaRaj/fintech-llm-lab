"""
Base generator class for all domain-specific generators.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
from src.llm.gemini_client import GeminiClient
from src.config.prompts import get_prompt


class BaseGenerator(ABC):
    """Abstract base class for financial data generators."""
    
    def __init__(self, llm_client: GeminiClient):
        """
        Initialize generator.
        
        Args:
            llm_client: Gemini LLM client instance
        """
        self.llm_client = llm_client
        self.domain = self.__class__.__name__.replace("Generator", "")
        logger.info(f"Initialized {self.domain} generator")
    
    @abstractmethod
    def generate(
        self,
        dataset_type: str,
        num_records: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Generate synthetic dataset.
        
        Args:
            dataset_type: Type of dataset to generate
            num_records: Number of records
            start_date: Start date for time-series data
            end_date: End date for time-series data
            **kwargs: Additional parameters
        
        Returns:
            Generated dataset as DataFrame
        """
        pass
    
    def _generate_in_batches(
        self,
        prompt_template: str,
        total_records: int,
        batch_size: int = 100,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Generate data in batches to handle large datasets.
        
        Args:
            prompt_template: Prompt template
            total_records: Total records to generate
            batch_size: Records per batch
            **kwargs: Variables for prompt
        
        Returns:
            List of generated records
        """
        all_records = []
        batches = (total_records + batch_size - 1) // batch_size
        
        logger.info(f"Generating {total_records} records in {batches} batches")
        
        for i in range(batches):
            records_in_batch = min(batch_size, total_records - len(all_records))
            logger.info(f"Generating batch {i + 1}/{batches} ({records_in_batch} records)")
            
            try:
                # Generate prompt with current batch size
                batch_kwargs = {**kwargs, 'num_records': records_in_batch}
                prompt = prompt_template.format(**batch_kwargs)
                
                # Generate data
                batch_data = self.llm_client.generate_json(prompt)
                
                if batch_data:
                    all_records.extend(batch_data)
                    logger.debug(f"Batch {i + 1} generated {len(batch_data)} records")
                else:
                    logger.warning(f"Batch {i + 1} returned no data")
                    
            except Exception as e:
                logger.error(f"Error generating batch {i + 1}: {str(e)}")
                # Continue with other batches
                continue
        
        logger.info(f"Total records generated: {len(all_records)}")
        return all_records
    
    def _validate_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate and clean generated records.
        
        Args:
            records: List of generated records
        
        Returns:
            Validated and cleaned records
        """
        if not records:
            return []
        
        # Remove any records with missing required fields
        valid_records = []
        required_fields = set(records[0].keys()) if records else set()
        
        for record in records:
            if all(key in record for key in required_fields):
                valid_records.append(record)
            else:
                logger.warning(f"Skipping invalid record: {record}")
        
        logger.info(f"Validated {len(valid_records)}/{len(records)} records")
        return valid_records
    
    def _to_dataframe(self, records: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert records to DataFrame with type inference.
        
        Args:
            records: List of records
        
        Returns:
            DataFrame
        """
        if not records:
            logger.warning("No records to convert to DataFrame")
            return pd.DataFrame()
        
        df = pd.DataFrame(records)
        
        # Infer and convert date columns
        for col in df.columns:
            if 'date' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except Exception as e:
                    logger.debug(f"Could not convert {col} to datetime: {str(e)}")
        
        logger.info(f"Created DataFrame with shape {df.shape}")
        return df
    
    def get_date_range(
        self, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> tuple:
        """
        Get or generate date range.
        
        Args:
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)
        
        Returns:
            Tuple of (start_date, end_date) as strings
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        return start_date, end_date
    
    def add_metadata(self, df: pd.DataFrame, **metadata) -> pd.DataFrame:
        """
        Add metadata columns to DataFrame.
        
        Args:
            df: DataFrame
            **metadata: Metadata key-value pairs
        
        Returns:
            DataFrame with metadata
        """
        for key, value in metadata.items():
            df[f"_meta_{key}"] = value
        
        df["_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df["_generator"] = self.domain
        
        return df