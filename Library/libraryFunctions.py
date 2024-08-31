from Library.book import Book
from Library.db_connection import init_db, close_db
import pandas as pd
import sqlite3

class LibraryFunctions:
    def __init__(self):
        self.conn = init_db()
        self.cursor = self.conn.cursor()

    def add_book(self, isbn, title, author, publication_year):
        if not isbn or not title or not author or not publication_year:
            return "Kindly Fill the form"
        try:
            self.cursor.execute("INSERT INTO books (isbn, title, author, publication_year) VALUES (?, ?, ?, ?)",
                                (isbn, title, author, publication_year))
            self.conn.commit()
            return "Book added."
        except sqlite3.IntegrityError:
            return "Book already exists."

    def borrow_book(self, isbn):
        self.cursor.execute("SELECT is_borrowed, title FROM books WHERE isbn = ?", (isbn,))
        result = self.cursor.fetchone()
        if result:
            is_borrowed, title = result
            if is_borrowed:
                return "Book already borrowed."
            else:
                self.cursor.execute("UPDATE books SET is_borrowed = 1 WHERE isbn = ?", (isbn,))
                self.conn.commit()
                return "Book borrowed."
        else:
            return "No book found."

    def return_book(self, isbn):
        self.cursor.execute("SELECT is_borrowed, title FROM books WHERE isbn = ?", (isbn,))
        result = self.cursor.fetchone()
        if result:
            is_borrowed, title = result
            if not is_borrowed:
                return "Book was not borrowed."
            else:
                self.cursor.execute("UPDATE books SET is_borrowed = 0 WHERE isbn = ?", (isbn,))
                self.conn.commit()
                return "Book returned."
        else:
            return "No book found."

    def get_books_df(self) -> pd.DataFrame:
        # Geting all books as a pandas DataFrame.
        self.cursor.execute("SELECT isbn, title, author, publication_year, is_borrowed FROM books")
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
