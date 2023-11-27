"""Scrapes the weather from environment canada """

# Tadgh Henry
# Oct 12, 2023
# ADEV-3005 241066

from html.parser import HTMLParser
import urllib.request
from contextlib import closing

from urllib.error import URLError
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


class WeatherScraper:
    """Scrapes environment Canada."""

    def __init__(self):
        """Instantiates the class and creates the ip found flag"""
        super().__init__()

        self.url_sections = (
            "https://climate.weather.gc.ca/climate_data",
            "/daily_data_e.html?StationID=27174&StartYear=1840&Year=",
            "&Month=",
        )

        self.weather = {}

    def scrape_weather(self):
        """Returns the weather data."""
        # on the website the earliest year available is 1996

        # No hard coding, there is a previous month button the page we can look for
        start_year = 1996
        end_year = datetime.now().year

        thread_count = 12

        # Used to keeps track of the final amount of tasks for the progress bar.
        total_tasks = (end_year - start_year + 1) * 12

        # tqdm is used to provide a progress bad in the console.
        with tqdm(total=total_tasks, desc="Scraping Weather") as pbar:
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                # tells the thread what method to run and provides the parameters for it.
                # Range is used to get the month and year
                futures = [
                    executor.submit(self.scrape_weather_thread, year, month, pbar)
                    for year in range(start_year, end_year + 1)
                    for month in range(1, 13)
                ]

                # Waits for all of the threads to complete
                for future in futures:
                    future.result()

        self.print_scraped_data(self.weather)
        self.write_scraped_data(self.weather)

    def scrape_weather_thread(self, year, month, pbar):
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
            with closing(urllib.request.urlopen(url)) as response:
                html_data = str(response.read())
                parser.feed(html_data)

                # Update our master dictionary with the newly returned data
                self.weather.update(parser.return_weather_dict())

        except URLError as error:
            print("URL Error:", error)
        finally:
            # Update the progress bar
            pbar.update(1)

    def print_scraped_data(self, scraped_data):
        """
        Prints the data stored within scraped_data in a formatted manner.

        Parameters:
        - scraped_data (dict): A dictionary containing the scraped data to be printed.

        Returns:
        None

        Raises:
        - AttributeError: If the input is not a dictionary and
        does not have the 'items()' method.

        The function prints the key-value pairs from the input dictionary
        'scraped_data' in a formatted manner.
        Each pair is printed as "'date': weather," within curly braces.
        If 'scraped_data' is not a dictionary or
        does not have the 'items()' method, an AttributeError is raised
        and an error message is printed.
        """
        try:
            print("{")
            for date, weather in scraped_data.items():
                print(f"    '{date}': {weather},")
            print("}")
        except AttributeError as error:
            print(error)
            print("Error: print_scraped_data - Does not have the 'items()' method.")

    def write_scraped_data(self, scraped_data):
        """
        Writes the scraped data to a text file, formatted to be used for testing with the database.

        Parameters:
        - scraped_data (dict): A dictionary containing the scraped data to be written to the file.

        Returns:
        None

        Raises:
        - PermissionError: If the current user lacks permission.

        The function opens a file at the path './test_output.txt'
        and writes the key-value pairs from the
        input dictionary 'scraped_data' to the file
        with each pair formatted as "key: value\n". The file
        is encoded using UTF-8.
        """
        file_path = "./test_output.txt"
        try:
            with open(file_path, "w", encoding="UTF-8") as file:
                # Loop through the dictionary items and write them to the file
                for key, value in scraped_data.items():
                    file.write(f'"{key}": {value},\n')
        except PermissionError as error:
            print(error)
            print(
                """Error: write_scraped_data -
                Permission error. Check if you have the necessary write permissions."""
            )

    class MyHTMLParser(HTMLParser):
        """The web scraper."""

        def __init__(self):
            """Instantiates the class and creates the ip found flag"""

            super().__init__()
            # flag properties
            self.in_table_body = False
            self.in_row_header = False
            self.in_row = False
            self.in_row_data = False
            self.end_of_table = False

            # row column counter
            self.row_column_index = 0

            # master dictionary
            self.weather = {}

            # dictionaries to be populated/accessed on each row iteration.
            self.temporary_daily_dict = {}
            self.column_temperature_legend = {0: "Max", 1: "Min", 2: "Mean"}

            # property to store the row date for each row iteration
            self.row_date = ""

        def handle_starttag(self, tag, attrs):
            """The tag to begin parsing at."""

            if tag == "tbody":
                self.in_table_body = True

            elif self.in_table_body and tag == "tr":
                self.in_row = True

            elif self.in_row and tag == "td":
                self.in_row_data = True

            # Find the table row header.
            elif self.in_row_data is False and tag == "th":
                # Any allows us to short circuit on the first occurrence of scope.
                if any(attr == "scope" and "row" in value for attr, value in attrs):
                    self.in_row_header = True

            # If we're in the table row header.
            # And the element is abbr.
            elif self.in_row_header is True and tag == "abbr":
                # Check for title, break off when found.
                title_attr = next(
                    (value for attr, value in attrs if attr == "title"), None
                )

                title_attr = self.convert_to_date(title_attr)

                if title_attr is not None:
                    self.row_date = title_attr
                self.in_row_header = False

        def handle_data(self, data):
            """Look through the data of the current element."""
            if data == "Sum":
                self.end_of_table = True
                self.reset_flags()

            # If we're in a data-row (<td>) and our counter is less than 3.
            elif self.end_of_table is False and self.in_row_data is True:
                if self.row_column_index < 3:
                    if self.is_float(data) or data == "M":
                        # Line up the data with the dictionary before adding it to the year.
                        self.temporary_daily_dict[
                            self.column_temperature_legend.get(self.row_column_index)
                        ] = data

                        self.row_column_index += 1
                        self.in_row_data = False

                # We are only looking for min, max, and mean, which are the first 3 columns.
                # If we've hit 3 columns we need to reset our flags to move to the next row element.
                elif self.row_column_index == 3:
                    self.weather[self.row_date] = self.temporary_daily_dict
                    self.temporary_daily_dict = {}
                    self.reset_flags()

        def return_weather_dict(self):
            """Returns the current dictionary."""
            return self.weather

        def reset_flags(self):
            """Resets the boolean flags indicating we are at a new row in the table."""
            self.in_row = False
            self.in_row_data = False
            self.in_row_header = False
            self.row_column_index = 0

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
                # print(error)
                # print("Error: convert_to_date an error occurred when parsing the date.")
                return None

        def is_float(self, test_input):
            """Indicates if the passed test_input is a float."""
            try:
                float(test_input)
                return True
            except ValueError:
                return False


if __name__ == "__main__":
    weatherScraper = WeatherScraper()
    weatherScraper.scrape_weather()
