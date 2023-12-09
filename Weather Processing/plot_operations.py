"""Plotting data on a graph/ graph creation."""
# Lead by Cole Cianflone, Transitioned to Tadgh and Karan

import logging
import matplotlib as mpl
import matplotlib.pyplot as plt

from db_operations import DBOperations


class PlotOperations:
    """Plots data onto a graph, visualization"""

    def __init__(self):
        """Initialize PlotOperations with a database operations object."""
        self.db = DBOperations()

    # Tadgh Henry
    def create_line_plot(self, graph_weather_data, year, month):
        """
        Create a line plot to visualize daily average temperatures for a specific year and month.

        Parameters:
        - graph_weather_data (list of tuples): Weather data for plotting the line graph.
        - year (str): The year for which data is being plotted.
        - month (str): The month for which data is being plotted.

        Description:
        - Plots a line graph representing daily average temperatures for a given year and month.
        - Displays the line plot and requires user interaction to continue
        execution after plot display.
        """
        if year is None or month is None:
            raise ValueError("Year or month was NoneType.")
        if year.isdigit() is False and month.isdigit() is False:
            raise ValueError("Year or month was not a digit.")

        days = [row[0] for row in graph_weather_data]
        mean_temps = [row[1] for row in graph_weather_data]

        # Plot the line graph
        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        plt.figure(figsize=(10, 6))

        plt.grid()
        plt.plot(days, mean_temps, linestyle="-", color="coral")
        plt.title(f"Daily Avg Temperatures {year}-{month}")
        plt.xlabel("Day of Month")
        plt.ylabel("Avg Daily Temp")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show(block=True)

    # Cole Cianflone
    def create_year_boxplot_graph(self, graph_weather_data, start_year, end_year):
        """
        Create a box plot to visualize monthly temperature distributions for a range of years.

        Parameters:
        - graph_weather_data (list of tuples): Weather data for plotting the box plot.
        - start_year (str): The starting year of the data range.
        - end_year (str): The ending year of the data range.

        -Exceptions
            ValueError if one of the ranges are a NoneType
        Description:
        - Generates a box plot representing the distribution of monthly temperatures
          for a specified range of years.
        - Displays the box plot and requires user interaction to continue
        execution after plot display.
        """
        if start_year is None or end_year is None:
            raise ValueError("One of the year ranges was a NoneType.")
        if start_year.isdigit() is False and end_year.isdigit() is False:
            raise ValueError("One of the ranges was not and integar")

        year_month_temperature_info = [month[1:] for month in graph_weather_data]
        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        plt.figure(figsize=(10, 6))

        plt.boxplot(
            year_month_temperature_info,
            medianprops={"color": "dodgerblue", "linewidth": 1.5},
        )
        plt.xlabel("Months")
        plt.ylabel("Temperature (Celsius)")
        plt.title(f"Monthly Temperature Distribution for: {start_year} to {end_year}")
        plt.tight_layout()
        plt.show(block=True)

    # Cole Cianflone, Tadgh Henry
    def create(self, start_year=None, end_year=None, month=None):
        """
        Create a graph based on the provided parameters.

        Parameters:
        - start_year (str or None): The starting year for data retrieval. Defaults to None.
        - end_year (str or None): The ending year for data retrieval. Defaults to None.
        - month (str or None): The month for data retrieval. Defaults to None.

        Description:
        - Fetches weather data based on provided parameters and generates a graph.
        - If a specific month is provided, creates a line plot; otherwise, creates a box plot.
        """
        try:
            weather_data = self.fetch_data(start_year, end_year, month)

            if month:
                logging.info(r"\n\nMaking line plot.")
                self.create_line_plot(
                    graph_weather_data=weather_data, year=start_year, month=month
                )
            else:
                logging.info(r"\n\nMaking box plot.")
                self.create_year_boxplot_graph(
                    graph_weather_data=weather_data,
                    start_year=start_year,
                    end_year=end_year,
                )
        except ValueError as error:
            logging.info(r"\n\Value Error when calling graphs. %e", error)

    # Tadgh Henry
    def fetch_data(self, start_year=None, end_year=None, month=None):
        """
        Fetch weather data based on provided parameters.

        Parameters:
        - start_year (str or None): The starting year for data retrieval. Defaults to None.
        - end_year (str or None): The ending year for data retrieval. Defaults to None.
        - month (str or None): The month for data retrieval. Defaults to None.

        Returns:
        - list of tuples: Fetched weather data based on the provided parameters.

        Description:
        - Fetches weather data from the database based on the specified criteria.
        - If a specific month is provided, retrieves year-month-based data;
          otherwise, retrieves monthly averages within the given year range.
        """
        try:
            if month is not None and month.isdigit() is True:
                logging.info(r"\n\Made line plot request to db.")
                return self.db.fetch_year_month_average(start_year, month)
            logging.info(r"\n\nNothing special, defaulting to box plot db call.")
            return self.db.fetch_monthly_averages(start_year, end_year)
        except ValueError as error:
            logging.warning(r"\n\nValue error before calling database %s", error)
        return None
