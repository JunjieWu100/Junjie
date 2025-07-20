import time
from datetime import datetime
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET

# Your Binance Testnet API keys
api_key = '3SO3ExbmTM8v37lorB841KXhEihX9ssMnTYuMMlXxDeNbQMdxd43kN6n825KqUoS'
api_secret = '2VZavaixPYNYVzChtxpRb0IS1mis0TaHXmcuMm0lCaYrjJ7MHan5SVNR01myAwFn'

# Initialize the Binance Testnet client
client = Client(api_key, api_secret, testnet=True)

# Function to place a market order
def place_order(symbol, side, quantity):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"Order successful: {side} {quantity} {symbol}")
        print(order)
    except Exception as e:
        print(f"Error placing order: {e}")

# Function to get the current price of the symbol
def get_market_price(symbol):
    try:
        ticker = client.futures_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"Error fetching market price: {e}")
        return None

# Automated trading loop based on price movement
def trading_loop(symbol, quantity):
    previous_price = None  # To store the previous price
    
    while True:
        current_price = get_market_price(symbol)
        
        if current_price is not None:
            # Print the current time and price for debugging
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"{current_time} - Current price of {symbol}: {current_price}")

            if previous_price is not None:
                if current_price > previous_price:
                    # Price went up, place a buy order
                    place_order(symbol, SIDE_BUY, quantity)
                elif current_price < previous_price:
                    # Price went down, place a sell order
                    place_order(symbol, SIDE_SELL, quantity)

            # Update the previous price for the next loop
            previous_price = current_price

        # Check price every second (adjust as needed)
        time.sleep(1)

# Run the trading loop on BTCUSDT with 0.001 BTC quantity
trading_loop('BTCUSDT', 0.001)
