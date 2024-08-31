
# This test script is written to implement test cases on skiplist for insertion, search and deletion of elements

import pytest
from Library.skiplist import SkipList

def test_skiplist_insert_and_search():
    skip_list = SkipList(max_level=4)
    skip_list.insert(1, "Book 1")
    assert skip_list.search(1) == "Book 1"
    assert skip_list.search(2) is None

def test_skiplist_delete():
    skip_list = SkipList(max_level=4)
    skip_list.insert(1, "Book 1")
    skip_list.delete(1)
    assert skip_list.search(1) is None
