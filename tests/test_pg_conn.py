import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from services.postgresql_connection import PostgreSQLConnection
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    db = PostgreSQLConnection(
        db_name=os.environ.get("POSTGRES_DB_NAME", "northwind"),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=5432,
    )

    db.connect()
    customers = db.fetch_all('SELECT * FROM "customers" WHERE "company_name"::TEXT LIKE %s ORDER BY "customer_id";', ("An%",))
    for customer in customers:
        print(customer)
    db.close()
