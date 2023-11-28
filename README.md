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
************* Module db_operations
Weather Processing/db_operations.py:285:1: E0001: Parsing failed: 'expected an indented block after 'if' statement on line 269 (<unknown>, line 285)' (syntax-error)
************* Module scrape_weather
Weather Processing/scrape_weather.py:36:9: W0511: TODO: No hard coding, there is a previous month button the page we can look for (fixme)
Weather Processing/scrape_weather.py:155:4: R0902: Too many instance attributes (10/7) (too-many-instance-attributes)
************* Module plot_operations
Weather Processing/plot_operations.py:4:0: E0001: Cannot import 'db_operations' due to 'expected an indented block after 'if' statement on line 269 (<unknown>, line 285)' (syntax-error)

-----------------------------------
Your code has been rated at 9.30/10

```
