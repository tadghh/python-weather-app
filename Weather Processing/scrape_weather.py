"""Scrapes the weather from environment canada """

# Tadgh Henry
# Oct 12, 2023
# ADEV-3005 241066

from html.parser import HTMLParser
import urllib.request
from urllib.error import URLError, HTTPError
from datetime import datetime


class WeatherScraper:
    """Scrapes environment Canada."""

    def __init__(self):
        """Instantiates the class and creates the ip found flag"""

        super().__init__()
        self.parser = self.MyHTMLParser()
        self.start_year = 1996  # on the website the earliest year available is 1996
        self.start_month = (
            0  # default value of zero will be changed to the earliest month
        )
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
            while self.start_year <= self.end_year:
                # if the month is 0 which is our starting value,
                # set it to 10 which is the earliest month available
                # on the website the earliest month for 1996 is october (10th month)
                if self.start_month == 0:
                    self.start_month = 10
                elif self.start_month == 12:
                    # if the month isn't 12, increment the month by 1
                    self.start_year += 1
                    self.start_month = 1

                else:
                    # if the month is 12, increment the year by 1
                    # and set the month to the start of the year (1)
                    self.start_month += 1

                self.search_url = self.update_url()
                print(self.search_url)
                print(
                    f"Current Year: {self.start_year}, current Month: {self.start_month}"
                )

                with urllib.request.urlopen(self.search_url) as response:
                    HTML_DATA = str(response.read())
                    self.parser.feed(HTML_DATA)

                    # update our master dictionary with the newly returned data
                    self.weather.update(self.parser.return_weather_dict())
                    self.parser.end_of_table = False

                    # print("{")
                    # for date, data in self.weather.items():
                    #     print(f"    '{date}': {data},")
                    # print("}")

            file_path = "test_output.txt"
            with open(file_path, "w") as file:
                # Loop through the dictionary items and write them to the file
                for key, value in self.weather.items():
                    file.write(f"{key}: {value}\n")
        except HTTPError as e:
            print("HTTP Error:", e)
        except URLError as e:
            print("URL Error:", e)

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
            self.daily_temps = {}  # dictionary stored inside of the master dictionary.

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

            # find the table row header
            elif tag == "th":
                # any allows us to short circut on the first occurance of scope, prevents us from processing unneeded attribute "if they exist"
                if any(attr == "scope" and "row" in value for attr, value in attrs):
                    self.in_row_header = True

            # if we're in the table row header
            if (
                self.in_table_body is True
                and self.end_of_table is False
                and self.in_row_header is True
            ):
                # and the element is abbr
                if tag == "abbr":
                    # Check for title, break off when found
                    title_attr = next(
                        (value for attr, value in attrs if attr == "title"), None
                    )
                    title_attr = is_valid_date(title_attr)
                    if title_attr is not None:
                        self.row_date = title_attr
                        self.row_column_index = 0
                        self.in_row = True

                    # for attr, value in attrs:
                    #     # if the attribute is title
                    #     if attr == "title":
                    #         # get the date value and append it to our daily_temps list
                    #         converted_date = is_valid_date(value)

                    #         if converted_date is not None:
                    #             self.row_date = converted_date
                    #             self.in_row = True

        def handle_data(self, data):
            """Look for ip in the data of the element."""

            # if we're in a data-row (<td>) and our counter is less than 3
            if (
                self.in_table_body is True
                and self.end_of_table is False
                and self.in_row_data is True
                and self.row_column_index < 3
            ):
                if is_float(data) or data == "M":
                    # we are inside of a <td> element data-row

                    self.temporary_daily_dict[
                        self.column_temperature_legend.get(self.row_column_index)
                    ] = data
                    self.row_column_index += 1
                    self.in_row_data = False

            # we are only looking for min, max, and mean, which are the first 3 columns of the table.
            elif (
                self.end_of_table is False
                and self.in_row_data is True
                and self.row_column_index == 3
            ):
                # if we've hit 3 columns we need to reset our flags to move to the next row element.

                self.weather[self.row_date] = self.temporary_daily_dict
                self.temporary_daily_dict = {}
                self.reset_flags()

            if self.in_row_header is True:
                if data == "Sum":
                    self.end_of_table = True
                    self.reset_flags()

                    # TODO: make function that accept a dict and prints it out.
                    # uncomment to print the formatted dictionary
                    # print('{')
                    # for date, data in self.weather.items():
                    #     print(f"    '{date}': {data},")
                    # print('}')

        def return_weather_dict(self):
            """Returns the current dictionary."""
            return self.weather

        def reset_flags(self):
            """Resets the boolean flags indicating we are at a new row in the table."""
            self.in_row = False
            self.in_row_data = False
            self.in_row_header = False
            self.row_column_index = 0


def is_valid_date(value):
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


def is_float(string):
    """Indicates if the passed string is a float."""
    try:
        float(string)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    # SEARCH_URL = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&Day=1&Year=2018&Month=5'
    weatherScraper = WeatherScraper()
    weatherScraper.scrape_weather()
