"""
Data export utilities for multiple formats.
"""
from pathlib import Path
from typing import Optional
import pandas as pd
from loguru import logger
from src.config.settings import settings


class DataExporter:
    """Export datasets to various formats."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize exporter.
        
        Args:
            output_dir: Output directory (uses settings default if None)
        """
        self.output_dir = output_dir or settings.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"DataExporter initialized with output dir: {self.output_dir}")
    
    def export(
        self,
        df: pd.DataFrame,
        filename: str,
        format_type: str,
        **kwargs
    ) -> Path:
        """
        Export DataFrame to specified format.
        
        Args:
            df: DataFrame to export
            filename: Base filename (without extension)
            format_type: Export format (CSV, JSON, XML, Parquet, Excel)
            **kwargs: Format-specific options
        
        Returns:
            Path to exported file
        """
        format_type = format_type.upper()
        
        export_map = {
            "CSV": self.to_csv,
            "JSON": self.to_json,
            "XML": self.to_xml,
            "PARQUET": self.to_parquet,
            "EXCEL": self.to_excel
        }
        
        export_func = export_map.get(format_type)
        if not export_func:
            raise ValueError(f"Unsupported format: {format_type}")
        
        logger.info(f"Exporting {len(df)} records to {format_type}")
        return export_func(df, filename, **kwargs)
    
    def to_csv(
        self,
        df: pd.DataFrame,
        filename: str,
        **kwargs
    ) -> Path:
        """Export to CSV format."""
        filepath = self.output_dir / f"{filename}.csv"
        
        df.to_csv(
            filepath,
            index=kwargs.get('index', False),
            encoding=kwargs.get('encoding', 'utf-8')
        )
        
        logger.info(f"Exported CSV: {filepath}")
        return filepath
    
    def to_json(
        self,
        df: pd.DataFrame,
        filename: str,
        **kwargs
    ) -> Path:
        """Export to JSON format."""
        filepath = self.output_dir / f"{filename}.json"
        
        df.to_json(
            filepath,
            orient=kwargs.get('orient', 'records'),
            indent=kwargs.get('indent', 2),
            date_format=kwargs.get('date_format', 'iso')
        )
        
        logger.info(f"Exported JSON: {filepath}")
        return filepath
    
    def to_xml(
        self,
        df: pd.DataFrame,
        filename: str,
        **kwargs
    ) -> Path:
        """Export to XML format."""
        filepath = self.output_dir / f"{filename}.xml"
        
        df.to_xml(
            filepath,
            index=kwargs.get('index', False),
            root_name=kwargs.get('root_name', 'data'),
            row_name=kwargs.get('row_name', 'record')
        )
        
        logger.info(f"Exported XML: {filepath}")
        return filepath
    
    def to_parquet(
        self,
        df: pd.DataFrame,
        filename: str,
        **kwargs
    ) -> Path:
        """Export to Parquet format."""
        filepath = self.output_dir / f"{filename}.parquet"
        
        df.to_parquet(
            filepath,
            engine=kwargs.get('engine', 'pyarrow'),
            compression=kwargs.get('compression', 'snappy'),
            index=kwargs.get('index', False)
        )
        
        logger.info(f"Exported Parquet: {filepath}")
        return filepath
    
    def to_excel(
        self,
        df: pd.DataFrame,
        filename: str,
        **kwargs
    ) -> Path:
        """Export to Excel format."""
        filepath = self.output_dir / f"{filename}.xlsx"
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(
                writer,
                sheet_name=kwargs.get('sheet_name', 'Data'),
                index=kwargs.get('index', False)
            )
            
            # Add data dictionary sheet if requested
            if kwargs.get('include_dictionary', True):
                data_dict = self._create_data_dictionary(df)
                data_dict.to_excel(
                    writer,
                    sheet_name='Data Dictionary',
                    index=False
                )
        
        logger.info(f"Exported Excel: {filepath}")
        return filepath
    
    def _create_data_dictionary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create data dictionary for DataFrame.
        
        Args:
            df: DataFrame
        
        Returns:
            Data dictionary DataFrame
        """
        dictionary = []
        
        for col in df.columns:
            col_data = {
                'Column Name': col,
                'Data Type': str(df[col].dtype),
                'Non-Null Count': df[col].count(),
                'Null Count': df[col].isnull().sum(),
                'Unique Values': df[col].nunique(),
                'Sample Values': ', '.join(map(str, df[col].dropna().head(3).tolist()))
            }
            dictionary.append(col_data)
        
        return pd.DataFrame(dictionary)
    
    def export_with_metadata(
        self,
        df: pd.DataFrame,
        filename: str,
        format_type: str,
        metadata: dict,
        **kwargs
    ) -> Path:
        """
        Export with metadata file.
        
        Args:
            df: DataFrame to export
            filename: Base filename
            format_type: Export format
            metadata: Metadata dictionary
            **kwargs: Format-specific options
        
        Returns:
            Path to exported file
        """
        # Export main data
        filepath = self.export(df, filename, format_type, **kwargs)
        
        # Export metadata
        metadata_path = self.output_dir / f"{filename}_metadata.json"
        pd.Series(metadata).to_json(metadata_path, indent=2)
        
        logger.info(f"Exported metadata: {metadata_path}")
        return filepath