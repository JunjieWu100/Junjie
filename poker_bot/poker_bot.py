#!pip install treys
import random, os, csv
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output
from treys import Card, Evaluator
import joblib

# Constants
STARTING_STACK = 100
SMALL_BLIND = 1
BIG_BLIND = 2
MIN_BET = 1
ranks = '23456789TJQKA'
suits = 'cdhs'
evaluator = Evaluator()

# Load models
try:
    model = joblib.load("player_model.pkl")
    le = joblib.load("label_encoder.pkl")
except:
    model = None
    le = None
    print("⚠️ No trained action model found.")

try:
    bet_model = joblib.load("bet_size_model.pkl")
except:
    bet_model = None
    print("⚠️ No bet size model found.")

def to_treys(cards):
    return [Card.new(c[0] + c[1]) for c in cards]

def monte_carlo_strength(player_cards, board, iterations=500):
    deck = [r + s for r in ranks for s in suits]
    known = player_cards + board
    for c in known:
        deck.remove(c)
    wins = ties = 0
    player = to_treys(player_cards)
    board_treys = to_treys(board)
    for _ in range(iterations):
        random.shuffle(deck)
        opp_cards = [deck[0], deck[1]]
        opp = to_treys(opp_cards)
        score_p = evaluator.evaluate(board_treys, player)
        score_o = evaluator.evaluate(board_treys, opp)
        if score_p < score_o:
            wins += 1
        elif score_p == score_o:
            ties += 1
    return round((wins + ties / 2) / iterations, 3)

def classify_board(board):
    high_cards = sum(1 for c in board if c[0] in '89TJQKA')
    suits_count = {s: 0 for s in suits}
    ranks_count = {r: 0 for r in ranks}
    for c in board:
        suits_count[c[1]] += 1
        ranks_count[c[0]] += 1
    flush = any(v >= 3 for v in suits_count.values())
    pair = any(v >= 2 for v in ranks_count.values())
    return 0.8 if flush or pair or high_cards >= 3 else 0.6

def generate_strength_map():
    strength_map = {}
    for r1 in ranks:
        for r2 in ranks:
            if r1 == r2:
                strength_map[r1 + r2] = 0
            else:
                for suited in ['s', 'o']:
                    key = ''.join(sorted([r1, r2], reverse=True)) + suited
                    strength_map[key] = 0
    unique_hands = list(strength_map.keys())
    unique_hands.sort(key=lambda h: (ranks.index(h[0]), ranks.index(h[1])), reverse=True)
    for i, h in enumerate(unique_hands):
        strength_map[h] = round(1.0 - i / len(unique_hands), 3)
    return strength_map

def get_hand_key(cards):
    r1, r2 = cards[0][0], cards[1][0]
    suited = cards[0][1] == cards[1][1]
    if r1 == r2:
        return r1 + r2
    return ''.join(sorted([r1, r2], reverse=True)) + ('s' if suited else 'o')

preflop_map = generate_strength_map()

def get_strength(cards, board=None, street="preflop"):
    if not board:
        return preflop_map.get(get_hand_key(cards), 0.4)
    return monte_carlo_strength(cards, board)

def bot_decision(street, strength, texture, pot, facing_bet=False):
    # Street encoding
    street_id = {"preflop": 0, "flop": 1, "turn": 2, "river": 3}[street]

    # Feature vector
    input_df = pd.DataFrame([{
        "hand_strength": strength,
        "board_texture": texture,
        "player_stack": player_stack,
        "bot_stack": bot_stack,
        "pot_size": pot,
        "street_id": street_id
    }])

    # Try to use bot's own action model first
    try:
        bot_model = joblib.load("bot_action_model.pkl")
        bot_encoder = joblib.load("bot_action_encoder.pkl")
        action_pred = bot_model.predict(input_df)[0]
        action = bot_encoder.inverse_transform([action_pred])[0]
    except:
        action = None

    # If no bot model, fallback to player model
    if action is None or action not in ["fold", "call", "check", "bet", "raise", "bluff"]:
        if model and le:
            action_pred = model.predict(input_df)[0]
            action = le.inverse_transform([action_pred])[0]
        else:
            # Last resort: heuristic fallback
            if street == "preflop":
                if strength >= 0.7:
                    return "raise"
                elif strength >= 0.5:
                    return "call"
                else:
                    return "fold" if facing_bet else "check"
            else:
                if strength >= 0.7:
                    return ("bet", 1.0)
                elif strength >= 0.5:
                    return ("bet", 0.5)
                else:
                    return "check"

    # Adjust folding logic when facing a bet
    if action == "fold":
        return "fold" if facing_bet else "check"

    # Predict bet size if betting-related action
    if action in ["bet", "raise", "bluff"]:
        try:
            bet_model = joblib.load("bot_bet_size_model.pkl")
            size = bet_model.predict(input_df)[0]
            size = min(max(size, 0.1), 1.5)  # Clamp between 0.1 and 1.5 pot
            print(f"🤖 Bot predicts bet size: {round(size, 3)} pot")
            return ("bet", size)
        except:
            return ("bet", 0.5)

    return action



def log_player_decision(hand_strength, board_texture, player_stack, bot_stack, pot, action, street, bet_size=0.0):
    data = {
        "hand_strength": hand_strength,
        "board_texture": board_texture,
        "player_stack": player_stack,
        "bot_stack": bot_stack,
        "pot_size": pot,
        "action": action,
        "street_id": {"preflop": 0, "flop": 1, "turn": 2, "river": 3}[street],
        "bet_size": bet_size
    }
    file_exists = os.path.isfile("player_training_data.csv")
    with open("player_training_data.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def log_bot_decision(hand_strength, board_texture, player_stack, bot_stack, pot, action, street, bet_size=0.0):
    data = {
        "hand_strength": hand_strength,
        "board_texture": board_texture,
        "player_stack": player_stack,
        "bot_stack": bot_stack,
        "pot_size": pot,
        "action": action,
        "street_id": {"preflop": 0, "flop": 1, "turn": 2, "river": 3}[street],
        "bet_size": bet_size
    }
    file_exists = os.path.isfile("bot_training_data.csv")
    with open("bot_training_data.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


# Game state
player_stack = STARTING_STACK
bot_stack = STARTING_STACK
dealer_button = 0

def play_hand():
    global player_stack, bot_stack, dealer_button
    if player_stack <= 0:
        player_stack = STARTING_STACK
        print("Player rebuys to 100bb.")
    if bot_stack <= 0:
        bot_stack = STARTING_STACK
        print("Bot rebuys to 100bb.")

    clear_output()
    deck = [r + s for r in ranks for s in suits]
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    bot_hand = [deck.pop(), deck.pop()]
    board = [deck.pop() for _ in range(5)]
    pot = 0
    log = []

    if dealer_button == 0:
        player_stack -= SMALL_BLIND
        bot_stack -= BIG_BLIND
        pot += SMALL_BLIND + BIG_BLIND
        log.append("Player posts SB (1), Bot posts BB (2)")
    else:
        bot_stack -= SMALL_BLIND
        player_stack -= BIG_BLIND
        pot += SMALL_BLIND + BIG_BLIND
        log.append("Bot posts SB (1), Player posts BB (2)")

    dealer_button = 1 - dealer_button
    street_order = ['preflop', 'flop', 'turn', 'river']
    board_progression = [[], board[:3], board[:4], board]
    current_street = 0

    def next_street():
        nonlocal current_street
        if current_street >= len(street_order):
            show_result(player_hand, bot_hand, board, pot, log)
        else:
            player_decision_ui(street_order[current_street], board_progression[current_street])
            current_street += 1

    def player_decision_ui(street, visible_board):
        global player_stack, bot_stack
        nonlocal pot
        clear_output()
        print(f"\n--- {street.upper()} ---")
        if street != 'preflop':
            print(f"Board: {visible_board}")
        strength = get_strength(player_hand, visible_board if street != 'preflop' else None, street)
        print(f"Your hand: {player_hand} (strength: {strength})")
        print(f"Pot: {pot} | Your stack: {player_stack} | Bot stack: {bot_stack}\n")

        bot_strength = get_strength(bot_hand, visible_board if street != 'preflop' else None, street)
        texture = classify_board(visible_board)

        # Bot always acts first for simplicity
        facing_bet = False
        decision = bot_decision(street, bot_strength, texture, pot, facing_bet=facing_bet)

        if isinstance(decision, tuple):
            bot_action, size = decision
        else:
            bot_action, size = decision, 0

        # ✅ Log bot decision
        log_bot_decision(
            round(bot_strength, 3), round(texture, 3),
            player_stack, bot_stack, pot,
            bot_action, street,
            bet_size=round(size, 3) if bot_action in ['bet', 'raise', 'bluff'] else 0.0
        )

        if bot_action == 'fold':
            log.append(f"Bot {street}: folds")
            player_stack += pot
            show_result(player_hand, bot_hand, board, pot, log, bot_folded=True)
            return
        elif bot_action == 'check':
            bot_bet = 0
            log.append(f"Bot {street}: check")
        elif bot_action == 'call':
            bot_bet = MIN_BET
            bot_stack -= bot_bet
            pot += bot_bet
            log.append(f"Bot {street}: call {bot_bet}")
        elif bot_action == 'raise':
            bot_bet = max(MIN_BET * 2, BIG_BLIND)
            bot_bet = min(bot_bet, bot_stack)
            bot_stack -= bot_bet
            pot += bot_bet
            log.append(f"Bot {street}: raise {bot_bet}")
        elif bot_action == 'bet':
            bot_bet = int(pot * size)
            bot_bet = max(bot_bet, MIN_BET)
            bot_bet = min(bot_bet, bot_stack)
            bot_stack -= bot_bet
            pot += bot_bet
            log.append(f"Bot {street}: bet {bot_bet}")
        else:
            bot_bet = 0
            log.append(f"Bot {street}: {bot_action}")
        print(f"Bot action: {bot_action} {bot_bet if bot_bet else ''}")

        def on_click(_, choice, size=0.0):
            global player_stack, bot_stack
            nonlocal pot

            log_player_decision(
                round(strength, 3), round(texture, 3),
                player_stack, bot_stack, pot,
                choice.lower(), street,
                bet_size=size if choice == "Raise" else 0.0
            )

            if choice == "Fold":
                log.append("Player folds. Bot wins the pot.")
                bot_stack += pot
                show_result(player_hand, bot_hand, board, pot, log)

            elif choice == "Call":
                player_stack -= bot_bet
                pot += bot_bet
                next_street()

            elif choice == "Raise":
                raise_amt = int(pot * size)
                raise_amt = max(raise_amt, MIN_BET)
                raise_amt = min(raise_amt, player_stack)
                player_stack -= raise_amt
                pot += raise_amt
                log.append(f"Player bets {raise_amt} ({size}x pot)")
                next_street()

        # Create buttons
        fold_btn = widgets.Button(description="Fold")
        call_btn = widgets.Button(description="Call")
        bet_025_btn = widgets.Button(description="Bet 0.25x Pot")
        bet_075_btn = widgets.Button(description="Bet 0.75x Pot")
        bet_150_btn = widgets.Button(description="Bet 1.5x Pot")

        # Attach click handlers
        fold_btn.on_click(lambda b: on_click(b, "Fold"))
        call_btn.on_click(lambda b: on_click(b, "Call"))
        bet_025_btn.on_click(lambda b: on_click(b, "Raise", 0.25))
        bet_075_btn.on_click(lambda b: on_click(b, "Raise", 0.75))
        bet_150_btn.on_click(lambda b: on_click(b, "Raise", 1.5))

        # Display buttons
        display(widgets.HBox([fold_btn, call_btn, bet_025_btn, bet_075_btn, bet_150_btn]))


    next_street()

def show_result(player_hand, bot_hand, board, pot, log, bot_folded=False):
    global player_stack, bot_stack
    if bot_folded:
        print("\nBot folded. You win the pot!")
        player_stack += pot
    else:
        p_score = monte_carlo_strength(player_hand, board)
        b_score = monte_carlo_strength(bot_hand, board)
        print("\n--- SHOWDOWN ---")
        print(f"Board: {board}")
        print(f"Your hand: {player_hand} ({p_score})")
        print(f"Bot hand: {bot_hand} ({b_score})")

        if abs(p_score - b_score) < 0.01:
            print("Split pot.")
            player_stack += pot // 2
            bot_stack += pot // 2
        elif p_score > b_score:
            print("You win the pot!")
            player_stack += pot
        else:
            print("Bot wins the pot.")
            bot_stack += pot

    print(f"\nPlayer stack: {player_stack} bb")
    print(f"Bot stack: {bot_stack} bb")
    print("\n--- Actions ---")
    for line in log:
        print(line)

    btn = widgets.Button(description="Next Hand")
    btn.on_click(lambda b: play_hand())
    display(btn)

# Start the game
play_hand()
