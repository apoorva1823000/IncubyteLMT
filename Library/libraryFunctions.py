import sqlite3

from Library.db_connection import execute_with_retry, get_db_connection, close_db
import pandas as pd


class LibraryFunctions:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def add_book(self, isbn, title, author, publication_year):
        if not isbn or not title or not author or not publication_year:
            return "Kindly fill all the fields."

        query = "INSERT INTO books (isbn, title, author, publication_year) VALUES (?, ?, ?, ?)"
        try:
            execute_with_retry(query, (isbn, title, author, publication_year))
            return "Book added successfully."
        except sqlite3.IntegrityError:
            return "Book with this ISBN already exists."

    def borrow_book(self, isbn):
        query = "SELECT is_borrowed, title FROM books WHERE isbn = ?"
        self.cursor.execute(query, (isbn,))
        result = self.cursor.fetchone()
        if result:
            is_borrowed, title = result
            if is_borrowed:
                return "Book already borrowed."
            else:
                update_query = "UPDATE books SET is_borrowed = 1 WHERE isbn = ?"
                execute_with_retry(update_query, (isbn,))
                return "Book borrowed successfully. Happy learning!"
        else:
            return "No book found with this ISBN."

    def return_book(self, isbn):
        query = "SELECT is_borrowed, title FROM books WHERE isbn = ?"
        self.cursor.execute(query, (isbn,))
        result = self.cursor.fetchone()
        if result:
            is_borrowed, title = result
            if not is_borrowed:
                return "Book was not borrowed."
            else:
                update_query = "UPDATE books SET is_borrowed = 0 WHERE isbn = ?"
                execute_with_retry(update_query, (isbn,))
                return "Book returned successfully. Thank you!"
        else:
            return "No book found with this ISBN."

    def delete_book(self, isbn):
        if not isbn:
            return "Kindly enter the ISBN number."

        delete_query = "DELETE FROM books WHERE isbn = ?"
        result = execute_with_retry(delete_query, (isbn,))
        if result == 0:
            return "Book not found."
        return "Book deleted successfully."

    def get_books_df(self) -> pd.DataFrame:
        """Get a DataFrame of all books in the library."""
        query = "SELECT isbn, title, author, publication_year, is_borrowed FROM books"
        self.cursor.execute(query)
        books = self.cursor.fetchall()

        books_list = []
        for isbn, title, author, publication_year, is_borrowed in books:
            books_list.append({
                "ISBN": isbn,
                "Title": title,
                "Author": author,
                "Publication Year": publication_year,
                "Available": "✔" if not is_borrowed else "",
                "Borrowed": "✔" if is_borrowed else ""
            })
        return pd.DataFrame(books_list)

    def __del__(self):
        close_db(self.conn)
