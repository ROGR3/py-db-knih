# DB Knih API - Python

A Python library for scraping book information from [databazeknih.cz](https://www.databazeknih.cz), the Czech book database.

This is a Python port of the original TypeScript implementation, designed with unit-testable code and clean architecture.

## Features

- **Search Books**: Search for books by title, author, or any text
- **Detailed Book Information**: Get comprehensive book details including:
  - Plot summary
  - Genres
  - Publication year and publisher
  - User ratings and reviews
  - Cover image
  - Page count, ISBN, original language
- **Unit Testable**: All parsing logic is thoroughly tested
- **Clean Architecture**: Modular design with separate services for different functionalities

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```python
from __init__ import db_knih

# Search for books
search_results = db_knih.search("harry potter")
print(f"Found {len(search_results)} books")

for book in search_results[:3]:  # Show first 3 results
    print(f"- {book.name} ({book.year}) by {book.author}")
    print(f"  ID: {book.id}, Clean name: {book.cleanName}")

# Get detailed information for a book
if search_results:
    first_book = search_results[0]
    book_link = f"{first_book.cleanName}-{first_book.id}"
    detailed_info = db_knih.get_book_info(book_link)
    
    if detailed_info:
        print(f"Plot: {detailed_info.plot}")
        print(f"Genres: {', '.join(detailed_info.genres) if detailed_info.genres else 'N/A'}")
        print(f"Rating: {detailed_info.rating}%")
        print(f"Pages: {detailed_info.pages}")
```

### Advanced Usage

```python
from book_service import BookService
from search_service import SearchService
from fetcher import Fetcher

# Use services independently
search_service = SearchService()
book_service = BookService()

# Or with custom fetcher (useful for testing)
custom_fetcher = Fetcher()
search_service = SearchService(custom_fetcher)
book_service = BookService(custom_fetcher)
```

## Data Models

### SearchInfo
Basic book information from search results:
- `name`: Book title
- `cleanName`: URL-friendly book name
- `id`: Unique book ID
- `year`: Publication year
- `author`: Author name

### BookInfo
Detailed book information:
- `plot`: Book summary/plot
- `genres`: List of genres
- `year`: Publication year
- `publisher`: Publisher name
- `rating`: Average user rating (percentage)
- `numberOfRatings`: Number of user ratings
- `reviews`: List of user reviews (up to 5)
- `cover`: Cover image URL
- `pages`: Number of pages
- `originalLanguage`: Original language
- `isbn`: ISBN number

### Review
User review information:
- `text`: Review text
- `rating`: User's rating (1-5 stars)
- `username`: Reviewer's username
- `date`: Review date

## Testing

The codebase includes comprehensive unit tests for all parsing logic and regexes:

```bash
# Run all tests
python -m pytest test_*.py -v

# Run specific test file
python -m pytest test_book_service.py -v

# Run with coverage
python -m pytest test_*.py --cov=. --cov-report=html
```

### Test Coverage

The tests cover:
- **Fetcher**: HTTP requests, URL generation, error handling
- **BookService**: HTML parsing, data extraction, regex patterns
- **SearchService**: Search result parsing, book route extraction
- **Main API**: Integration between services

## Architecture

The code is organized into several modules:

- **`models.py`**: Data classes for type safety
- **`fetcher.py`**: HTTP client with proper headers and error handling
- **`book_service.py`**: Detailed book information extraction
- **`search_service.py`**: Book search functionality
- **`__init__.py`**: Main API class that combines services

## Error Handling

The library handles various error conditions gracefully:
- Network errors return 'Error' string
- Missing HTML elements return `None` or empty lists
- Invalid data is safely converted (e.g., non-numeric strings to 0)
- All methods are designed to not raise exceptions

## Dependencies

- `requests`: HTTP client
- `beautifulsoup4`: HTML parsing
- `lxml`: Fast XML/HTML parser
- `pytest`: Testing framework
- `pytest-mock`: Mocking utilities for tests

## Example Output

```
DB Knih API Example
==================================================

1. Searching for 'harry potter'...
Found 30 books:
  1. Harry Potter (None) by None
     ID: 572730, Clean name: potterovsky-pruvodce-mini-potterovky-harry-potter
  2. Harry Potter a Fénixův řád (None) by None
     ID: 13, Clean name: harry-potter-harry-potter-a-fenixuv-rad

2. Getting detailed info for 'Harry Potter'...
   Plot: Not available
   Genres: Not available
   Year: None
   Publisher: None
   Rating: None%
   Number of ratings: None
   Pages: 32.0
   Original language: None
   ISBN: None
   Cover: https://www.databazeknih.cz/img/books/57_/572730/bmid_harry-potter.jpg?v=1752940477
```

## License

MIT License - see the original TypeScript project for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Notes

- This library is for educational and personal use only
- Please respect the website's terms of service and robots.txt
- Consider adding delays between requests to be respectful to the server
- The website structure may change, which could break the parsing logic
