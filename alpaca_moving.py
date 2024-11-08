# Generate buy (1) and sell (-1) signals
df['signal'] = 0  # Default signal is 0 (no action)
df['signal'][df['short_ma'] > df['long_ma']] = 1  # Buy signal when short MA > long MA
df['signal'][df['short_ma'] < df['long_ma']] = -1  # Sell signal when short MA < long MA

# Print the last few rows to see the signals
print(df.tail())
