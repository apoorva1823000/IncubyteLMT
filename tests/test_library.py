import pytest
from Library.libraryFunctions import LibraryFunctions


def test_add_book():
    library = LibraryFunctions()
    result = library.add_book("1234567890", "It Starts With Us", "Colleen Hoover", "2022")
    assert result == "Book added."

    # Verifying if the book was added to the database
    books_df = library.get_books_df()
    assert not books_df[books_df['ISBN'] == "1234567890"].empty


def test_borrow_book():
    library = LibraryFunctions()
    library.add_book("1234567890", "The Great Book", "John Doe", "2024")

    # Borrowing the book
    result = library.borrow_book("1234567890")

    # Verifying the result and borrow status
    assert "Book borrowed." in result

    # Extracting borrow_id from the result message
    borrow_id = result.split("ID is ")[1].split('.')[0]

    # Verifying the borrow record in the `borrow` table
    library.cursor.execute("SELECT * FROM borrow WHERE borrow_id = ?", (borrow_id,))
    borrow_record = library.cursor.fetchone()
    assert borrow_record is not None
    assert borrow_record[1] == "1234567890"  # ISBN
    assert borrow_record[3] is not None  # Borrow date should be set


def test_return_book():
    library = LibraryFunctions()
    library.add_book("1234567890", "The Great Book", "John Doe", "2024")

    # Borrow the book first to generate a borrow_id
    borrow_result = library.borrow_book("1234567890")
    borrow_id = borrow_result.split("ID is ")[1].split('.')[0]

    # Returning the book
    return_result = library.return_book(borrow_id)

    # Verifying the result and return status
    assert return_result == "Book returned. Thank You!"

    # Check if the book is marked as not borrowed in `books` table
    library.cursor.execute("SELECT is_borrowed FROM books WHERE isbn = ?", ("1234567890",))
    is_borrowed = library.cursor.fetchone()[0]
    assert is_borrowed == 0

    # Verify if the `return_date` is set in the `borrow` table
    library.cursor.execute("SELECT return_date FROM borrow WHERE borrow_id = ?", (borrow_id,))
    return_date = library.cursor.fetchone()[0]
    assert return_date is not None

