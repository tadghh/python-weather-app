"""Common actions between weather scraper and the database"""

import logging
from db_operations import DBOperations
from scrape_weather import WeatherScraper


class ScrapingActor:
    """Serves as a collective entity for the database and scraper to live in."""

    def __init__(self):
        """Initializes the Scraping Actor.

        Initializes class attributes including weather database connection,
        weather scraper, plot operations, year range, and latest dates.
        """
        self.weather_db = DBOperations()
        self.weather_db.initialize_db()
        self.weather_scraper = WeatherScraper()

    def database_fetch(self):
        """Fetches and saves weather data to the database."""

        # Setup database
        self.weather_db.initialize_db()

        # Reset DB
        self.weather_db.purge_data()

        # scrape weather
        current_weather = self.weather_scraper.scrape_weather()
        self.weather_db.save_data(current_weather)
        self.update_range()

    def update_range(self):
        """Updates the year range"""
        latest_dates = self.weather_db.get_year_ends()

        return {
            "lower": None if latest_dates is None else latest_dates[0],
            "upper": None if latest_dates is None else latest_dates[1],
        }

    def database_update(self):
        """Updates the database with current weather data."""
        # if we fail to get the recent year from the db we will just fetch
        # Check last date in database
        # Give the last data to weather scraper as the start_date
        try:
            last_date = self.weather_db.get_latest_date()
            year = None
            month = None
            if last_date is not None:
                logging.info("We got the updated end years for an update correctly")
                (year, month) = last_date

            current_weather = self.weather_scraper.scrape_weather(
                start_year_override=year, start_month_override=month
            )
            self.weather_db.save_data(current_weather)
            self.update_range()
        except TypeError as error:
            logging.warning(
                "Tried to update without a database/any data. Fetching all data. %e",
                error,
            )
            self.database_fetch()

    def empty_database(self, burn=False):
        """Wrapper for the database purge method"""
        self.weather_db.purge_data(burn)
