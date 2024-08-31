# db_connection.py

import sqlite3

def init_db():
    # Initializing the SQLite database and creating the books table if it doesn't exist.
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                     isbn TEXT PRIMARY KEY,
                     title TEXT NOT NULL,
                     author TEXT NOT NULL,
                     publication_year TEXT NOT NULL,
                     is_borrowed INTEGER DEFAULT 0)''')
    conn.commit()
    return conn, c

class Library:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def add_book(self, isbn, title, author, publication_year):
        try:
            self.cursor.execute("INSERT INTO books (isbn, title, author, publication_year) VALUES (?, ?, ?, ?)",
                                (isbn, title, author, publication_year))
            self.conn.commit()
            return f"Book '{title}' added to the library."
        except sqlite3.IntegrityError:
            return f"Book with ISBN {isbn} already exists."

    def borrow_book(self, isbn):
        self.cursor.execute("SELECT is_borrowed, title FROM books WHERE isbn = ?", (isbn,))
        result = self.cursor.fetchone()
        if result:
            is_borrowed, title = result
            if is_borrowed:
                return f"Sorry, the book '{title}' is already borrowed."
            else:
                self.cursor.execute("UPDATE books SET is_borrowed = 1 WHERE isbn = ?", (isbn,))
                self.conn.commit()
                return f"You have borrowed '{title}'."
        else:
            return f"No book found with ISBN {isbn}."

    def return_book(self, isbn):
        self.cursor.execute("SELECT is_borrowed, title FROM books WHERE isbn = ?", (isbn,))
        result = self.cursor.fetchone()
        if result:
            is_borrowed, title = result
            if not is_borrowed:
                return f"The book '{title}' was not borrowed."
            else:
                self.cursor.execute("UPDATE books SET is_borrowed = 0 WHERE isbn = ?", (isbn,))
                self.conn.commit()
                return f"Thank you for returning '{title}'."
        else:
            return f"No book found with ISBN {isbn}."