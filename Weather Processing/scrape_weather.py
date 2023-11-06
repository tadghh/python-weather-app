"""Scrapes the weather from enviroment canada """

# Tadgh Henry
# Oct 12, 2023
# ADEV-3005 241066


import re
from html.parser import HTMLParser
import urllib.request
from urllib.error import URLError, HTTPError


class MyHTMLParser(HTMLParser):
    """The web scraper."""

    def __init__(self):
        """Instantiates the class and creates the ip found flag"""

        super().__init__()
        self.date_found = False
        self.in_row = False
        self.in_col = False
        self.scraped = {}
        self.start_date = "2013-5-"

    def handle_starttag(self, tag, attrs):
        """We know the body is unique in this scenario."""
        if tag == "tr":
            self.in_row = True
            if tag == "td":
                self.in_col = True
        elif tag == "abbr" and attrs["title"] != "ficj":
            self.start_date += attrs["title"]

    def handle_data(self, data):
        """Look for ip in the data of the element."""
        self.daily_temps = {}
        if self.in_row:
            ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            ip_addresses = re.findall(ip_pattern, data)
            for type_string in ip_addresses:
                self.daily_temps[type_string] = type_string
            self.scraped[self.date_found] = self.daily_temps


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
        except HTTPError as e:
            print("HTTP Error:", e)
        except URLError as e:
            print("URL Error:", e)
