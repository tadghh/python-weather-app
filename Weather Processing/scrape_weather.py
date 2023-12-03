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


class WeatherScraper:
    """Scrapes environment Canada."""

    def __init__(self):
        """Instantiates the class and creates the ip found flag"""
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
        """Returns the weather data."""

        month_and_year = self.get_earliest_date()
        start_year = start_year_override or month_and_year.get("Year")
        start_month = start_month_override or month_and_year.get("Month")
        start_year, start_month = (int(start_year), int(start_month))
        end_year = datetime.now().year

        total_tasks = (end_year - start_year + 1) * 12

        # tqdm is used to provide a progress bad in the console.
        with tqdm(
            total=total_tasks, desc="Scraping: ", smoothing=0.1, miniters=1
        ) as pbar:
            with ThreadPoolExecutor() as executor:
                # An array for all our threads of months for all years.
                futures = [
                    # Tells the thread what method to run and provides the parameters for it.
                    executor.submit(self.scrape_weather_thread, year, month)
                    for year in range(start_year, end_year + 1)
                    for month in range(start_month if year == start_year else 1, 13)
                ]

                # Gets threads as they cpomplete, 30 seconds total runtime.
                for _ in as_completed(futures):
                    pbar.update(1)

        return self.weather

    def scrape_weather_thread(self, year, month):
        """
        Thread function for scraping weather.

        Parameters:
        - year: the year to be used for the search url.
        - month: the month to be used for the search url.
        - pbar: used for increase the state of the progress bar.

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
            print("URL Error:", error)

    # def print_scraped_data(self, scraped_data):
    #     """
    #     Prints the data stored within scraped_data in a formatted manner.

    #     Parameters:
    #     - scraped_data (dict): A dictionary containing the scraped data to be printed.

    #     Returns:
    #     None

    #     Raises:
    #     - AttributeError: If the input is not a dictionary and
    #     does not have the 'items()' method.

    #     The function prints the key-value pairs from the input dictionary
    #     'scraped_data' in a formatted manner.
    #     Each pair is printed as "'date': weather," within curly braces.
    #     If 'scraped_data' is not a dictionary or
    #     does not have the 'items()' method, an AttributeError is raised
    #     and an error message is printed.
    #     """
    #     try:
    #         print("{")
    #         for date, weather in scraped_data.items():
    #             print(f"    '{date}': {weather},")
    #         print("}")
    #     except AttributeError as error:
    #         print(error)
    #         print("Error: print_scraped_data - Does not have the 'items()' method.")

    # def write_scraped_data(self, scraped_data):
    #     """
    #     Writes the scraped data to a text file, formatted to be used for testing with the database.

    #     Parameters:
    #     - scraped_data (dict): A dictionary containing the scraped data to be written to the file.

    #     Returns:
    #     None

    #     Raises:
    #     - PermissionError: If the current user lacks permission.

    #     The function opens a file at the path './test_output.txt'
    #     and writes the key-value pairs from the
    #     input dictionary 'scraped_data' to the file
    #     with each pair formatted as "key: value\n". The file
    #     is encoded using UTF-8.
    #     """
    #     file_path = "./test_output.txt"
    #     try:
    #         with open(file_path, "w", encoding="UTF-8") as file:
    #             # Loop through the dictionary items and write them to the file
    #             for key, value in scraped_data.items():
    #                 file.write(f'"{key}": {value},\n')
    #     except PermissionError as error:
    #         print(error)
    #         print(
    #             """Error: write_scraped_data -
    #             Permission error. Check if you have the necessary write permissions."""
    #         )

    def change_weather_station(self, new_station_id):
        """
        Allows input to change what station is used.

        -Note: No idea how to handle error handling,
        to be used for future features.

        Input: An interger representing a station id.

        """
        self.weather_station_id = new_station_id
        self.url_sections = (
            "https://climate.weather.gc.ca/climate_data",
            f"/daily_data_e.html?StationID={self.weather_station_id}&StartYear=1840&Year=",
            "&Month=",
        )

    def get_earliest_date(self):
        """Gets the earliest year and month for the current weather station.

        Returns: A dict with intergers of the month, year
            Type: dict<int>
            None is returned otherwise

        """

        def extract_month_and_date(text):
            """Extracts the month and year to a dict.

            Returns: A dict with intergers of the month, year
            Type: dict<int>

            """

            # Underscore to shutup pylint.
            _ = """
            Regex used against the site title.

            Groups are made by using parenthises.

            1st group:(month search string)
            2nd group:(look for 4 digits)
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
            print("URL Error:", error)

        # A None value can bubble up from this method
        return extract_month_and_date((p.find(".//title").text))

    class MyHTMLParser(HTMLParser):
        """The web scraper."""

        def __init__(self):
            """Prepares the class to scrape data,
            booleans are used to keep track of the current element"""

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
            """The tag to begin parsing at."""

            if tag == "tbody":
                self.table_bounds["start"] = True

            elif self.table_bounds["start"] is True and tag == "tr":
                self.row_status["row"] = True

            elif self.row_status["row"] is True and tag == "td":
                self.row_status["data"] = True

            # Find the table row header.
            elif self.row_status["data"] is False and tag == "th":
                # Any allows us to short circuit on the first occurrence of scope.
                if any(attr == "scope" and "row" in value for attr, value in attrs):
                    self.row_status["header"] = True

            # If we're in the table row header.
            elif self.row_status["header"] is True and tag == "abbr":
                # Check for title, break off when found.
                title_attr = dict(attrs).get("title")

                # Parse that rows date from the link attribute.
                title_attr = self.convert_to_date(title_attr)

                if title_attr is not None:
                    self.row_date = title_attr
                self.row_status["header"] = False

        def handle_data(self, data):
            """Look through the data of the current element."""

            # If we're in a data-row (<td>) and our counter is less than 3.
            # Sum check to make sure we havent run off the table.
            if data != "Sum" and self.row_status["data"] is True:
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
            """Returns the current dictionary."""
            return self.weather

        def reset_flags(self):
            """Resets the boolean flags indicating we are at a new row in the table."""
            # Reset all the row status flags
            self.row_status.fromkeys("row", False)

            self.daily_temperatures = {}
            self.row_column_temperature_index = 0

        def convert_to_date(self, value):
            """Attempts to parse the value as a date in the 'YYYY-MM-DD' format."""
            try:
                # Parse the value as a date in the 'Month Day, Year' format
                parsed_date = datetime.strptime(value, "%B %d, %Y")
                # Convert the parsed date to 'YYYY-MM-DD' format
                converted_date = parsed_date.strftime("%Y-%m-%d")
                return converted_date
            except ValueError:
                # Return None if the value is not in the expected date format
                return None

        def is_float(self, test_input):
            """Indicates if the passed test_input is a float."""
            try:
                float(test_input)
                return True
            except ValueError:
                return False
