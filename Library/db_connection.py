import sqlite3
import threading
import time

class SQLiteConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = sqlite3.connect('library.db', check_same_thread=False)
                cls._instance.execute('PRAGMA busy_timeout = 30000')  # Set timeout to 30 seconds
                cls._instance.execute('''CREATE TABLE IF NOT EXISTS books (
                                         isbn TEXT PRIMARY KEY,
                                         title TEXT NOT NULL,
                                         author TEXT NOT NULL,
                                         publication_year TEXT NOT NULL,
                                         is_borrowed INTEGER DEFAULT 0)''')
                cls._instance.commit()
        return cls._instance

def get_db_connection():
    return SQLiteConnection()

def close_db(conn):
    """Close the SQLite database connection."""
    conn.close()

def execute_with_retry(query, params=(), retries=5, delay=1):
    """Execute a database query with retry on lock errors."""
    conn = get_db_connection()
    for _ in range(retries):
        try:
            conn.execute(query, params)
            conn.commit()
            return
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(delay)
            else:
                raise
        finally:
            close_db(conn)
    raise Exception("Failed to execute query after multiple retries")
