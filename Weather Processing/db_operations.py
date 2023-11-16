import sqlite3
from DBCM import DBCM

class DBOperations:
    """The DB operations class."""

    def __init__(self):
        """Setup the context manager, taking a parameter for the name."""
        try:
            self.db_name = "database_name"
            self.database_context = DBCM(self.db_name)
            self.conn = None
            self.cursor = None
        except sqlite3.DatabaseError as error:
            print("Error initalizing DB: ", error)

    def fetch_data(self):
        """Fetch the current data in the database."""
        with self.database_context as cursor:
            cursor.execute("SELECT * FROM samples")
            data = cursor.fetchall()
            print("Current data:")
            for row in data:
                print(row)

    def save_data(self):
        """Save new data to the database."""
        with self.database_context as cursor:
            for date, data in weather.items():
                cursor.execute(
                    "INSERT INTO samples (date, location, min_temp, max_temp, avg_temp) VALUES (?, ?, ?, ?, ?)",
                    (date, "Winnipeg, MB", data["Min"], data["Max"], data["Mean"]),
                )
            print("Sample data inserted successfully.")

    def initialize_db(self):
        """Initialize the database."""
        with self.database_context as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS samples (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sample_date TEXT NOT NULL, location TEXT NOT NULL, min_temp REAL NOT NULL, max_temp REAL NOT NULL, avg_temp REAL NOT NULL)"
            )

    def purge_data(self):
        """Remove all data from the database."""
        with self.database_context as cursor:
            cursor.execute("DELETE FROM samples")
            print("Data deleted from samples table.")
