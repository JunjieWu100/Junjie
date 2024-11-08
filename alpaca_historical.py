import alpaca_trade_api as tradeapi
import pandas as pd

# Use your actual API Key and Secret
API_KEY = 'PKSB3IMOM2RL3LX19TLD'
API_SECRET = 'gwnO2nNTlqvXH1pm5dKZgwvuw8yLVys5g41F9zQm'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading endpoint

# Initialize the API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Fetch historical price data for AAPL using IEX feed
barset = api.get_bars('AAPL', tradeapi.TimeFrame.Minute, '2024-10-01', '2024-10-20', feed='iex')

# Convert the bars into a Pandas DataFrame
df = pd.DataFrame({
    'time': [bar.t for bar in barset],  # Time of each bar
    'close': [bar.c for bar in barset]  # Closing price of each bar
})

# Calculate short and long moving averages
df['short_ma'] = df['close'].rolling(window=5).mean()  # 5-period MA
df['long_ma'] = df['close'].rolling(window=20).mean()  # 20-period MA

# Generate buy/sell signals
df['signal'] = 0
df['signal'][df['short_ma'] > df['long_ma']] = 1  # Buy
df['signal'][df['short_ma'] < df['long_ma']] = -1  # Sell

# Print the last 10 rows of the DataFrame
print(df.tail(10))

logging.info(f"Collected {len(df)} bars so far.")