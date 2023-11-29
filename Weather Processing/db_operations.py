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

    # this function can be passed any query, but validate the query before-hand.
    def get_query_data(self, sql_query):
        """
        TODO: use a tuple or list for paramters like in save_data
        Method template for fetching data.

        Parameters:
        TODO: FIX DOCUMENTATION

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
            # TODO: Maybe add extra validation just in-case someone forgets to validate before calling this function.
            with self.database_context as cursor:
                cursor.execute(sql_query)
                return cursor.fetchall()
        except sqlite3.OperationalError as error:
            # Table in db might not exist, value will be returned up from the recursive call
            try:
                print(error)
                print("Error: fetch_data Table might not exist trying to initialize.")
                self.initialize_db()
                return self.get_query_data(sql_query)
            except sqlite3.OperationalError as error_two:
                print(error_two)
                print("Error: fetch_data Table creation failed.")
        return None

    # this function is used for the box plot
    def fetch_monthy_averages(self, start_year="", end_year="", debug=False):
        """
        Fetch min, mean, max averages from all months in the database.
        # TODO: FIX DOCUMENTATION HERE
        Parameters:

        Returns:
        -
        Raises:

        """

        if debug == True:
            sql_query = "SELECT * FROM weather"
        else:
            if start_year.isdigit() and end_year.isdigit():
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
            else:
                raise ValueError("start_year and end_year must both be digits.")
        
        return self.get_query_data(sql_query)

    # this function is used for the line chart
    def fetch_year_month_average(self, year="", month=""):
        """
        Fetch min, mean, max averages for specified year and month from the database.
        # TODO: FIX DOCUMENTATION HERE
        Returns:
        -
        Raises:

        """
        if year.isdigit() and month.isdigit():
            sql_query = (
                "SELECT strftime('%Y-%m-%d', sample_date) AS day,  "
                "AVG(avg_temp) AS mean_daily_temp "
                "FROM weather "
                f"WHERE strftime('%Y', sample_date) = '{year}' "
                f"AND strftime('%m', sample_date) = '{month}' "
                "GROUP BY day "
                "ORDER BY day; "
            )
        else:
            raise ValueError("year and month must both be digits.")

        return self.get_query_data(sql_query)

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


# debugging only
if __name__ == "__main__":
    # test data
    # weather = {
    #     "1996-10-01": {'Max': '6.2', 'Min': '0.4', 'Mean': '3.3'},
    #     "1996-10-02": {'Max': '9.4', 'Min': '-1.4', 'Mean': '4.0'},
    #     "1996-10-03": {'Max': '9.8', 'Min': '-3.9', 'Mean': '3.0'},
    #     "1996-10-04": {'Max': '16.9', 'Min': '3.8', 'Mean': '10.4'},
    #     "1996-10-05": {'Max': '23.2', 'Min': '9.3', 'Mean': '16.3'},
    #     }

    db = DBOperations()
    db.initialize_db()

    #db.save_data(weather)
    #db.purge_data()
    print(db.fetch_monthy_averages(debug=True))
