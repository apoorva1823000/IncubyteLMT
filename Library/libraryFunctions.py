from Library.book import Book
from Library.db_connection import init_db, close_db
import pandas as pd
import sqlite3
from datetime import datetime
import random

class LibraryFunctions:
    def __init__(self):
        self.conn = init_db()
        self.cursor = self.conn.cursor()

    def generate_user_id(self):
        # Generate a unique user ID (for example, combining ISBN with a unique hash)
        return f"{random.randint(1000, 9999)}"

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

    # def borrow_book(self, isbn):
    #     self.cursor.execute("SELECT is_borrowed, title FROM books WHERE isbn = ?", (isbn,))
    #     result = self.cursor.fetchone()
    #     if result:
    #         is_borrowed, title = result
    #         if is_borrowed:
    #             return "Book already borrowed."
    #         else:
    #             self.cursor.execute("UPDATE books SET is_borrowed = 1 WHERE isbn = ?", (isbn,))
    #             self.conn.commit()
    #             return "Book borrowed. Happy Learning !"
    #     else:
    #         return "No book found."
    def borrow_book(self, isbn):
        self.cursor.execute("SELECT is_borrowed, title FROM books WHERE isbn = ?", (isbn,))
        result = self.cursor.fetchone()
        if result:
            is_borrowed, title = result
            if is_borrowed:
                return "Book already borrowed."
            else:
                # Generate a unique user_id for this borrow operation
                user_id = self.generate_user_id()
                borrow_id = f"{isbn}_{user_id}"
                borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Insert into borrow table
                self.cursor.execute("INSERT INTO borrow (borrow_id, isbn, user_id, borrow_date) VALUES (?, ?, ?, ?)",
                                    (borrow_id, isbn, user_id, borrow_date))
                self.cursor.execute("UPDATE books SET is_borrowed = 1 WHERE isbn = ?", (isbn,))
                self.conn.commit()
                return (f"Book borrowed. Happy Learning! Your borrow ID is {borrow_id}. "
                        f"Kindly remember or save the borrow ID as it will be required while returning the book")
        else:
            return "No book found."

    # def return_book(self, isbn):
    #     self.cursor.execute("SELECT is_borrowed, title FROM books WHERE isbn = ?", (isbn,))
    #     result = self.cursor.fetchone()
    #     if result:
    #         is_borrowed, title = result
    #         if not is_borrowed:
    #             return "Book was not borrowed."
    #         else:
    #             self.cursor.execute("UPDATE books SET is_borrowed = 0 WHERE isbn = ?", (isbn,))
    #             self.conn.commit()
    #             return "Book returned. Thank You !"
    #     else:
    #         return "No book found."

    def return_book(self, borrow_id):
        # Extract ISBN and user_id from borrow_id
        try:
            isbn, user_id = borrow_id.split('_', 1)
        except:
            return "Wrong ID"

        # Check if the book was borrowed by this user
        self.cursor.execute(
            "SELECT user_id, is_borrowed FROM borrow JOIN books ON borrow.isbn = books.isbn WHERE borrow.borrow_id = "
            "? AND return_date IS NULL",
            (borrow_id,))
        result = self.cursor.fetchone()
        if result:
            record_user_id, is_borrowed = result
            if record_user_id != user_id:
                return "This book was borrowed by another user. You cannot return it."
            if not is_borrowed:
                return "Book was not borrowed."
            else:
                return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute("UPDATE books SET is_borrowed = 0 WHERE isbn = ?", (isbn,))
                self.cursor.execute("UPDATE borrow SET return_date = ? WHERE borrow_id = ?", (return_date, borrow_id))
                self.conn.commit()
                return "Book returned. Thank You!"
        else:
            return "No matching borrow record found."

    def delete_book(self, isbn):
        if not isbn:
            return "Kindly enter the ISBN number"
        self.cursor.execute("SELECT is_borrowed, title FROM books WHERE isbn = ?", (isbn,))
        result = self.cursor.fetchone()
        if result:
            is_borrowed, title = result
            if is_borrowed:
                return "Book already borrowed. Cannot be deleted until returned"
            else:
                try:
                    self.cursor.execute("DELETE FROM books WHERE isbn=?", (isbn,))
                    self.conn.commit()
                    # Check if any rows were affected
                    if self.cursor.rowcount == 0:
                        return "Book Not Found"
                    return "Book Deleted Successfully"
                except sqlite3.Error as e:
                    # Handling other possible exceptions
                    return f"An error occurred: {str(e)}"

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
