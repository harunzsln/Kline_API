import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class KlineGenerator:
    @staticmethod
    def generate(start_date_str: str, end_date_str: str):
       
        print(f"KlineGenerator: Generating data between {start_date_str} and {end_date_str}...")

        # 1. Step: Create a date range for 1-minute intervals
        kline_starts = pd.to_datetime(pd.date_range(start=start_date_str, end=end_date_str, freq='1min'))
        
        if len(kline_starts) < 2:
            return pd.DataFrame()

        # 2. Step: Generate price series
        num_points = len(kline_starts)
        price_changes = 1 + np.random.randn(num_points) / 1000

        prices = 100 * price_changes.cumprod() 

        # 3. Step: Create Open and Close DataFrames
        data = {
            'open': prices[:-1],
            'close': prices[1:]
        }
        
        df = pd.DataFrame(data, index=kline_starts[:-1])
        
        print(f"KlineGenerator: {len(df)} minute candles generated.")
        return df

class KlineReceiver:
    def __init__(self, generator_class):
        self._generator = generator_class
        self._raw_data = pd.DataFrame()
        self.df_1h = pd.DataFrame()
        print("KlineReceiver class initialized.")

    def fetch(self, start_date_str: str, end_date_str: str):
        print("\nKlineReceiver: 'fetch' method is being executed...")
        self._raw_data = self._generator.generate(start_date_str, end_date_str)
        print(f"Fetch completed. {len(self._raw_data)} rows of raw data fetched.")

    def get_1h_klines(self):
        print("\nKlineReceiver: 'get_1h_klines' method is being executed...")
        if self._raw_data.empty:
            print("Warning: No raw data available for processing. Please run the 'fetch' method first.")
            self.df_1h = pd.DataFrame()
            return self.df_1h

        aggregation_rules = {
            'open': 'first',
            'close': 'last'
        }
        
        self.df_1h = self._raw_data.resample('1h').agg(aggregation_rules)
        self.df_1h.dropna(inplace=True)
        
        print(f"get_1h_klines completed. {len(self.df_1h)} 1-hour candles generated.")
        return self.df_1h

    def get_4h_klines(self):
        print("\nKlineReceiver: 'get_4h_klines' method is being executed...")
        if self._raw_data.empty:
            print("Warning: No raw data available for processing. Please run the 'fetch' method first.")
            return pd.DataFrame()

       
        df_4h = self._raw_data.resample('4h').agg({'open': 'first', 'close': 'last'})
        df_4h.dropna(inplace=True)
        
        print(f"get_4h_klines completed. {len(df_4h)} 4-hour candles generated.")
        return df_4h

    def get_1d_klines(self):
        print("\nKlineReceiver: 'get_1d_klines' method is being executed...")
        if self._raw_data.empty:
            print("Warning: No raw data available for processing. Please run the 'fetch' method first.")
            return pd.DataFrame()

        
        df_1d = self._raw_data.resample('1D').agg({'open': 'first', 'close': 'last'})
        df_1d.dropna(inplace=True)
        
        print(f"get_1d_klines completed. {len(df_1d)} 1-day klines generated.")
        return df_1d


if __name__ == "__main__":
    # 1. Create a KlineReceiver object by providing the KlineGenerator class as the data generator.
    receiver = KlineReceiver(generator_class=KlineGenerator)

    # 2. Getting data for the last 2 days
    end_time = datetime.now()
    start_time = end_time - timedelta(days=2)
    start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
    
    receiver.fetch(start_str, end_str)

    # 3. Fetch kline data for different timeframes
    df_1h = receiver.get_1h_klines()
    print("\n--- 1 Hour data ---")
    print(df_1h.tail())

    df_4h = receiver.get_4h_klines()
    print("\n--- 4 Hour data ---")
    print(df_4h.tail())

    df_1d = receiver.get_1d_klines()
    print("\n--- 1 Day data ---")
    print(df_1d.tail())
