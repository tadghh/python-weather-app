"""Scrapes the weather from environment canada """

# Tadgh Henry
# Oct 12, 2023
# ADEV-3005 241066

from html.parser import HTMLParser
import urllib.request
from urllib.error import URLError, HTTPError
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

class WeatherScraper:
    """Scrapes environment Canada."""

    def __init__(self):
        """Instantiates the class and creates the ip found flag"""

        super().__init__()
        self.parser = self.MyHTMLParser()

        # on the website the earliest year available is 1996
        self.start_year = 1996

        # default value of zero will be changed to the earliest month
        self.start_month = 0

        self.end_year = datetime.now().year
        self.url_sections = (
            "https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&Day=1&Year=",
            "&Month=",
        )
        self.search_url = self.update_url()
        self.weather = {}

    def update_url(self):
        """Updates the search url with the latest values"""
        return f"{self.url_sections[0]}{self.start_year}{self.url_sections[1]}{self.start_month}"

    def scrape_weather(self):
        """Returns the weather data."""
        try:
            thread_count = 12

            # Used to keeps track of the final amount of tasks for the progress bar.
            total_tasks = (self.end_year - self.start_year + 1) * 12

            # tqdm is used to provide a progress bad in the console.
            with tqdm(total=total_tasks, desc="Scraping Weather") as pbar:
                with ThreadPoolExecutor(max_workers=thread_count) as executor:

                    # tells the thread what method to run and provides the parameters for it.
                    # Range is used to get the month and year
                    futures = [executor.submit(self.scrape_weather_thread, year, month, pbar)
                               for year in range(self.start_year, self.end_year + 1)
                               for month in range(1, 13)]

                    # Waits for all of the threads to complete
                    for future in futures:
                        future.result()

        except HTTPError as error:
            print("HTTP Error:", error)
        except URLError as error:
            print("URL Error:", error)
        finally:
           self.print_scraped_data(self.weather)
           self.write_scraped_data(self.weather)


    def scrape_weather_thread(self, year, month, pbar):
        """Thread function for scraping weather."""
        try:

            # Update URL for the current year and month
            search_url = f"{self.url_sections[0]}{year}{self.url_sections[1]}{month}"

            with urllib.request.urlopen(search_url) as response:
                html_data = str(response.read())
                parser = self.MyHTMLParser()
                parser.feed(html_data)

                # Update our master dictionary with the newly returned data
                self.weather.update(parser.return_weather_dict())

        except HTTPError as error:
            print("HTTP Error:", error)
        except URLError as error:
            print("URL Error:", error)
        finally:
            # Update the progress bar
            pbar.update(1)

    def print_scraped_data(scraped_data):
        """print the data stored within scraped_data."""
        print("{")
        for date, weather in scraped_data.items():
            print(f"    '{date}': {weather},")
        print("}")

    def write_scraped_data(scraped_data):
        """Write out scraped_data to a file."""
        file_path = "test_output.txt"
        try:
            with open(file_path, "w",  encoding='UTF-8') as file:
                # Loop through the dictionary items and write them to the file
                for key, value in scraped_data.items():
                    file.write(f"{key}: {value}\n")
        except FileExistsError as error:
            print(error)
            print("Error: write_scraped_data an error occurred.")

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

            # dictionary stored inside of the master dictionary.
            self.daily_temps = {}

            # dictionaries to be populated/accessed on each row iteration.
            self.temporary_daily_dict = {}
            self.column_temperature_legend = {0: "Max", 1: "Min", 2: "Mean"}

            # property to store the row date for each row iteration
            self.row_date = ""

        def handle_starttag(self, tag, attrs):
            """The tag to begin parsing at."""

            if tag == "tbody":
                self.in_table_body = True

            elif tag == "tr" and self.in_table_body:
                self.in_row = True

            elif self.in_row and tag == "td":
                self.in_row_data = True

            # Find the table row header.
            elif tag == "th":

                # Any allows us to short circuit on the first occurrence of scope.
                if any(attr == "scope" and "row" in value for attr, value in attrs):
                    self.in_row_header = True

            # If we're in the table row header.
            if self.in_row_header is True:

                # And the element is abbr.
                if tag == "abbr":

                    # Check for title, break off when found.
                    title_attr = next(
                        (value for attr, value in attrs if attr == "title"), None
                    )

                    title_attr = self.convert_to_date(title_attr)

                    if title_attr is not None:
                        self.row_date = title_attr
                        # TODO: test if col index is needed here
                        self.row_column_index = 0
                        self.in_row = True
                        self.in_row_header = False

        def handle_data(self, data):
            """Look for ip in the data of the element."""
            if(data == "Sum"):
                self.end_of_table = True
                self.reset_flags()

            # If we're in a data-row (<td>) and our counter is less than 3.
            if (
                self.in_table_body is True
                and self.end_of_table is False
                and self.in_row_data is True
                and self.row_column_index < 3
            ):
                if self.is_float(data) or data == "M":
                    # We are inside of a <td> element data-row.

                    # Line up the data with the dictionary before adding it to the year.
                    self.temporary_daily_dict[
                        self.column_temperature_legend.get(self.row_column_index)
                    ] = data

                    self.row_column_index += 1
                    self.in_row_data = False

            # We are only looking for min, max, and mean, which are the first 3 columns.
            elif (
                self.end_of_table is False
                and self.in_row_data is True
                and self.row_column_index == 3
            ):
                # If we've hit 3 columns we need to reset our flags to move to the next row element.

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

        def convert_to_date(value):
            """Attempts to parse the value as a date in the 'YYYY-MM-DD' format."""
            try:
                # Parse the value as a date in the 'Month Day, Year' format
                parsed_date = datetime.strptime(value, "%B %d, %Y")
                # Convert the parsed date to 'YYYY-MM-DD' format
                converted_date = parsed_date.strftime("%Y-%m-%d")
                return converted_date
            except ValueError as error:
                # Return None if the value is not in the expected date format
                print(error)
                print("Error: convert_to_date an error occurred when parsing the date.")
            return None

        def is_float(test_input):
            """Indicates if the passed test_input is a float."""
            try:
                float(test_input)
                return True
            except ValueError:
                return False




if __name__ == "__main__":
    weatherScraper = WeatherScraper()
    weatherScraper.scrape_weather()
