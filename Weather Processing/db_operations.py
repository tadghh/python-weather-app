"""Handles all database operations."""

import sqlite3
from dbcm import DBCM


class DBOperations:
    """The DB operations class."""

    def __init__(self):
        """Setup the context manager, taking a parameter for the name."""
        try:
            self.db_name = "weather_data"
            self.database_context = DBCM(self.db_name)
            self.conn = None
            self.cursor = None
        except sqlite3.DatabaseError as error:
            print("Error initializing DB: ", error)

    def initialize_db(self):
        """Initialize the database."""
        with self.database_context as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                sample_date TEXT NOT NULL,
                location TEXT NOT NULL,
                min_temp REAL NOT NULL,
                max_temp REAL NOT NULL,
                avg_temp REAL NOT NULL
                )"""
            )

    def fetch_data(self, start_year="", end_year=""):
        """Fetch the current data in the database."""
        # TODO: Scenario when there is no database
        try:
            with self.database_context as cursor:
                if start_year == "" and end_year == "":
                    cursor.execute("SELECT * FROM weather")
                else:
                    if start_year.isdigit() and end_year.isdigit():
                        cursor.execute(
                            f"SELECT * FROM weather WHERE strftime('%Y', sample_date) BETWEEN '{start_year}' AND '{end_year}'"
                        )
                    else:
                        raise ValueError("Year values must be digits")

                data = cursor.fetchall()
                # print(f"Current data:{data}")
                # for row in data:
                #     print(row)

                return data
        except ValueError as error:
            print(error)

        return None

    def save_data(self, data_to_save):
        """Save new data to the database."""
        # TODO: Scenario when there is no db, Secnario where data is duplicated
        with self.database_context as cursor:
            for date, data in data_to_save.items():
                min_temp = data.get("Min")
                max_temp = data.get("Max")
                avg_temp = data.get("Mean")
                location = "Winnipeg, MB"

                cursor.execute(
                    "INSERT INTO weather (sample_date, location, min_temp, max_temp, avg_temp) VALUES (?, ?, ?, ?, ?)",
                    (date, location, min_temp, max_temp, avg_temp),
                )
            print("Sample data inserted successfully.")

    def purge_data(self):
        """Remove all data from the database."""
        with self.database_context as cursor:
            cursor.execute("DELETE FROM weather")
            print("Data deleted from weather table.")


if __name__ == "__main__":
    weather = {
        "2018-06-01": {"Max": 12.0, "Min": 5.6, "Mean": 7.1},
        "2018-06-02": {"Max": 22.2, "Min": 11.1, "Mean": 15.5},
        "2018-06-03": {"Max": 31.3, "Min": 29.9, "Mean": 30.0},
        "2017-06-01": {"Max": 12.0, "Min": 5.6, "Mean": 7.1},
        "2017-05-02": {"Max": 22.2, "Min": 11.1, "Mean": 15.5},
        "2017-03-03": {"Max": 31.3, "Min": 29.9, "Mean": 30.0},
        "2016-01-01": {"Max": 12.0, "Min": 5.6, "Mean": 7.1},
        "2016-03-02": {"Max": 22.2, "Min": 11.1, "Mean": 15.5},
        "2016-09-03": {"Max": 31.3, "Min": 29.9, "Mean": 30.0},
    }

    db = DBOperations()
    db.initialize_db()

    db.save_data(weather)
    # db.purge_data()
    db.fetch_data()
