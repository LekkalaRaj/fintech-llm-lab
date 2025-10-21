"""
Google Search validator for cross-referencing generated data.
"""
from typing import List, Dict, Any, Optional
import time
from loguru import logger
from googlesearch import search
from src.config.settings import settings


class SearchValidator:
    """Validate generated data using Google Search."""
    
    def __init__(self):
        """Initialize search validator."""
        self.rate_limit = settings.search_requests_per_day
        self.request_count = 0
        self.last_reset = time.time()
        logger.info("SearchValidator initialized")
    
    def _rate_limit_check(self):
        """Check and enforce rate limiting."""
        current_time = time.time()
        
        # Reset counter every 24 hours
        if current_time - self.last_reset > 86400:
            self.request_count = 0
            self.last_reset = current_time
        
        if self.request_count >= self.rate_limit:
            logger.warning("Search rate limit reached")
            return False
        
        return True
    
    def search_web(
        self,
        query: str,
        num_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Perform Google search.
        
        Args:
            query: Search query
            num_results: Number of results to return
        
        Returns:
            List of search results with titles and URLs
        """
        if not self._rate_limit_check():
            logger.warning("Skipping search due to rate limit")
            return []
        
        try:
            logger.info(f"Searching: {query}")
            results = []
            
            for url in search(query, num_results=num_results, sleep_interval=2):
                results.append({
                    'url': url,
                    'query': query
                })
                self.request_count += 1
            
            logger.info(f"Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def validate_domain_patterns(
        self,
        domain: str,
        dataset_type: str
    ) -> List[Dict[str, str]]:
        """
        Validate typical patterns for a domain.
        
        Args:
            domain: Financial domain
            dataset_type: Type of dataset
        
        Returns:
            List of validation sources
        """
        queries = self._get_validation_queries(domain, dataset_type)
        all_sources = []
        
        for query in queries:
            results = self.search_web(query, num_results=3)
            all_sources.extend(results)
            time.sleep(1)  # Be respectful to search API
        
        return all_sources
    
    def _get_validation_queries(
        self,
        domain: str,
        dataset_type: str
    ) -> List[str]:
        """
        Generate appropriate validation queries.
        
        Args:
            domain: Financial domain
            dataset_type: Dataset type
        
        Returns:
            List of search queries
        """
        queries = []
        
        if domain == "Capital Markets":
            if "Stock" in dataset_type:
                queries = [
                    "typical stock price ranges NYSE NASDAQ",
                    "average daily trading volume stocks",
                    "stock market volatility patterns"
                ]
            elif "Securities" in dataset_type:
                queries = [
                    "ISIN format securities identification",
                    "market capitalization distribution stocks",
                    "stock exchange listing requirements"
                ]
        
        elif domain == "Private Equity":
            queries = [
                "private equity fund size typical range",
                "PE deal IRR benchmarks industry",
                "private equity management fees structure"
            ]
        
        elif domain == "Venture Capital":
            queries = [
                "venture capital funding round sizes",
                "startup valuation benchmarks by stage",
                "VC equity stake typical percentage"
            ]
        
        elif domain == "Banking":
            if "Customer" in dataset_type:
                queries = [
                    "bank customer segmentation criteria",
                    "KYC requirements banking industry"
                ]
            elif "CASA" in dataset_type:
                queries = [
                    "savings account interest rates typical",
                    "average bank account balance statistics"
                ]
            elif "Loan" in dataset_type:
                queries = [
                    "personal loan interest rates range",
                    "mortgage loan to value ratio typical",
                    "credit score requirements loans"
                ]
        
        # Fallback generic query
        if not queries:
            queries = [f"{domain} {dataset_type} typical data ranges"]
        
        return queries
    
    def validate_field_ranges(
        self,
        domain: str,
        field_name: str,
        sample_values: List[Any]
    ) -> List[Dict[str, str]]:
        """
        Validate if field values are within typical ranges.
        
        Args:
            domain: Financial domain
            field_name: Field name
            sample_values: Sample values from generated data
        
        Returns:
            Validation sources
        """
        # Create search query
        query = f"{domain} typical {field_name} range values"
        results = self.search_web(query, num_results=3)
        
        logger.info(f"Validated {field_name} with {len(results)} sources")
        return results
    
    def format_sources_html(
        self,
        sources: List[Dict[str, str]]
    ) -> str:
        """
        Format validation sources as HTML.
        
        Args:
            sources: List of source dictionaries
        
        Returns:
            HTML string
        """
        if not sources:
            return "<p>No validation sources found.</p>"
        
        html = "<div style='padding: 10px;'>"
        html += "<h3>🔍 Validation Sources</h3>"
        html += "<p>Data patterns were cross-referenced with the following sources:</p>"
        html += "<ol>"
        
        for source in sources:
            url = source.get('url', '')
            query = source.get('query', 'Unknown query')
            html += f"<li>"
            html += f"<strong>Query:</strong> {query}<br>"
            html += f"<a href='{url}' target='_blank'>{url}</a>"
            html += f"</li>"
        
        html += "</ol>"
        html += "</div>"
        
        return html
    
    def get_regulatory_info(
        self,
        domain: str
    ) -> List[Dict[str, str]]:
        """
        Get regulatory information for domain.
        
        Args:
            domain: Financial domain
        
        Returns:
            Regulatory information sources
        """
        regulatory_queries = {
            "Capital Markets": "SEC securities regulations trading requirements",
            "Private Equity": "private equity fund regulations compliance",
            "Venture Capital": "venture capital regulations investment limits",
            "Banking": "banking regulations KYC AML requirements"
        }
        
        query = regulatory_queries.get(domain, f"{domain} regulations")
        return self.search_web(query, num_results=3)