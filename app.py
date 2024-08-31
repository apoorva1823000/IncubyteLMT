import streamlit as st
from Library.libraryFunctions import LibraryFunctions

# library = LibraryFunctions()
if 'library' not in st.session_state:
    st.session_state.library = LibraryFunctions()

st.set_page_config(page_title="Library Management Tool",
                   layout="centered",
                   page_icon="https://img.icons8.com/?size=100&id=ADLVLEVwdHGD&format=png&color=000000",
                   initial_sidebar_state='auto',
                   menu_items={
                       'Get Help': 'https://apoorvaportfolio.netlify.app/',
                       'About': "This Streamlit app was created by Apoorva .S. Mehta as a part of the technical round "
                                "for the placement in Incubytes"
                   }
                   )

with st.sidebar:
    st.image("https://img.icons8.com/?size=100&id=QQWitn2kaDjj&format=png&color=000000")
    st.title("Library Manager")
    choice = st.radio(
        "Navigation",
        ["View", "Add", "Borrow", "Return"],
        key="navigation_radio"  # Unique key added here
    )
    st.info(
        "This application allows you to access Library and add, borrow, return or look through the available books."
    )


def app():
    library = st.session_state.library

    st.title("Library Management System")

    if choice == "Add":
        isbn = st.text_input("Enter ISBN")
        title = st.text_input("Enter Title")
        author = st.text_input("Enter Author")
        publication_year = st.text_input("Enter Publication Year")
        if st.button("Add Book"):
            result = library.add_book(isbn, title, author, publication_year)
            st.info(result)

    elif choice == "Borrow":
        isbn = st.text_input("Enter ISBN")
        if st.button("Borrow Book"):
            result = library.borrow_book(isbn)
            st.info(result)

    elif choice == "Return":
        isbn = st.text_input("Enter ISBN")
        if st.button("Return Book"):
            result = library.return_book(isbn)
            st.write(result)

    elif choice == "View":
        available_books_df = library.get_books_df()
        st.dataframe(available_books_df)


# Run the app function
if __name__ == "__main__":
    app()
