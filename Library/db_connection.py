import sqlite3


def init_db():
    # Initializing the SQLite database and creating the necessary tables.
    conn = sqlite3.connect('Apoorva_Incubyte_library.db', check_same_thread=False)
    c = conn.cursor()

    # Create books table
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                 isbn TEXT PRIMARY KEY,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 publication_year TEXT NOT NULL,
                 is_borrowed INTEGER DEFAULT 0)''')

    # Create borrow table
    c.execute('''CREATE TABLE IF NOT EXISTS borrow (
                 borrow_id TEXT PRIMARY KEY,
                 isbn TEXT NOT NULL,
                 user_id TEXT NOT NULL,
                 borrow_date TEXT NOT NULL,
                 return_date TEXT,
                 FOREIGN KEY(isbn) REFERENCES books(isbn))''')

    conn.commit()
    return conn


def close_db(conn):
    # Closing the database connection.
    conn.close()
