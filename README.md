# Weather Scraper Apprentice

<p align="center">
  <img src="./Build%20Files/icons/icon.png">
</p>

## Building

- Install Python 3.12
- Create a virtual environment
- Run BuildMe.ps1
  - Temporarily bypass the execution policy

### Download and Build

```
git clone git@github.com:tadghh/PythonWeatherApp.git
cd .\PythonWeatherApp\
python -m venv venv
venv\Scripts\activate
pip install -r '.\Weather Processing\requirements.txt'
powershell -ExecutionPolicy Bypass -File .\BuildMe.ps1
```

After running _BuildMe.ps1_ a dist folder will be created that contains the built CLI program.

_Optional_

> The [Inno Script.iss](./Inno%20Script.iss) file can be used with [Inno Setup](https://jrsoftware.org/isdl.php#stable) to create an installer

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

## Libraries

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

## Code quality

Our code quality is currently...

[![Pylint](https://github.com/tadghh/python-weather-app/actions/workflows/pylint.yml/badge.svg?branch=main&event=push)](https://github.com/tadghh/python-weather-app/actions/workflows/pylint.yml)

Here are the linting recommendations

```python

------------------------------------
Your code has been rated at 10.00/10

```
