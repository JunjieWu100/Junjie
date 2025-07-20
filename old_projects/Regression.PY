# Simple Linear Regression - Predicting Patterns
import random

# Generate synthetic data for a simple y = mx + c relation
X = [i for i in range(10)]
y = [2 * x + random.uniform(-1, 1) for x in X]

# Calculate the mean of X and y
mean_x = sum(X) / len(X)
mean_y = sum(y) / len(y)

# Calculate coefficients
numerator = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(len(X)))
denominator = sum((X[i] - mean_x) ** 2 for i in range(len(X)))
m = numerator / denominator
c = mean_y - m * mean_x

# Predictions
y_pred = [m * x + c for x in X]
print("Predicted values:", y_pred)
