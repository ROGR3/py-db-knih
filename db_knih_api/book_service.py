"""
Book service for extracting detailed book information from databazeknih.cz.
"""
import re
from typing import List, Optional

from bs4 import BeautifulSoup

from .fetcher import Fetcher
from .models import BookInfo, Review


class BookService:
    """Service for extracting detailed book information from HTML."""
    
    def __init__(self, fetcher: Optional[Fetcher] = None):
        """Initialize the book service with an optional fetcher for testing."""
        self.fetcher = fetcher or Fetcher()
    
    def get_book_info(self, book_link: str) -> Optional[BookInfo]:
        """
        Get detailed book information from the book link.
        
        Args:
            book_link: The book identifier (e.g., "harry-potter-a-kamen-mudrcu-12345")
            
        Returns:
            BookInfo object with extracted data, or None if extraction fails
        """
        book_url = self.fetcher.create_book_info_url(book_link)
        additional_url = self.fetcher.create_additional_book_info_url(
            book_link.split("-")[-1] if "-" in book_link else ""
        )
        
        book_html = self.fetcher.fetch_page(book_url)
        additional_html = self.fetcher.fetch_page(additional_url)
        
        if book_html == 'Error' or additional_html == 'Error':
            return None
        
        book_soup = BeautifulSoup(book_html, 'lxml')
        additional_soup = BeautifulSoup(additional_html, 'lxml')
        
        book_content = book_soup.select_one("#faux > #content")
        if not book_content:
            return None
        
        return BookInfo(
            plot=self._get_book_plot(book_content),
            genres=self._get_genres(book_content),
            year=self._get_published_year(book_content),
            author=self._get_author(book_content),
            publisher=self._get_publisher(book_content, additional_soup),
            rating=self._get_rating(book_content),
            numberOfRatings=self._get_number_of_ratings(book_content),
            reviews=self._get_reviews(book_content),
            cover=self._get_cover_image(book_content),
            pages=self._get_page_count(additional_soup),
            originalLanguage=self._get_original_language(additional_soup),
            isbn=self._get_isbn(additional_soup),
        )
    
    def _get_book_plot(self, book_content: BeautifulSoup) -> Optional[str]:
        """Extract the book plot from the HTML content."""
        # Try multiple selectors for plot/summary
        plot_selectors = [
            ".justify.new2.odtop",
            ".plot",
            ".summary",
            ".synopsis"
        ]
        
        for selector in plot_selectors:
            plot_elem = book_content.select_one(selector)
            if plot_elem:
                plot_text = plot_elem.get_text(strip=True)
                # Remove ".... celý text" and ".." patterns
                plot_text = re.sub(r'\.\.\.\. celý text|\.\.', '', plot_text)
                return plot_text
        
        # Try to find a description that's not mixed with metadata
        desc_elem = book_content.select_one("[class*='description']")
        if desc_elem:
            desc_text = desc_elem.get_text(strip=True)
            # Try to extract just the plot part, not the metadata
            # Look for patterns that indicate the actual plot
            lines = desc_text.split('\n')
            plot_lines = []
            for line in lines:
                line = line.strip()
                # Skip lines that look like metadata
                if not any(keyword in line.lower() for keyword in ['vydáno:', 'originální', 'isbn:', 'jazyk:', 'počet']):
                    if len(line) > 20:  # Likely plot text
                        plot_lines.append(line)
            
            if plot_lines:
                return ' '.join(plot_lines)
        
        return None
    
    def _get_genres(self, book_content: BeautifulSoup) -> Optional[List[str]]:
        """Extract genres from the HTML content."""
        # Try multiple selectors for genres
        genre_selectors = [
            '[itemprop="genre"]',
            '.genre',
            '[class*="genre"]'
        ]
        
        for selector in genre_selectors:
            genre_elems = book_content.select(selector)
            if genre_elems:
                genres = []
                for elem in genre_elems:
                    genre_text = elem.get_text(strip=True)
                    if genre_text and genre_text not in genres:
                        genres.append(genre_text)
                if genres:
                    return genres
        
        return None
    
    def _get_published_year(self, book_content: BeautifulSoup) -> Optional[int]:
        """Extract the published year from the HTML content."""
        # Try multiple selectors for year
        year_selectors = [
            ".detail_description > h4",
            '[itemprop="datePublished"]',
            '.year',
            '[class*="year"]'
        ]
        
        for selector in year_selectors:
            year_elems = book_content.select(selector)
            for elem in year_elems:
                year_text = elem.get_text(strip=True)
                # Look for 4-digit year in the text
                year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
                if year_match:
                    return self._safe_number_convert(year_match.group())
        
        return None
    
    def _get_author(self, book_content: BeautifulSoup) -> Optional[str]:
        """Extract the author from the HTML content."""
        # Try multiple selectors for author
        author_selectors = [
            '[itemprop="author"]',
            '.author',
            '[class*="author"]'
        ]
        
        for selector in author_selectors:
            author_elems = book_content.select(selector)
            for elem in author_elems:
                author_text = elem.get_text(strip=True)
                if author_text and author_text not in ['Autor:', 'Author:']:
                    return author_text
        
        return None
    
    def _get_publisher(self, book_content: BeautifulSoup, additional_content: BeautifulSoup = None) -> Optional[str]:
        """Extract the publisher from the HTML content."""
        # Try multiple selectors for publisher
        publisher_selectors = [
            '[itemprop="publisher"]',
            '.publisher',
            '[class*="publisher"]'
        ]
        
        for selector in publisher_selectors:
            publisher_elem = book_content.select_one(selector)
            if publisher_elem:
                publisher_text = publisher_elem.get_text(strip=True)
                if publisher_text and publisher_text not in ['Vydavatel:', 'Publisher:']:
                    return publisher_text
        
        # Try to find publisher in additional content
        if additional_content:
            all_text = additional_content.get_text()
            publisher_match = re.search(r'Vydáno:\s*([^,]+)', all_text)
            if publisher_match:
                return publisher_match.group(1).strip()
        
        return None
    
    def _get_rating(self, book_content: BeautifulSoup) -> Optional[float]:
        """Extract the rating from the HTML content."""
        # Try multiple selectors for rating
        rating_selectors = [
            ".bpoints",
            '[class*="rating"]',
            '.rating',
            '.score'
        ]
        
        for selector in rating_selectors:
            rating_elems = book_content.select(selector)
            for elem in rating_elems:
                rating_text = elem.get_text(strip=True)
                # Look for percentage pattern
                rating_match = re.search(r'(\d+)%', rating_text)
                if rating_match:
                    return self._safe_number_convert(rating_match.group(1))
        
        return None
    
    def _get_number_of_ratings(self, book_content: BeautifulSoup) -> Optional[int]:
        """Extract the number of ratings from the HTML content."""
        # Try multiple selectors for number of ratings
        ratings_selectors = [
            "#voixis > .ratingDetail",
            '[class*="rating"]',
            '.rating'
        ]
        
        for selector in ratings_selectors:
            rating_elems = book_content.select(selector)
            for elem in rating_elems:
                rating_text = elem.get_text(strip=True)
                # Look for "X hodnocení" pattern
                ratings_match = re.search(r'(\d+)\s*hodnocení', rating_text)
                if ratings_match:
                    return self._safe_number_convert(ratings_match.group(1))
        
        return None
    
    def _get_reviews(self, book_content: BeautifulSoup) -> List[Review]:
        """Extract reviews from the HTML content."""
        review_elements = book_content.select(".komentars_user")[:5]  # Limit to 5 reviews
        
        reviews = []
        for review_elem in review_elements:
            review = Review(
                text=self._get_text_content(review_elem, ".komholdu > p"),
                rating=self._get_review_rating(review_elem),
                username=self._get_attribute(review_elem, "img", "title"),
                date=self._get_text_content(review_elem, ".fright.clear_comm > .pozn_light.odleft_pet"),
            )
            reviews.append(review)
        
        return reviews
    
    def _get_review_rating(self, review_elem: BeautifulSoup) -> Optional[float]:
        """Extract rating from a review element."""
        rating_img = review_elem.select_one(".fright.clear_comm > img")
        if not rating_img:
            return None
        
        title_attr = rating_img.get("title", "")
        if title_attr:
            rating_text = title_attr.split(" ")[0]
            return self._safe_number_convert(rating_text)
        
        return None
    
    def _get_page_count(self, additional_content: BeautifulSoup) -> Optional[int]:
        """Extract page count from additional content."""
        pages_elem = additional_content.select_one('[itemprop="numberOfPages"]')
        if not pages_elem:
            return None
        
        pages_text = pages_elem.get_text(strip=True)
        return self._safe_number_convert(pages_text)
    
    def _get_original_language(self, additional_content: BeautifulSoup) -> Optional[str]:
        """Extract original language from additional content."""
        # Look for language in the additional info
        # The debug showed "Jazyk vydání: český" pattern
        all_text = additional_content.get_text()
        language_match = re.search(r'Jazyk vydání:\s*([^\n\r]+)', all_text)
        if language_match:
            return language_match.group(1).strip()
        
        # Fallback to structured data
        language_elem = additional_content.select_one('[itemprop="language"]')
        return language_elem.get_text(strip=True) if language_elem else None
    
    def _get_isbn(self, additional_content: BeautifulSoup) -> Optional[str]:
        """Extract ISBN from additional content."""
        # Look for ISBN in the additional info
        # The debug showed "ISBN: 97880000777" pattern
        all_text = additional_content.get_text()
        isbn_match = re.search(r'ISBN:\s*([^\n\r]+)', all_text)
        if isbn_match:
            return isbn_match.group(1).strip()
        
        # Fallback to structured data
        isbn_elem = additional_content.select_one('[itemprop="isbn"]')
        return isbn_elem.get_text(strip=True) if isbn_elem else None
    
    def _get_cover_image(self, book_content: BeautifulSoup) -> Optional[str]:
        """Extract cover image URL from the HTML content."""
        cover_elem = book_content.select_one(".kniha_img")
        return cover_elem.get("src") if cover_elem else None
    
    def _get_text_content(self, element: BeautifulSoup, selector: str) -> Optional[str]:
        """Get text content from an element using CSS selector."""
        selected_elem = element.select_one(selector)
        return selected_elem.get_text(strip=True) if selected_elem else None
    
    def _get_attribute(self, element: BeautifulSoup, selector: str, attribute_name: str) -> Optional[str]:
        """Get attribute value from an element using CSS selector."""
        selected_elem = element.select_one(selector)
        return selected_elem.get(attribute_name) if selected_elem else None
    
    def _split_and_trim(self, text: Optional[str], separator: str, index: int) -> Optional[str]:
        """Split text by separator and return the element at the given index, trimmed."""
        if not text:
            return None
        
        parts = text.strip().split(separator)
        if index < len(parts):
            return parts[index].strip()
        return None
    
    def _safe_number_convert(self, text: Optional[str]) -> Optional[float]:
        """Safely convert text to number, handling None and empty strings."""
        if not text:
            return None
        
        # Remove spaces and try to convert
        cleaned_text = text.replace(" ", "")
        try:
            return float(cleaned_text)
        except ValueError:
            return None
