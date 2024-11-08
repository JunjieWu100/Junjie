import tkinter as tk
from tkinter import messagebox
from treys import Evaluator, Card, Deck
import itertools
import threading

# Initialize evaluator and deck
evaluator = Evaluator()
deck = Deck()

# Function to calculate equity in a separate thread
def calculate_equity_thread(your_hand, opponent_range, community_cards):
    win_count = 0
    loss_count = 0
    total_count = 0

    # Convert hand to Card objects
    try:
        your_hand = [Card.new(card) for card in your_hand.split()]
        community_cards = [Card.new(card) for card in community_cards.split()]
    except ValueError:
        messagebox.showerror("Error", "Invalid card format! Use format like 'As Kd'")
        return

    # Parse opponent range
    opponent_range = [hand.split() for hand in opponent_range.split(',')]
    try:
        opponent_range = [[Card.new(card) for card in opp_hand] for opp_hand in opponent_range]
    except ValueError:
        messagebox.showerror("Error", "Invalid opponent hand format! Use format like 'Ah Qh, Jc Js'")
        return

    # Iterate through opponent range
    for opp_hand in opponent_range:
        # Get remaining cards in the deck
        remaining_deck = deck.cards.copy()
        for card in your_hand + opp_hand + community_cards:
            remaining_deck.remove(card)

        # For each possible board scenario
        for combo in itertools.combinations(remaining_deck, 5 - len(community_cards)):
            board = community_cards + list(combo)
            your_score = evaluator.evaluate(board, your_hand)
            opp_score = evaluator.evaluate(board, opp_hand)

            if your_score < opp_score:
                win_count += 1
            elif your_score > opp_score:
                loss_count += 1
            total_count += 1

    win_rate = (win_count / total_count) * 100
    loss_rate = (loss_count / total_count) * 100
    result_text.set(f"Win rate: {win_rate:.2f}%, Loss rate: {loss_rate:.2f}%")

# Function to start the calculation in a new thread
def start_calculation():
    your_hand = your_hand_entry.get()
    opponent_range = opponent_range_entry.get()
    community_cards = community_cards_entry.get()
    
    # Run the calculation in a separate thread to avoid blocking the GUI
    threading.Thread(target=calculate_equity_thread, args=(your_hand, opponent_range, community_cards)).start()

# Set up the GUI
app = tk.Tk()
app.title("Poker Equity Calculator")

# Labels and input fields
tk.Label(app, text="Your Hand (e.g., 'As Kd')").grid(row=0, column=0, padx=5, pady=5)
your_hand_entry = tk.Entry(app)
your_hand_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(app, text="Opponent Range (e.g., 'Ah Qh, Jc Js')").grid(row=1, column=0, padx=5, pady=5)
opponent_range_entry = tk.Entry(app)
opponent_range_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(app, text="Community Cards (e.g., '2h 7d Th')").grid(row=2, column=0, padx=5, pady=5)
community_cards_entry = tk.Entry(app)
community_cards_entry.grid(row=2, column=1, padx=5, pady=5)

# Result label
result_text = tk.StringVar()
result_text.set("Win rate: N/A, Loss rate: N/A")
result_label = tk.Label(app, textvariable=result_text)
result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# Calculate button
calculate_button = tk.Button(app, text="Calculate Equity", command=start_calculation)
calculate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Run the application
app.mainloop()
