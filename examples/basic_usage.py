#!/usr/bin/env python3
"""
Basic usage example for py-db-knih package.

This example demonstrates how to search for books and get detailed information.
"""

from db_knih_api import db_knih


def main():
    """Demonstrate basic API usage."""
    print("🔍 DB Knih API - Basic Usage Example")
    print("=" * 50)
    
    # Search for books
    search_term = "harry potter"
    print(f"\n📚 Searching for '{search_term}'...")
    
    try:
        search_results = db_knih.search(search_term)
        
        if search_results:
            print(f"✅ Found {len(search_results)} books:")
            
            # Show first 3 results
            for i, book in enumerate(search_results[:3], 1):
                print(f"\n  {i}. {book.name}")
                print(f"     📅 Year: {book.year}")
                print(f"     ✍️  Author: {book.author}")
                print(f"     🆔 ID: {book.id}")
                print(f"     🔗 Clean name: {book.cleanName}")
            
            # Get detailed info for the first book
            if search_results:
                first_book = search_results[0]
                print(f"\n📖 Getting detailed info for '{first_book.name}'...")
                
                # Use the clean name and ID to get detailed info
                book_link = f"{first_book.cleanName}-{first_book.id}"
                detailed_info = db_knih.get_book_info(book_link)
                
                if detailed_info:
                    print("✅ Detailed book information:")
                    print(f"   📝 Plot: {detailed_info.plot[:100] if detailed_info.plot else 'Not available'}...")
                    print(f"   🏷️  Genres: {', '.join(detailed_info.genres) if detailed_info.genres else 'Not available'}")
                    print(f"   📅 Year: {detailed_info.year}")
                    print(f"   ✍️  Author: {detailed_info.author}")
                    print(f"   🏢 Publisher: {detailed_info.publisher}")
                    print(f"   ⭐ Rating: {detailed_info.rating}%")
                    print(f"   👥 Number of ratings: {detailed_info.numberOfRatings}")
                    print(f"   📄 Pages: {detailed_info.pages}")
                    print(f"   🌍 Original language: {detailed_info.originalLanguage}")
                    print(f"   📚 ISBN: {detailed_info.isbn}")
                    print(f"   🖼️  Cover: {detailed_info.cover}")
                    
                    if detailed_info.reviews:
                        print(f"   💬 Reviews ({len(detailed_info.reviews)}):")
                        for review in detailed_info.reviews[:2]:  # Show first 2 reviews
                            print(f"     - {review.username}: {review.rating}/5 stars")
                            if review.text:
                                print(f"       \"{review.text[:50]}...\"")
                else:
                    print("❌ Failed to get detailed information")
        else:
            print("❌ No books found")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
