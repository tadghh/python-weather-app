# Weather Scraper Apprentice

![Application Icon](./Build%20Files/icons/icon.png)
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

After running *BuildMe.ps1* a dist folder will be created that contains the built CLI program.

Optional
> To create an installer use the spec file with Inno Setup

## Features
- PEP8 Compliant
- Multithreading
  - Can scrape weather data from 1996 to 2023 in 30 seconds
- Uses SQLite to store weather info
	- Added an index to quickly update data with distinct data
- Error handling
- UX focused menu
- Data visualization
	- Box plot that can show average temperatures for each month across a range of years
	- Line graph, this allows you to see the temperature of a specific month and year
- Error logging 

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

[![Pylint](https://github.com/tadghh/PythonWeatherApp/actions/workflows/pylint.yml/badge.svg?branch=main&event=push)](https://github.com/tadghh/PythonWeatherApp/actions/workflows/pylint.yml)

Here are the linting recommendations
```python

------------------------------------
Your code has been rated at 10.00/10

```
