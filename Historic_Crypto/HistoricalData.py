import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from random import randint

class HistoricalData:
    """
    Retrieves historical cryptocurrency data from the Coinbase Advanced Trade API.
    """
    def __init__(self, ticker, granularity, start_date, end_date=None, api_key=None, api_secret=None, passphrase=None, verbose=True):
        self.ticker = ticker
        self.granularity = granularity
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.now().strftime("%Y-%m-%d-%H-%M")
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.verbose = verbose
        self.base_url = "https://api.exchange.coinbase.com"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'  # Use the API key for authentication
        }

    def _date_cleaner(self, date_time):
        """Formats dates in ISO format for the API."""
        if isinstance(date_time, str):
            return datetime.strptime(date_time, '%Y-%m-%d-%H-%M').isoformat()
        elif isinstance(date_time, datetime):
            return date_time.isoformat()
        else:
            raise TypeError("Invalid date format. Must be a string or datetime object.")

    def retrieve_data(self):
        """Fetch historical data in chunks to handle API limits."""
        if self.verbose:
            print("Formatting dates...")
        start_iso = self._date_cleaner(self.start_date)
        end_iso = self._date_cleaner(self.end_date)
    
        # Calculate the maximum interval size based on granularity
        max_interval_seconds = self.granularity * 300  # Maximum 300 data points
        max_interval_days = max_interval_seconds / (60 * 60 * 24)  # Convert to days
    
        start = datetime.strptime(self.start_date, "%Y-%m-%d-%H-%M")
        end = datetime.strptime(self.end_date, "%Y-%m-%d-%H-%M")
    
        # Initialize the data container
        data = pd.DataFrame()
    
        # Iterate over chunks
        current_start = start
        while current_start < end:
            current_end = min(current_start + timedelta(days=max_interval_days), end)
            start_chunk_iso = self._date_cleaner(current_start.strftime("%Y-%m-%d-%H-%M"))
            end_chunk_iso = self._date_cleaner(current_end.strftime("%Y-%m-%d-%H-%M"))
    
            # Request data for the chunk
            url = f"{self.base_url}/products/{self.ticker}/candles"
            params = {
                'start': start_chunk_iso,
                'end': end_chunk_iso,
                'granularity': self.granularity
            }
    
            if self.verbose:
                print(f"Requesting data chunk: {start_chunk_iso} to {end_chunk_iso}")
    
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                chunk_data = pd.DataFrame(response.json(), columns=["time", "low", "high", "open", "close", "volume"])
                chunk_data["time"] = pd.to_datetime(chunk_data["time"], unit='s')
                data = pd.concat([data, chunk_data], ignore_index=True)
                if self.verbose:
                    print(f"Retrieved {len(chunk_data)} rows.")
            else:
                print(f"Error: Status code {response.status_code}, message: {response.json()}")
                response.raise_for_status()
    
            # Move to the next interval
            current_start = current_end
            time.sleep(randint(0, 2))  # Avoid rate limiting
    
        # Finalize the DataFrame
        data.set_index("time", inplace=True)
        data.sort_index(ascending=True, inplace=True)
        return data



# Example Usage
#api_key = "" # replace with your CoinBase API key
#ticker = 'BTC-USD'
#granularity = 3600
#start_date = '2021-06-01-00-00'
#end_date = '2021-07-01-00-00'
#
#historical_data = HistoricalData_new(ticker, granularity, start_date, end_date, api_key=api_key)
#data = historical_data.retrieve_data()
#print(data.head())

