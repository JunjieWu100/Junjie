from binance.client import Client

# Your Binance Testnet API keys
api_key = '3SO3ExbmTM8v37lorB841KXhEihX9ssMnTYuMMlXxDeNbQMdxd43kN6n825KqUoS'
api_secret = '2VZavaixPYNYVzChtxpRb0IS1mis0TaHXmcuMm0lCaYrjJ7MHan5SVNR01myAwFn'

# Connect to Binance Testnet by setting testnet=True
client = Client(api_key, api_secret, testnet=True)

# Test getting futures account balance
try:
    balance = client.futures_account_balance()
    print(balance)
except Exception as e:
    print(f"Error: {e}")
