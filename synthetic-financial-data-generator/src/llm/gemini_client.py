"""
Google Gemini API client for LLM-based data generation.
"""
import json
import time
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from loguru import logger
from src.config.settings import settings
from src.config.prompts import SYSTEM_PROMPT


class GeminiClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client."""
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        self.rate_limit = settings.gemini_requests_per_minute
        self.last_request_time = 0
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        logger.info(f"Initialized Gemini client with model: {self.model_name}")
    
    def _rate_limit(self):
        """Apply rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 60.0 / self.rate_limit
        
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def generate_text(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> str:
        """
        Generate text using Gemini.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (uses default if None)
            temperature: Generation temperature (0.0 to 1.0)
            max_retries: Maximum number of retries on failure
        
        Returns:
            Generated text
        """
        self._rate_limit()
        
        # Combine system and user prompts
        full_prompt = f"{system_prompt or SYSTEM_PROMPT}\n\n{prompt}"
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Generating text (attempt {attempt + 1}/{max_retries})")
                
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                    )
                )
                
                if response.text:
                    logger.debug(f"Generated {len(response.text)} characters")
                    return response.text
                else:
                    logger.warning("Empty response from Gemini")
                    
            except Exception as e:
                logger.error(f"Error generating text (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
        
        raise Exception("Failed to generate text after all retries")
    
    def generate_json(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Generate JSON data using Gemini.
        
        Args:
            prompt: User prompt requesting JSON output
            system_prompt: System prompt
            temperature: Generation temperature
        
        Returns:
            Parsed JSON data as list of dictionaries
        """
        response_text = self.generate_text(prompt, system_prompt, temperature)
        
        try:
            # Try to extract JSON from response
            json_data = self._extract_json(response_text)
            return json_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.debug(f"Response text: {response_text[:500]}")
            raise ValueError(f"Invalid JSON in response: {str(e)}")
    
    def _extract_json(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract JSON from text that might contain markdown formatting.
        
        Args:
            text: Text potentially containing JSON
        
        Returns:
            Parsed JSON data
        """
        # Remove markdown code blocks if present
        text = text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        # Try to parse
        parsed = json.loads(text)
        
        # Ensure it's a list
        if isinstance(parsed, dict):
            return [parsed]
        elif isinstance(parsed, list):
            return parsed
        else:
            raise ValueError(f"Unexpected JSON type: {type(parsed)}")
    
    def generate_batch(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> List[str]:
        """
        Generate text for multiple prompts.
        
        Args:
            prompts: List of prompts
            system_prompt: System prompt
            temperature: Generation temperature
        
        Returns:
            List of generated texts
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            logger.info(f"Processing batch item {i + 1}/{len(prompts)}")
            result = self.generate_text(prompt, system_prompt, temperature)
            results.append(result)
        
        return results
    
    def test_connection(self) -> bool:
        """
        Test connection to Gemini API.
        
        Returns:
            True if connection successful
        """
        try:
            response = self.generate_text("Say 'Hello'", temperature=0.1)
            logger.info("Gemini API connection test successful")
            return True
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {str(e)}")
            return False