# Python Weather App

# Features
- Multithreading
  - Can scrape weather data from 1996 to 2023 in under 55 seconds
- Error handling
- Data Visualization
Bump
# To-do
- Check platform support
  - Add workflow to make installers
- Finish UI
- Add Linux/macOS support 

## Status


Our code quality is currently...

[![Pylint](https://github.com/tadghh/PythonWeatherApp/actions/workflows/pylint.yml/badge.svg?branch=main&event=push)](https://github.com/tadghh/PythonWeatherApp/actions/workflows/pylint.yml)

Here are the linting recommendations
```python
************* Module scrape_weather
Weather Processing/scrape_weather.py:219:4: R0902: Too many instance attributes (10/7) (too-many-instance-attributes)
************* Module plot_operations
Weather Processing/plot_operations.py:15:5: W0511: TODO: Cant take input in this way, must be given from weather_processor. (fixme)
************* Module db_operations
Weather Processing/db_operations.py:69:0: C0301: Line too long (117/100) (line-too-long)
Weather Processing/db_operations.py:40:5: W0511: TODO: Need a query to get the most recent date in the data base (fixme)
Weather Processing/db_operations.py:69:13: W0511: TODO: Maybe add extra validation just in-case someone forgets to validate before calling this function. (fixme)

-----------------------------------
Your code has been rated at 9.85/10

```
