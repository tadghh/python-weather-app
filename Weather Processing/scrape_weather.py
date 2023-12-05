"""Scrapes the weather from environment canada """

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen
from urllib.error import URLError
from contextlib import closing
from html.parser import HTMLParser
import re
from lxml.html import parse
from tqdm import tqdm
import logging


class WeatherScraper:
    """Scrapes environment Canada."""

    def __init__(self):
        """Instantiates the WeatherScraper class and initializes required attributes."""
        super().__init__()

        self.weather_station_id = 27174
        self.url_sections = (
            "https://climate.weather.gc.ca/climate_data",
            f"/daily_data_e.html?StationID={self.weather_station_id}&StartYear=1840&Year=",
            "&Month=",
        )

        self.weather = {}

    def scrape_weather(
        self,
        start_year_override=None,
        start_month_override=None,
    ):
        """
        Scrapes weather data from Environment Canada.

        Parameters:
        - start_year_override (int): Starting year to override scraping from the earliest date.
        - start_month_override (int): Starting month to override scraping from the earliest date.

        Returns:
        - dict: Weather data scraped from Environment Canada.

        Description:
        - Scrapes weather data for each month from the earliest date or overridden
        start date to the current year.
        - Utilizes multi-threading for efficient scraping with a progress bar.
        """
        month_and_year = self.get_earliest_date()
        start_year = start_year_override or month_and_year.get("Year")
        start_month = start_month_override or month_and_year.get("Month")
        start_year, start_month = (int(start_year), int(start_month))
        end_year = datetime.now().year

        total_tasks = (end_year - start_year + 1) * 12

        # tqdm is used to provide a progress bad in the console.
        with tqdm(
            total=total_tasks, desc="Scraping: ", smoothing=0.1, miniters=1
        ) as progress_bar:
            with ThreadPoolExecutor() as executor:
                # An array for all our threads of months for all years.
                futures = [
                    # Tells the thread what method to run and provides the parameters for it.
                    executor.submit(self.scrape_weather_thread, year, month)
                    for year in range(start_year, end_year + 1)
                    for month in range(start_month if year == start_year else 1, 13)
                ]

                # Gets threads as they complete, 30 seconds total runtime.
                for _ in as_completed(futures):
                    progress_bar.update(1)

        return self.weather

    def scrape_weather_thread(self, year, month):
        """
        Thread function for scraping weather data for a specific year and month.

        Parameters:
        - year (int): The year for which weather data is to be scraped.
        - month (int): The month for which weather data is to be scraped.

        Description:
        - Scrapes weather data for a specific year and month from Environment Canada.
        """
        try:
            parser = self.MyHTMLParser()
            url = f"{self.url_sections[0]+self.url_sections[1]}{year}{self.url_sections[2]}{month}"

            # Update URL for the current year and month and open the url
            with closing(urlopen(url)) as response:
                html_data = response.read().decode("utf-8")
                parser.feed(html_data)

                # Update our master dictionary with the newly returned data
                self.weather.update(parser.return_weather_dict())
        except URLError as error:
            logging.warning(
                "We had issues scraping from the following url %e and the following error %e",
                url,
                error,
            )

    def change_weather_station(self, new_station_id):
        """
        Change the weather station for scraping data.

        Parameters:
        - new_station_id (string): The new weather station ID.

        Note:
        - This method changes the weather station ID for scraping data.
        """
        if new_station_id.isdigit() is False:
            raise TypeError

        self.weather_station_id = new_station_id
        self.url_sections = (
            "https://climate.weather.gc.ca/climate_data",
            f"/daily_data_e.html?StationID={self.weather_station_id}&StartYear=1840&Year=",
            "&Month=",
        )

    def get_earliest_date(self):
        """
        Retrieve the earliest year and month for the current weather station.


        Returns:
        - dict or None: A dictionary with integers representing the earliest month and year.
                        Returns None if data retrieval fails.

        Description:
        - Retrieves the earliest available year and month for the current weather
        station from Environment Canada.
        """

        def extract_month_and_date(text):
            """
            Extracts the month and year from text.

            Parameters:
            - text (str): Text containing the month and year information.

            Returns:
            - dict or None: A dictionary with integers representing the month and year.
                            Returns None if no pattern is found.

            Description:
            - Uses regex to extract the month and year from the provided text.
            - Parses the month name and converts it to its corresponding month number.
            """
            pattern = r"""(\b(?:January|February|March|April|May|June|July
            |August|September|October|November|December)\b) (\d{4})"""

            # check if we can find a pattern.
            match = re.search(pattern, text)

            if match:
                month = datetime.strptime(match.group(1), "%B").month
                year = int(match.group(2))
                return {"Month": month, "Year": year}

            return None

        try:
            with urlopen(self.url_sections[0] + self.url_sections[1] + "1840") as page:
                p = parse(page)
        except URLError as error:
            logging.warning(
                "There was an issue grabbing the start date from the website title %e",
                error,
            )

        # A None value can bubble up from this method
        return extract_month_and_date((p.find(".//title").text))

    class MyHTMLParser(HTMLParser):
        """The web scraper."""

        def __init__(self):
            """Initialize the MyHTMLParser class and prepare for scraping."""

            super().__init__()
            # flag properties
            self.table_bounds = {"start": False, "end": False}

            self.row_status = {"row": False, "header": False, "data": False}

            # dictionaries to be populated/accessed on each row iteration.
            self.column_temperature_legend = {0: "Max", 1: "Min", 2: "Mean"}
            self.daily_temperatures = {}

            self.row_column_temperature_index = 0

            # master dictionary
            self.weather = {}

            # property to store the row date for each row iteration
            self.row_date = None

        def handle_starttag(self, tag, attrs):
            """Handle start tags encountered during parsing."""

            if tag == "tbody":
                self.table_bounds["start"] = True

            elif self.table_bounds["start"] == (tag == "tr"):
                self.row_status["row"] = True

            elif self.row_status["row"] and tag == "td":
                self.row_status["data"] = True

            # Find the table row header.
            elif not self.row_status["data"] and tag == "th":
                # Any allows us to short circuit on the first occurrence of scope.
                self.row_status["header"] = any(
                    attr == "scope" and "row" in value for attr, value in attrs
                )

            # If we're in the table row header.
            elif self.row_status["header"] and tag == "abbr":
                # Check for title, break off when found.
                title_attr = next(
                    (value for attr, value in attrs if attr == "title"), None
                )

                # Parse that rows date from the link attribute.
                title_attr = self.convert_to_date(title_attr)

                if title_attr is not None:
                    self.row_date = title_attr
                self.row_status["header"] = False

        def handle_data(self, data):
            """
            Handle the data encountered during HTML parsing.

            Parameters:
            - data (str): The data encountered during parsing.

            Description:
            - Processes the data encountered during parsing.
            - Checks if the parser is in a data row (<td>) and the counter is less than 3.
            - Handles temperature data (min, max, mean) and adds it to the daily
              temperatures dictionary.
            - Resets flags when the three columns (min, max, mean) are processed for a row.
            """
            # If we're in a data-row (<td>) and our counter is less than 3.
            # Sum check to make sure we haven't run off the table.
            if data != "Sum" and self.row_status["data"]:
                if (
                    self.row_column_temperature_index < 3
                    and self.is_float(data)
                    or data == "M"
                ):
                    # Line up the data with the dictionary before adding it to the year.
                    self.daily_temperatures[
                        self.column_temperature_legend.get(
                            self.row_column_temperature_index
                        )
                    ] = data

                    self.row_column_temperature_index += 1
                    self.row_status["data"] = False

                # We are only looking for min, max, and mean, which are the first 3 columns.
                # If we've hit 3 columns we need to reset our flags to move to the next row element.
                elif self.row_column_temperature_index == 3:
                    self.weather[self.row_date] = self.daily_temperatures
                    self.reset_flags()

        def return_weather_dict(self):
            """
            Return the scraped weather data.

            Returns:
            - dict: Weather data scraped from Environment Canada.

            Description:
            - Returns the weather data collected during parsing.
            """
            return self.weather

        def reset_flags(self):
            """
            Reset the boolean flags indicating a new row in the table.

            Description:
            - Resets all the row status flags indicating the parser is at a new row in the table.
            - Clears the daily temperatures dictionary and resets the column index counter.
            """
            self.row_status = {key: False for key in self.row_status}

            self.daily_temperatures = {}
            self.row_column_temperature_index = 0

        def convert_to_date(self, value):
            """
            Attempt to parse the value as a date in the 'YYYY-MM-DD' format.

            Parameters:
            - value (str): The value to be parsed as a date.

            Returns:
            - str or None: A string representing the parsed date in 'YYYY-MM-DD' format.
                        Returns None if the value is not in the expected date format.

            Description:
            - Attempts to parse the provided value as a date in the 'Month Day, Year' format.
            - Converts the parsed date to 'YYYY-MM-DD' format if successful.
            - Returns the formatted date string or None if the value is not in the expected format.
            """
            try:
                # Parse the value as a date in the 'Month Day, Year' format and
                # format it to 'YYYY-MM-DD'
                # Convert the parsed date to 'YYYY-MM-DD' format

                return datetime.strptime(value, "%B %d, %Y").strftime("%Y-%m-%d")
            except ValueError:
                # Return None if the value is not in the expected date format
                return None

        def is_float(self, test_input):
            """
            Check if the passed test_input is a float.

            Parameters:
            - test_input (str): The input to be checked.

            Returns:
            - bool: True if the test_input can be converted to a float, False otherwise.

            Description:
            - Checks if the provided input can be converted to a float.
            - Returns True if the conversion to float is successful, False otherwise.
            """
            try:
                float(test_input)
                return True
            except ValueError:
                return False
