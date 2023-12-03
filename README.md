# Python Weather App

# Features
- Multithreading
  - Can scrape weather data from 1996 to 2023 in under 55 seconds
- Error handling
- Data Visualization

### Mark: 76
### Weather Scraper

- [x] **Name / 6**
    - WeatherScraper class has been created inside a scrape_weather module.

- [x] **Parse / 6**
    - Code uses the Python HTMLParser class to parse the website html.

- [x] **Collect Data / 6**
    - Code successfully scrapes the min, max & mean temperature and date, and stores them in a dictionary of dictionaries.

- [x] **Detect End / 6**
    - Code successfully scrapes weather data from the current date, as far back in time as is available.
    - Last available weather date should be automatically detected in some way, not hard coded.

- [ ] **I/O / 6**
    - Code receives a url to scrape as input, and outputs the scraped data for use in other parts of the program.

### Database Operations

- [x] **Name / 4**
    - A class named DBOperations has been created inside a db_operations module.

- [x] **Context Manager / 4**
    - Code uses a database context manager named DBCM correctly.
    - DBCM returns a cursor object in __enter__.
    - DBCM commits changes and closes all connection objects in __exit__.

- [x] **Initialise / 4**
    - Code successfully initializes the database and creates the necessary tables/fields if they don't already exist, every time the program starts.

- [x] **Store / 4**
    - Code receives & processes date, min, max & mean temperature as input, checks for duplicates in some way, and successfully stores it in the database.

- [x] **I/O / 4**
    - DBOperations outputs the data required for plotting.

### Plotting

- [x] **Name / 3**
    - A class named PlotOperations has been created inside a plot_operations module.

- [x] **Box Plot / 3**
    - Code successfully uses Python matplotlib to create a basic boxplot of mean temperature data with the same labels/design given in the example.

- [ ] **Line Plot / 3**
    - Code successfully uses Python matplotlib to create a line plot of mean temperature data for a particular month.

- [x] **Process / 3**
    - PlotOperations receives & processes the data to be used in the plots. Data is processed in PlotOperations not DBOperations.

- [x] **Format / 3**
    - Plots are formatted nicely and include axis labels and title.
    - Title includes the correct year or month/day.
    - No axis items are overlapping.

### User Interaction

- [x] **Name / 5**
    - A class named WeatherProcessor has been created in a module named weather_processor.

- [x] **Fetch Data / 5**
    - On startup, code successfully prompts the user to download a full set of weather data, or update their existing data.

- [ ] **Plot / 5**
    - Code successfully prompts the user for a date range of interest to display.
        - From year, to year for box plot.
        - Year and month for line plot.
    - User prompt shows date format example.

- [ ] **Manage / 5**
    - Code successfully launches and manages all the other tasks.

### Packaging

- [ ] **Create / 5**
    - Successfully create a Windows package installer using Inno Setup, which includes a logo and license agreement.

- [ ] **Install & Run / 5**
    - Package can be installed successfully on Windows.
    - Program runs successfully after installation.

### Additional Requirements

- [x] **PEP8 Compliance / 1**
    - Code adheres to PEP8 standard by achieving a score of 8 or higher using pylint.

- [x] **Docstrings / 1**
    - Code blocks include comments.
    - Code documentation includes module, class & function/method level docstrings.

- [x] **Participation / 1**
    - Each module/class/function documentation contains the names of the people who worked on it.

- [ ] **Error Handling & Logging / 1**
    - Every function/method implements error handling that logs errors to a file using the python logging module.

- [ ] **Q&A / 1**

### Bonus 1 - Optional

- [ ] **UI / 10**
    - Create a user interface for all user interaction. All the widgets are labelled and aligned properly. The UI is polished and presentable, ready for sale.

### Bonus 2 - Optional

- [x] **Thread / 5**
    - Implement threading in your scraping class to speed up scraping operations.



## Status


Our code quality is currently...

[![Pylint](https://github.com/tadghh/PythonWeatherApp/actions/workflows/pylint.yml/badge.svg?branch=main&event=push)](https://github.com/tadghh/PythonWeatherApp/actions/workflows/pylint.yml)

Here are the linting recommendations
```python
************* Module plot_operations
Weather Processing/plot_operations.py:69:24: R1735: Consider using '{"color": 'dodgerblue', "linewidth": 1.5}' instead of a call to 'dict'. (use-dict-literal)
************* Module weather_processor
Weather Processing/weather_processor.py:41:19: R1716: Simplify chained comparison between the operands (chained-comparison)
Weather Processing/weather_processor.py:44:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
Weather Processing/weather_processor.py:109:18: R1714: Consider merging these comparisons with 'in' by using 'user_response not in ('c', 'r')'. Use a set instead if elements are hashable. (consider-using-in)
Weather Processing/weather_processor.py:52:4: R0912: Too many branches (13/12) (too-many-branches)

-----------------------------------
Your code has been rated at 9.87/10

```
