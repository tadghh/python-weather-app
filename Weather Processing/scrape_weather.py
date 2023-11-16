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
        self.in_table_body = False
        self.in_row_header = False
        self.in_row = False
        self.in_row_data = False
        self.row_column_index = 0
        self.end_of_table = False\
            
        
        #self.in_col = False
        #self.scraped = {}
        self.start_date = "2013-5-"
        
        
        
        self.weather = {}
        self.daily_temps = {}
        self.temp_daily_temps = {}
        self.daily_temps_keys = {0:"Max", 1:"Min", 2:"Mean"}
        
        self.row_date = ""
        self.formatted_date = ""
        
        
        
        
        
        

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
        if self.end_of_table == False and self.in_row_header == True:
            # and the element is abbr
            if tag == "abbr":
                for attr, value in attrs:
                    # if the attribute is title
                    if attr == "title":
                        # get the date value and append it to our daily_temps list                                
                        print(value)
                        converted_date = is_valid_date(value)
                        
                        if converted_date is not None:
                            #self.weather.append(converted_date) for a list
                            self.row_date = converted_date
                            self.formatted_date = converted_date

    def handle_data(self, data):
        """Look for ip in the data of the element."""
        
        if self.in_row_header == True:
            if data == 'Sum':
                self.end_of_table = True
                self.reset_flags()
        
        # if we're in a datarow (<td>) and our counter is less than 3
        if self.end_of_table == False and self.in_row_data == True and self.row_column_index <= 3:
            if is_float(data) or data == 'M':
                # we are inside of a <td> element datarow
                
                #if self.row_column_index == 1:
                    
                    self.row_column_index += 1
                
                #print(data)
                    
                                
        # we are only looking for min, max, and mean, which are the first 3 columns of the table.
        if self.in_row_data == True and self.row_column_index == 3:
            # if we've hit 3 columns we need to reset our flags to move to the next row element.
            self.reset_flags()
            
        # self.daily_temps = {}
        
        # if self.in_row:
        #     ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        #     ip_addresses = re.findall(ip_pattern, data)
            
        #     for type_string in ip_addresses:
        #         self.daily_temps[type_string] = type_string
        #     self.scraped[self.date_found] = self.daily_temps  
        
    def reset_flags(self):
        """Resets the boolean flags indicating we are at a new row in the table."""    
        self.in_row = False
        self.in_row_data = False
        self.in_row_header = False
        self.row_column_index = 0


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
    searchUrl = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5'
    weatherScraper = WeatherScraper()
    weatherScraper.scrape_weather(searchUrl)