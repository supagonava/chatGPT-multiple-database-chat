# Example usage:
from services.postgresql_connection import PostgreSQLConnection


if __name__ == "__main__":
    db = PostgreSQLConnection(db_name="your_db_name", user="your_username", password="your_password", host="your_host", port=5432)  # Default is 'localhost'  # Default is 5432
    db.connect()

    # Create a sample table
    db.execute_query(
        """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    )
    """
    )

    # Insert a sample user
    db.execute_query("INSERT INTO users (name, email) VALUES (%s, %s)", ("John Doe", "john@example.com"))

    # Fetch and print all users
    users = db.fetch_all("SELECT * FROM users")
    for user in users:
        print(user)

    # Close the connection
    db.close()
