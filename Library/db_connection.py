import sqlite3


def init_db():
    # Initializing the SQLite database and create the books table if it doesn't exist.
    conn = sqlite3.connect('library.db',check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                 isbn TEXT PRIMARY KEY,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 publication_year TEXT NOT NULL,
                 is_borrowed INTEGER DEFAULT 0)''')
    conn.commit()
    return conn


def close_db(conn):
    # Closing the database connection.
    conn.close()
