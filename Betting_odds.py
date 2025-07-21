# Betting Odds Fairness Checker

def implied_probability(odds):
    """Convert decimal odds to implied probability."""
    return 1 / odds

def calculate_margin(odds_list):
    """
    Calculate the bookmaker margin.
    Positive = unfair (bookmaker edge), 0 = fair, Negative = arbitrage.
    """
    total_implied_prob = sum(implied_probability(o) for o in odds_list)
    margin = (total_implied_prob - 1) * 100  # percentage
    return round(margin, 2)

def interpret_margin(margin):
    if margin == 0:
        return "Fair odds (no margin)."
    elif margin > 0:
        return f"Unfair odds. Bookmaker margin is {margin}%."
    else:
        return f"Arbitrage opportunity! Margin is {margin}%."

# Example: Replace with your own odds
odds = [1.56, 4.8, 6.9]

# Run calculations
margin = calculate_margin(odds)
interpretation = interpret_margin(margin)

# Output results
print(f"Odds: {odds}")
print(f"Bookmaker Margin: {margin}%")
print(f"Interpretation: {interpretation}")
