"""
Integration tests that fetch real data from databazeknih.cz to verify parsing logic.
"""
import pytest
import time
from bs4 import BeautifulSoup

from db_knih_api.fetcher import Fetcher
from db_knih_api.book_service import BookService
from db_knih_api.search_service import SearchService


class TestIntegration:
    """Integration tests with real website data."""
    
    def setup_method(self):
        """Set up for each test method."""
        self.fetcher = Fetcher()
        self.book_service = BookService(self.fetcher)
        self.search_service = SearchService(self.fetcher)
        # Add small delay to be respectful to the server
        time.sleep(0.5)
    
    def test_search_real_data(self):
        """Test search with real website data."""
        print("\n=== Testing Search with Real Data ===")
        
        search_results = self.search_service.search("harry potter")
        
        print(f"Found {len(search_results)} search results")
        
        # Check that we got results
        assert len(search_results) > 0, "Should find at least one book"
        
        # Check first few results
        for i, book in enumerate(search_results[:3]):
            print(f"\nResult {i+1}:")
            print(f"  Name: {book.name}")
            print(f"  ID: {book.id}")
            print(f"  Clean Name: {book.cleanName}")
            print(f"  Year: {book.year}")
            print(f"  Author: {book.author}")
            
            # Basic assertions
            assert book.name is not None, f"Book name should not be None for result {i+1}"
            assert book.id is not None, f"Book ID should not be None for result {i+1}"
            assert book.cleanName is not None, f"Clean name should not be None for result {i+1}"
    
    def test_book_info_real_data(self):
        """Test book info extraction with real website data."""
        print("\n=== Testing Book Info with Real Data ===")
        
        # First get a search result
        search_results = self.search_service.search("harry potter")
        assert len(search_results) > 0, "Should find at least one book"
        
        # Use the first result
        first_book = search_results[0]
        book_link = f"{first_book.cleanName}-{first_book.id}"
        
        print(f"Testing book: {first_book.name}")
        print(f"Book link: {book_link}")
        
        # Get detailed info
        book_info = self.book_service.get_book_info(book_link)
        
        print(f"\nDetailed Book Info:")
        print(f"  Plot: {book_info.plot[:100] if book_info.plot else 'None'}...")
        print(f"  Genres: {book_info.genres}")
        print(f"  Year: {book_info.year}")
        print(f"  Publisher: {book_info.publisher}")
        print(f"  Rating: {book_info.rating}")
        print(f"  Number of ratings: {book_info.numberOfRatings}")
        print(f"  Pages: {book_info.pages}")
        print(f"  Original language: {book_info.originalLanguage}")
        print(f"  ISBN: {book_info.isbn}")
        print(f"  Cover: {book_info.cover}")
        print(f"  Reviews count: {len(book_info.reviews) if book_info.reviews else 0}")
        
        # Check that we got some data
        assert book_info is not None, "Book info should not be None"
        
        # At least some fields should have data
        has_data = any([
            book_info.plot,
            book_info.genres,
            book_info.year,
            book_info.publisher,
            book_info.rating,
            book_info.pages,
            book_info.cover
        ])
        assert has_data, "At least some book info fields should have data"
    
    def test_debug_html_structure(self):
        """Debug the actual HTML structure to understand parsing issues."""
        print("\n=== Debugging HTML Structure ===")
        
        # Get a search result first
        search_results = self.search_service.search("harry potter")
        assert len(search_results) > 0, "Should find at least one book"
        
        first_book = search_results[0]
        book_link = f"{first_book.cleanName}-{first_book.id}"
        
        print(f"Debugging book: {first_book.name}")
        
        # Fetch raw HTML
        book_url = self.fetcher.create_book_info_url(book_link)
        additional_url = self.fetcher.create_additional_book_info_url(str(first_book.id))
        
        print(f"Book URL: {book_url}")
        print(f"Additional URL: {additional_url}")
        
        # Get HTML content
        book_html = self.fetcher.fetch_page(book_url)
        additional_html = self.fetcher.fetch_page(additional_url)
        
        if book_html != 'Error':
            soup = BeautifulSoup(book_html, 'lxml')
            
            print("\n=== Book HTML Structure ===")
            
            # Check for main content area
            content = soup.select_one("#faux > #content")
            if content:
                print("✓ Found main content area")
            else:
                print("✗ Main content area not found")
                # Try alternative selectors
                alt_content = soup.select_one("#content")
                if alt_content:
                    print("✓ Found alternative content area")
                else:
                    print("✗ No content area found at all")
            
            # Check for plot
            plot_elem = soup.select_one(".justify.new2.odtop")
            if plot_elem:
                print("✓ Found plot element")
                print(f"  Plot text: {plot_elem.get_text(strip=True)[:100]}...")
            else:
                print("✗ Plot element not found")
                # Try alternative selectors
                alt_plot = soup.select_one(".plot, .description, .summary")
                if alt_plot:
                    print("✓ Found alternative plot element")
                else:
                    print("✗ No plot elements found")
            
            # Check for genres
            genre_elem = soup.select_one('[itemprop="genre"]')
            if genre_elem:
                print("✓ Found genre element")
                print(f"  Genres: {genre_elem.get_text(strip=True)}")
            else:
                print("✗ Genre element not found")
            
            # Check for rating
            rating_elem = soup.select_one(".bpoints")
            if rating_elem:
                print("✓ Found rating element")
                print(f"  Rating: {rating_elem.get_text(strip=True)}")
            else:
                print("✗ Rating element not found")
                # Try alternative selectors
                alt_rating = soup.select_one(".rating, .score, .stars")
                if alt_rating:
                    print("✓ Found alternative rating element")
                else:
                    print("✗ No rating elements found")
            
            # Check for year
            year_elem = soup.select_one(".detail_description > h4")
            if year_elem:
                print("✓ Found year element")
                print(f"  Year text: {year_elem.get_text(strip=True)}")
            else:
                print("✗ Year element not found")
            
            # Check for publisher
            publisher_elem = soup.select_one('[itemprop="publisher"]')
            if publisher_elem:
                print("✓ Found publisher element")
                print(f"  Publisher: {publisher_elem.get_text(strip=True)}")
            else:
                print("✗ Publisher element not found")
        
        if additional_html != 'Error':
            additional_soup = BeautifulSoup(additional_html, 'lxml')
            
            print("\n=== Additional Info HTML Structure ===")
            
            # Check for pages
            pages_elem = additional_soup.select_one('[itemprop="numberOfPages"]')
            if pages_elem:
                print("✓ Found pages element")
                print(f"  Pages: {pages_elem.get_text(strip=True)}")
            else:
                print("✗ Pages element not found")
            
            # Check for language
            language_elem = additional_soup.select_one('[itemprop="language"]')
            if language_elem:
                print("✓ Found language element")
                print(f"  Language: {language_elem.get_text(strip=True)}")
            else:
                print("✗ Language element not found")
            
            # Check for ISBN
            isbn_elem = additional_soup.select_one('[itemprop="isbn"]')
            if isbn_elem:
                print("✓ Found ISBN element")
                print(f"  ISBN: {isbn_elem.get_text(strip=True)}")
            else:
                print("✗ ISBN element not found")
    
    def test_search_html_structure(self):
        """Debug the search results HTML structure."""
        print("\n=== Debugging Search HTML Structure ===")
        
        # Get search URL and HTML
        search_url = self.fetcher.create_search_url("harry potter")
        search_html = self.fetcher.fetch_page(search_url)
        
        if search_html != 'Error':
            soup = BeautifulSoup(search_html, 'lxml')
            
            print(f"Search URL: {search_url}")
            
            # Check for search results
            book_elements = soup.select('p.new')
            print(f"Found {len(book_elements)} book elements with 'p.new' selector")
            
            if len(book_elements) == 0:
                # Try alternative selectors
                alt_elements = soup.select('.book, .result, .item')
                print(f"Found {len(alt_elements)} elements with alternative selectors")
                
                # Print some HTML structure
                print("\nFirst 500 characters of search HTML:")
                print(search_html[:500])
            
            # Check first book element structure
            if book_elements:
                first_book = book_elements[0]
                print(f"\nFirst book element HTML:")
                print(first_book.prettify()[:500])
                
                # Check for title link
                title_link = first_book.select_one("a.new")
                if title_link:
                    print(f"✓ Found title link: {title_link.get_text(strip=True)}")
                    print(f"  Href: {title_link.get('href')}")
                else:
                    print("✗ Title link not found")
                
                # Check for metadata
                metadata = first_book.select_one("span.smallfind")
                if metadata:
                    print(f"✓ Found metadata: {metadata.get_text(strip=True)}")
                else:
                    print("✗ Metadata not found")


if __name__ == "__main__":
    # Run integration tests manually
    test = TestIntegration()
    test.setup_method()
    
    try:
        test.test_search_real_data()
        test.test_debug_html_structure()
        test.test_search_html_structure()
        test.test_book_info_real_data()
    except Exception as e:
        print(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
