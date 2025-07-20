import tkinter as tk
from PIL import Image, ImageTk
import random

# Card and Deck classes
class Card:
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

# Simple Pavlovian AI Class
class SimplePavlovianAI:
    def __init__(self):
        self.previous_action = None
        self.previous_outcome = None

    def decide_action(self):
        if self.previous_action == "Call" and self.previous_outcome == "Win":
            return "Call"
        elif self.previous_action == "Call" and self.previous_outcome == "Lose":
            return random.choice(["Fold", "Call"])  # More cautious
        else:
            return random.choice(["Call", "Raise", "Fold"])  # Random on first move

    def update_memory(self, action, outcome):
        self.previous_action = action
        self.previous_outcome = outcome

# Poker game class
class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.ai_hand = []
        self.community_cards = []
        self.pot = 0
        self.ai = SimplePavlovianAI()
        self.round = 0  # Track the round of community cards

    def start_new_hand(self):
        self.deck = Deck()  # Reset the deck for a new hand
        self.player_hand = [self.deck.deal(), self.deck.deal()]
        self.ai_hand = [self.deck.deal(), self.deck.deal()]
        self.community_cards = []
        self.round = 0  # Reset the round

    def deal_community_cards(self):
        if self.round == 0:
            # Deal first three cards (flop)
            self.community_cards.extend([self.deck.deal() for _ in range(3)])
            self.round += 1
        elif self.round == 1:
            # Deal the turn
            self.community_cards.append(self.deck.deal())
            self.round += 1
        elif self.round == 2:
            # Deal the river
            self.community_cards.append(self.deck.deal())
            self.round += 1

    def ai_decision(self):
        action = self.ai.decide_action()
        # Placeholder for win/lose determination logic
        outcome = random.choice(["Win", "Lose"])  # This should be based on actual game logic
        self.ai.update_memory(action, outcome)
        return action

# GUI class
class PokerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Heads-Up Poker Game")
        self.master.configure(bg='black')

        # Load card images
        self.card_images = self.load_card_images()

        self.game = PokerGame()
        self.setup_ui()
        self.start_new_hand()

    def setup_ui(self):
        self.player_label = tk.Label(self.master, text="Your Hand:", bg='black', fg='white')
        self.player_label.pack()

        self.player_canvas = tk.Canvas(self.master, bg='black', height=100)
        self.player_canvas.pack()

        self.community_label = tk.Label(self.master, text="Community Cards:", bg='black', fg='white')
        self.community_label.pack()

        self.community_canvas = tk.Canvas(self.master, bg='black', height=100)
        self.community_canvas.pack()

        self.pot_label = tk.Label(self.master, text="Pot: $0", bg='black', fg='white')
        self.pot_label.pack()

        self.deal_button = tk.Button(self.master, text="Deal Community Cards", command=self.deal_community, bg='green', fg='white')
        self.deal_button.pack()

        self.ai_decision_label = tk.Label(self.master, text="", bg='black', fg='white')
        self.ai_decision_label.pack()

        self.next_hand_button = tk.Button(self.master, text="Next Hand", command=self.start_new_hand, bg='blue', fg='white')
        self.next_hand_button.pack()

        self.update_ui()

    def load_card_images(self):
        card_images = {}
        for suit in Card.suits:
            for value in Card.values:
                # Adjust the filename based on the value
                if value == 'T':
                    image_path = f'C:\\Users\\Junjie\\Images\\10_of_{suit}.png'  # Use 10 for Ten
                elif value == 'J':
                    image_path = f'C:\\Users\\Junjie\\Images\\jack_of_{suit}.png'  # Use jack for Jack
                elif value == 'Q':
                    image_path = f'C:\\Users\\Junjie\\Images\\queen_of_{suit}.png'  # Use queen for Queen
                elif value == 'K':
                    image_path = f'C:\\Users\\Junjie\\Images\\king_of_{suit}.png'  # Use king for King
                elif value == 'A':
                    image_path = f'C:\\Users\\Junjie\\Images\\ace_of_{suit}.png'  # Use ace for Ace
                else:
                    image_path = f'C:\\Users\\Junjie\\Images\\{value}_of_{suit}.png'  # For other values
                
                try:
                    # Load the image using PIL and convert to PhotoImage
                    img = Image.open(image_path)
                    img = img.resize((100, 140), Image.ANTIALIAS)  # Resize image to desired dimensions
                    card_images[f"{value} of {suit}"] = ImageTk.PhotoImage(img)
                except FileNotFoundError:
                    print(f"Image not found: {image_path}")
        return card_images

    def update_ui(self):
        self.player_canvas.delete("all")
        for i, card in enumerate(self.game.player_hand):
            # Create a smaller version of the card image
            small_card_image = self.card_images[str(card)]  # No resizing needed here as it's already done in load
            self.player_canvas.create_image(10 + i * 55, 10, anchor='nw', image=small_card_image)

        self.community_canvas.delete("all")
        for i, card in enumerate(self.game.community_cards):
            # Create a smaller version of the community card image
            small_card_image = self.card_images[str(card)]  # No resizing needed here as it's already done in load
            self.community_canvas.create_image(10 + i * 55, 10, anchor='nw', image=small_card_image)

        ai_action = self.game.ai_decision()
        self.ai_decision_label['text'] = "AI Decision: " + ai_action

    def deal_community(self):
        if len(self.game.community_cards) < 5:  # Only deal up to 5 community cards
            self.game.deal_community_cards()
            self.update_ui()

    def start_new_hand(self):
        self.game.start_new_hand()  # Start a new hand and reset UI
        self.update_ui()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PokerGUI(root)
    root.mainloop()
