# Import libraries
import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations


class PlotOperations:
    def __init__(self):
        self.start_year = ''
        self.end_year = ''
        # self.correct_input = False

        while self.start_year.isdigit() is False or self.end_year.isdigit() is False:
            if(self.start_year.isdigit() is False or self.end_year.isdigit() is False):
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

        if(self.weather_data == []):
            print("No weather data found for specified year range.")
    


if __name__ == "__main__":
    myPlot = PlotOperations()
    # # Creating dataset
    # np.random.seed(10)
    # data = np.random.normal(100, 20, 200)

    # fig = plt.figure(figsize=(10, 7))

    # # Creating plot
    # plt.boxplot(data)

    # # show plot
    # plt.show()
