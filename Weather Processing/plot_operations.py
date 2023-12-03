"""Plotting data on a graph/ graph creation."""

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
from db_operations import DBOperations


class PlotOperations:
    """Plots data onto a graph, visualization"""

    def __init__(self):
        self.db = DBOperations()

    def create_line_plot(self, graph_weather_data, year, month):
        """Makes a line plot (omg!)"""
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
        """Creates the box plot."""
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
        """Create the graph and everything."""

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
        """Fetch the weather data."""
        if month is not None and month.isdigit() is True:
            return self.db.fetch_year_month_average(start_year, month)
        return self.db.fetch_monthy_averages(start_year, end_year)
