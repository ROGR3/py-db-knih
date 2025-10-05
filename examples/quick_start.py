#!/usr/bin/env python3
"""
Quick start example for py-db-knih.

This is a simple example that users can run after installing the package.
"""

from db_knih_api import db_knih


def main():
    """Simple example showing basic usage."""
    print("🔍 DB Knih API - Quick Start")
    print("=" * 40)
    
    # Search for books
    search_term = "harry potter"
    print(f"\n📚 Searching for '{search_term}'...")
    
    try:
        results = db_knih.search(search_term)
        
        if results:
            print(f"✅ Found {len(results)} books!")
            
            # Show first 3 results
            for i, book in enumerate(results[:3], 1):
                print(f"\n  {i}. {book.name}")
                print(f"     📅 Year: {book.year}")
                print(f"     ✍️  Author: {book.author}")
                print(f"     🆔 ID: {book.id}")
            
            # Get detailed info for the first book
            if results:
                first_book = results[0]
                print(f"\n📖 Getting detailed info for '{first_book.name}'...")
                
                book_link = f"{first_book.cleanName}-{first_book.id}"
                detailed = db_knih.get_book_info(book_link)
                
                if detailed:
                    print("✅ Detailed information:")
                    print(f"   🏷️  Genres: {', '.join(detailed.genres) if detailed.genres else 'Not available'}")
                    print(f"   ⭐ Rating: {detailed.rating}%")
                    print(f"   👥 Ratings: {detailed.numberOfRatings}")
                    print(f"   📄 Pages: {detailed.pages}")
                    print(f"   🌍 Language: {detailed.originalLanguage}")
                    print(f"   📚 ISBN: {detailed.isbn}")
                else:
                    print("❌ Could not get detailed information")
        else:
            print("❌ No books found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have an internet connection!")


if __name__ == "__main__":
    main()
