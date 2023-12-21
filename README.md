<div align="center">

<img src="./Build%20Files/icons/icon.png">

# Weather Scraper Apprentice

A Python application that scapes historical weather data from Enviroment Canada. This was the final submission for my college's Python course.

</div>

## Building

- Install Python 3.12
- Create a virtual environment
- Run BuildMe.ps1

### Download and Build

> ⚠️ The following script will prompt you to temporarily bypass powershell's execution policy

> _BuildMe.ps1_ Is responsible for the creation of the applications executable file

> The [Inno Script.iss](./Inno%20Script.iss) file can be used with [Inno Setup](https://jrsoftware.org/isdl.php#stable) to create an installer

> ⚠️ The below command is designed for windows

```
git clone git@github.com:tadghh/PythonWeatherApp.git
cd .\PythonWeatherApp\
python -m venv venv
venv\Scripts\activate
pip install -r '.\Weather Processing\requirements.txt'
powershell -ExecutionPolicy Bypass -File .\BuildMe.ps1
```
### Build output location
After running the above commands you will find an executable file inside the **dist directory** of the downloaded **python-weather-app** repository.

### Libraries used

- pylint
- contourpy
- kiwisolver
- lxml
- matplotlib
- numpy
- Pillow
- pyinstaller
- pyinstaller-hooks-contrib
- Menu
- tqdm

## Features

- PEP8 Compliant
- Multithreaded data scraping
  - 27 years worth of tempertaure data can be processed, saved and formatted in under 30 seconds
- Uses SQLite to store weather info
  - Index used to quickly update with distinct data
- Error handling
- UX focused menu
  - If the range of years was put in backwards a prompt appears offering to swap the dates
  - Explanations for incorrect input
- Data visualization
  - Box plot that displays the min, avg, max temperatures for each month across a range of years
  - Line graph, used to show the temperature across of a specific month and year
- Error logging, to assist trouble shooting

## Code quality

<div align="center">

Our code quality is currently...

[![Pylint](https://github.com/tadghh/python-weather-app/actions/workflows/pylint.yml/badge.svg?branch=main&event=push)](https://github.com/tadghh/python-weather-app/actions/workflows/pylint.yml)

</div>

Here are the linting recommendations
```python
************* Module weather_processor
Weather Processing/weather_processor.py:229:47: E0001: Parsing failed: 'f-string: unmatched '(' (<unknown>, line 229)' (syntax-error)

-----------------------------------
Your code has been rated at 9.86/10

```
