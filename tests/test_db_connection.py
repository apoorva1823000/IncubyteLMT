# test_db_connection.py

import pytest
import sqlite3
from Library.db_connection import init_db, close_db

@pytest.fixture
def db_connection():
    """Fixture to set up and tear down a test database."""
    # Initialize the database
    conn = init_db()
    yield conn
    # Clean up the database
    conn.close()
    # Optionally, remove the test database file if needed
    import os
    if os.path.exists('Apoorva_Incubyte_library.db'):
        os.remove('Apoorva_Incubyte_library.db')

def test_init_db(db_connection):
    """Test the database initialization."""
    # Check if the database file is created
    assert db_connection is not None

    # Check if the books table is created
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books';")
    table_exists = cursor.fetchone() is not None
    assert table_exists

def test_create_books_table(db_connection):
    """Test if the books table exists and has the correct columns."""
    cursor = db_connection.cursor()
    cursor.execute("PRAGMA table_info(books);")
    columns = [column[1] for column in cursor.fetchall()]

    expected_columns = {'isbn', 'title', 'author', 'publication_year', 'is_borrowed'}
    assert set(columns) == expected_columns

def test_close_db(db_connection):
    """Test the database connection close function."""
    close_db(db_connection)
    # Attempt to execute a query after closing the connection should raise an error
    with pytest.raises(sqlite3.ProgrammingError):
        cursor = db_connection.cursor()
        cursor.execute("SELECT 1;")
