import pytest
from unittest.mock import patch
import streamlit as st
from app import app  # Import the app function
from Library.libraryFunctions import LibraryFunctions

# Test Add Book functionality
def test_add_book(monkeypatch):
    # Mock Streamlit inputs
    monkeypatch.setattr('streamlit.text_input', lambda label: "1234567890" if "ISBN" in label else "The Great Book" if "Title" in label else "John Doe" if "Author" in label else "2024")
    monkeypatch.setattr('streamlit.button', lambda label: True)

    # Mock the add_book method of the Library class
    with patch.object(st.session_state.library, 'add_book', return_value="Book added.") as mock_add_book:
        app()
        mock_add_book.assert_called_once_with("1234567890", "The Great Book", "John Doe", "2024")
        assert st.session_state.library.books.search("1234567890").title == "The Great Book"

# Test Borrow Book functionality
def test_borrow_book(monkeypatch):
    # First, add a book to the library
    st.session_state.library.add_book("1234567890", "The Great Book", "John Doe", "2024")

    # Mock Streamlit inputs
    monkeypatch.setattr('streamlit.text_input', lambda label: "1234567890")
    monkeypatch.setattr('streamlit.button', lambda label: True)

    # Mock the borrow_book method of the Library class
    with patch.object(st.session_state.library, 'borrow_book', return_value="Book borrowed.") as mock_borrow_book:
        app()
        mock_borrow_book.assert_called_once_with("1234567890")
        assert st.session_state.library.books.search("1234567890").is_borrowed

# Test Return Book functionality
def test_return_book(monkeypatch):
    # First, add and borrow a book
    st.session_state.library.add_book("1234567890", "The Great Book", "John Doe", "2024")
    st.session_state.library.borrow_book("1234567890")

    # Mock Streamlit inputs
    monkeypatch.setattr('streamlit.text_input', lambda label: "1234567890")
    monkeypatch.setattr('streamlit.button', lambda label: True)

    # Mock the return_book method of the Library class
    with patch.object(st.session_state.library, 'return_book', return_value="Book returned.") as mock_return_book:
        app()
        mock_return_book.assert_called_once_with("1234567890")
        assert not st.session_state.library.books.search("1234567890").is_borrowed

# Test View Books functionality
def test_view_books(monkeypatch):
    # Add books to the library
    st.session_state.library.add_book("1234567890", "The Great Book", "John Doe", "2024")
    st.session_state.library.add_book("0987654321", "Another Book", "Jane Smith", "2023")

    # Mock Streamlit inputs
    monkeypatch.setattr('streamlit.radio', lambda label, options: "View")

    # Run the app and test output
    app()
    available_books_df = st.session_state.library.get_books_df()

    assert len(available_books_df) == 2
    assert available_books_df.loc[available_books_df["ISBN"] == "1234567890", "Title"].values[0] == "The Great Book"
    assert available_books_df.loc[available_books_df["ISBN"] == "0987654321", "Title"].values[0] == "Another Book"
