"""Holds the database context manager class."""

import sqlite3


class DBCM:
    """Class for enacting operations on SQLite database."""

    def __init__(self, database_name):
        """Setup the context manager, taking a parameter for the name."""
        try:
            self.db_name = database_name
            self.conn = None
            self.cursor = None
        except sqlite3.DatabaseError as error:
            print("Error initalizing DB: ", error)

    def __enter__(self):
        """This runs after init and will return the DB cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup, closing the cursor and commiting and changes, then closing the connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
