"""Handles all database operations."""

import sqlite3
from dbcm import DBCM

class DBOperations:
    """The DB operations class."""

    def __init__(self):
        """
        Initialize the database connection and setup the context manager.

        Description:
        - Sets up the context manager for the database connection by initializing
        the necessary attributes.
        - The 'db_name' attribute is set to 'weather_data.sqlite'.
        - Creates a 'database_context' attribute using the DBCM class with the provided
        database name.
        - Initializes 'conn' and 'cursor' attributes to None.

        Raises:
        - sqlite3.DatabaseError: If there are issues with initializing the database
        connection or setting up the context manager.
        """
        try:
            self.db_name = "weather_data.sqlite"
            self.database_context = DBCM(self.db_name)
            self.conn = None
            self.cursor = None
        except sqlite3.DatabaseError as error:
            print(error)
            print("Error: __init__ initializing DB.")

    def initialize_db(self):
        """
        Initialize the database by creating necessary tables and indexes if they don't exist.

        Raises:
        - sqlite3.OperationalError: If there are issues with the database operation,
        such as table creation failure.

        Description:
        - Establishes a connection to the database and creates the 'weather' table
        if it doesn't already exist.
        - The 'weather' table includes columns for id, sample_date, location, min_temp,
        max_temp, and avg_temp. The 'sample_date' column is indexed for faster access.
        - If the table creation or index creation fails due to an OperationalError,
        it prints an error message indicating the failure to initialize the database.
        """
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

                # Make index on sample_date for faster access
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_sample_date ON weather (sample_date)"
                )

        except sqlite3.OperationalError as error:
            print(error)
            print("Error: Failed to initialize database.")

    # this function can be passed any query, but validate the query before-hand.
    def get_query_data(self, sql_query):
        """
        Performs an SQL Query and retrieves data from the database.

        Parameters: 
        - sql_query (str): SQL Query to execute in the database.

        Returns:
        - list or None: Data fetched from the executed SQL query. 
        Returns None if an error occurs.

        Raises:
        - sqlite3.OperationalError: If there are issues with the database operation, 
        such as the table not existing or other operational errors.

        Description:
        - Executes the provided SQL query on the database. If successful, 
        retrieves and returns the fetched data as a list of tuples.
        - If an OperationalError occurs, indicating potential issues like a missing table,
        it attempts to handle it by initializing the database and trying the query again.
        - If the table 'weather' doesn't exist, it attempts to create it. 
        If the table creation fails, None is returned.
        """
        try:
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
    def fetch_monthly_averages(self, start_year=None, end_year=None):
        """
        Fetches minimum, mean, and maximum averages for each month within the specified
        range of years.

        Parameters:
        - start_year (str or None): The starting year for fetching data. If None, the query 
        fetches from the earliest available year.
        - end_year (str or None): The ending year for fetching data. If None, the query 
        fetches up to the latest available year.

        Returns:
        - list or None: A list of tuples containing monthly average data (min, mean, max) 
        within the specified year range. 
        Returns None if an error occurs or no data is found.

        Raises:
        - ValueError: If start_year or end_year are not valid digits.

        Description:
        - Constructs an SQL query to calculate monthly averages for minimum, mean, and maximum 
        temperatures.
        - Filters the data based on the provided start_year and end_year, excluding records with 
        missing or invalid temperature values ('M' or null).
        - Groups the calculated averages by month and orders the results by month.
        - Calls the 'get_query_data' method to execute the constructed SQL query and fetch the data
          from the database.
        """
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
    def fetch_year_month_average(self, year=None, month=None):
        """
        Fetches minimum, mean, and maximum averages for the specified year and month from the 
        database.

        Parameters:
        - year (str or None): The year for which data is to be fetched. If None, data for all years
          is considered.
        - month (str or None): The month for which data is to be fetched. If None, data for all 
        months is considered.

        Returns:
        - list or None: A list of tuples containing daily average data for the specified year and 
        month. 
        Returns None if an error occurs or no data is found.

        Raises:
        - ValueError: If year or month are not valid digits.

        Description:
        - Constructs an SQL query to calculate daily average temperatures for the specified year 
        and month.
        - Filters the data based on the provided year and month.
        - Groups the calculated averages by day and orders the results by day.
        - Calls the 'get_query_data' method to execute the constructed SQL query and fetch the data
          from the database.
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

    def get_earliest_date(self):
        """
        Retrieves the earliest date available in the dataset.

        Returns:
        - list or None: A list containing the earliest year and month found in the dataset
        formatted as ['year', 'month']. Returns None if there is no data.

        Description:
        - Constructs an SQL query to fetch the minimum date available in the 'sample_date' column.
        - Calls the 'get_query_data' method to execute the constructed SQL query and fetch 
        the data from the database.
        - Parses the retrieved date string to extract the earliest year and month if available.
        """
        earliest_date_query = """SELECT MIN(strftime('%Y-%m', sample_date)) AS
        earliest_year FROM weather"""
        earliest_year = self.get_query_data(earliest_date_query)[0][0]
        if earliest_year is not None:
            return earliest_year.split("-")
        return None

    def get_year_ends(self):
        """
        Retrieves information about the newest and oldest data points in the dataset.

        Returns:
        - tuple or None: A tuple containing information about the newest and oldest data points.
        If no data is available, returns None.

        Description:
        - Checks for the availability of new data and the earliest date in the dataset using
        the 'get_new_data' and 'get_earliest_date' methods.
        - If both new data and the earliest date are available, it returns a tuple
        containing the newest and oldest data points.
        - If either new data or the earliest date is not available, it returns None.
        """
        if self.get_new_data() is None and self.get_earliest_date() is None:
            return None
        return (self.get_new_data(), self.get_earliest_date())

    def get_new_data(self):
        """
        Retrieves the most recent date available in the dataset.

        Returns:
        - list or None: A list containing the most recent year and month found in the dataset
        formatted as ['year', 'month']. Returns None if there is no data.

        Description:
        - Constructs an SQL query to fetch the maximum date available in the 'sample_date' column.
        - Calls the 'get_query_data' method to execute the constructed SQL query and fetch 
        the data from the database.
        - Parses the retrieved date string to extract the most recent year and month if available.
        """
        recent_date_query = (
            "SELECT MAX(strftime('%Y-%m', sample_date)) AS latest_date FROM weather"
        )
        last_date_available = self.get_query_data(recent_date_query)[0][0]
        if last_date_available is not None:
            print(last_date_available[0][0])
            return last_date_available.split("-")
        return None

    def save_data(self, data_to_save):
        """
        Save new (non-duplicate) data to the database.

        Saves new data to the 'weather' table in the database.

        Parameters:
        - data_to_save (dict): A dictionary containing data to be saved.
        Keys are dates, and values are dictionaries with temperature information
        (keys: 'Min', 'Max', 'Mean').

        Description:
        - Attempts to save new data to the 'weather' table in the database.
        - Loops through the provided 'data_to_save' dictionary, extracting date and 
        temperature information.
        - Inserts the extracted data into the 'weather' table if the sample_date 
        doesn't already exist,
        using an 'INSERT OR IGNORE' SQL statement.
        - If there's an OperationalError while saving the data, attempts to handle it 
        by initializing the database
        and re-saving the data.
        - If there's an IntegrityError due to conflicts with existing data during insertion,
        prints an error message indicating an Integrity Error occurred with the save_data function.
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
                    min_temp, max_temp, avg_temp)
                    SELECT ?, ?, ?, ?, ?
                    WHERE NOT EXISTS (
                    SELECT 1 FROM weather WHERE sample_date = ?
                    )""",
                        (date, location, min_temp, max_temp, avg_temp, date),
                    )
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
                print("Error: save_data Could'nt initialize or save to table.")
        except sqlite3.IntegrityError as error:
            print(error)
            print("Error: save_data Integrity Error with the save_data function.")

    def purge_data(self, burn=False):
        """
        Remove all data from the 'weather' table, or drop all tables in the database.

        Parameters:
        - burn (bool): If True, drops all tables in the database.
                    If False (default), deletes data from the 'weather' table only.

        Note:
        - Be cautious when using burn=True, as it will permanently delete all tables and their data.
        - This method ensures new inserts will start at index 0 after data deletion.

        Usage:
        Example 1: obj.purge_data()  # Deletes data from the 'weather' table.
        Example 2: obj.purge_data(burn=True)  # Drops all tables in the database.
        """
        try:
            with self.database_context as cursor:
                cursor.execute("DELETE FROM weather")
                cursor.execute("DELETE FROM sqlite_sequence")

                print("Data deleted from weather table.")

                if burn is True:
                    print("Dropping any views, index's found in sqlite_master.")

                    cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
                    views = cursor.fetchall()
                    for view in views:
                        cursor.execute(f"DROP VIEW IF EXISTS {view[0]}")
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
                    indexes = cursor.fetchall()
                    for index in indexes:
                        cursor.execute(f"DROP INDEX IF EXISTS {index[0]}")
        except sqlite3.OperationalError as error:
            print(error)
            print(
                f"purge_data An error occurred while purging data. Burn state is {burn}."
            )
