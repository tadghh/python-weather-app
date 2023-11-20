# Import libraries
import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations
from datetime import datetime

# We need to debug extract_monthly_temps to see why its not capturing entries for each month

class PlotOperations:
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
    myPlot = PlotOperations()
    # Creating dataset
    # np.random.seed(10)
    # data = np.random.normal(100, 20, 200)

    # fig = plt.figure(figsize=(10, 7))

    # # Creating plot
    # plt.boxplot(data)

    # # show plot
    # plt.show()

    # Extracting temperatures for each month

    def extract_monthly_temperatures(data):
        months = {
            i: [] for i in range(1, 13)
        }  # Dictionary to store temperatures for each month
        for entry in data:
            date = datetime.strptime(entry[1], "%Y-%m-%d")
            month = date.month
            months[month].append(entry[3:])  # Extract temperatures

        monthly_avg_temps = {month: [] for month in months}

        for month, temps in months.items():
            if temps:
                num_days = len(temps)
                avg_temp = [sum(temp) / num_days for temp in zip(*temps)]
                monthly_avg_temps[month] = avg_temp

        return monthly_avg_temps

    #-# Extracting average temperatures for each month across all years
    monthly_avg_temperatures = extract_monthly_temperatures(myPlot.weather_data)

    #-# Organizing temperatures for plotting
    temps = [monthly_avg_temperatures[i] for i in range(1, 13)]

    #-# Creating a box plot
    plt.figure(figsize=(10, 6))

    plt.boxplot(temps)
    plt.xlabel('Months')
    plt.ylabel('Temperature (°C)')
    plt.title('Average Temperature Distribution for Each Month Across Years')
    plt.xticks(range(1, 13), [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ], rotation=45)
    plt.tight_layout()

    plt.show()

    plt.pause(5000)
