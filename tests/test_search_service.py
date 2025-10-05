"""
Unit tests for the SearchService class.
"""
import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup

from db_knih_api.search_service import SearchService
from db_knih_api.models import SearchInfo


class TestSearchService:
    """Test cases for the SearchService class."""
    
    def test_init_with_fetcher(self):
        """Test initialization with a custom fetcher."""
        mock_fetcher = Mock()
        service = SearchService(mock_fetcher)
        assert service.fetcher is mock_fetcher
    
    def test_search_success(self):
        """Test successful search."""
        html = """
        <p class="new">
            <a class="new" href="/prehled-knihy/harry-potter-12345">Harry Potter</a>
            <span class="pozn">2020, J.K. Rowling (p)</span>
        </p>
        <p class="new">
            <a class="new" href="/prehled-knihy/lord-of-rings-67890">Lord of the Rings</a>
            <span class="pozn">1954, J.R.R. Tolkien (p)</span>
        </p>
        """
        
        mock_fetcher = Mock()
        mock_fetcher.create_search_url.return_value = "search_url"
        mock_fetcher.fetch_page.return_value = html
        
        service = SearchService(mock_fetcher)
        result = service.search("harry potter")
        
        assert len(result) == 2
        assert isinstance(result[0], SearchInfo)
        assert result[0].name == "Harry Potter"
        assert result[0].id == 12345
        assert result[0].cleanName == "harry-potter"
        assert result[0].year == 2020
        assert result[0].author == "J.K. Rowling"
        
        assert result[1].name == "Lord of the Rings"
        assert result[1].id == 67890
        assert result[1].cleanName == "lord-of-rings"
        assert result[1].year == 1954
        assert result[1].author == "J.R.R. Tolkien"
    
    def test_search_error(self):
        """Test search with fetch error."""
        mock_fetcher = Mock()
        mock_fetcher.fetch_page.return_value = 'Error'
        
        service = SearchService(mock_fetcher)
        result = service.search("test")
        
        assert result == []
    
    def test_parse_book_info(self):
        """Test book info parsing from search result element."""
        html = """
        <p class="new">
            <a class="new" href="/prehled-knihy/harry-potter-12345">Harry Potter</a>
            <span class="pozn">2020, J.K. Rowling (p)</span>
        </p>
        """
        soup = BeautifulSoup(html, 'lxml')
        element = soup.select_one('p.new')
        
        service = SearchService()
        result = service._parse_book_info(element)
        
        assert result.name == "Harry Potter"
        assert result.id == 12345
        assert result.cleanName == "harry-potter"
        assert result.year == 2020
        assert result.author == "J.K. Rowling"
    
    def test_extract_book_route(self):
        """Test book route extraction from href."""
        html = '<p class="new"><a class="new" href="/knihy/harry-potter-12345">Harry Potter</a></p>'
        soup = BeautifulSoup(html, 'lxml')
        element = soup.select_one('p.new')
        
        service = SearchService()
        result = service._extract_book_route(element)
        
        assert result == ["harry", "potter", "12345"]
    
    def test_extract_book_route_no_href(self):
        """Test book route extraction with no href."""
        html = '<a class="new">Harry Potter</a>'
        soup = BeautifulSoup(html, 'lxml')
        element = soup.select_one('a.new')
        
        service = SearchService()
        result = service._extract_book_route(element)
        
        assert result == []
    
    def test_extract_year(self):
        """Test year extraction from search result."""
        html = '<p class="new"><span class="pozn">2020, J.K. Rowling (p)</span></p>'
        soup = BeautifulSoup(html, 'lxml')
        element = soup.select_one('p.new')
        
        service = SearchService()
        result = service._extract_year(element)
        
        assert result == 2020
    
    def test_extract_year_no_content(self):
        """Test year extraction with no content."""
        html = '<span class="smallfind"></span>'
        soup = BeautifulSoup(html, 'lxml')
        element = soup.select_one('span.smallfind')
        
        service = SearchService()
        result = service._extract_year(element)
        
        assert result is None
    
    def test_extract_author(self):
        """Test author extraction from search result."""
        html = '<p class="new"><span class="pozn">2020, J.K. Rowling (p)</span></p>'
        soup = BeautifulSoup(html, 'lxml')
        element = soup.select_one('p.new')
        
        service = SearchService()
        result = service._extract_author(element)
        
        assert result == "J.K. Rowling"
    
    def test_extract_author_no_content(self):
        """Test author extraction with no content."""
        html = '<span class="smallfind"></span>'
        soup = BeautifulSoup(html, 'lxml')
        element = soup.select_one('span.smallfind')
        
        service = SearchService()
        result = service._extract_author(element)
        
        assert result is None
    
    def test_safe_number_convert_valid(self):
        """Test safe number conversion with valid input."""
        service = SearchService()
        assert service._safe_number_convert("123") == 123
        assert service._safe_number_convert(" 123 ") == 123
    
    def test_safe_number_convert_invalid(self):
        """Test safe number conversion with invalid input."""
        service = SearchService()
        assert service._safe_number_convert(None) is None
        assert service._safe_number_convert("") is None
        assert service._safe_number_convert("abc") is None
    
    def test_split_and_trim(self):
        """Test split and trim functionality."""
        service = SearchService()
        assert service._split_and_trim("a, b, c", ",", 1) == "b"
        assert service._split_and_trim("a, b, c", ",", 0) == "a"
        assert service._split_and_trim("a, b, c", ",", 2) == "c"
        assert service._split_and_trim("a, b, c", ",", 3) is None
        assert service._split_and_trim(None, ",", 0) is None
