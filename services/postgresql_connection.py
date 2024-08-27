import psycopg2
from psycopg2 import sql, OperationalError
from psycopg2.extensions import connection as Connection, cursor as Cursor


class PostgreSQLConnection:
    def __init__(self, db_name: str, user: str, password: str, host: str = "localhost", port: int = 5432):
        """Initialize the connection to the PostgreSQL database."""
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection: Connection | None = None
        self.cursor: Cursor | None = None

    def connect(self):
        """Connect to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host, port=self.port)
            self.cursor = self.connection.cursor()
            print(f"Connected to the PostgreSQL database {self.db_name} at {self.host}:{self.port}")
        except OperationalError as e:
            print(f"Error connecting to the database: {e}")
            raise

    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query with optional parameters."""
        if not self.cursor:
            raise ConnectionError("Database connection is not established.")

        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print(f"Query executed successfully: {query}")
        except psycopg2.Error as e:
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
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
        else:
            print("No connection to close.")
