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
Weather Processing/scrape_weather.py:36:9: W0511: TODO: No hard coding, there is a previous month button the page we can look for (fixme)
Weather Processing/scrape_weather.py:155:4: R0902: Too many instance attributes (10/7) (too-many-instance-attributes)
************* Module db_operations
Weather Processing/db_operations.py:67:0: C0301: Line too long (117/100) (line-too-long)
Weather Processing/db_operations.py:117:0: C0303: Trailing whitespace (trailing-whitespace)
Weather Processing/db_operations.py:67:13: W0511: TODO: Maybe add extra validation just in-case someone forgets to validate before calling this function. (fixme)
Weather Processing/db_operations.py:96:11: C0121: Comparison 'debug == True' should be 'debug is True' if checking for the singleton value True, or 'debug' if testing for truthiness (singleton-comparison)

-----------------------------------
Your code has been rated at 9.77/10

```
