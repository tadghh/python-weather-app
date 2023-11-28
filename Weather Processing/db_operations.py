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
            print(error)
            print("Error: __init__ initializing DB.")

    def initialize_db(self):
        """Initialize the database."""
        try:
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
        except sqlite3.OperationalError as error:
            print(error)
            print("Error: Failed to initialize database.")

    def safely_get_data(self, sql_query, start_year="", end_year=""):
        """
        TODO: use a tuple or list for paramters like in save_data
        Method template for fetching data.

        Parameters:
        - start_year (str): Default is an empty string.
        - end_year (str): Default is an empty string.

        Returns:
        - list of tuples: A list containing tuples representing weather data records.
         'sample_date', 'location', 'min_temp', 'max_temp', and 'avg_temp'.

        Raises:
        - ValueError: If start_year or end_year is provided and is not a digit.
        - OperationalError: If there are issues with the database operation,
         such as table not existing.

        Note:
        - If start_year and end_year are provided,
         the method filters data based on the year part of 'sample_date'.

        - If the table 'weather' does not exist in the database,
         the method attempts to create it.
        - If table creation fails, returns None.

        """
        try:
            with self.database_context as cursor:
                # TODO: Input error checking should be in respective functions.
                # Error handling should handle issues for inputs here
                if start_year == "" and end_year == "":
                    cursor.execute("SELECT * FROM weather")
                else:
                    if start_year.isdigit() and end_year.isdigit():
                        cursor.execute(sql_query)
                    else:
                        raise ValueError("start_year or end_year must be digits.")

                return cursor.fetchall()
        except ValueError as error:
            print(error)
            print("Error: fetch_data provided values are invalid.")
        except sqlite3.OperationalError as error:
            # Table in db might not exist, value will be returned up from the recursive call
            try:
                print(error)
                print("Error: fetch_data Table might not exist trying to initialize.")
                self.initialize_db()
                return self.safely_get_data(sql_query, start_year, end_year)
            except sqlite3.OperationalError as error_two:
                print(error_two)
                print("Error: fetch_data Table creation failed.")
        return None

    # def fetch_data(self, start_year="", end_year=""):
    #     """
    #     Fetch weather data from the database with a given range, years.

    #     Parameters:
    #     - start_year (str): Optional start year for filtering data. Default is an empty string.
    #     - end_year (str): Optional end year for filtering data. Default is an empty string.

    #     Returns:
    #     - list of tuples: A list containing tuples representing weather data records.
    #      'sample_date', 'location', 'min_temp', 'max_temp', and 'avg_temp'.

    #     Raises:
    #     - ValueError: If start_year or end_year is provided and is not a digit.
    #     - OperationalError: If there are issues with the database operation,
    #      such as table not existing.

    #     Note:
    #     - If start_year and end_year are provided,
    #      the method filters data based on the year part of 'sample_date'.

    #     - If the table 'weather' does not exist in the database,
    #      the method attempts to create it.
    #     - If table creation fails, returns None.

    #     """
    #     sql_query = f'''
    #     SELECT sample_date,
    #         CASE
    #             WHEN min_temp LIKE '%M%' THEN NULL
    #             ELSE min_temp
    #         END AS min_temp,
    #         CASE
    #             WHEN max_temp LIKE '%M%' THEN NULL
    #             ELSE max_temp
    #         END AS max_temp,
    #         CASE
    #             WHEN avg_temp LIKE '%M%' THEN NULL
    #             ELSE avg_temp
    #         END AS avg_temp
    #     FROM
    #         weather
    #     WHERE
    #         strftime('%Y', sample_date) BETWEEN '{start_year}' AND '{end_year}'
    #         AND NOT (
    #             (min_temp LIKE '%M%' OR min_temp IS null)
    #             AND (max_temp LIKE '%M%' OR max_temp IS null)
    #             AND (avg_temp LIKE '%M%' OR avg_temp IS null)
    #         );
    #     '''
    #     return self.safely_get_data(sql_query, start_year, end_year)

    def fetch_monthy_averages(self, start_year="", end_year=""):
        """
        Fetch min, mean, max averages from all months in the database.

        Returns:
        -
        Raises:

        """
        sql_query = (
            "SELECT strftime('%m', sample_date) AS month, "
            "AVG(min_temp) AS avg_min_temp, "
            "AVG(max_temp) AS avg_max_temp, "
            "AVG(avg_temp) AS avg_mean_temp "
            "FROM weather "
            f"WHERE strftime('%Y', sample_date) BETWEEN '{start_year}' AND '{end_year}' "
            "AND NOT ( "
            "(min_temp LIKE '%M%' OR min_temp IS null) "
            "AND (max_temp LIKE '%M%' OR max_temp IS null) "
            "AND (avg_temp LIKE '%M%' OR avg_temp IS null) "
            ") "
            "GROUP BY month "
            "ORDER BY month; "
        )

        return self.safely_get_data(sql_query, start_year, end_year)

    def save_data(self, data_to_save):
        """
        Save new (non duplicate) data to the database.

        Save new data to the 'weather' table in the database.

        Parameters:
        - data_to_save (dict): A dictionary containing data to be saved
        keys are dates, values are dictionaries with temperature.
        """
        try:
            with self.database_context as cursor:
                for date, data in data_to_save.items():
                    min_temp = data.get("Min")
                    max_temp = data.get("Max")
                    avg_temp = data.get("Mean")
                    location = "Winnipeg, MB"

                    cursor.execute(
                        """INSERT OR IGNORE INTO weather (sample_date, location,
                        min_temp, max_temp, avg_temp) VALUES (?, ?, ?, ?, ?)""",
                        (date, location, min_temp, max_temp, avg_temp),
                    )
                print("Sample data inserted successfully.")
        except sqlite3.OperationalError as error:
            try:
                print(error)
                print(
                    "Error: save_data saving data, making sure table exists. Will try to re-save."
                )
                self.initialize_db()
                self.save_data(data_to_save)

            except sqlite3.OperationalError as error_two:
                print(error_two)
                print("Error: save_data Could'nt initalize or save to table.")
        except sqlite3.IntegrityError as error:
            print(error)
            print("Error: save_data Integrity Error with the save_data function.")

    def purge_data(self, burn=False):
        """
        Remove all data from the 'weather' table, or drop all tables in the database.

        Parameters:
        - burn (bool): If True, all tables in the database will be dropped.
                    If False (default), only data from the 'weather' table will be deleted.

        Note:
        - Be cautious when using burn=True, as it will permanently delete all tables and their data.

        Usage:
        Example 1: obj.purge_data()  # Deletes data from the 'weather' table.
        Example 2: obj.purge_data(burn=True)  # Drops all tables in the database.
        """
        try:
            with self.database_context as cursor:
                cursor.execute("DELETE FROM weather")
                print("Data deleted from weather table.")

                if burn is True:
                    print("Dropping any remaining tables found in sqlite_master.")
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    for table in tables:
                        cursor.execute(f"DROP TABLE {table[0]};")
                    print("All tables dropped.")
        except sqlite3.OperationalError as error:
            print(error)
            print(
                f" purge_data An error occured while purging data. Burn state is {burn}."
            )


if __name__ == "__main__":
    weather = {
        "1996-10-01": {"Max": "M", "Min": "0.4", "Mean": "M"},
        "1996-10-02": {"Max": "9.4", "Min": "-1.4", "Mean": "4.0"},
        "1996-10-03": {"Max": "9.8", "Min": "-3.9", "Mean": "3.0"},
        "1996-10-04": {"Max": "16.9", "Min": "3.8", "Mean": "10.4"},
        "1996-10-05": {"Max": "23.2", "Min": "9.3", "Mean": "16.3"},
        "1996-10-06": {"Max": "10.6", "Min": "-3.3", "Mean": "3.7"},
        "1996-10-07": {"Max": "11.0", "Min": "-5.2", "Mean": "2.9"},
        "1996-10-08": {"Max": "17.4", "Min": "6.4", "Mean": "11.9"},
        "1996-10-09": {"Max": "9.3", "Min": "-0.5", "Mean": "4.4"},
        "1996-10-10": {"Max": "15.5", "Min": "1.0", "Mean": "8.3"},
        "1996-10-11": {"Max": "18.3", "Min": "4.2", "Mean": "11.3"},
        "1996-10-12": {"Max": "22.7", "Min": "0.0", "Mean": "11.4"},
        "1996-10-13": {"Max": "12.4", "Min": "0.0", "Mean": "6.2"},
        "1996-10-14": {"Max": "12.5", "Min": "4.9", "Mean": "8.7"},
        "1996-10-15": {"Max": "18.6", "Min": "7.9", "Mean": "13.3"},
        "1996-10-16": {"Max": "14.2", "Min": "-2.1", "Mean": "6.1"},
    }

    db = DBOperations()
    db.initialize_db()

    # db.save_data(weather)
    # db.purge_data()
    # db.fetch_data()
