import streamlit as st
from Library.libraryFunctions import LibraryFunctions

# library = LibraryFunctions()
# State Management by Streamlit to manage session history
if 'library' not in st.session_state:
    st.session_state.library = LibraryFunctions()

# Set up the streamlit page
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

# Sidebar setup with options for adding, borrowing, returning and scouting through the library
with st.sidebar:
    st.image("https://img.icons8.com/?size=100&id=QQWitn2kaDjj&format=png&color=000000")
    st.title("Library Manager")
    choice = st.radio(
        "Navigation",
        ["View", "Add", "Borrow", "Return", "Delete"],
        key="navigation_radio"  # Unique key added here
    )
    st.info(
        "This application allows you to access Library and add, borrow, return or look through the available books."
    )


def app():
    library = st.session_state.library

    st.title("Library Management System")

    if choice == "Add":
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://img.icons8.com/?size=100&id=42690&format=png&color=000000")
        with col2:
            st.info("We are always happy to see our users donate new books for everyone to read and gain knowledge")
        isbn = st.text_input("Enter ISBN")
        title = st.text_input("Enter Title")
        author = st.text_input("Enter Author")
        publication_year = st.text_input("Enter Publication Year")
        if st.button("Add Book"):
            result = library.add_book(isbn, title, author, publication_year)
            st.info(result)

    elif choice == "Borrow":
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://img.icons8.com/?size=100&id=13199&format=png&color=000000")
        with col2:
            st.info("You can borrow various books as per your choice from here")
        isbn = st.text_input("Enter ISBN")
        if st.button("Borrow Book"):
            result = library.borrow_book(isbn)
            st.info(result)

    elif choice == "Return":
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://img.icons8.com/?size=100&id=13217&format=png&color=000000")
        with col2:
            st.info("Kindly timely return the books you've borrowed so that others can access the same too")
        borrowID = st.text_input("Enter the unique Book ID")
        if st.button("Return Book"):
            result = library.return_book(borrowID)
            st.info(result)

    elif choice == "View":
        col1,col2 = st.columns(2)
        with col1:
            st.image("https://img.icons8.com/?size=100&id=RXrON5kyN96A&format=png&color=000000")
        with col2:
            st.info("Here you get access to the whole catalogue of available books along with the info of them being "
                    "available or borrowed")
        available_books_df = library.get_books_df()
        if available_books_df.size==0:
            st.info("No books available currently")
        else:
            st.dataframe(available_books_df)

    elif choice == "Delete":
        col1,col2 = st.columns(2)
        with col1:
            st.image("https://img.icons8.com/?size=100&id=79kWwPwewtvH&format=png&color=000000")
        with col2:
            st.info("You can remove the book from the catalogue if its no more available in the library.")
        isbn = st.text_input("Enter ISBN")
        if st.button("Delete the book"):
            results = library.delete_book(isbn)
            st.info(results)

# Run the app function
if __name__ == "__main__":
    app()
