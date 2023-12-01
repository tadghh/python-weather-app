"""Main program."""
from menu import Menu
from db_operations import DBOperations
from scrape_weather import WeatherScraper


class WeatherProcessor:
    """The main class, handling interaction and general flow."""

    def __init__(self):
        self.g = 12
        self.weather_db = DBOperations()
        self.weather_scraper = WeatherScraper()

    def start_main(self):
        "The main menu."
        main_menu = Menu(title="Main Menu")
        main_menu.set_options(
            [
                ("Data Plotting", self.plot_data_menu),
                ("Database options", self.data_menu),
                ("Exit", exit),
            ]
        )
        main_menu.set_message("Select an item")
        main_menu.set_prompt(">:")
        main_menu.open()

    def box_plot(self):
        "Take in the year inputs."
        print("-Box Plot-")
        start_year = 0
        end_year = 0
        start_year = input("Enter Starting Year: ")
        end_year = input("Enter End year: ")
        print(start_year + end_year)
        return {"Start": start_year, "End": end_year}

    def line_plot(self):
        "Take in the year inputs."
        print("-Line Plot-")
        selected_year = input("Enter Year: ")
        selected_month = input("Enter Month: ")
        print(selected_month + selected_year)

    def plot_data_menu(self):
        "Handle menu plotting logic."

        plot_menu = Menu(title="Plotting options")
        plot_menu.set_options(
            [
                ("Box plot", self.box_plot),
                ("Line plot", self.line_plot),
                ("Main menu", self.start_main),
                ("Exit", exit),
            ]
        )
        plot_menu.set_message("Select an item")
        plot_menu.set_prompt(">:")
        plot_menu.open()

    def database_fetch(self):
        "Setup the database"

        # Setup database
        self.weather_db.initialize_db()

        # scrape weather
        current_weather = self.weather_scraper.scrape_weather()

        self.weather_db.save_data(current_weather)

        print("Data should be saved ig")

        # Open menu again
        self.data_menu().open()

    def database_update(self):
        "Updates the database, without overwriting"
        # Check last date in database
        # Give the last data to weather scraper as the start_date
        print("tbd")
        self.data_menu().open()

    def data_menu(self):
        "Handles database actions."

        db_data_menu = Menu(title="Database options")
        db_data_menu.set_options(
            [
                ("Fetch data", self.database_fetch),
                ("Update current data", self.database_update),
                ("Reset data", self.line_plot),
                ("Main menu", self.start_main),
                ("Exit", exit),
            ]
        )
        db_data_menu.set_message("Select an item")
        db_data_menu.set_prompt(">:")
        db_data_menu.open()


if __name__ == "__main__":
    weatherProcessor = WeatherProcessor()
    weatherProcessor.start_main()
