"""
HTTP fetcher module for making requests to databazeknih.cz.
"""
import random
import urllib.parse
from typing import Optional

import requests


class Fetcher:
    """Handles HTTP requests with proper headers and error handling."""
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36'
    ]
    
    def __init__(self, session: Optional[requests.Session] = None):
        """Initialize the fetcher with an optional session for testing."""
        self.session = session or requests.Session()
        self._setup_headers()
    
    def _setup_headers(self) -> None:
        """Set up random user agent headers."""
        user_agent = random.choice(self.USER_AGENTS)
        self.session.headers.update({
            'User-Agent': user_agent
        })
    
    def fetch_page(self, url: str) -> str:
        """
        Fetch a web page and return its content as text.
        
        Args:
            url: The URL to fetch
            
        Returns:
            The HTML content of the page, or 'Error' if request fails
            
        Raises:
            requests.RequestException: If the request fails
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return 'Error'
    
    @staticmethod
    def create_search_url(text: str) -> str:
        """
        Create a search URL for the given text.
        
        Args:
            text: The search query
            
        Returns:
            The complete search URL
        """
        encoded_text = urllib.parse.quote(text)
        return f"https://www.databazeknih.cz/search?q={encoded_text}"
    
    @staticmethod
    def create_book_info_url(book: str) -> str:
        """
        Create a book info URL for the given book identifier.
        
        Args:
            book: The book identifier (usually from search results)
            
        Returns:
            The complete book info URL
        """
        encoded_book = urllib.parse.quote(book)
        return f"https://www.databazeknih.cz/prehled-knihy/{encoded_book}"
    
    @staticmethod
    def create_additional_book_info_url(book_id: str) -> str:
        """
        Create an additional book info URL for the given book ID.
        
        Args:
            book_id: The book ID
            
        Returns:
            The complete additional book info URL
        """
        encoded_book_id = urllib.parse.quote(book_id)
        return f"https://www.databazeknih.cz/book-detail-more-info/{encoded_book_id}"
