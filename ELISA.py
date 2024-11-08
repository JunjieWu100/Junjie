//@version=5
strategy("Frequent Buy/Sell Strategy for ELISA", overlay=true)

// Get the current price
price = close

// Define extremely sensitive thresholds
sensitivity = 0.01  // Sensitivity threshold for triggering buy/sell

// Set the buy and sell thresholds just above/below the current price
threshold_buy = price - sensitivity
threshold_sell = price + sensitivity

// Condition to buy: price drops just below the threshold
if price < threshold_buy
    strategy.entry("Buy", strategy.long)

// Condition to sell: price rises just above the threshold
if price > threshold_sell
    strategy.close("Buy")

// Plot thresholds on the chart for visualization
plot(threshold_buy, color=color.green, linewidth=1, title="Buy Threshold")
plot(threshold_sell, color=color.red, linewidth=1, title="Sell Threshold")
