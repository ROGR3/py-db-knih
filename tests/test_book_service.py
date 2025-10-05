"""
Unit tests for the BookService class.
"""
import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup

from db_knih_api.book_service import BookService
from db_knih_api.models import BookInfo, Review


class TestBookService:
    """Test cases for the BookService class."""
    
    def test_init_with_fetcher(self):
        """Test initialization with a custom fetcher."""
        mock_fetcher = Mock()
        service = BookService(mock_fetcher)
        assert service.fetcher is mock_fetcher
    
    def test_get_book_plot(self):
        """Test book plot extraction."""
        html = """
        <div class="justify new2 odtop">
            This is the main plot text.... celý text
            <span>This is additional plot text..</span>
        </div>
        """
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_book_plot(soup)
        expected = "This is the main plot textThis is additional plot text"
        assert result == expected
    
    def test_get_book_plot_no_content(self):
        """Test book plot extraction with no content."""
        html = "<div></div>"
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_book_plot(soup)
        assert result is None
    
    def test_get_genres(self):
        """Test genres extraction."""
        html = """
        <div class="genre">Fantasy</div>
        <div class="genre">Adventure</div>
        <div class="genre">Fiction</div>
        """
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_genres(soup)
        expected = ["Fantasy", "Adventure", "Fiction"]
        assert result == expected
    
    def test_get_genres_no_content(self):
        """Test genres extraction with no content."""
        html = "<div></div>"
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_genres(soup)
        assert result is None
    
    def test_get_published_year_from_detail(self):
        """Test published year extraction from detail description."""
        html = '<div class="year">2020</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_published_year(soup)
        assert result == 2020
    
    def test_get_published_year_from_date_published(self):
        """Test published year extraction from datePublished."""
        html = '<div itemprop="datePublished">2020</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_published_year(soup)
        assert result == 2020
    
    def test_get_publisher(self):
        """Test publisher extraction."""
        html = '<div itemprop="publisher">Test Publisher</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_publisher(soup)
        assert result == "Test Publisher"
    
    def test_get_rating(self):
        """Test rating extraction."""
        html = '<div class="rating">85%</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_rating(soup)
        assert result == 85.0
    
    def test_get_number_of_ratings(self):
        """Test number of ratings extraction."""
        html = '<div class="rating">85% 150 hodnocení</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_number_of_ratings(soup)
        assert result == 150
    
    def test_get_author(self):
        """Test author extraction."""
        html = '<div class="author">J.K. Rowling</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_author(soup)
        assert result == "J.K. Rowling"
    
    def test_get_author_no_content(self):
        """Test author extraction with no content."""
        html = "<div></div>"
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_author(soup)
        assert result is None
    
    def test_get_reviews(self):
        """Test reviews extraction."""
        html = """
        <div class="komentars_user">
            <img title="User Name" />
            <div class="komholdu"><p>Great book!</p></div>
            <div class="fright clear_comm">
                <img title="5 hvězd" />
                <div class="pozn_light odleft_pet">2023-01-01</div>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_reviews(soup)
        assert len(result) == 1
        assert result[0].text == "Great book!"
        assert result[0].rating == 5.0
        assert result[0].username == "User Name"
        assert result[0].date == "2023-01-01"
    
    def test_get_review_rating(self):
        """Test review rating extraction."""
        html = """
        <div class="komentars_user">
            <div class="fright clear_comm">
                <img title="4 hvězd" />
            </div>
        </div>
        """
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_review_rating(soup)
        assert result == 4.0
    
    def test_get_page_count(self):
        """Test page count extraction."""
        html = '<div itemprop="numberOfPages">300</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_page_count(soup)
        assert result == 300
    
    def test_get_original_language(self):
        """Test original language extraction."""
        html = '<div itemprop="language">English</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_original_language(soup)
        assert result == "English"
    
    def test_get_isbn(self):
        """Test ISBN extraction."""
        html = '<div itemprop="isbn">978-1234567890</div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_isbn(soup)
        assert result == "978-1234567890"
    
    def test_get_cover_image(self):
        """Test cover image extraction."""
        html = '<div class="kniha_img" src="https://example.com/cover.jpg"></div>'
        soup = BeautifulSoup(html, 'lxml')
        service = BookService()
        
        result = service._get_cover_image(soup)
        assert result == "https://example.com/cover.jpg"
    
    def test_safe_number_convert_valid(self):
        """Test safe number conversion with valid input."""
        service = BookService()
        assert service._safe_number_convert("123") == 123.0
        assert service._safe_number_convert("123.45") == 123.45
        assert service._safe_number_convert(" 123 ") == 123.0
    
    def test_safe_number_convert_invalid(self):
        """Test safe number conversion with invalid input."""
        service = BookService()
        assert service._safe_number_convert(None) is None
        assert service._safe_number_convert("") is None
        assert service._safe_number_convert("abc") is None
    
    def test_split_and_trim(self):
        """Test split and trim functionality."""
        service = BookService()
        assert service._split_and_trim("a, b, c", ",", 1) == "b"
        assert service._split_and_trim("a, b, c", ",", 0) == "a"
        assert service._split_and_trim("a, b, c", ",", 2) == "c"
        assert service._split_and_trim("a, b, c", ",", 3) is None
        assert service._split_and_trim(None, ",", 0) is None
    
    @patch('db_knih_api.book_service.BeautifulSoup')
    def test_get_book_info_success(self, mock_soup):
        """Test successful book info extraction."""
        # Mock HTML content
        book_html = """
        <div id="faux">
            <div id="content">
                <div class="justify new2 odtop">Plot text</div>
                <div itemprop="genre">Fantasy, Adventure</div>
                <div class="detail_description"><h4>Title, 2020, Author</h4></div>
                <div itemprop="publisher">Test Publisher</div>
                <div class="rating">85% 150 hodnocení</div>
                <div class="kniha_img" src="cover.jpg"></div>
            </div>
        </div>
        """
        
        additional_html = """
        <div itemprop="numberOfPages">300</div>
        <div itemprop="language">English</div>
        <div itemprop="isbn">978-1234567890</div>
        """
        
        mock_fetcher = Mock()
        mock_fetcher.create_book_info_url.return_value = "book_url"
        mock_fetcher.create_additional_book_info_url.return_value = "additional_url"
        mock_fetcher.fetch_page.side_effect = [book_html, additional_html]
        
        mock_soup.side_effect = [
            BeautifulSoup(book_html, 'lxml'),
            BeautifulSoup(additional_html, 'lxml')
        ]
        
        service = BookService(mock_fetcher)
        result = service.get_book_info("test-book-123")
        
        assert isinstance(result, BookInfo)
        assert result.plot == "Plot text"
        assert result.genres == ["Fantasy, Adventure"]  # Single element with comma-separated genres
        assert result.year == 2020
        assert result.publisher == "Test Publisher"
        assert result.rating == 85.0
        assert result.numberOfRatings == 150
        assert result.cover == "cover.jpg"
        assert result.pages == 300
        assert result.originalLanguage == "English"
        assert result.isbn == "978-1234567890"
    
    def test_get_book_info_error(self):
        """Test book info extraction with fetch error."""
        mock_fetcher = Mock()
        mock_fetcher.fetch_page.return_value = 'Error'
        
        service = BookService(mock_fetcher)
        result = service.get_book_info("test-book-123")
        
        assert result is None
