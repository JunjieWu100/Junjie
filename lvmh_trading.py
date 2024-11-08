import time
from ib_insync import *

# Connect to the IBKR API (assumes TWS is running on localhost, port 7497)
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define the stock you want to trade
stock = Stock('AAPL', 'SMART', 'USD')  # Replace with the stock symbol you are interested in

# Define your trading parameters
buy_threshold = 170.00  # Example threshold to buy if price drops below
sell_threshold = 180.00  # Example threshold to sell if price rises above
quantity = 10  # Number of shares to trade

# Function to get the current market price
def get_current_price():
    # Request market data
    ticker = ib.reqMktData(stock, '', False, False)
    ib.sleep(0.5)  # Allow time for data to be received
    return ticker.last  # Last traded price

# Function to place an order
def place_order(action, quantity):
    order = MarketOrder(action, quantity)
    trade = ib.placeOrder(stock, order)
    ib.sleep(1)  # Allow time for order to be placed
    print(f"{action} {quantity} shares of {stock.symbol} at market price.")
    return trade

# Main trading loop
try:
    while True:
        start_time = time.time()  # Record the start time
        
        current_price = get_current_price()
        print(f"Current price: {current_price}")
        
        # Decision to buy or sell based on thresholds
        if current_price is not None:  # Ensure price data was received
            if current_price < buy_threshold:
                place_order('BUY', quantity)
            elif current_price > sell_threshold:
                place_order('SELL', quantity)
        
        # Sleep for the remainder of the second, ensuring checks occur every second
        elapsed_time = time.time() - start_time
        time_to_sleep = max(0, 1 - elapsed_time)  # Ensure we wait only for the remainder of the second
        time.sleep(time_to_sleep)

except KeyboardInterrupt:
    print("Stopping the trading bot...")

finally:
    # Disconnect from IBKR API
    ib.disconnect()
