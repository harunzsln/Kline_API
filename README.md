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

# Fetch data (last 30 hours)
end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
start_time = end_time - timedelta(hours=30)
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

Generates financial data for a specified date range (1-hour intervals).

```python
KlineGenerator.generate(start_date_str, end_date_str) → DataFrame
```

**Parameters:**
- `start_date_str`: Start date (`"YYYY-MM-DD HH:MM:SS"`)
- `end_date_str`: End date (`"YYYY-MM-DD HH:MM:SS"`)

**Returns:**
- Pandas DataFrame with `open` and `close` columns

### KlineReceiver

Takes hourly data and transforms it into different time intervals.

```python
receiver = KlineReceiver(generator_class=KlineGenerator)
```

**Methods:**

| Method | Description |
| :--- | :--- |
| `fetch(start, end)` | Runs the data generator and retrieves hourly data |
| `get_1h_klines()` | Returns 1-hour data |
| `get_4h_klines()` | Returns 4-hour data |
| `get_1d_klines()` | Returns 1-day data |

## How It Works

1. **When fetch() is called:**
   - `KlineGenerator.generate()` produces hourly data
   - `open` and `close` prices are created for each hour
   - Data is stored in `self.df_1h`

2. **When get_1h_klines() is called:**
   - Returns the stored 1-hour data directly

3. **When get_4h_klines() is called:**
   - 1-hour data is grouped into 4-hour blocks
   - The `open` value is taken from the first record of each block
   - The `close` value is taken from the last record of each block
   - A new DataFrame is returned

4. **When get_1d_klines() is called:**
   - 1-hour data is grouped into 1-day blocks
   - Same aggregation logic as 4-hour data

## Example Output

```
                     open      close
2023-05-01 00:00:00  100.12   100.45
2023-05-01 01:00:00  100.44   100.78
2023-05-01 02:00:00  100.77   100.92
```

## Architecture

**KlineGenerator** → Produces hourly data
**KlineReceiver** → Processes and transforms data into different intervals

The two classes work independently. `KlineReceiver` doesn't know where the data comes from. `KlineGenerator` doesn't know how the data will be processed.

## File Structure

```
kline_api.py
├── KlineGenerator (class)
│   └── generate() (static method)
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

The program will generate data for the last 30 hours and display it in 1h, 4h, and 1D formats.

## Data Flow

```
fetch(start, end)
    ↓
KlineGenerator.generate()
    ↓
Hourly data (df_1h)
    ↓
get_1h_klines()  →  1-hour data
get_4h_klines()  →  4-hour data (resample + aggregate)
get_1d_klines()  →  1-day data (resample + aggregate)
```
