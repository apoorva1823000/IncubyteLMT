from book import Book
from skiplist import SkipList


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
