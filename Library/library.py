from Library.book import Book
from Library.skiplist import SkipList
class Library:
    def __init__(self):
        self.books = SkipList(max_level=4)
    pass