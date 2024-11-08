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

# Fetch recent historical data from Yahoo Finance for LVMH (MC)
def get_historical_data(ticker='MC'):
    try:
        historical_df = yf.download(ticker, interval='1m', period='1d')  # Fetch minute-level data for the last day
        historical_df.reset_index(inplace=True)  # Reset index to get time in a column
        historical_df.rename(columns={"Datetime": "time", "Close": "close"}, inplace=True)
        print(f"Fetched {len(historical_df)} rows of historical data.")  # Immediate output
        logging.info(f"Fetched {len(historical_df)} rows of historical data.")
        return historical_df[['time', 'close']]  # Return only time and close columns
    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        print(f"Error fetching historical data: {e}")
        return pd.DataFrame(columns=['time', 'close'])

# Function to execute trades on IBKR for LVMH
def execute_trade(symbol, action, quantity):
    # Define the stock contract for LVMH (Euronext Paris)
    contract = Stock(symbol, 'SMART', 'EUR')  # LVMH trades in EUR on Euronext
    order = MarketOrder(action, quantity)  # Market order for Buy or Sell
    trade = ib.placeOrder(contract, order)
    print(f"Placed {action} order for {quantity} shares of {symbol}.")
    return trade

# Define the trading function to calculate moving averages and generate signals
def execute_trading_strategy(df, symbol):
    # Calculate short-term and long-term moving averages
    df['short_ma'] = df['close'].rolling(window=2).mean()  # Short-term moving average (2 periods)
    df['long_ma'] = df['close'].rolling(window=5).mean()  # Long-term moving average (5 periods)

    # Log moving averages for debugging
    logging.info(f"Short MA: {df['short_ma'].iloc[-1]}, Long MA: {df['long_ma'].iloc[-1]}")
    print(f"Short MA: {df['short_ma'].iloc[-1]}, Long MA: {df['long_ma'].iloc[-1]}")  # Immediate output

    # Generate buy/sell signals: Buy = 1, Sell = -1
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1  # Buy when short MA crosses above long MA
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Sell when short MA crosses below long MA

    # Get the most recent signal
    latest_signal = df['signal'].iloc[-1]
    latest_price = df['close'].iloc[-1].item()  # Convert to scalar

    # Execute trade based on the signal
    if latest_signal == 1:
        # Buy action
        print(f"Buy signal detected. Last closing price: {latest_price:.2f}")
        logging.info(f"Buy signal detected at {df['time'].iloc[-1]}.")
        execute_trade(symbol, 'BUY', 1)
    elif latest_signal == -1:
        # Sell action
        print(f"Sell signal detected. Last closing price: {latest_price:.2f}")
        logging.info(f"Sell signal detected at {df['time'].iloc[-1]}.")
        execute_trade(symbol, 'SELL', 1)
    else:
        print(f"No signal at {df['time'].iloc[-1]}")
        logging.info(f"No signal at {df['time'].iloc[-1]}")

# Main loop for continuous trading
def main():
    symbol = 'MC'  # LVMH on Euronext Paris

    while True:
        # Fetch the most recent data
        df = get_historical_data(symbol)

        # Check if we have enough rows to calculate moving averages
        if len(df) >= 5:
            # Execute trading strategy based on the moving averages
            execute_trading_strategy(df, symbol)

        # Sleep for 60 seconds (1 minute) before fetching new data
        time.sleep(60)

if __name__ == "__main__":
    print("Running main trading loop...")  # Immediate output
    main()
