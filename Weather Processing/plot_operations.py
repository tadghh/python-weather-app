"""Plotting data on a graph/ graph creation."""

import matplotlib.pyplot as plt
from db_operations import DBOperations


class PlotOperations:
    """Plots data onto a graph, visualization"""

    def __init__(self):
        self.start_year = ""
        self.end_year = ""
        self.db = DBOperations()

    # TODO: Cant take input in this way, must be given from weather_processor.
    def user_year_input(self):
        """Wait for user to input years."""
        while self.start_year.isdigit() is False or self.end_year.isdigit() is False:
            if self.start_year.isdigit() is False or self.end_year.isdigit() is False:
                print("Input must be in a valid format e.g. 1996")
            self.start_year = input("Enter Starting Year: ")
            self.end_year = input("Enter Ending Year: ")

    def create_year_boxplot_graph(self, graph_data):
        """Creates the box plot."""
        temp_data = [temp[1:] for temp in graph_data]

        plt.figure(figsize=(10, 6))
        plt.boxplot(temp_data)
        plt.xlabel("Months")
        plt.ylabel("Temperature (°C)")
        plt.title(
            f"Monthly Temperature Distribution for: {self.start_year} to {self.end_year}"
        )
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

    def fetch_data(self):
        """Fetch the weather data."""
        return self.db.fetch_monthy_averages(
            start_year=self.start_year, end_year=self.end_year
        )

    def create(self):
        """Create the graph and everything.
        TODO: I think data might need some massaging still.
        """
        self.user_year_input()
        print(self.start_year, self.end_year)
        weather_data = self.fetch_data()
        print(weather_data)
        self.create_year_boxplot_graph(graph_data=weather_data)


if __name__ == "__main__":
    myPlotNew = PlotOperations()
    myPlotNew.create()
