"""
Example usage of the DB Knih API.
"""
from db_knih_api import db_knih


def main():
    """Demonstrate the API usage."""
    print("DB Knih API Example")
    print("=" * 50)
    
    # Search for books
    print("\n1. Searching for 'harry potter'...")
    search_results = db_knih.search("harry potter")
    
    if search_results:
        print(f"Found {len(search_results)} books:")
        for i, book in enumerate(search_results[:3], 1):  # Show first 3 results
            print(f"  {i}. {book.name} ({book.year}) by {book.author}")
            print(f"     ID: {book.id}, Clean name: {book.cleanName}")
        
        # Get detailed info for the first book
        if search_results:
            first_book = search_results[0]
            print(f"\n2. Getting detailed info for '{first_book.name}'...")
            
            # Use the clean name and ID to get detailed info
            book_link = f"{first_book.cleanName}-{first_book.id}"
            detailed_info = db_knih.get_book_info(book_link)
            
            if detailed_info:
                print(f"   Plot: {detailed_info.plot[:100]}..." if detailed_info.plot else "   Plot: Not available")
                print(f"   Genres: {', '.join(detailed_info.genres) if detailed_info.genres else 'Not available'}")
                print(f"   Year: {detailed_info.year}")
                print(f"   Publisher: {detailed_info.publisher}")
                print(f"   Rating: {detailed_info.rating}%")
                print(f"   Number of ratings: {detailed_info.numberOfRatings}")
                print(f"   Pages: {detailed_info.pages}")
                print(f"   Original language: {detailed_info.originalLanguage}")
                print(f"   ISBN: {detailed_info.isbn}")
                print(f"   Cover: {detailed_info.cover}")
                
                if detailed_info.reviews:
                    print(f"   Reviews ({len(detailed_info.reviews)}):")
                    for review in detailed_info.reviews[:2]:  # Show first 2 reviews
                        print(f"     - {review.username}: {review.rating}/5 stars")
                        if review.text:
                            print(f"       \"{review.text[:50]}...\"")
            else:
                print("   Failed to get detailed information")
    else:
        print("No books found")


if __name__ == "__main__":
    main()
