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
Weather Processing/scrape_weather.py:153:4: R0902: Too many instance attributes (10/7) (too-many-instance-attributes)
************* Module plot_operations
Weather Processing/plot_operations.py:38:0: C0301: Line too long (133/100) (line-too-long)
Weather Processing/plot_operations.py:1:0: C0114: Missing module docstring (missing-module-docstring)
Weather Processing/plot_operations.py:9:0: R0903: Too few public methods (0/2) (too-few-public-methods)
Weather Processing/plot_operations.py:51:19: W0621: Redefining name 'temps' from outer scope (line 64) (redefined-outer-name)
Weather Processing/plot_operations.py:4:0: C0411: standard import "from datetime import datetime" should be placed before "import matplotlib.pyplot as plt" (wrong-import-order)
************* Module db_operations
Weather Processing/db_operations.py:43:0: C0301: Line too long (108/100) (line-too-long)
Weather Processing/db_operations.py:46:0: C0301: Line too long (121/100) (line-too-long)
Weather Processing/db_operations.py:47:0: C0301: Line too long (115/100) (line-too-long)
Weather Processing/db_operations.py:50:0: C0301: Line too long (113/100) (line-too-long)
Weather Processing/db_operations.py:55:0: C0301: Line too long (104/100) (line-too-long)
Weather Processing/db_operations.py:58:0: C0301: Line too long (115/100) (line-too-long)
Weather Processing/db_operations.py:70:0: C0301: Line too long (126/100) (line-too-long)
Weather Processing/db_operations.py:83:0: C0301: Line too long (109/100) (line-too-long)
Weather Processing/db_operations.py:101:0: C0301: Line too long (121/100) (line-too-long)
Weather Processing/db_operations.py:113:0: C0301: Line too long (133/100) (line-too-long)

-----------------------------------
Your code has been rated at 9.40/10

```
