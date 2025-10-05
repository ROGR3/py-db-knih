"""
Unit tests for the main DBKnih API class.
"""
import pytest
from unittest.mock import Mock

from db_knih_api import DBKnih
from db_knih_api.models import BookInfo, SearchInfo


class TestDBKnih:
    """Test cases for the DBKnih main API class."""
    
    def test_init_with_services(self):
        """Test initialization with custom services."""
        mock_book_service = Mock()
        mock_search_service = Mock()
        
        api = DBKnih(mock_book_service, mock_search_service)
        
        assert api.book_service is mock_book_service
        assert api.search_service is mock_search_service
    
    def test_init_without_services(self):
        """Test initialization without custom services."""
        api = DBKnih()
        
        # Should create default services
        assert api.book_service is not None
        assert api.search_service is not None
    
    def test_search(self):
        """Test search functionality."""
        mock_search_service = Mock()
        expected_results = [
            SearchInfo(name="Book 1", id=1),
            SearchInfo(name="Book 2", id=2)
        ]
        mock_search_service.search.return_value = expected_results
        
        api = DBKnih(search_service=mock_search_service)
        result = api.search("test query")
        
        assert result == expected_results
        mock_search_service.search.assert_called_once_with("test query")
    
    def test_get_book_info(self):
        """Test get book info functionality."""
        mock_book_service = Mock()
        expected_book = BookInfo(
            year=2020,
            author="Test Author",
            rating=85.0
        )
        mock_book_service.get_book_info.return_value = expected_book
        
        api = DBKnih(book_service=mock_book_service)
        result = api.get_book_info("test-book-123")
        
        assert result == expected_book
        mock_book_service.get_book_info.assert_called_once_with("test-book-123")
    
    def test_get_book_info_none(self):
        """Test get book info when service returns None."""
        mock_book_service = Mock()
        mock_book_service.get_book_info.return_value = None
        
        api = DBKnih(book_service=mock_book_service)
        result = api.get_book_info("invalid-book")
        
        assert result is None
