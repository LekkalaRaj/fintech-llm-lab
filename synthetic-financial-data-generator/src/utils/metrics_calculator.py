"""
Calculate data quality metrics for generated datasets.
"""
from typing import Dict, Any
import pandas as pd
import numpy as np
from loguru import logger


class MetricsCalculator:
    """Calculate comprehensive data quality metrics."""
    
    def calculate_all_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate all quality metrics for DataFrame.
        
        Args:
            df: DataFrame to analyze
        
        Returns:
            Dictionary of metrics
        """
        logger.info(f"Calculating metrics for DataFrame with shape {df.shape}")
        
        metrics = {
            'basic': self.calculate_basic_metrics(df),
            'completeness': self.calculate_completeness(df),
            'uniqueness': self.calculate_uniqueness(df),
            'validity': self.calculate_validity(df),
            'distribution': self.calculate_distributions(df)
        }
        
        return metrics
    
    def calculate_basic_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic dataset metrics."""
        return {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'columns': df.columns.tolist()
        }
    
    def calculate_completeness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate data completeness metrics."""
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        
        completeness_by_column = {}
        for col in df.columns:
            non_null = df[col].count()
            total = len(df)
            completeness_by_column[col] = {
                'completeness_pct': round((non_null / total) * 100, 2) if total > 0 else 0,
                'null_count': total - non_null
            }
        
        return {
            'overall_completeness_pct': round(((total_cells - null_cells) / total_cells) * 100, 2) if total_cells > 0 else 0,
            'total_null_cells': int(null_cells),
            'by_column': completeness_by_column
        }
    
    def calculate_uniqueness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate uniqueness metrics."""
        uniqueness_by_column = {}
        
        for col in df.columns:
            total = len(df)
            unique = df[col].nunique()
            duplicate_count = total - unique
            
            uniqueness_by_column[col] = {
                'unique_count': int(unique),
                'duplicate_count': int(duplicate_count),
                'uniqueness_pct': round((unique / total) * 100, 2) if total > 0 else 0
            }
        
        return {
            'by_column': uniqueness_by_column,
            'duplicate_rows': int(df.duplicated().sum())
        }
    
    def calculate_validity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate validity metrics."""
        validity_by_column = {}
        
        for col in df.columns:
            col_data = df[col].dropna()
            
            if len(col_data) == 0:
                validity_by_column[col] = {
                    'data_type': str(df[col].dtype),
                    'valid_pct': 0
                }
                continue
            
            # Check for valid ranges based on data type
            validity_info = {
                'data_type': str(df[col].dtype),
                'valid_pct': 100.0  # Assume valid unless we detect issues
            }
            
            # For numeric columns, check for outliers
            if pd.api.types.is_numeric_dtype(df[col]):
                q1 = col_data.quantile(0.25)
                q3 = col_data.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 3 * iqr
                upper_bound = q3 + 3 * iqr
                
                outliers = ((col_data < lower_bound) | (col_data > upper_bound)).sum()
                validity_info['outlier_count'] = int(outliers)
                validity_info['outlier_pct'] = round((outliers / len(col_data)) * 100, 2)
            
            validity_by_column[col] = validity_info
        
        return {
            'by_column': validity_by_column
        }
    
    def calculate_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate distribution statistics."""
        distributions = {}
        
        for col in df.columns:
            col_data = df[col].dropna()
            
            if len(col_data) == 0:
                continue
            
            if pd.api.types.is_numeric_dtype(df[col]):
                distributions[col] = {
                    'mean': float(col_data.mean()),
                    'median': float(col_data.median()),
                    'std': float(col_data.std()) if len(col_data) > 1 else 0,
                    'min': float(col_data.min()),
                    'max': float(col_data.max()),
                    'q25': float(col_data.quantile(0.25)),
                    'q75': float(col_data.quantile(0.75))
                }
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                distributions[col] = {
                    'min_date': str(col_data.min()),
                    'max_date': str(col_data.max()),
                    'date_range_days': (col_data.max() - col_data.min()).days
                }
            else:
                # Categorical
                value_counts = col_data.value_counts()
                distributions[col] = {
                    'top_values': value_counts.head(5).to_dict(),
                    'unique_count': int(col_data.nunique())
                }
        
        return distributions
    
    def format_metrics_html(self, metrics: Dict[str, Any]) -> str:
        """
        Format metrics as HTML for display.
        
        Args:
            metrics: Metrics dictionary
        
        Returns:
            HTML string
        """
        html = "<div style='padding: 10px;'>"
        html += "<h3>📊 Data Quality Metrics</h3>"
        
        # Basic metrics
        basic = metrics.get('basic', {})
        html += "<div style='background-color: #f0f8ff; padding: 10px; margin: 10px 0; border-radius: 5px;'>"
        html += "<h4>Basic Information</h4>"
        html += f"<p><strong>Total Records:</strong> {basic.get('total_records', 0):,}</p>"
        html += f"<p><strong>Total Columns:</strong> {basic.get('total_columns', 0)}</p>"
        html += f"<p><strong>Memory Usage:</strong> {basic.get('memory_usage_mb', 0):.2f} MB</p>"
        html += "</div>"
        
        # Completeness
        completeness = metrics.get('completeness', {})
        html += "<div style='background-color: #f0fff0; padding: 10px; margin: 10px 0; border-radius: 5px;'>"
        html += "<h4>Completeness</h4>"
        html += f"<p><strong>Overall Completeness:</strong> {completeness.get('overall_completeness_pct', 0):.2f}%</p>"
        html += f"<p><strong>Total Null Cells:</strong> {completeness.get('total_null_cells', 0):,}</p>"
        
        # Show worst columns for completeness
        by_col = completeness.get('by_column', {})
        if by_col:
            sorted_cols = sorted(by_col.items(), key=lambda x: x[1]['completeness_pct'])
            html += "<p><strong>Columns with Missing Data:</strong></p><ul>"
            for col, info in sorted_cols[:5]:
                if info['null_count'] > 0:
                    html += f"<li>{col}: {info['completeness_pct']:.1f}% complete ({info['null_count']} nulls)</li>"
            html += "</ul>"
        html += "</div>"
        
        # Uniqueness
        uniqueness = metrics.get('uniqueness', {})
        html += "<div style='background-color: #fff0f5; padding: 10px; margin: 10px 0; border-radius: 5px;'>"
        html += "<h4>Uniqueness</h4>"
        html += f"<p><strong>Duplicate Rows:</strong> {uniqueness.get('duplicate_rows', 0):,}</p>"
        html += "</div>"
        
        # Validity
        validity = metrics.get('validity', {})
        html += "<div style='background-color: #fffacd; padding: 10px; margin: 10px 0; border-radius: 5px;'>"
        html += "<h4>Validity</h4>"
        
        by_col_validity = validity.get('by_column', {})
        outlier_cols = {k: v for k, v in by_col_validity.items() if 'outlier_count' in v and v['outlier_count'] > 0}
        
        if outlier_cols:
            html += "<p><strong>Columns with Outliers:</strong></p><ul>"
            for col, info in outlier_cols.items():
                html += f"<li>{col}: {info['outlier_count']} outliers ({info['outlier_pct']:.1f}%)</li>"
            html += "</ul>"
        else:
            html += "<p>✅ No significant outliers detected</p>"
        
        html += "</div>"
        
        html += "</div>"
        return html