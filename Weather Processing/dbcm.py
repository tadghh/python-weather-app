"""Holds the database context manager class."""

import sqlite3
import logging


class DBCM:
    """Class for enacting operations on SQLite database."""

    def __init__(self, database_name):
        """
        Initialize the DBCM instance with the given database name.

        Parameters:
        - database_name (str): The name of the SQLite database.
        """

        self.db_name = database_name
        self.conn = None
        self.cursor = None
        logging.info(r"\n\nCreated DB Content manager.")

    def __enter__(self):
        """
        Enter method for the context manager.

        Establishes a connection to the SQLite database and returns a cursor.

        Returns:
        - sqlite3.Cursor: The cursor object associated with the database connection.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            return self.cursor
        except sqlite3.InternalError as error:
            logging.critical("Error with SQLite3 runtime library: %e", error)
        except sqlite3.InterfaceError as error:
            logging.critical("Error with SQLite3 python module: %e", error)
        except sqlite3.DatabaseError as error:
            logging.warning("Error initializing DB: %e", error)
        except sqlite3.OperationalError as error:
            logging.warning("Database Operational Error: %e", error)

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
            logging.info("Closed DB cursor.\n\n")
        if self.conn:
            self.conn.commit()
            self.conn.close()
            logging.info("Commited to DB and closed connection.\n\n")
