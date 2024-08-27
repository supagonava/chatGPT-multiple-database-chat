import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from services.sqlite_connection import SQLiteConnection
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    db = SQLiteConnection(os.environ.get("SQLITE_DB_PATH", "database/chinook.db"))
    db.connect()

    # Fetch and print all users
    employees = db.fetch_all("select * from employees;")
    for employee in employees:
        print(employee)

    # Close the connection
    db.close()
