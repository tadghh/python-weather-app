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
Weather Processing/scrape_weather.py:151:4: R0902: Too many instance attributes (10/7) (too-many-instance-attributes)
************* Module plot_operations
Weather Processing/plot_operations.py:39:0: C0301: Line too long (133/100) (line-too-long)
Weather Processing/plot_operations.py:1:0: C0114: Missing module docstring (missing-module-docstring)
Weather Processing/plot_operations.py:10:0: R0903: Too few public methods (0/2) (too-few-public-methods)
Weather Processing/plot_operations.py:40:4: C0116: Missing function or method docstring (missing-function-docstring)
Weather Processing/plot_operations.py:51:19: W0621: Redefining name 'temps' from outer scope (line 64) (redefined-outer-name)
Weather Processing/plot_operations.py:5:0: C0411: standard import "from datetime import datetime" should be placed before "import matplotlib.pyplot as plt" (wrong-import-order)
Weather Processing/plot_operations.py:3:0: W0611: Unused numpy imported as np (unused-import)
************* Module db_operations
Weather Processing/db_operations.py:44:0: C0301: Line too long (108/100) (line-too-long)
Weather Processing/db_operations.py:47:0: C0301: Line too long (121/100) (line-too-long)
Weather Processing/db_operations.py:48:0: C0301: Line too long (115/100) (line-too-long)
Weather Processing/db_operations.py:51:0: C0301: Line too long (113/100) (line-too-long)
Weather Processing/db_operations.py:56:0: C0301: Line too long (104/100) (line-too-long)
Weather Processing/db_operations.py:59:0: C0301: Line too long (115/100) (line-too-long)
Weather Processing/db_operations.py:71:0: C0301: Line too long (126/100) (line-too-long)
Weather Processing/db_operations.py:83:0: C0301: Line too long (109/100) (line-too-long)
Weather Processing/db_operations.py:101:0: C0301: Line too long (121/100) (line-too-long)
Weather Processing/db_operations.py:113:0: C0301: Line too long (133/100) (line-too-long)
Weather Processing/db_operations.py:120:0: C0301: Line too long (101/100) (line-too-long)
Weather Processing/db_operations.py:153:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
Weather Processing/db_operations.py:89:12: W0621: Redefining name 'error' from outer scope (line 82) (redefined-outer-name)
Weather Processing/db_operations.py:122:16: E1101: Instance of 'DBOperations' has no 'save_date' member; maybe 'save_data'? (no-member)
Weather Processing/db_operations.py:124:12: W0621: Redefining name 'error' from outer scope (line 117) (redefined-outer-name)
Weather Processing/db_operations.py:153:19: E1101: Instance of 'DBOperations' has no 'burn' member (no-member)
Weather Processing/db_operations.py:162:84: E1101: Instance of 'DBOperations' has no 'burn' member (no-member)
Weather Processing/db_operations.py:133:25: W0613: Unused argument 'burn' (unused-argument)

-----------------------------------
Your code has been rated at 8.59/10

```
