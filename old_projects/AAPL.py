import time
import alpaca_trade_api as tradeapi
from datetime import datetime

# Alpaca API keys (Replace with your own keys)
API_KEY = 'your-api-key-here'
API_SECRET = 'your-secret-key-here'
BASE_URL = 'https://paper-api.alpaca.markets'

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Stock symbol and quantity to trade
symbol = 'AAPL'
quantity = 1  # Number of shares to trade each time

# Function to get the latest trade price of AAPL
def get_last_price(symbol):
    trade = api.get_latest_trade(symbol)
    return trade.price

# Main trading loop
try:
    last_price = get_last_price(symbol)  # Get the initial last price

    while True:
        # Get the latest price of AAPL
        current_price = get_last_price(symbol)
        print(f"{datetime.now()}: Current price of {symbol}: ${current_price}")

        # Calculate thresholds for buying/selling
        buy_threshold = last_price - 0.01  # Buy if the price drops 0.01 below the last price
        sell_threshold = last_price + 0.01  # Sell if the price rises 0.01 above the last price

        # Check if the price is below the buy threshold
        if current_price < buy_threshold:
            print(f"Buying {quantity} shares of {symbol} at ${current_price}")
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            last_price = current_price  # Update last price after buying

        # Check if the price is above the sell threshold
        elif current_price > sell_threshold:
            print(f"Selling {quantity} shares of {symbol} at ${current_price}")
            api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            last_price = current_price  # Update last price after selling

        # Wait for 1 second before the next iteration
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")
