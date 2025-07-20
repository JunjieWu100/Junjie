import yfinance as yf
import pandas as pd
import time
import logging
from ib_insync import *

# Initialize IBKR connection
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)  # Use port 7496 for paper trading

# Initialize logging
logging.basicConfig(filename='lvmh_trading_log.log', level=logging.INFO)
print("Script started successfully.")  # Immediate feedback
logging.info("Script started successfully.")  # Immediate log

# Fetch recent historical data from Yahoo Finance for LVMH (MC.PA)
def get_latest_price(ticker='MC.PA'):
    try:
        # Fetch the last minute of data
        historical_df = yf.download(ticker, interval='1m', period='1d')
        print(historical_df)  # Check the fetched data
        historical_df.reset_index(inplace=True)
        latest_price = historical_df['Close'].iloc[-1]  # Get the latest closing price
        return latest_price.item()  # Convert to scalar
    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        print(f"Error fetching historical data: {e}")
        return None

# Function to execute trades on IBKR for LVMH
def execute_trade(symbol, action, quantity):
    try:
        # Define the stock contract for LVMH (Euronext Paris)
        contract = Stock(symbol, 'SMART', 'EUR')  # LVMH trades in EUR on Euronext
        order = MarketOrder(action, quantity)  # Market order for Buy or Sell
        trade = ib.placeOrder(contract, order)

        # Wait for the order to be filled
        ib.sleep(1)  # Short wait for order to process
        if trade.orderStatus == "Filled":
            print(f"Placed {action} order for {quantity} shares of {symbol}.")
            logging.info(f"Placed {action} order for {quantity} shares of {symbol}.")
        else:
            print(f"Order for {quantity} shares of {symbol} not filled. Status: {trade.orderStatus}")

    except Exception as e:
        logging.error(f"Error executing trade: {e}")
        print(f"Error executing trade: {e}")

# Main loop for continuous trading
def main():
    symbol = 'MC.PA'  # LVMH on Euronext Paris
    previous_price = None  # Variable to store the previous price

    # Instant buy and sell upon start
    initial_price = get_latest_price(symbol)
    if initial_price is not None:
        print(f"Initial price for {symbol}: {initial_price:.2f}")
        execute_trade(symbol, 'BUY', 1)  # Initial buy
        time.sleep(1)  # Short delay for the order to process
        execute_trade(symbol, 'SELL', 1)  # Initial sell

    while True:
        # Fetch the latest price
        latest_price = get_latest_price(symbol)

        if latest_price is not None:
            print(f"Latest price for {symbol}: {latest_price:.2f}")
            logging.info(f"Latest price for {symbol}: {latest_price:.2f}")

            # Buy or Sell based on price movement
            if previous_price is None:  # First iteration
                previous_price = latest_price
                continue
            
            if latest_price > previous_price:
                print(f"Buy signal detected. Last closing price: {latest_price:.2f}")
                logging.info(f"Buy signal detected at {latest_price:.2f}.")
                execute_trade(symbol, 'BUY', 1)  # Buy 1 share
            elif latest_price < previous_price:
                print(f"Sell signal detected. Last closing price: {latest_price:.2f}")
                logging.info(f"Sell signal detected at {latest_price:.2f}.")
                execute_trade(symbol, 'SELL', 1)  # Sell 1 share

            # Update the previous price
            previous_price = latest_price

        # Sleep for 30 seconds before fetching new data
        time.sleep(30)

if __name__ == "__main__":
    print("Running main trading loop...")  # Immediate output
    main()
