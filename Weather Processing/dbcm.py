"""Holds the database context manager class."""

import sqlite3


class DBCM:
    """Class for enacting operations on SQLite database."""

    def __init__(self, database_name):
        """
        Initialize the DBCM instance with the given database name.

        Parameters:
        - database_name (str): The name of the SQLite database.
        """
        try:
            self.db_name = database_name
            self.conn = None
            self.cursor = None
        except sqlite3.DatabaseError as error:
            print("Error initializing DB: ", error)

    def __enter__(self):
        """
        Enter method for the context manager.

        Establishes a connection to the SQLite database and returns a cursor.

        Returns:
        - sqlite3.Cursor: The cursor object associated with the database connection.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit method for the context manager.

        Cleans up by closing the cursor, committing any pending changes,
        and then closing the connection to the database.

        Parameters:
        - exc_type: Exception type.
        - exc_value: Exception value.
        - traceback: Traceback information.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
