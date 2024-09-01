# Library Management System
This is a Library Management System built as a part of technical round for placement in Incubytes.
<br>This is a streamlit web app that can be accessed either by cloning the repository or via link provided below:
<br>Access = [LMT](https://incubyte-lmt.streamlit.app/)

# About
This LMT features adding new books to the library, viewing them, borrowing as well as returning the books too.
<br>The datastructure used here is a skiplist for faster transactions with increased users. 
<br>The database used is SQLite for easier and lite data handling.
<br>The test cases included in the repositories ensure TDD method being followed while constructing the project.
<br>The LMT provides you with options to view the available books, add any new book, borrow the same and return as well as delete if the book is unavailable now. The borrower receives a unique ID each time he borrows the book to ensure authenticity of the one who wishes to return the book i.e. only the borrower can return the book not anyone else.
<br>Choose the appropriate option from the side bar to perform the functionality 

# Cloning the repository
To clone this repository you can fetch the repo link from "<>Code" section and clone this repository using 
<br>
```bash
git clone https://github.com/apoorva1823000/IncubyteLMT.git
```
<br>Download the requirements mentioned in the requirements.txt to run the project
<br> Once you've installed the requirements open the terminal and run 
```python
streamlit run app.py
```
This will start a localhost network and run the streamlit webapp

