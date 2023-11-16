"""Scrapes the weather from enviroment canada """

# Tadgh Henry
# Oct 12, 2023
# ADEV-3005 241066

from html.parser import HTMLParser
import urllib.request
from urllib.error import URLError, HTTPError
from datetime import datetime


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
        self.daily_temps = {} # dictionary stored inside of the master dictionary.

        # dictionaries to be populated/accessed on each row iteration.
        self.temporary_daily_dict = {}
        self.column_temperature_legend = {0:"Max", 1:"Min", 2:"Mean"}
        # property to store the row date for each row iteration
        self.row_date = ""

    def handle_starttag(self, tag, attrs):
        """The tag to begin parsing at."""

        if tag == "tbody":
            self.in_table_body = True

        if tag == "tr" and self.in_table_body:
            self.in_row = True

        if self.in_row and tag == "td":
            self.in_row_data = True

        # find the table row header
        if tag == "th":
            for attr, value in attrs:
                # if its attribute is scope and the value is row
                if attr == "scope" and 'row' in value:
                    # set the flag
                    self.in_row_header = True

        # if we're in the table row header
        if self.end_of_table is False and self.in_row_header is True:
            # and the element is abbr
            if tag == "abbr":
                for attr, value in attrs:
                    # if the attribute is title
                    if attr == "title":
                        # get the date value and append it to our daily_temps list
                        converted_date = is_valid_date(value)

                        if converted_date is not None:
                            self.row_date = converted_date

    def handle_data(self, data):
        """Look for ip in the data of the element."""

        if self.in_row_header is True:
            if data == "Sum":
                self.end_of_table = True

                # TODO: make function that accept a dict and prints it out.
                # uncomment to print the formatted dictionary
                # print('{')
                # for date, data in self.weather.items():
                #     print(f"    '{date}': {data},")
                # print('}')
                # self.reset_flags()

        # if we're in a data-row (<td>) and our counter is less than 3
        if (self.end_of_table is False and self.in_row_data is True and self.row_column_index <= 3):
            if is_float(data) or data == "M":
                # we are inside of a <td> element data-row

                # if self.row_column_index == 1:
                self.temporary_daily_dict[
                    self.column_temperature_legend.get(self.row_column_index)] = data
                self.row_column_index += 1

        # we are only looking for min, max, and mean, which are the first 3 columns of the table.
        if self.in_row_data is True and self.row_column_index == 3:
            # if we've hit 3 columns we need to reset our flags to move to the next row element.
            self.weather[self.row_date] = self.temporary_daily_dict
            self.temporary_daily_dict = {}
            self.reset_flags()

    def reset_flags(self):
        """Resets the boolean flags indicating we are at a new row in the table."""    
        self.in_row = False
        self.in_row_data = False
        self.in_row_header = False
        self.row_column_index = 0

class WeatherScraper:
    """Scrapes environment Canada."""

    def __init__(self):
        """Instantiates the class and creates the ip found flag"""

        super().__init__()
        self.parser = MyHTMLParser()
        self.current_year = ""
        self.end_year = datetime.now().strftime('%Y')
        self.month = ""

    def scrape_weather(self, search_url):
        """Returns the weather data."""
        try:           
            with urllib.request.urlopen(search_url) as response:
                HTML_DATA = str(response.read())
                self.parser.feed(HTML_DATA)
                
                #print(self.parser.weather)
        except HTTPError as e:
            print("HTTP Error:", e)
        except URLError as e:
            print("URL Error:", e)

def is_valid_date(value):
    """Attempts to parse the value as a date in the 'YYYY-MM-DD' format."""
    try:
        # Parse the value as a date in the 'Month Day, Year' format
        parsed_date = datetime.strptime(value, '%B %d, %Y')
        # Convert the parsed date to 'YYYY-MM-DD' format
        converted_date = parsed_date.strftime('%Y-%m-%d')
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
    SEARCH_URL = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5'
    weatherScraper = WeatherScraper()
    weatherScraper.scrape_weather(SEARCH_URL)
    