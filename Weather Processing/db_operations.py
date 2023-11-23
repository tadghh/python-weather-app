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

                return data
        except ValueError as error:
            print(error)
        except sqlite3.OperationalError as error:
            # Table in db might not exist, trying to create value will be returned up from the recursive call
            try:
                print("Trying to make table.")
                print(error)
                self.initialize_db()
                return self.fetch_data(self.start_year,self.end_year)
            except sqlite3.OperationalError as error:
                print("Table creation failed.")
                print(error)
        return None

    def save_data(self, data_to_save):
        """Save new data to the database."""
        # TODO: Scenario when there is no db, Secnario where data is duplicated
        try:
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
        except sqlite3.OperationalError as error:
            try:
                print(error)
                print("Error saving data, making sure table exists. Will try to re-save")
                self.initialize_db()
                self.save_date(self.data_to_save)

            except sqlite3.OperationalError as error:
                print(error)
                print("Could'nt create table.")
        except sqlite3.IntegrityError as error:
            print(error)
            print("Error: Attempted to insert duplicate data. Handle accordingly.")



    def purge_data(self, burn = False):
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

                if(self.burn is True):
                    print("Dropping any remaining tables found in sqlite_master.")
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    for table in tables:
                        cursor.execute(f"DROP TABLE {table[0]};")
                    print("All tables dropped.")
        except sqlite3.OperationalError as error:
            print(error)
            print(f"An error occured while purging data. Burn state is {self.burn}")



if __name__ == "__main__":
    weather = {
        "1996-10-01": {'Max': '6.2', 'Min': '0.4', 'Mean': '3.3'},
        "1996-10-02": {'Max': '9.4', 'Min': '-1.4', 'Mean': '4.0'},
        "1996-10-03": {'Max': '9.8', 'Min': '-3.9', 'Mean': '3.0'},
        "1996-10-04": {'Max': '16.9', 'Min': '3.8', 'Mean': '10.4'},
        "1996-10-05": {'Max': '23.2', 'Min': '9.3', 'Mean': '16.3'},
        "1996-10-06": {'Max': '10.6', 'Min': '-3.3', 'Mean': '3.7'},
        "1996-10-07": {'Max': '11.0', 'Min': '-5.2', 'Mean': '2.9'},
        "1996-10-08": {'Max': '17.4', 'Min': '6.4', 'Mean': '11.9'},
        "1996-10-09": {'Max': '9.3', 'Min': '-0.5', 'Mean': '4.4'},
        "1996-10-10": {'Max': '15.5', 'Min': '1.0', 'Mean': '8.3'},
        "1996-10-11": {'Max': '18.3', 'Min': '4.2', 'Mean': '11.3'},
        "1996-10-12": {'Max': '22.7', 'Min': '0.0', 'Mean': '11.4'},
        "1996-10-13": {'Max': '12.4', 'Min': '0.0', 'Mean': '6.2'},
        "1996-10-14": {'Max': '12.5', 'Min': '4.9', 'Mean': '8.7'},
        "1996-10-15": {'Max': '18.6', 'Min': '7.9', 'Mean': '13.3'},
        "1996-10-16": {'Max': '14.2', 'Min': '-2.1', 'Mean': '6.1'},
        "1996-10-17": {'Max': '6.5', 'Min': '-2.6', 'Mean': '2.0'},
        "1996-10-18": {'Max': '7.1', 'Min': '-0.6', 'Mean': '3.3'},
        "1996-10-19": {'Max': '12.2', 'Min': '3.4', 'Mean': '7.8'},
        "1996-10-20": {'Max': '14.0', 'Min': '2.8', 'Mean': '8.4'},
        "1996-10-21": {'Max': '9.0', 'Min': '4.7', 'Mean': '6.9'},
        "1996-10-22": {'Max': '4.7', 'Min': '2.0', 'Mean': '3.4'},
        "1996-10-23": {'Max': '4.3', 'Min': '1.5', 'Mean': '2.9'},
        "1996-10-24": {'Max': '9.3', 'Min': '-4.2', 'Mean': '2.6'},
        "1996-10-25": {'Max': '5.9', 'Min': '1.9', 'Mean': '3.9'},
        "1996-10-26": {'Max': '6.8', 'Min': '3.6', 'Mean': '5.2'},
        "1996-10-27": {'Max': '7.2', 'Min': '1.0', 'Mean': '4.1'},
        "1996-10-28": {'Max': '8.4', 'Min': '-0.6', 'Mean': '3.9'},
        "1996-10-29": {'Max': '8.3', 'Min': '-6.6', 'Mean': '0.9'},
        "1996-10-30": {'Max': '-6.5', 'Min': '-12.2', 'Mean': '-9.4'},
        "1996-10-31": {'Max': '-3.5', 'Min': '-12.8', 'Mean': '-8.2'},
        "1997-03-01": {'Max': '-7.7', 'Min': '-19.5', 'Mean': '-13.6'},
        "1997-03-02": {'Max': '-13.1', 'Min': '-24.8', 'Mean': '-19.0'},
        "1997-03-03": {'Max': '-11.1', 'Min': '-22.5', 'Mean': '-16.8'},
        "1997-03-04": {'Max': '-16.0', 'Min': '-24.7', 'Mean': '-20.4'},
        "1997-03-05": {'Max': '-13.3', 'Min': '-23.6', 'Mean': '-18.5'},
        "1997-03-06": {'Max': '-13.1', 'Min': '-26.0', 'Mean': '-19.6'},
        "1997-03-07": {'Max': '-7.7', 'Min': '-22.0', 'Mean': '-14.9'},
        "1997-03-08": {'Max': '-3.3', 'Min': '-19.7', 'Mean': '-11.5'},
        "1997-03-09": {'Max': '-3.8', 'Min': '-9.1', 'Mean': '-6.5'},
        "1997-03-10": {'Max': '-4.0', 'Min': '-14.5', 'Mean': '-9.3'},
        "1997-03-11": {'Max': '-9.8', 'Min': '-21.1', 'Mean': '-15.5'},
        "1997-03-12": {'Max': '-13.3', 'Min': '-27.5', 'Mean': '-20.4'},
        "1997-03-13": {'Max': '-11.3', 'Min': '-23.2', 'Mean': '-17.3'},
        "1997-03-14": {'Max': '-12.7', 'Min': '-24.6', 'Mean': '-18.7'},
        "1997-03-15": {'Max': '-12.1', 'Min': '-24.5', 'Mean': '-18.3'},
        "1997-03-16": {'Max': '-8.8', 'Min': '-24.2', 'Mean': '-16.5'},
        "1997-03-17": {'Max': '-6.4', 'Min': '-19.6', 'Mean': '-13.0'},
        "1997-03-18": {'Max': '-4.1', 'Min': '-21.7', 'Mean': '-12.9'},
        "1997-03-19": {'Max': '-1.3', 'Min': '-10.6', 'Mean': '-6.0'},
        "1997-03-20": {'Max': '1.4', 'Min': '-14.2', 'Mean': '-6.4'},
        "1997-03-21": {'Max': '0.1', 'Min': '-4.1', 'Mean': '-2.0'},
        "1997-03-22": {'Max': '-2.0', 'Min': '-13.1', 'Mean': '-7.6'},
        "1997-03-23": {'Max': '-1.0', 'Min': '-15.2', 'Mean': '-8.1'},
        "1997-03-24": {'Max': '0.2', 'Min': '-2.4', 'Mean': '-1.1'},
        "1997-03-25": {'Max': '1.8', 'Min': '-7.3', 'Mean': '-2.8'},
        "1997-03-26": {'Max': '5.9', 'Min': '-2.9', 'Mean': '1.5'},
        "1997-03-27": {'Max': '4.7', 'Min': '-4.5', 'Mean': '0.1'},
        "1997-03-28": {'Max': '2.1', 'Min': '-3.1', 'Mean': '-0.5'},
        "1997-03-29": {'Max': '1.7', 'Min': '-7.9', 'Mean': '-3.1'},
        "1997-03-30": {'Max': '-2.1', 'Min': '-8.9', 'Mean': '-5.5'},
        "1997-03-31": {'Max': '4.2', 'Min': '-2.9', 'Mean': '0.7'},
        "1996-11-01": {'Max': '-4.6', 'Min': '-13.6', 'Mean': '-9.1'},
        "1996-11-02": {'Max': '2.9', 'Min': '-14.1', 'Mean': '-5.6'},
        "1996-11-03": {'Max': '10.3', 'Min': '-3.2', 'Mean': '3.6'},
        "1996-11-04": {'Max': '2.4', 'Min': '-6.3', 'Mean': '-2.0'},
        "1996-11-05": {'Max': '2.8', 'Min': '-6.3', 'Mean': '-1.8'},
        "1996-11-06": {'Max': '0.4', 'Min': '-0.6', 'Mean': '-0.1'},
        "1996-11-07": {'Max': '0.5', 'Min': '-8.2', 'Mean': '-3.9'},
        "1996-11-08": {'Max': '0.2', 'Min': '-13.6', 'Mean': '-6.7'},
        "1996-11-09": {'Max': '-6.1', 'Min': '-12.9', 'Mean': '-9.5'},
        "1996-11-10": {'Max': '-7.5', 'Min': '-19.7', 'Mean': '-13.6'},
        "1996-11-11": {'Max': '-10.8', 'Min': '-20.0', 'Mean': '-15.4'},
        "1996-11-12": {'Max': '-12.1', 'Min': '-24.1', 'Mean': '-18.1'},
        "1996-11-13" :{'Max': '-13.6', 'Min': '-25.1', 'Mean': '-19.4'},
        "1996-11-14" :{'Max': '-4.8', 'Min': '-21.2', 'Mean': '-13.0'},
        "1996-11-15" :{'Max': '-0.2', 'Min': '-5.7', 'Mean': '-3.0'},
        "1996-11-16" :{'Max': '-3.6', 'Min': '-13.0', 'Mean': '-8.3'},
        "1996-11-17" :{'Max': '-6.4', 'Min': '-11.0', 'Mean': '-8.7'},
        "1996-11-18" :{'Max': '-10.7', 'Min': '-24.2', 'Mean': '-17.5'},
        "1996-11-19" :{'Max': '-15.2', 'Min': '-24.0', 'Mean': '-19.6'},
        "1996-11-20" :{'Max': '-6.9', 'Min': '-21.6', 'Mean': '-14.3'},
        "1996-11-21" :{'Max': '-12.3', 'Min': '-23.4', 'Mean': '-17.9'},
        "1996-11-22" :{'Max': '-15.7', 'Min': '-24.8', 'Mean': '-20.3'},
        "1996-11-23" :{'Max': '-16.1', 'Min': '-26.4', 'Mean': '-21.3'},
        "1996-11-24" :{'Max': '-13.6', 'Min': '-27.0', 'Mean': '-20.3'},
        "1996-11-25" :{'Max': '-17.7', 'Min': '-29.7', 'Mean': '-23.7'},
        "1996-11-26" :{'Max': '-17.9', 'Min': '-27.9', 'Mean': '-22.9'},
    }

    db = DBOperations()
    db.initialize_db()

    db.save_data(weather)
    # db.purge_data()
    db.fetch_data()
