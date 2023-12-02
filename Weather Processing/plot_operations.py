"""Plotting data on a graph/ graph creation."""

import matplotlib.pyplot as plt
from db_operations import DBOperations


class PlotOperations:
    """Plots data onto a graph, visualization"""

    def __init__(self):
        self.db = DBOperations()

    def create_line_plot(self):
        print("poof a graph!")

    def create_year_boxplot_graph(self, graph_data, start_year, end_year):
        """Creates the box plot."""
        temp_data = [temp[1:] for temp in graph_data]

        plt.figure(figsize=(10, 6))
        plt.boxplot(temp_data)
        plt.xlabel("Months")
        plt.ylabel("Temperature (°C)")
        plt.title(f"Monthly Temperature Distribution for: {start_year} to {end_year}")
        plt.xticks(
            range(1, 13),
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            rotation=45,
        )
        plt.tight_layout()
        plt.show(block=True)

    def fetch_data(self, start_year=None, end_year=None, month=None):
        """Fetch the weather data."""
        if month is not None and month.isdigit() is True:
            return self.db.fetch_year_month_average(start_year, month)
        return self.db.fetch_monthy_averages(start_year, end_year)

    def create(self, start_year=None, end_year=None, month=None):
        """Create the graph and everything."""

        weather_data = self.fetch_data(start_year, end_year, month)
        if month is not None and month.isdigit() is True:
            self.create_line_plot()
        else:
            self.create_year_boxplot_graph(
                graph_data=weather_data, start_year=start_year, end_year=end_year
            )
