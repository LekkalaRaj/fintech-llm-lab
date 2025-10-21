"""
Data quality validator.
"""
from typing import Dict, List, Any
import pandas as pd
from loguru import logger
from src.config.settings import QUALITY_THRESHOLDS


class DataValidator:
    """Validate data quality and consistency."""
    
    def __init__(self):
        """Initialize validator."""
        self.thresholds = QUALITY_THRESHOLDS
        logger.info("DataValidator initialized")
    
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform comprehensive data validation.
        
        Args:
            df: DataFrame to validate
        
        Returns:
            Validation results dictionary
        """
        logger.info(f"Validating DataFrame with shape {df.shape}")
        
        results = {
            'passed': True,
            'checks': [],
            'issues': [],
            'summary': {}
        }
        
        # Completeness check
        completeness_result = self.check_completeness(df)
        results['checks'].append(completeness_result)
        if not completeness_result['passed']:
            results['passed'] = False
            results['issues'].extend(completeness_result.get('issues', []))
        
        # Uniqueness check
        uniqueness_result = self.check_uniqueness(df)
        results['checks'].append(uniqueness_result)
        if not uniqueness_result['passed']:
            results['passed'] = False
            results['issues'].extend(uniqueness_result.get('issues', []))
        
        # Data type consistency
        dtype_result = self.check_data_types(df)
        results['checks'].append(dtype_result)
        
        # Summary
        results['summary'] = {
            'total_checks': len(results['checks']),
            'passed_checks': sum(1 for c in results['checks'] if c['passed']),
            'total_issues': len(results['issues'])
        }
        
        logger.info(f"Validation complete: {results['summary']}")
        return results
    
    def check_completeness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check data completeness."""
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        completeness = (total_cells - null_cells) / total_cells if total_cells > 0 else 0
        
        threshold = self.thresholds['completeness']
        passed = completeness >= threshold
        
        issues = []
        if not passed:
            # Find columns with high null rates
            for col in df.columns:
                null_pct = df[col].isnull().sum() / len(df)
                if null_pct > (1 - threshold):
                    issues.append(f"Column '{col}' has {null_pct*100:.1f}% null values")
        
        return {
            'check': 'Completeness',
            'passed': passed,
            'score': completeness,
            'threshold': threshold,
            'issues': issues
        }
    
    def check_uniqueness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check uniqueness where expected."""
        # Identify potential ID columns
        id_columns = [col for col in df.columns if 'id' in col.lower() or col.lower().endswith('_number')]
        
        passed = True
        issues = []
        
        for col in id_columns:
            uniqueness = df[col].nunique() / len(df) if len(df) > 0 else 0
            threshold = self.thresholds['uniqueness']
            
            if uniqueness < threshold:
                passed = False
                issues.append(f"Column '{col}' has only {uniqueness*100:.1f}% unique values (expected {threshold*100:.0f}%)")
        
        return {
            'check': 'Uniqueness',
            'passed': passed,
            'issues': issues
        }
    
    def check_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check data type consistency."""
        issues = []
        
        for col in df.columns:
            # Check if numeric columns have non-numeric values
            if 'amount' in col.lower() or 'price' in col.lower() or 'value' in col.lower():
                if not pd.api.types.is_numeric_dtype(df[col]):
                    issues.append(f"Column '{col}' should be numeric but is {df[col].dtype}")
            
            # Check if date columns are datetime
            if 'date' in col.lower():
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    issues.append(f"Column '{col}' should be datetime but is {df[col].dtype}")
        
        return {
            'check': 'Data Types',
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def find_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Find data anomalies."""
        anomalies = []
        
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                # Check for outliers using IQR method
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                outliers = df[(df[col] < Q1 - 3*IQR) | (df[col] > Q3 + 3*IQR)]
                
                if len(outliers) > 0:
                    anomalies.append({
                        'column': col,
                        'type': 'outliers',
                        'count': len(outliers),
                        'percentage': len(outliers) / len(df) * 100
                    })
        
        return anomalies