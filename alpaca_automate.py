import alpaca_trade_api as tradeapi
import pandas as pd
import time
import logging

# Use your actual API Key and Secret
API_KEY = 'PKFUXSML6CYUTIBQUED3'
API_SECRET = 'IQ3y6iVTzJgacvtL7X08xHDhysxpLuGTbr0lfep7'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading endpoint

# Initialize the API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Set up logging
logging.basicConfig(filename='btc_trading_log.log', level=logging.INFO)

# Initialize an empty DataFrame to store past data
df = pd.DataFrame(columns=['time', 'close'])

def get_realtime_data():
    try:
        # Fetch the most recent 10-minute bars for BTCUSD
        barset = api.get_bars('BTCUSD', tradeapi.TimeFrame.Minute, limit=10)  # Fetch 10 bars initially
        new_data = pd.DataFrame({
            'time': [bar.t for bar in barset],
            'close': [bar.c for bar in barset]
        })
        return new_data
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame(columns=['time', 'close'])

# Define the trading function to check signals and place trades
def execute_trade():
    global df  # Access the global DataFrame to store past bars

    # Fetch the latest data
    new_data = get_realtime_data()

    # Append the new data to the DataFrame
    df = pd.concat([df, new_data], ignore_index=True)

    # Ensure we don't have too much data (keep only the latest 10 rows)
    df = df.tail(10).reset_index(drop=True)  # Shorten the length to only the necessary number of bars

    # Log the number of collected bars
    logging.info(f"Collected {len(df)} bars so far.")
    
    # Check if there is enough data to calculate moving averages
    if len(df) < 10:  # Need 10 bars to calculate the long-term moving average
        logging.info("Not enough data to calculate moving averages yet.")
        return

    # Calculate short-term and long-term moving averages
    df['short_ma'] = df['close'].rolling(window=3).mean()  # Short MA (3 periods)
    df['long_ma'] = df['close'].rolling(window=10).mean()  # Long MA (10 periods)

    # Ensure that the moving averages are not NaN
    if pd.isna(df['short_ma'].iloc[-1]) or pd.isna(df['long_ma'].iloc[-1]):
        logging.info("Not enough data for moving average calculations.")
        return

    # Generate signals: Buy = 1, Sell = -1
    df['signal'] = 0
    df['signal'][df['short_ma'] > df['long_ma']] = 1  # Buy
    df['signal'][df['short_ma'] < df['long_ma']] = -1  # Sell

    # Get the most recent signal (the last row)
    latest_signal = df['signal'].iloc[-1]
    latest_price = df['close'].iloc[-1]

    # Check and log the trade
    try:
        if latest_signal == 1:
            logging.info(f"Buy signal detected at {df['time'].iloc[-1]}: placing a buy order at {df['close'].iloc[-1]}")
            api.submit_order(
                symbol='BTCUSD',
                qty=0.001,  # Use small fractions for Bitcoin trades
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        elif latest_signal == -1:
            logging.info(f"Sell signal detected at {df['time'].iloc[-1]}: placing a sell order at {df['close'].iloc[-1]}")
            api.submit_order(
                symbol='BTCUSD',
                qty=0.001,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
        else:
            logging.info(f"No signal at {df['time'].iloc[-1]}")
    except Exception as e:
        logging.error(f"Error placing order: {e}")

# Execute one trade
execute_trade()  # Only run once for a single trade
