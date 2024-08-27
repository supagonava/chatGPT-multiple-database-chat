# Example usage:
from services.sqlite_connection import SQLiteConnection


if __name__ == "__main__":
    db = SQLiteConnection("example.db")
    db.connect()

    # Create a sample table
    db.execute_query(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    """
    )

    # Insert a sample user
    db.execute_query("INSERT INTO users (name, email) VALUES (?, ?)", ("John Doe", "john@example.com"))

    # Fetch and print all users
    users = db.fetch_all("SELECT * FROM users")
    for user in users:
        print(user)

    # Close the connection
    db.close()
