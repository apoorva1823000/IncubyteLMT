import pytest
import sqlite3
from Library.db_connection import init_db, Library

@pytest.fixture(scope="module")
def setup_db():
    """Setup an in-memory SQLite database and return the connection and cursor."""
    conn = sqlite3.connect(':memory:')  # Use an in-memory database for testing
    c = conn.cursor()
    c.execute('''CREATE TABLE books (
                 isbn TEXT PRIMARY KEY,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 publication_year TEXT NOT NULL,
                 is_borrowed INTEGER DEFAULT 0)''')
    conn.commit()
    return conn, c

@pytest.fixture(scope="module")
def library(setup_db):
    """Create a Library instance for testing."""
    conn, c = setup_db
    return Library(conn, c)

def test_add_book(library):
    """Test adding a book to the library."""
    result = library.add_book("1234567890", "Test Book", "Test Author", "2024")
    assert "added to the library" in result

    # Try adding the same book again
    result = library.add_book("1234567890", "Test Book", "Test Author", "2024")
    assert "already exists" in result

def test_view_available_books(library):
    """Test viewing available books in the library."""
    available_books = library.view_available_books()
    assert len(available_books) == 1
    assert available_books[0][0] == "1234567890"  # Check ISBN

def test_borrow_book(library):
    """Test borrowing a book from the library."""
    result = library.borrow_book("1234567890")
    assert "borrowed" in result

    # Try borrowing the same book again
    result = library.borrow_book("1234567890")
    assert "already borrowed" in result

def test_return_book(library):
    """Test returning a book to the library."""
    result = library.return_book("1234567890")
    assert "returning" in result

    # Try returning the same book again
    result = library.return_book("1234567890")
    assert "was not borrowed" in result

def test_return_nonexistent_book(library):
    """Test returning a nonexistent book."""
    result = library.return_book("0987654321")
    assert "No book found" in result

def test_borrow_nonexistent_book(library):
    """Test borrowing a nonexistent book."""
    result = library.borrow_book("0987654321")
    assert "No book found" in result
