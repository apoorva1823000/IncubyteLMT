from Library.book import Book
from Library.skiplist import SkipList
import pandas as pd


class LibraryFunctions:
    def __init__(self):
        self.books = SkipList(max_level=4)

    def add_book(self, isbn, title, author, publication_year):
        if self.books.search(isbn):
            return "Book already exists."
        new_book = Book(isbn, title, author, publication_year)
        self.books.insert(isbn, new_book)
        return "Book added."

    def borrow_book(self, isbn):
        book = self.books.search(isbn)
        if book is None:
            return "No book found."
        if book.is_borrowed:
            return "Book already borrowed."
        book.is_borrowed = True
        return "Book borrowed."

    def return_book(self, isbn):
        book = self.books.search(isbn)
        if book is None:
            return "No book found."
        if not book.is_borrowed:
            return "Book was not borrowed."
        book.is_borrowed = False
        return "Book returned."

    def get_books_df(self) -> pd.DataFrame:
        # Extract data from skip list for displaying
        books = []
        current = self.books.header.forward[0]
        while current:
            books.append({
                "ISBN": current.key,
                "Title": current.value.title,
                "Author": current.value.author,
                "Publication Year": current.value.publication_year,
                "Available": "✔" if not current.value.is_borrowed else "",
                "Borrowed": "✔" if current.value.is_borrowed else ""
            })
            current = current.forward[0]
        return pd.DataFrame(books)
