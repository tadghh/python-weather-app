"""Scrapes the weather from enviroment canada """

# Tadgh Henry
# Oct 12, 2023
# ADEV-3005 241066

import re
from html.parser import HTMLParser
import urllib.request
from urllib.error import URLError, HTTPError
from datetime import datetime


class MyHTMLParser(HTMLParser):
    """The web scraper."""

    def __init__(self):
        """Instantiates the class and creates the ip found flag"""

        super().__init__()
        self.date_found = False
        self.in_row = False
        self.in_col = False
        self.in_rowheader = False
        self.scraped = {}
        self.start_date = "2013-5-"
        self.weather = []
        self.daily_temps = []

    def handle_starttag(self, tag, attrs):
        """The tag to begin parsing at."""
        
        # find the table row header
        if tag == "th":
            for attr, value in attrs:
                # if its attribute is scope and the value is row
                if attr == "scope" and 'row' in value:
                    # set the flag
                    self.in_rowheader = True
                
        # if we're in the table row header
        if self.in_rowheader == True:
            # and the element is abbr
            if tag == "abbr":
                for attr, value in attrs:
                    # if the attribute is title
                    if attr == "title":
                        # get the date value and append it to our daily_temps list                                
                        converted_date = is_valid_date(value)
                        
                        if converted_date is not None:                   
                            self.weather.append(converted_date)


    def handle_data(self, data):
        """Look for ip in the data of the element."""
        # self.daily_temps = {}
        
        # if self.in_row:
        #     ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        #     ip_addresses = re.findall(ip_pattern, data)
            
        #     for type_string in ip_addresses:
        #         self.daily_temps[type_string] = type_string
        #     self.scraped[self.date_found] = self.daily_temps     


class WeatherScraper:
    """Scrapes enviro canada."""

    def __init__(self):
        """Instantiates the class and creates the ip found flag"""

        super().__init__()
        self.parser = MyHTMLParser()

    def scrape_weather(self, search_url):
        """Returns the weather data."""
        output = ""
        try:
            with urllib.request.urlopen(search_url) as response:
                HTML_DATA = str(response.read())
                self.parser.feed(HTML_DATA)
                print(self.parser.weather)
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

if __name__ == "__main__":
    searchUrl = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5'
    weatherScraper = WeatherScraper()
    weatherScraper.scrape_weather(searchUrl)