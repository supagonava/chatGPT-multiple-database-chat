import sqlite3
from sqlite3 import Connection, Cursor


class SQLiteConnection:
    def __init__(self, db_path: str):
        """Initialize the connection to the SQLite database."""
        self.db_path = db_path
        self.connection: Connection | None = None
        self.cursor: Cursor | None = None

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print(f"Connected to the database at {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query with optional parameters."""
        if not self.cursor:
            raise ConnectionError("Database connection is not established.")

        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print(f"Query executed successfully: {query}")
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise

    def fetch_all(self, query: str, params: tuple = ()) -> list:
        """Execute a query and fetch all results."""
        if not self.cursor:
            raise ConnectionError("Database connection is not established.")

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
        else:
            print("No connection to close.")
