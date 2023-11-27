# Import libraries
import matplotlib.pyplot as plt
from db_operations import DBOperations
from datetime import datetime

# We need to debug extract_monthly_temps to see why its not capturing entries for each month


class PlotOperations:
    """Plots data onto a graph, visualization"""

    def __init__(self):
        self.start_year = ""
        self.end_year = ""
        # self.correct_input = False

        while self.start_year.isdigit() is False or self.end_year.isdigit() is False:
            if self.start_year.isdigit() is False or self.end_year.isdigit() is False:
                print("Start year and end year must be in a valid format e.g. 1996")
            self.start_year = input("Enter a starting year: ")
            self.end_year = input("Enter a ending year: ")

        self.db = DBOperations()
        self.db.initialize_db()
        self.weather_data = self.db.fetch_data(
            start_year=self.start_year, end_year=self.end_year
        )
        print(self.start_year, self.end_year)
        print(self.weather_data)

        if self.weather_data == []:
            print("No weather data found for specified year range.")


if __name__ == "__main__":
    myPlotNew = PlotOperations()

    # While extracting monthly tempratures, we should only be extracting the "Mean" temprature for each day of the month of each year
    def extract_monthly_temperatures(data):
        """Gets the average min, mean, max"""
        months = {
            i: [] for i in range(1, 13)
        }  # Dictionary to store temperatures for each month
        for entry in data:
            # Assuming entry[1:] contains the temperature values
            temperature_values = entry[1:]

            # Check if any of the temperature values is NoneType
            if any(value is None for value in temperature_values):
                # Skip this entry if any value is None
                continue

            date = datetime.strptime(entry[0], "%Y-%m-%d")
            month = date.month

            # Append the non-NoneType values to the list
            months[month].append(temperature_values)

        monthly_avg_temps = {month: [] for month in months}

        # for month, temps in months.items():
        #     if temps:
        #         num_days = len(temps)
        #         avg_temp = [sum(temp) / num_days for temp in zip(*temps)]
        #         monthly_avg_temps[month] = avg_temp

        for month, temps in months.items():
            if temps:
                num_days = len(temps)
                avg_temp = [0] * len(temps[0])  # Initialize a list to store the sum of temperatures for each day

                # Manually add up temperatures for each day
                for temp_set in temps:
                    avg_temp = [avg_temp[i] + temp_set[i] for i in range(len(temp_set))]

                # Calculate the average temperature for each day
                avg_temp = [temp_sum / num_days for temp_sum in avg_temp]

                monthly_avg_temps[month] = avg_temp

        return monthly_avg_temps

    # -# Extracting average temperatures for each month across all years
    # myPlot is not getting refreshed
    monthly_avg_temperatures = extract_monthly_temperatures(myPlotNew.weather_data)

    # -# Organizing temperatures for plotting
    temps = [monthly_avg_temperatures[i] for i in range(1, 13)]

    # -# Creating a box plot
    plt.figure(figsize=(10, 6))

    plt.boxplot(temps)
    plt.xlabel("Months")
    plt.ylabel("Temperature (°C)")
    plt.title("Average Temperature Distribution for Each Month Across Years")
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

    plt.show()

    plt.pause(5000)
