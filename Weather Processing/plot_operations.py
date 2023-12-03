"""Plotting data on a graph/ graph creation."""

import matplotlib.pyplot as plt
import matplotlib as mpl
from db_operations import DBOperations

class PlotOperations:
    """Plots data onto a graph, visualization"""

    def __init__(self):
        """Initialize PlotOperations with a database operations object."""
        self.db = DBOperations()

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
        print("poof a graph!")
        print("Close graph to continue execution")
        days = [row[0] for row in graph_weather_data]
        mean_temps = [row[1] for row in graph_weather_data]

        # Plot the line graph
        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        plt.figure(figsize=(10, 6))
        plt.tight_layout()

        plt.grid()
        plt.plot(days, mean_temps, linestyle="-", color="coral")
        plt.title(f"Daily Avg Temperatures {year}-{month}")
        plt.xlabel("Day of Month")
        plt.ylabel("Avg Daily Temp")
        plt.xticks(rotation=45)
        plt.show(block=True)

    def create_year_boxplot_graph(self, graph_weather_data, start_year, end_year):
        """
        Create a box plot to visualize monthly temperature distributions for a range of years.

        Parameters:
        - graph_weather_data (list of tuples): Weather data for plotting the box plot.
        - start_year (str): The starting year of the data range.
        - end_year (str): The ending year of the data range.

        Description:
        - Generates a box plot representing the distribution of monthly temperatures
          for a specified range of years.
        - Displays the box plot and requires user interaction to continue 
        execution after plot display.
        """
        year_month_temperature_info = [month[1:] for month in graph_weather_data]
        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        plt.figure(figsize=(10, 6))
        plt.tight_layout()
        plt.boxplot(
            year_month_temperature_info,
            medianprops=dict(color="dodgerblue", linewidth=1.5),
        )
        plt.xlabel("Months")
        plt.ylabel("Temperature (Celcius)")
        plt.title(f"Monthly Temperature Distribution for: {start_year} to {end_year}")

        plt.show(block=True)

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
        weather_data = self.fetch_data(start_year, end_year, month)
        if month is not None and month.isdigit() is True:
            self.create_line_plot(
                graph_weather_data=weather_data, year=start_year, month=month
            )
        else:
            self.create_year_boxplot_graph(
                graph_weather_data=weather_data,
                start_year=start_year,
                end_year=end_year,
            )

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
        if month is not None and month.isdigit() is True:
            return self.db.fetch_year_month_average(start_year, month)
        return self.db.fetch_monthy_averages(start_year, end_year)
