# Import libraries
import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations


class PlotOperations:
    def __init__(self):
        self.year_from = input("Enter a starting year: ")
        self.year_to = input("Enter a ending year: ")
        self.db = DBOperations()
        self.db.initialize_db()
        print(self.year_from, self.year_to)

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
