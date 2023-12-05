"""Main program."""
import logging

from menu import Menu
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations

logging.basicConfig(filename=r".\example.log", encoding="utf-8", level=logging.DEBUG)


class WeatherProcessor:
    """The main class, handling interaction and general flow."""

    def __init__(self):
        """Initializes the Weather Processor.

        Initializes class attributes including weather database connection,
        weather scraper, plot operations, year range, and latest dates.
        """
        self.weather_db = DBOperations()
        self.weather_db.initialize_db()
        self.weather_scraper = WeatherScraper()
        self.plot_ops = PlotOperations()

        self.latest_dates = self.database_check_ends()

        lower_year = self.latest_dates
        upper_year = self.latest_dates
        self.year_range = {
            "lower": None if lower_year is None else lower_year[0],
            "upper": None if upper_year is None else upper_year[0],
        }

    def start_main(self):
        """Displays the main menu.

        Provides a menu interface for plotting data, accessing database options,
        and exiting the application.
        """
        main_menu = Menu(title="Main Menu")
        main_menu.set_message("Select an item")
        main_menu.set_prompt(">:")
        main_menu.set_options(
            [
                ("Weather Data Plotting", self.plot_data_menu),
                ("Database Options", lambda: (self.data_menu(), main_menu.close())),
                ("Exit", exit),
            ]
        )
        main_menu.open()

    def plot_data_menu(self):
        """Handles menu options for plotting.

        Provides menu options for box plot, line plot, and displaying latest dates.
        """
        plot_menu = Menu(title="Plotting options")
        plot_menu.set_message("Select an item")
        plot_menu.set_prompt(">:")

        options = []
        if self.latest_dates is not None:
            options.append(("Box plot", self.box_plot))
            options.append(("Line plot", self.line_plot))
            options.append(
                (
                    f"""Latest dates: {self.latest_dates}""",
                    (self.data_menu),
                )
            )
        else:
            options.append(("No data, UPDATE", self.database_fetch))

        # Default options
        options.append(("Main menu", lambda: (plot_menu.close(), self.start_main())))
        options.append(("Exit", exit))

        # Apply our array of tuple("option name", ACTION) options
        plot_menu.set_options(options)
        plot_menu.open()

    def data_menu(self):
        """Handles database-related options.

        Provides menu options for fetching, updating, or resetting database data.
        """

        db_data_menu = Menu(title="Database options")
        db_data_menu.set_options(
            [
                ("Fetch data", self.database_fetch),
                ("Update current data", self.database_update),
                ("Reset data", self.database_reset),
                ("Reset hard", lambda: self.database_reset(burn=True)),
                ("Main menu", lambda: (self.start_main(), db_data_menu.close())),
                ("Exit", exit),
            ]
        )
        db_data_menu.set_message("Select an item")
        db_data_menu.set_prompt(">:")
        db_data_menu.open()

    #
    #   HELPER METHODS below
    #

    def update_range(self):
        """Updates the year range"""
        self.latest_dates = self.database_check_ends()

        lower_year = self.latest_dates
        upper_year = self.latest_dates
        self.year_range = {
            "lower": None if lower_year is None else lower_year[0],
            "upper": None if upper_year is None else upper_year[0],
        }

    def validate_input(self, user_input, errors, can_month=False):
        """Validates year date input.

        Validates the user input for year dates ensuring they are within the
        range of the database.

        Parameters:
        - user_input (str): User input for year dates.
        - errors (list): List to append error messages if validation fails.
        - can_month (bool): Flag to validate month input if True.

        Returns:
        - bool: True if input is valid, False otherwise.
        """
        try:
            if user_input.isdigit() is True:
                user_input = int(user_input)

                if can_month is True and ((user_input >= 1) == (user_input <= 12)):
                    return True

                if self.is_in_range(user_input) is True:
                    return True
                errors.append("not in range.")
            else:
                errors.append("must be integer.")
        except ValueError as error:
            logging.warning("Value error when validating input %e", error)
        return False

    def get_input(self, line_plot=False):
        """Gets input for the graphs.

        Collects user input for generating graphs and validates it.
        Provides input prompts for start and end years or months.

        Args:
        - line_plot (bool): Flag to determine input requirements for line plot.

        Returns:
        - tuple: A tuple containing start and end years or months.
        """

        # Input text
        first_input_prompt = "Enter Starting Year ex 2002: "
        second_input_prompt = (
            "Enter End Year ex 2005: "
            if line_plot is False
            else "Enter a month ex 02: "
        )

        input_errors = {"start_year": [], "end_year": []}
        validated_inputs = {"start_year": False, "end_year": False}

        start_year = None
        end_year = None
        in_input = True

        while in_input:
            if validated_inputs["start_year"] is False:
                start_year = input(first_input_prompt)
                validated_inputs["start_year"] = self.validate_input(
                    start_year, input_errors["start_year"], can_month=False
                )

            if validated_inputs["end_year"] is False:
                end_year = input(second_input_prompt)
                validated_inputs["end_year"] = self.validate_input(
                    end_year, input_errors["end_year"], can_month=True
                )

            if validated_inputs["start_year"] and validated_inputs["end_year"]:
                in_input = False
            else:
                for key, errors in input_errors.items():
                    # Make sure there are errors
                    logging.info("User had erranous inputs.")
                    if len(errors) != 0:
                        print(f"{key.capitalize()} year errors:")
                        for i, error in enumerate(errors):
                            print(f"  {i + 1}. {error}")

                # Reset errors
                input_errors["start_year"] = []
                input_errors["end_year"] = []

        # Input correction
        return self.plot_checks(start_year, end_year, line_plot)

    def plot_checks(self, start_year, end_year, is_line_plot):
        """Some simple error checking and convience for the user."""
        logging.info("Doing final input checks.")
        try:
            if is_line_plot is False and start_year > end_year:
                print(
                    "Start year is after end year.\nWould you like us to correct this or reset?"
                )
                user_response = input("Enter (c)orrect or (r)eset: ")

                while user_response not in ("c", "r"):
                    print("Invalid input, try again.\n")
                    logging.info("User failed to enter 'c' or 'r'")
                    user_response = input("Enter (c)correct or (r)reset: ")

                if user_response == "c":
                    return (end_year, start_year)

                # return up from the recursive call
                # Once below function finish it will only return inside itself
                # Still gotta direct it to return through originally method
                # This can result in a buffer overflow if the user made # enough incorrect attempts,
                # QA doesnt have the attention span for this
                return self.get_input()

            # User was lazy and only entered one number, we'll help them
            if is_line_plot is True and len(end_year) < 2:
                return (start_year, "0" + end_year)
        except ValueError as error:
            logging.log(
                "Plot Checking: One of the user inputs was not the correct type. %e",
                error,
            )
        return (start_year, end_year)

    def is_in_range(self, year_input):
        """Checks if the input year is within the database range.

        Parameters:
        - year_input (int): The year input to be validated.

        Returns:
        - bool: True if year is within range, False otherwise.
        """
        try:
            lower, higher = int(self.year_range["lower"]), int(self.year_range["upper"])
            if int(year_input) > lower and int(year_input) < higher:
                return True
        except ValueError as error:
            logging.log(
                "Value error when checking the year against the upper and lower bounds %e",
                error,
            )
        return False

    def box_plot(self):
        """Generates a box plot.

        Initiates the creation of a box plot for weather data based on user input.
        """
        # the asterisk makes the tuple puke up its contents regardless of the variable
        # parameter names.  *tuple(y,x) => method(x,y) = result method(y,x)
        # The example method above expects x as the first param
        PlotOperations().create(*self.get_input())

    def line_plot(self):
        """Generates a line plot.

        Initiates the creation of a line plot for weather data based on user input.
        """
        start_year, month = self.get_input(True)
        PlotOperations().create(start_year, month=month)

    def database_check_ends(self):
        """Retrieves and displays the latest available dates in the database.

        Returns:
        - tuple: A tuple containing latest start and end dates.
        """

        return self.weather_db.get_year_ends()

    def database_fetch(self):
        """Fetches and saves weather data to the database."""

        # Setup database
        self.weather_db.initialize_db()

        # Reset DB
        self.database_reset()

        # scrape weather
        current_weather = self.weather_scraper.scrape_weather()
        self.weather_db.save_data(current_weather)
        self.update_range()

    def database_update(self):
        """Updates the database with current weather data."""
        # Check last date in database
        # Give the last data to weather scraper as the start_date
        try:
            last_date = self.weather_db.get_new_data()

            (year, month) = last_date
            current_weather = self.weather_scraper.scrape_weather(
                start_year_override=year, start_month_override=month
            )
            self.weather_db.save_data(current_weather)
            self.update_range()
        except TypeError as error:
            logging.warning(
                "Tried to update without a database/any data. Fetching all data. %e",
                error,
            )
            self.database_fetch()

    def database_reset(self, burn=False):
        """Resets the database by deleting weather data.

        Parameters:
        - burn (bool): If True, drops all tables in the database.

        """
        self.weather_db.purge_data(burn)


if __name__ == "__main__":
    weatherProcessor = WeatherProcessor()
    weatherProcessor.start_main()
