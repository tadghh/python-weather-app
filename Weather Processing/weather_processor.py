"""Main program."""
from menu import Menu
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations


class WeatherProcessor:
    """The main class, handling interaction and general flow."""

    def __init__(self):
        """Initializes the Weather Processor"""
        self.g = 12
        self.weather_db = DBOperations()
        self.weather_db.initialize_db()
        self.weather_scraper = WeatherScraper()
        self.plot_ops = PlotOperations()

    def start_main(self):
        """The main menu."""
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

    def get_input(self, line_plot=False):
        """Get input for the graphs."""

        second_input_prompt = (
            "Enter End Year: " if line_plot is False else "Enter a month ex 02: "
        )
        first_input_prompt = "Enter Starting Year ex 2002: "
        lower_date_bound = self.weather_db.get_earliest_date()
        last_date = self.weather_db.get_new_data()
        (year, month) = last_date

        upper_year_bound = year
        print(lower_date_bound)
        print(upper_year_bound)
        start_year = input(first_input_prompt)
        end_year = input(second_input_prompt)
        while (
            start_year is None
            or start_year.isdigit() is False
            and end_year is None
            or end_year.isdigit() is False
        ):
            if (
                start_year.isdigit()
                and start_year < lower_date_bound
                or start_year > upper_year_bound
            ):
                print("Invalid start year\n")
                start_year = input(first_input_prompt)
            if start_year.isdigit() is True:
                end_year = input(second_input_prompt)
            else:
                start_year = input(first_input_prompt)

        # Input correction
        if line_plot is False and start_year > end_year:
            print(
                "Start year is after end year.\nWould you like us to correct this or reset?"
            )
            user_response = input("Enter (c)orrect or (r)eset: ")

            while user_response != "c" and user_response != "r":
                print("Invalid input, try again.\n")
                user_response = input("Enter (c)orrect or (r)eset: ")
            if user_response == "c":
                (start_year, end_year) = (end_year, start_year)
            else:
                # return up from the recursive call
                # Once below function finish it will only return inside itself
                # Still gotta direct it to return through originally method
                # This can result in a buffer overflow if the user messed up their input enough
                return self.get_input()

        # User was lazy and only entered one number, well help them
        if line_plot is True:
            if len(end_year) < 2:
                end_year = "0" + end_year
        return (start_year, end_year)

    def box_plot(self):
        """Take in the year inputs."""
        # the astrisk makes the tuple puke up its values in order regardless of the variable names.
        PlotOperations().create(*self.get_input())

    def line_plot(self):
        """Take in the year inputs."""
        start_year, month = self.get_input(True)
        PlotOperations().create(start_year, month=month)

    def plot_data_menu(self):
        """Handle menu plotting logic."""
        # TODO: handle when there is no data
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
        """Setup the database"""

        # Setup database
        self.weather_db.initialize_db()

        # Reset DB
        self.database_reset()

        # scrape weather
        current_weather = self.weather_scraper.scrape_weather()
        self.weather_db.save_data(current_weather)

        # Open menu again
        self.data_menu().open()

    def database_update(self):
        """Updates the database, without overwriting"""
        # Check last date in database
        # Give the last data to weather scraper as the start_date

        last_date = self.weather_db.get_new_data()

        (year, month) = last_date
        current_weather = self.weather_scraper.scrape_weather(
            start_year_override=year, start_month_override=month
        )
        self.weather_db.save_data(current_weather)

    def database_reset(self, burn=False):
        """empty db"""
        self.weather_db.purge_data(burn)

    def data_menu(self):
        """Handles database actions."""

        db_data_menu = Menu(title="Database options")
        db_data_menu.set_options(
            [
                ("Fetch data", self.database_fetch),
                ("Update current data", self.database_update),
                ("Reset data", self.database_reset),
                ("Reset hard", lambda: self.database_reset(burn=True)),
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
