"""
Search service for finding books on databazeknih.cz.
"""
from typing import List, Optional

from bs4 import BeautifulSoup

from .fetcher import Fetcher
from .models import SearchInfo


class SearchService:
    """Service for searching books and extracting basic information."""
    
    def __init__(self, fetcher: Optional[Fetcher] = None):
        """Initialize the search service with an optional fetcher for testing."""
        self.fetcher = fetcher or Fetcher()
    
    def search(self, text: str) -> List[SearchInfo]:
        """
        Search for books with the given text.
        
        Args:
            text: The search query
            
        Returns:
            List of SearchInfo objects with basic book information
        """
        url = self.fetcher.create_search_url(text)
        response = self.fetcher.fetch_page(url)
        
        if response == 'Error':
            return []
        
        soup = BeautifulSoup(response, 'lxml')
        book_elements = soup.select('p.new')
        
        return [self._parse_book_info(element) for element in book_elements]
    
    def _parse_book_info(self, element: BeautifulSoup) -> SearchInfo:
        """Parse book information from a search result element."""
        book_route = self._extract_book_route(element)
        
        return SearchInfo(
            name=self._get_text_content(element, "a.new"),
            id=self._safe_number_convert(book_route[-1]) if book_route else None,
            cleanName="-".join(book_route[:-1]) if len(book_route) > 1 else None,
            year=self._extract_year(element),
            author=self._extract_author(element),
        )
    
    def _extract_book_route(self, element: BeautifulSoup) -> List[str]:
        """Extract book route from the href attribute."""
        link_elem = element.select_one("a")
        if not link_elem:
            return []
        
        href = link_elem.get("href", "")
        if not href:
            return []
        
        # Handle both old and new URL formats
        # Old: /knihy/book-name-123
        # New: /prehled-knihy/book-name-123
        parts = href.strip().split("/")
        if len(parts) > 2:
            route_part = parts[2]
            return route_part.split("-")
        
        return []
    
    def _extract_year(self, element: BeautifulSoup) -> Optional[int]:
        """Extract year from the search result element."""
        # Look for year in the pozn span
        pozn_elem = element.select_one("span.pozn")
        if pozn_elem:
            pozn_text = pozn_elem.get_text(strip=True)
            # Look for 4-digit year at the beginning
            import re
            year_match = re.search(r'^(\d{4})', pozn_text)
            if year_match:
                return self._safe_number_convert(year_match.group(1))
        return None
    
    def _extract_author(self, element: BeautifulSoup) -> Optional[str]:
        """Extract author from the search result element."""
        # Look for author in the pozn span
        pozn_elem = element.select_one("span.pozn")
        if pozn_elem:
            pozn_text = pozn_elem.get_text(strip=True)
            # Extract author after the year and comma
            import re
            # Pattern: "2025, J. K. Rowling (p)" -> extract "J. K. Rowling"
            author_match = re.search(r'^\d{4},\s*([^(]+)', pozn_text)
            if author_match:
                author = author_match.group(1).strip()
                return author
        return None
    
    def _get_text_content(self, element: BeautifulSoup, selector: str) -> Optional[str]:
        """Get text content from an element using CSS selector."""
        selected_elem = element.select_one(selector)
        return selected_elem.get_text(strip=True) if selected_elem else None
    
    def _split_and_trim(self, text: Optional[str], separator: str, index: int) -> Optional[str]:
        """Split text by separator and return the element at the given index, trimmed."""
        if not text:
            return None
        
        parts = text.strip().split(separator)
        if index < len(parts):
            return parts[index].strip()
        return None
    
    def _safe_number_convert(self, text: Optional[str]) -> Optional[int]:
        """Safely convert text to integer, handling None and empty strings."""
        if not text:
            return None
        
        try:
            return int(text)
        except ValueError:
            return None
