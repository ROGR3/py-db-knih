"""
Data models for the DB Knih API.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Review:
    """Represents a book review."""
    text: Optional[str] = None
    rating: Optional[float] = None
    username: Optional[str] = None
    date: Optional[str] = None


@dataclass
class BookInfo:
    """Represents detailed book information."""
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    year: Optional[int] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    rating: Optional[float] = None
    numberOfRatings: Optional[int] = None
    reviews: Optional[List[Review]] = None
    cover: Optional[str] = None
    pages: Optional[int] = None
    originalLanguage: Optional[str] = None
    isbn: Optional[str] = None


@dataclass
class SearchInfo:
    """Represents basic book information from search results."""
    name: Optional[str] = None
    cleanName: Optional[str] = None
    id: Optional[int] = None
    year: Optional[int] = None
    author: Optional[str] = None
