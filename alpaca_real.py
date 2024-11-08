import alpaca_trade_api as tradeapi
import pandas as pd
import time

# Use your actual API Key and Secret
API_KEY = 'PKSB3IMOM2RL3LX19TLD'
API_SECRET = 'gwnO2nNTlqvXH1pm5dKZgwvuw8yLVys5g41F9zQm'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading endpoint

# Initialize the API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Fetch real-time data (for example, AAPL)
def get_realtime_data():
    barset = api.get_barset('AAPL', 'minute', limit=5)  # Get the last 5 minutes of data
    df = pd.DataFrame({
        'time': [bar.t for bar in barset['AAPL']],
        'close': [bar.c for bar in barset['AAPL']]
    })
    return df

# Example: Get the latest data and print it
df = get_realtime_data()
print(df)
