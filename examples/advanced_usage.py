#!/usr/bin/env python3
"""
Advanced usage example for db-knih-api package.

This example demonstrates advanced features like custom services and error handling.
"""

from db_knih_api import DBKnih, BookService, SearchService, Fetcher
import time


def main():
    """Demonstrate advanced API usage."""
    print("🚀 DB Knih API - Advanced Usage Example")
    print("=" * 50)
    
    # Example 1: Using custom services
    print("\n1️⃣ Custom Services Example")
    print("-" * 30)
    
    # Create custom fetcher with different settings
    custom_fetcher = Fetcher()
    
    # Create custom services
    custom_search_service = SearchService(custom_fetcher)
    custom_book_service = BookService(custom_fetcher)
    
    # Create API with custom services
    custom_api = DBKnih(custom_book_service, custom_search_service)
    
    # Search with custom API
    results = custom_api.search("fantasy")
    print(f"Found {len(results)} fantasy books with custom services")
    
    # Example 2: Batch processing
    print("\n2️⃣ Batch Processing Example")
    print("-" * 30)
    
    search_terms = ["sci-fi", "romance", "thriller"]
    all_results = []
    
    for term in search_terms:
        print(f"Searching for '{term}'...")
        results = db_knih.search(term)
        all_results.extend(results[:2])  # Take first 2 results from each
        time.sleep(0.5)  # Be respectful to the server
    
    print(f"Total books found across all searches: {len(all_results)}")
    
    # Example 3: Error handling
    print("\n3️⃣ Error Handling Example")
    print("-" * 30)
    
    try:
        # Try to get info for a non-existent book
        result = db_knih.get_book_info("non-existent-book-999999")
        if result is None:
            print("✅ Properly handled non-existent book (returned None)")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Example 4: Data analysis
    print("\n4️⃣ Data Analysis Example")
    print("-" * 30)
    
    if all_results:
        # Analyze years
        years = [book.year for book in all_results if book.year]
        if years:
            print(f"📅 Year range: {min(years)} - {max(years)}")
            print(f"📅 Average year: {sum(years) / len(years):.0f}")
        
        # Analyze authors
        authors = [book.author for book in all_results if book.author]
        if authors:
            unique_authors = set(authors)
            print(f"✍️  Unique authors: {len(unique_authors)}")
            print(f"✍️  Most common authors: {', '.join(list(unique_authors)[:3])}")
        
        # Analyze genres (from detailed info)
        print("\n📊 Getting detailed info for genre analysis...")
        genres_count = {}
        
        for book in all_results[:3]:  # Analyze first 3 books
            book_link = f"{book.cleanName}-{book.id}"
            detailed = db_knih.get_book_info(book_link)
            
            if detailed and detailed.genres:
                for genre in detailed.genres:
                    genres_count[genre] = genres_count.get(genre, 0) + 1
            time.sleep(0.5)  # Be respectful
        
        if genres_count:
            print("🏷️  Genre distribution:")
            for genre, count in sorted(genres_count.items(), key=lambda x: x[1], reverse=True):
                print(f"   {genre}: {count}")
    
    print("\n✅ Advanced examples completed!")


if __name__ == "__main__":
    main()
