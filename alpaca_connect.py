import alpaca_trade_api as tradeapi

# Use your own API key and secret here
API_KEY = 'PKSB3IMOM2RL3LX19TLD'
API_SECRET = 'gwnO2nNTlqvXH1pm5dKZgwvuw8yLVys5g41F9zQm'
BASE_URL = 'https://paper-api.alpaca.markets'  # Using paper trading endpoint

# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Check your account information
account = api.get_account()
print(account)
