"""
Unit tests for the Fetcher class.
"""
import pytest
from unittest.mock import Mock, patch

from db_knih_api.fetcher import Fetcher


class TestFetcher:
    """Test cases for the Fetcher class."""
    
    def test_init_with_session(self):
        """Test initialization with a custom session."""
        mock_session = Mock()
        fetcher = Fetcher(mock_session)
        assert fetcher.session is mock_session
    
    def test_init_without_session(self):
        """Test initialization without a custom session."""
        with patch('db_knih_api.fetcher.requests.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session
            fetcher = Fetcher()
            assert fetcher.session is mock_session
    
    def test_setup_headers(self):
        """Test that headers are set up with a random user agent."""
        mock_session = Mock()
        fetcher = Fetcher(mock_session)
        
        # Check that headers were updated
        mock_session.headers.update.assert_called_once()
        call_args = mock_session.headers.update.call_args[0][0]
        assert 'User-Agent' in call_args
        assert call_args['User-Agent'] in Fetcher.USER_AGENTS
    
    def test_fetch_page_success(self):
        """Test successful page fetching."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.text = "<html>Test content</html>"
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        
        fetcher = Fetcher(mock_session)
        result = fetcher.fetch_page("https://example.com")
        
        assert result == "<html>Test content</html>"
        mock_session.get.assert_called_once_with("https://example.com", timeout=30)
    
    def test_fetch_page_error(self):
        """Test page fetching with error."""
        import requests
        mock_session = Mock()
        mock_session.get.side_effect = requests.RequestException("Network error")
        
        fetcher = Fetcher(mock_session)
        with patch('builtins.print'):  # Suppress print output
            result = fetcher.fetch_page("https://example.com")
        
        assert result == 'Error'
    
    def test_create_search_url(self):
        """Test search URL creation."""
        result = Fetcher.create_search_url("harry potter")
        expected = "https://www.databazeknih.cz/search?q=harry%20potter"
        assert result == expected
    
    def test_create_search_url_special_chars(self):
        """Test search URL creation with special characters."""
        result = Fetcher.create_search_url("česká kniha & více")
        expected = "https://www.databazeknih.cz/search?q=%C4%8Desk%C3%A1%20kniha%20%26%20v%C3%ADce"
        assert result == expected
    
    def test_create_book_info_url(self):
        """Test book info URL creation."""
        result = Fetcher.create_book_info_url("harry-potter-123")
        expected = "https://www.databazeknih.cz/prehled-knihy/harry-potter-123"
        assert result == expected
    
    def test_create_additional_book_info_url(self):
        """Test additional book info URL creation."""
        result = Fetcher.create_additional_book_info_url("12345")
        expected = "https://www.databazeknih.cz/book-detail-more-info/12345"
        assert result == expected
