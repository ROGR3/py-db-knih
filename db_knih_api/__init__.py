"""
DB Knih API - A Python library for scraping book information from databazeknih.cz.

This package provides a clean interface to search for books and retrieve detailed
information from the Czech book database website.
"""

from .book_service import BookService
from .fetcher import Fetcher
from .models import BookInfo, Review, SearchInfo
from .search_service import SearchService

__version__ = "1.0.0"
__author__ = "Your Name"  # Replace with your name
__email__ = "your.email@example.com"  # Replace with your email

# Create a default instance for easy importing
from .book_service import BookService
from .search_service import SearchService

class DBKnih:
    """Main API class that combines search and book services."""
    
    def __init__(self, book_service: BookService = None, search_service: SearchService = None):
        """
        Initialize the DB Knih API.
        
        Args:
            book_service: Optional BookService instance for testing
            search_service: Optional SearchService instance for testing
        """
        self.book_service = book_service or BookService()
        self.search_service = search_service or SearchService()
    
    def search(self, text: str) -> list[SearchInfo]:
        """
        Search for books with the given text.
        
        Args:
            text: The search query
            
        Returns:
            List of SearchInfo objects with basic book information
        """
        return self.search_service.search(text)
    
    def get_book_info(self, book_link: str) -> BookInfo | None:
        """
        Get detailed book information from the book link.
        
        Args:
            book_link: The book identifier (e.g., "harry-potter-a-kamen-mudrcu-12345")
            
        Returns:
            BookInfo object with extracted data, or None if extraction fails
        """
        return self.book_service.get_book_info(book_link)


# Create a default instance for easy importing
db_knih = DBKnih()

__all__ = [
    'DBKnih',
    'BookService', 
    'SearchService',
    'Fetcher',
    'BookInfo',
    'SearchInfo', 
    'Review',
    'db_knih',
    '__version__',
    '__author__',
    '__email__'
]