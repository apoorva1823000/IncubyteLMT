# This test script is for implementing functionalities in the libraryFunctions file to test the add, borrow, return features of the libraryFunction file

import pytest
from Library.libraryFunctions import LibraryFunctions


def test_add_book():
    library = LibraryFunctions()
    result = library.add_book("1234567890", "It Starts With Us", "Collen Hoover", "2022")
    assert result == "Book added."
    assert library.books.search("1234567890") is not None


def test_borrow_book():
    library = LibraryFunctions()
    library.add_book("1234567890", "The Great Book", "John Doe", "2024")
    result = library.borrow_book("1234567890")
    assert result == "Book borrowed."
    assert library.books.search("1234567890").is_borrowed


def test_return_book():
    library = LibraryFunctions()
    library.add_book("1234567890", "The Great Book", "John Doe", "2024")
    library.borrow_book("1234567890")
    result = library.return_book("1234567890")
    assert result == "Book returned."
    assert not library.books.search("1234567890").is_borrowed
