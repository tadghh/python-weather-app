"""Main program."""
# Tadgh Henry

# Cole Cianflone - Documentation
# Karan Brar - Testing
import logging
import sys

from menu import Menu

from plot_operations import PlotOperations
from actor import ScrapingActor

logging.basicConfig(
    filename=r".\weather_scraper_logfile.log", encoding="utf-8", level=logging.DEBUG
)


class WeatherProcessor:
    """The main class, handling interaction and general flow."""

    def __init__(self):
        """Initializes the Weather Processor.

        Initializes class attributes including weather database connection,
        weather scraper, plot operations, year range, and latest dates.
        """

        self.plot_ops = PlotOperations()
        self.scraping_actor = ScrapingActor()
        self.latest_dates = self.scraping_actor.update_range()

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
                ("Exit", lambda: sys.exit(0)),
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
        year_range = self.scraping_actor.update_range()
        options = []
        if year_range["lower"] is None and year_range["upper"] is None:
            options.append(
                (
                    "No data, UPDATE",
                    lambda: (
                        self.scraping_actor.database_fetch(),
                        plot_menu.close(),
                        self.plot_data_menu(),
                    ),
                )
            )
        else:
            options.append(("Box plot", self.box_plot))
            options.append(("Line plot", self.line_plot))
            options.append(
                (
                    f"""Latest dates: {year_range}""",
                    (self.data_menu),
                )
            )

        # Default options
        options.append(("Main menu", lambda: (plot_menu.close(), self.start_main())))
        options.append(("Exit", lambda: sys.exit(0)))

        # Apply our array of tuple("option name", ACTION) options
        plot_menu.set_options(options)
        plot_menu.open()

    def data_menu(self):
        """Handles database-related options.

        Provides menu options for fetching, updating, or resetting database data.
        """
        actor = self.scraping_actor
        db_data_menu = Menu(title="Database options")
        db_data_menu.set_options(
            [
                ("Fetch data", actor.database_fetch),
                ("Update current data", actor.database_update),
                ("Reset data", actor.empty_database),
                ("Reset hard", lambda: actor.empty_database(burn=True)),
                ("Main menu", lambda: (self.start_main(), db_data_menu.close())),
                ("Exit", lambda: sys.exit(0)),
            ]
        )
        db_data_menu.set_message("Select an item")
        db_data_menu.set_prompt(">:")
        db_data_menu.open()

    #
    #   HELPER METHODS below
    #

    def validate_input(self, user_input, errors, year_range, can_month=False):
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

                if self.is_in_range(user_input, year_range) is True:
                    return True
                errors.append("not in range.")
            else:
                errors.append("must be integer.")
        except ValueError as error:
            logging.warning("Value error when validating input %s", error)
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
        year_range = self.scraping_actor.update_range()
        start_year = None
        end_year = None
        in_input = True

        while in_input:
            if validated_inputs["start_year"] is False:
                start_year = input(first_input_prompt)
                validated_inputs["start_year"] = self.validate_input(
                    start_year,
                    input_errors["start_year"],
                    year_range,
                    can_month=False,
                )

            if validated_inputs["end_year"] is False:
                end_year = input(second_input_prompt)
                validated_inputs["end_year"] = self.validate_input(
                    end_year,
                    input_errors["end_year"],
                    year_range,
                    can_month=True,
                )

            if validated_inputs["start_year"] and validated_inputs["end_year"]:
                in_input = False
            else:
                for key, errors in input_errors.items():
                    # Make sure there are errors
                    logging.info("User had erranous inputs.")
                    if len(errors) != 0:
                        print(f"{key.capitalize()} errors:")
                        logging.info(" %s errors:", key.capitalize())
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
            logging.warning(
                "Plot Checking: One of the user inputs was not the correct type. %s",
                error,
            )
        return (start_year, end_year)

    def is_in_range(self, year_input, year_range):
        """Checks if the input year is within the database range.

        Parameters:
        - year_input (int): The year input to be validated.

        Returns:
        - bool: True if year is within range, False otherwise.
        """
        try:
            int_year_input = int(year_input)

            lower, higher = int(year_range["lower"]), int(year_range["upper"])

            if lower <= int_year_input <= higher:
                return True
        except ValueError as error:
            logging.log(
                "Value error when checking the year against the upper and lower bounds %s",
                error,
            )
            print("val eeerrr")
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


if __name__ == "__main__":
    weatherProcessor = WeatherProcessor()
    weatherProcessor.start_main()
