import pytest
from Library.book import Book


def test_book_initialization():
    book = Book("1234567890", "The Great Book", "John Doe", "2024")
    assert book.isbn == "1234567890"
    assert book.title == "The Great Book"
    assert book.author == "John Doe"
    assert book.publication_year == "2024"
    assert not book.is_borrowed


def test_book_status():
    book = Book("1234567890", "The Great Book", "John Doe", "2024")
    book.is_borrowed = True
    assert str(book) == "The Great Book by John Doe (2024) - ISBN: 1234567890 [Borrowed]"
