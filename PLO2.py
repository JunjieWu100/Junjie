import tkinter as tk
import random

class PLOTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("PLO Training Tool")
        self.root.geometry("700x800")
        
        # Game State Variables
        self.hero_stack = 200  # 200 BB for hero (assuming BB is $1)
        self.opponent_stack = 200  # 200 BB for opponent
        self.pot = 3  # Initial pot with small blind ($1) and big blind ($2)
        self.hero_cumulative = 0  # Cumulative winnings/losses
        self.hands_played = 0  # Counter for hands played
        
        # UI Elements
        self.pot_label = tk.Label(root, text="Total Pot: $3", font=("Helvetica", 14))
        self.pot_label.pack(pady=10)
        
        self.hero_stack_label = tk.Label(root, text=f"Hero Stack: ${self.hero_stack}", font=("Helvetica", 12))
        self.hero_stack_label.pack()
        
        self.opponent_stack_label = tk.Label(root, text=f"Opponent Stack: ${self.opponent_stack}", font=("Helvetica", 12))
        self.opponent_stack_label.pack()
        
        # Display Board
        tk.Label(root, text="Board:", font=("Helvetica", 14)).pack(pady=5)
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(pady=10)
        
        # Display Hero's Hand
        tk.Label(root, text="Your Hand:", font=("Helvetica", 14)).pack(pady=5)
        self.hero_hand_frame = tk.Frame(root)
        self.hero_hand_frame.pack(pady=10)
        
        # Display Opponent's Hand at Showdown
        tk.Label(root, text="Opponent's Hand (at Showdown):", font=("Helvetica", 14)).pack(pady=5)
        self.opponent_hand_frame = tk.Frame(root)
        self.opponent_hand_frame.pack(pady=10)
        
        # Cumulative Win/Loss Display
        self.cumulative_label = tk.Label(root, text=f"Cumulative Winnings: ${self.hero_cumulative}", font=("Helvetica", 12))
        self.cumulative_label.pack(pady=5)
        
        # Hands Played Counter
        self.hands_played_label = tk.Label(root, text=f"Hands Played: {self.hands_played}", font=("Helvetica", 12))
        self.hands_played_label.pack(pady=5)
        
        # Action Buttons
        self.fold_button = tk.Button(root, text="Fold", command=self.fold, font=("Helvetica", 12), bg="red", fg="white")
        self.fold_button.pack(side="left", padx=20)
        
        self.call_button = tk.Button(root, text="Call", command=self.call, font=("Helvetica", 12), bg="yellow", fg="black")
        self.call_button.pack(side="left", padx=20)
        
        self.raise_button = tk.Button(root, text="Bet/Raise", command=self.raise_action, font=("Helvetica", 12), bg="green", fg="white")
        self.raise_button.pack(side="left", padx=20)
        
        # Betting Slider
        self.bet_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Bet Size (% of Pot)", font=("Helvetica", 12))
        self.bet_slider.pack(pady=10)
        
        # Bet Size Buttons
        self.bet_size_buttons = tk.Frame(root)
        self.bet_size_buttons.pack(pady=10)
        tk.Button(self.bet_size_buttons, text="1/4 Pot", command=lambda: self.set_bet_size(0.25)).pack(side="left", padx=5)
        tk.Button(self.bet_size_buttons, text="1/3 Pot", command=lambda: self.set_bet_size(0.33)).pack(side="left", padx=5)
        tk.Button(self.bet_size_buttons, text="1/2 Pot", command=lambda: self.set_bet_size(0.5)).pack(side="left", padx=5)
        tk.Button(self.bet_size_buttons, text="2/3 Pot", command=lambda: self.set_bet_size(0.67)).pack(side="left", padx=5)
        tk.Button(self.bet_size_buttons, text="Pot", command=lambda: self.set_bet_size(1)).pack(side="left", padx=5)
        
        # GTO Advice Label
        self.advice_label = tk.Label(root, text="GTO: N/A", font=("Helvetica", 12))
        self.advice_label.pack(pady=10)
        
        # Game state tracking
        self.street = "flop"  # Current betting round: "flop", "turn", "river"
        
        # Start a new hand
        self.new_hand()
    
    def new_hand(self):
        # Reset the pot and generate new hands and flop
        self.pot = 3  # Initial pot with small blind and big blind
        self.street = "flop"  # Reset to flop
        self.update_pot()
        
        # Increment hands played counter
        self.hands_played += 1
        self.hands_played_label.config(text=f"Hands Played: {self.hands_played}")
        
        # Generate random PLO hands for Hero and Opponent and display Hero's hand
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.hero_hand = [random.choice(ranks) + random.choice(suits) for _ in range(4)]
        self.opponent_hand = [random.choice(ranks) + random.choice(suits) for _ in range(4)]
        self.display_hand(self.hero_hand_frame, self.hero_hand)
        
        # Clear opponent hand display until showdown
        for widget in self.opponent_hand_frame.winfo_children():
            widget.destroy()
        
        # Generate a random flop (only three cards to start)
        self.board = [random.choice(ranks) + random.choice(suits) for _ in range(3)]
        self.display_hand(self.board_frame, self.board)
        
        # Generate GTO-inspired advice for the flop
        self.generate_gto_advice()
    
    def display_hand(self, frame, cards):
        # Clear previous cards
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Display each card with the appropriate color and larger font
        color_map = {
            '♠': 'black',
            '♥': 'red',
            '♦': 'blue',
            '♣': 'green'
        }
        
        for card in cards:
            rank, suit = card[:-1], card[-1]
            color = color_map.get(suit, 'black')
            card_label = tk.Label(frame, text=f"{rank}{suit}", fg=color, font=("Helvetica", 20, "bold"), padx=5)
            card_label.pack(side="left", padx=5)
    
    def update_pot(self):
        self.pot_label.config(text=f"Total Pot: ${self.pot}")
        self.hero_stack_label.config(text=f"Hero Stack: ${self.hero_stack}")
        self.opponent_stack_label.config(text=f"Opponent Stack: ${self.opponent_stack}")
    
    def fold(self):
        self.advice_label.config(text="GTO: You folded. Starting next hand...")
        self.hero_cumulative -= self.pot // 2  # Deduct half of the pot as a loss
        self.cumulative_label.config(text=f"Cumulative Winnings: ${self.hero_cumulative}")
        self.new_hand()
    
    def call(self):
        call_amount = min(self.pot // 2, self.hero_stack)
        if self.hero_stack >= call_amount:
            self.pot += call_amount * 2
            self.hero_stack -= call_amount
            self.opponent_stack -= call_amount
            self.update_pot()
            self.advice_label.config(text="GTO: You called.")
            self.next_street_or_opponent_action()
        else:
            self.advice_label.config(text="GTO: Not enough stack to call.")
    
    def raise_action(self):
        # Calculate raise amount as a percentage of the current pot
        raise_percentage = self.bet_slider.get() / 100
        raise_amount = int(self.pot * raise_percentage)
        
        if raise_amount > 0 and self.hero_stack >= raise_amount:
            self.pot += raise_amount * 2
            self.hero_stack -= raise_amount
            self.opponent_stack -= raise_amount
            self.update_pot()
            self.advice_label.config(text="GTO: You raised.")
            self.next_street_or_opponent_action()
        else:
            self.advice_label.config(text="GTO: Raise amount is too low or not enough stack to raise.")
    
    def next_street_or_opponent_action(self):
        if self.street == "flop":
            self.street = "turn"
            self.board.append(self.random_card())
            self.display_hand(self.board_frame, self.board)
            self.generate_gto_advice()
        elif self.street == "turn":
            self.street = "river"
            self.board.append(self.random_card())
            self.display_hand(self.board_frame, self.board)
            self.generate_gto_advice()
        else:
            self.street = "showdown"
            self.showdown()

    def showdown(self):
        # Display opponent's hand at showdown
        self.display_hand(self.opponent_hand_frame, self.opponent_hand)
        
        # Determine winner based on hand strength evaluation (simplified)
        hero_strength = self.evaluate_hand_strength(self.hero_hand, self.board)
        opponent_strength = self.evaluate_hand_strength(self.opponent_hand, self.board)
        
        if hero_strength > opponent_strength:
            self.hero_stack += self.pot
            self.hero_cumulative += self.pot // 2
            result_text = f"GTO: You won the pot of ${self.pot}!"
        else:
            self.opponent_stack += self.pot
            self.hero_cumulative -= self.pot // 2
            result_text = f"GTO: You lost the pot of ${self.pot}."
        
        self.cumulative_label.config(text=f"Cumulative Winnings: ${self.hero_cumulative}")
        self.advice_label.config(text=result_text)
        
        # Pause before starting a new hand
        self.root.after(3000, self.new_hand)
    
    def set_bet_size(self, fraction):
        # Set the slider value based on the chosen fraction of the pot
        self.bet_slider.set(int(fraction * 100))
    
    def generate_gto_advice(self):
        hand_strength = self.evaluate_hand_strength(self.hero_hand, self.board)
        
        if hand_strength == "strong":
            advice = "GTO: Strong hand. Bet or raise."
        elif hand_strength == "medium":
            advice = "GTO: Medium hand. Play cautiously."
        else:
            advice = "GTO: Weak hand. Consider folding."
        
        self.advice_label.config(text=advice)
    
    def evaluate_hand_strength(self, hand, board):
        # Simplified hand strength categorization for PLO
        suited = len(set(card[-1] for card in hand)) < 4
        connected_high = sum(1 for card in hand if card[0] in 'TJQKA') >= 2
        flush_draw = len([card for card in board if card[-1] == hand[0][-1]]) >= 2  # Simple flush draw check
        
        if suited and connected_high:
            return "strong"
        elif connected_high or flush_draw:
            return "medium"
        else:
            return "weak"
    
    def random_card(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♦', '♣']
        return random.choice(ranks) + random.choice(suits)

# Run the tool
root = tk.Tk()
app = PLOTrainer(root)
root.mainloop()
