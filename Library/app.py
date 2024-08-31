import streamlit as st
from Library.libraryFunctions import LibraryFunctions

library = LibraryFunctions()

st.title("Library Management System")

choice = st.sidebar.radio("Navigation", ["View", "Add", "Borrow", "Return"])

if choice == "Add":
    isbn = st.text_input("Enter ISBN")
    title = st.text_input("Enter Title")
    author = st.text_input("Enter Author")
    publication_year = st.text_input("Enter Publication Year")
    if st.button("Add Book"):
        result = library.add_book(isbn, title, author, publication_year)
        st.write(result)

elif choice == "Borrow":
    isbn = st.text_input("Enter ISBN")
    if st.button("Borrow Book"):
        result = library.borrow_book(isbn)
        st.write(result)

elif choice == "Return":
    isbn = st.text_input("Enter ISBN")
    if st.button("Return Book"):
        result = library.return_book(isbn)
        st.write(result)

elif choice == "View":
    st.write("Here you can view available books and their statuses.")
    # Implement viewing functionality here
