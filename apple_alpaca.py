import yfinance as yf
import pandas as pd
import time
import logging
import alpaca_trade_api as tradeapi

# Alpaca API setup
API_KEY = 'PKFUXSML6CYUTIBQUED3'
API_SECRET = 'IQ3y6iVTzJgacvtL7X08xHDhysxpLuGTbr0lfep7'
BASE_URL = 'https://paper-api.alpaca.markets'  # For paper trading, use the live URL for live trading

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Initialize logging
logging.basicConfig(filename='aapl_trading_log.log', level=logging.INFO)
print("Script started successfully.")  # Immediate feedback
logging.info("Script started successfully.")  # Immediate log

# Fetch historical daily data from Yahoo Finance for AAPL
def get_historical_data():
    try:
        # Fetch daily bars for AAPL (Apple Inc.)
        ticker = 'AAPL'
        historical_df = yf.download(ticker, interval='1d', period='1mo')  # Daily data for the last month
        historical_df.reset_index(inplace=True)  # Reset index to get time in a column
        historical_df.rename(columns={"Date": "time", "Close": "close"}, inplace=True)
        print(f"Fetched {len(historical_df)} rows of historical data.")  # Immediate output
        logging.info(f"Fetched {len(historical_df)} rows of historical data.")
        print(historical_df.head())  # Print the historical data for debugging
        return historical_df[['time', 'close']]  # Return only time and close columns
    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        print(f"Error fetching historical data: {e}")
        return pd.DataFrame(columns=['time', 'close'])

# Define the trading function to calculate moving averages and generate signals
def execute_trade(df):
    # Calculate short-term and long-term moving averages
    df['short_ma'] = df['close'].rolling(window=2).mean()  # Short-term moving average (2 days)
    df['long_ma'] = df['close'].rolling(window=5).mean()  # Long-term moving average (5 days)

    # Log moving averages for debugging
    logging.info(f"Short MA: {df['short_ma'].iloc[-1]}, Long MA: {df['long_ma'].iloc[-1]}")
    print(f"Short MA: {df['short_ma'].iloc[-1]}, Long MA: {df['long_ma'].iloc[-1]}")  # Immediate output

    # Generate buy/sell signals: Buy = 1, Sell = -1 using .loc[] to avoid SettingWithCopyWarning
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1  # Buy when short MA crosses above long MA
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Sell when short MA crosses below long MA

    # Get the most recent signal
    latest_signal = df['signal'].iloc[-1]
    latest_price = df['close'].iloc[-1].item()  # Convert to scalar

    # Execute trade based on the signal
    symbol = 'AAPL'  # AAPL for Apple Inc.
    if latest_signal == 1:
        # Buy action
        print(f"Buy signal detected. Last closing price: {latest_price:.2f}")
        logging.info(f"Buy signal detected at {df['time'].iloc[-1]}.")
        try:
            api.submit_order(
                symbol=symbol,
                qty=1,  # Buy 1 share of AAPL
                side='buy',
                type='market',
                time_in_force='gtc'  # Good 'til canceled
            )
            print("Buy order placed successfully.")
        except Exception as e:
            logging.error(f"Error placing buy order: {e}")
            print(f"Error placing buy order: {e}")
    elif latest_signal == -1:
        # Sell action
        print(f"Sell signal detected. Last closing price: {latest_price:.2f}")
        logging.info(f"Sell signal detected at {df['time'].iloc[-1]}.")
        try:
            api.submit_order(
                symbol=symbol,
                qty=1,  # Sell 1 share of AAPL
                side='sell',
                type='market',
                time_in_force='gtc'  # Good 'til canceled
            )
            print("Sell order placed successfully.")
        except Exception as e:
            logging.error(f"Error placing sell order: {e}")
            print(f"Error placing sell order: {e}")
    else:
        print(f"No signal at {df['time'].iloc[-1]}")
        logging.info(f"No signal at {df['time'].iloc[-1]}")

# Main loop for continuous trading
def main():
    # Fetch historical data to start
    df = get_historical_data()

    while True:
        # Check if we have enough rows to calculate moving averages
        if len(df) < 5:
            print(f"Still not enough data to calculate moving averages. Current rows: {len(df)}")
            time.sleep(60)  # Wait for a minute before retrying
            continue

        # Execute trade logic
        execute_trade(df)

        # End the loop after calculating moving averages and signals once
        break

if __name__ == "__main__":
    print("Running main trading loop...")  # Immediate output
    main()
