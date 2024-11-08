import alpaca_trade_api as tradeapi
import pandas as pd
import time
import logging

# Use your actual API Key and Secret from Alpaca
API_KEY = 'PKFUXSML6CYUTIBQUED3'
API_SECRET = 'IQ3y6iVTzJgacvtL7X08xHDhysxpLuGTbr0lfep7'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading endpoint

# Initialize the API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Set up logging
logging.basicConfig(filename='elisa_trading_log.log', level=logging.INFO)
print("Script started successfully.")  # Immediate feedback
logging.info("Script started successfully.")  # Immediate log

# Fetch historical data to bootstrap the algorithm
def get_historical_data():
    try:
        # Fetch 15-minute bars for Elisa Oyj (to ensure enough data is fetched)
        barset = api.get_bars('ELISA.HE', tradeapi.TimeFrame.Minute, limit=15)  # Fetch 15 historical bars
        historical_df = pd.DataFrame({
            'time': [bar.t for bar in barset],
            'close': [bar.c for bar in barset]
        })
        print(f"Fetched {len(historical_df)} rows of historical data.")  # Immediate output
        logging.info(f"Fetched {len(historical_df)} rows of historical data.")
        print(historical_df.head())  # Print the historical data for debugging
        return historical_df
    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        print(f"Error fetching historical data: {e}")
        return pd.DataFrame(columns=['time', 'close'])

# Fetch the most recent real-time bar for Elisa Oyj (ELISA.HE)
def get_realtime_data():
    try:
        barset = api.get_bars('ELISA.HE', tradeapi.TimeFrame.Minute, limit=1)  # Fetch only the latest 1-minute bar
        realtime_df = pd.DataFrame({
            'time': [bar.t for bar in barset],
            'close': [bar.c for bar in barset]
        })
        print(f"Fetched real-time data: {len(realtime_df)} row.")  # Immediate output
        logging.info("Fetched real-time data.")
        print(realtime_df.head())  # Print the real-time data for debugging
        return realtime_df
    except Exception as e:
        logging.error(f"Error fetching real-time data: {e}")
        print(f"Error fetching real-time data: {e}")
        return pd.DataFrame(columns=['time', 'close'])

# Define the trading function to check signals and place trades
def execute_trade(df):
    # Ensure we don't have too much data (keep only the latest 5 rows for speed)
    df = df.tail(5).reset_index(drop=True)  # Shorten the length to only the necessary number of bars

    # Check if there is enough data to calculate moving averages
    if len(df) < 5:  # Need 5 bars to calculate the long-term moving average
        logging.info(f"Not enough data to calculate moving averages yet. Current rows: {len(df)}")
        print(f"Not enough data to calculate moving averages yet. Current rows: {len(df)}")  # Print debug info
        return df

    # Calculate short-term and long-term moving averages
    df['short_ma'] = df['close'].rolling(window=2).mean()  # Short-term moving average (2 periods)
    df['long_ma'] = df['close'].rolling(window=5).mean()  # Long-term moving average (5 periods)

    # Log moving averages for debugging
    logging.info(f"Short MA: {df['short_ma'].iloc[-1]}, Long MA: {df['long_ma'].iloc[-1]}")
    print(f"Short MA: {df['short_ma'].iloc[-1]}, Long MA: {df['long_ma'].iloc[-1]}")  # Immediate output

    # Ensure that the moving averages are not NaN
    if pd.isna(df['short_ma'].iloc[-1]) or pd.isna(df['long_ma'].iloc[-1]):
        logging.info("Not enough data for moving average calculations.")
        print("Not enough data for moving average calculations.")  # Immediate output
        return df

    # Generate signals: Buy = 1, Sell = -1
    df['signal'] = 0
    df['signal'][df['short_ma'] > df['long_ma']] = 1  # Buy signal when short MA is above long MA
    df['signal'][df['short_ma'] < df['long_ma']] = -1  # Sell signal when short MA is below long MA

    # Get the most recent signal (the last row)
    latest_signal = df['signal'].iloc[-1]
    latest_price = df['close'].iloc[-1]

    # Check and log the trade
    if latest_signal == 1:
        logging.info(f"Buy signal detected at {df['time'].iloc[-1]}: placing a buy order at {latest_price}")
        print(f"Buy signal detected: placing a buy order at {latest_price}")  # Immediate output
        api.submit_order(
            symbol='ELISA.HE',
            qty=1,  # Buy 1 share of Elisa Oyj
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    elif latest_signal == -1:
        logging.info(f"Sell signal detected at {df['time'].iloc[-1]}: placing a sell order at {latest_price}")
        print(f"Sell signal detected: placing a sell order at {latest_price}")  # Immediate output
        api.submit_order(
            symbol='ELISA.HE',
            qty=1,  # Sell 1 share of Elisa Oyj
            side='sell',
            type='market',
            time_in_force='gtc'
        )
    else:
        logging.info(f"No signal at {df['time'].iloc[-1]}")
        print(f"No signal at {df['time'].iloc[-1]}")  # Immediate output

    return df

# Main loop for continuous trading
def main():
    # Fetch historical data to start
    df = get_historical_data()

    while True:
        # Fetch real-time data and append it to the historical data
        new_data = get_realtime_data()
        df = pd.concat([df, new_data], ignore_index=True)

        # Execute trades based on the updated data
        df = execute_trade(df)

        time.sleep(60)  # Wait for 1 minute before checking again

# Run the main trading loop
if __name__ == "__main__":
    print("Running main trading loop...")  # Immediate output
    main()
