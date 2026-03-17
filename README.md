# Kline API

A Python API that generates financial data (open/close prices) and transforms it into different time intervals (1h, 4h, 1D).

## Installation

```bash
pip install pandas numpy
```

## Quick Start

```python
from kline_api import KlineGenerator, KlineReceiver
from datetime import datetime, timedelta

# Create a receiver
receiver = KlineReceiver(generator_class=KlineGenerator)

# Fetch data (last 2 days)
end_time = datetime.now()
start_time = end_time - timedelta(days=2)
start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

receiver.fetch(start_str, end_str)

# Get data in different time intervals
df_1h = receiver.get_1h_klines()
df_4h = receiver.get_4h_klines()
df_1d = receiver.get_1d_klines()

# View results
print(df_1h.head())
```

## API Reference

### KlineGenerator

Generates fake financial data for a specified date range.

```python
KlineGenerator.generate(start_date_str, end_date_str) → DataFrame
```

**Parameters:**
- `start_date_str`: Start date (`"YYYY-MM-DD HH:MM:SS"`)
- `end_date_str`: End date (`"YYYY-MM-DD HH:MM:SS"`)

**Returns:**
- Pandas DataFrame with `open` and `close` columns

### KlineReceiver

Takes raw data and transforms it into different time intervals.

```python
receiver = KlineReceiver(generator_class=KlineGenerator)
```

**Methods:**

| Method | Description |
| :--- | :--- |
| `fetch(start, end)` | Runs the data generator and retrieves raw data |
| `get_1h_klines()` | Returns 1-hour data |
| `get_4h_klines()` | Returns 4-hour data |
| `get_1d_klines()` | Returns 1-day data |

## How It Works

1. **When fetch() is called:**
   - `KlineGenerator.generate()` produces data
   - `open` and `close` prices are created for each minute
   - Data is stored in `self._raw_data`

2. **When get_1h_klines() is called:**
   - Minute-level data is grouped into 1-hour blocks
   - The `open` value is taken from the first record of each block
   - The `close` value is taken from the last record of each block
   - A new DataFrame is returned

3. **get_4h_klines() and get_1d_klines() work the same way**

## Example Output

```
                     open      close
2023-05-01 00:00:00  100.12   100.45
2023-05-01 01:00:00  100.44   100.78
2023-05-01 02:00:00  100.77   100.92
```

## Architecture

**KlineGenerator** → Produces raw data (minute-level)
**KlineReceiver** → Processes data (hourly, 4-hourly, daily)

The two classes work independently. `KlineReceiver` doesn't know where the data comes from. `KlineGenerator` doesn't know how the data will be processed.

## File Structure

```
kline_api.py
├── KlineGenerator (class)
│   └── generate() (method)
└── KlineReceiver (class)
    ├── __init__() (constructor)
    ├── fetch() (method)
    ├── get_1h_klines() (method)
    ├── get_4h_klines() (method)
    └── get_1d_klines() (method)
```

## Running

```bash
python kline_api.py
```

The program will generate data for the last 2 days and display it in 1h, 4h, and 1D formats.
