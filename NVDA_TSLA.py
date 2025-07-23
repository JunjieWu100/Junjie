# 📊 Finance Dashboard with yfinance (Colab-Compatible & Fixed)

!pip install yfinance --quiet

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- 🔧 CONFIGURATION ---
TICKERS = ['NVDA', 'TSLA']  # Change to your portfolio
START_DATE = '2022-01-01'
END_DATE = '2025-07-23'
INVESTED_AMOUNT = 10000  # Total simulated investment

# --- 📥 DOWNLOAD DATA (Corrected for yfinance changes) ---
df = yf.download(TICKERS, start=START_DATE, end=END_DATE, auto_adjust=True)

# Handle multi-index DataFrame for multiple tickers
if isinstance(df.columns, pd.MultiIndex):
    if 'Adj Close' in df.columns.levels[0]:
        data = df['Adj Close']
    elif 'Close' in df.columns.levels[0]:
        data = df['Close']
    else:
        raise ValueError("Couldn't find 'Adj Close' or 'Close' in data.")
else:
    data = df[['Adj Close']] if 'Adj Close' in df.columns else df[['Close']]
    data.columns = TICKERS  # Single ticker case fallback

data.dropna(inplace=True)

# --- 📈 DAILY RETURNS ---
daily_returns = data.pct_change().dropna()

# --- 📈 CUMULATIVE RETURNS ---
cumulative_returns = (1 + daily_returns).cumprod()

# --- 💰 SIMULATED PORTFOLIO CALCULATION ---
equal_weight = 1 / len(TICKERS)
weighted_cum_returns = cumulative_returns.dot([equal_weight] * len(TICKERS))
portfolio_value = INVESTED_AMOUNT * weighted_cum_returns

# --- 📊 PLOTS ---

# Plot 1: Stock Prices
plt.figure(figsize=(12, 6))
for ticker in TICKERS:
    plt.plot(data[ticker], label=ticker)
plt.title('Stock Prices Over Time')
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid()
plt.show()

# Plot 2: Daily Returns
plt.figure(figsize=(12, 6))
daily_returns.plot(title="Daily Returns")
plt.xlabel("Date")
plt.ylabel("Daily % Return")
plt.grid()
plt.show()

# Plot 3: Cumulative Returns
plt.figure(figsize=(12, 6))
cumulative_returns.plot(title="Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.grid()
plt.show()

# Plot 4: Portfolio Value
plt.figure(figsize=(12, 6))
portfolio_value.plot(title='Simulated Portfolio Value Over Time', color='purple')
plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.grid()
plt.show()

# --- 📊 Portfolio Summary ---
print("\n--- Portfolio Summary ---")
final_value = portfolio_value.iloc[-1]
total_return = final_value - INVESTED_AMOUNT
percent_return = (total_return / INVESTED_AMOUNT) * 100
print(f"Initial Investment: ${INVESTED_AMOUNT:,.2f}")
print(f"Final Portfolio Value: ${final_value:,.2f}")
print(f"Total Return: ${total_return:,.2f} ({percent_return:.2f}%)")
