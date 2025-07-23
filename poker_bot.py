!pip install treys
!pip install ipywidgets
import random
import ipywidgets as widgets
from IPython.display import display, clear_output
from itertools import combinations
from treys import Card, Evaluator, Deck

# Constants
STARTING_STACK = 100
SMALL_BLIND = 1
BIG_BLIND = 2
MIN_BET = 1
ranks = '23456789TJQKA'
suits = 'cdhs'

evaluator = Evaluator()

# Convert string cards to treys format
def to_treys(cards):
    return [Card.new(c[0] + c[1]) for c in cards]

# Monte Carlo equity estimation
def monte_carlo_strength(player_cards, board, iterations=1000):
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

    total = iterations
    return round((wins + ties / 2) / total, 3)

# Fast hand strength for preflop/flop/turn
def evaluate_5card_hand(hand):
    values = sorted([ranks.index(c[0]) for c in hand], reverse=True)
    suits_ = [c[1] for c in hand]
    flush = len(set(suits_)) == 1
    straight = all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1))
    counts = {v: values.count(v) for v in set(values)}
    count_vals = sorted(counts.values(), reverse=True)

    if flush and straight:
        if values[0] == 12 and values[1] == 11:
            return 9
        return 8
    elif 4 in count_vals:
        return 7
    elif 3 in count_vals and 2 in count_vals:
        return 6
    elif flush:
        return 5
    elif straight:
        return 4
    elif 3 in count_vals:
        return 3
    elif count_vals.count(2) == 2:
        return 2
    elif 2 in count_vals:
        return 1 + max(values) / 100
    else:
        return 0 + max(values) / 100

def evaluate_postflop_strength(hand, board):
    best_score = 0
    for combo in combinations(hand + board, 5):
        score = evaluate_5card_hand(combo)
        best_score = max(best_score, score)
    return round(best_score / 9, 3)

# Mixed evaluation logic
def get_strength(cards, board=None, street="preflop"):
    if not board:
        return preflop_map.get(get_hand_key(cards), 0.4)
    elif street == "river":
        return monte_carlo_strength(cards, board)
    else:
        return evaluate_postflop_strength(cards, board)

# Hand label
def get_hand_rank_name(cards, board):
    player = to_treys(cards)
    board_treys = to_treys(board)
    rank_class = evaluator.get_rank_class(evaluator.evaluate(board_treys, player))
    return evaluator.class_to_string(rank_class)

# Preflop strength map
def generate_strength_map():
    strength_map = {}
    all_hands = []
    for r1 in ranks:
        for r2 in ranks:
            if r1 == r2:
                all_hands.append(r1 + r2)
            else:
                all_hands.append(r1 + r2 + 's')
                all_hands.append(r1 + r2 + 'o')
    unique_hands = list(set(all_hands))
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

# Bot decision
def classify_board(board):
    high_cards = sum(1 for c in board if c[0] in '89TJQKA')
    suits_count = {s: 0 for s in suits}
    ranks_count = {r: 0 for r in ranks}
    for c in board:
        suits_count[c[1]] += 1
        ranks_count[c[0]] += 1
    flush = any(v >= 3 for v in suits_count.values())
    pair = any(v >= 2 for v in ranks_count.values())
    if flush or pair or high_cards >= 3:
        return 0.8
    return 0.6

def bot_decision(street, strength, texture):
    if street == 'preflop':
        if strength >= 0.7:
            return 'raise'
        elif strength >= 0.5:
            return 'call'
        return 'fold'
    else:
        if strength >= 0.8:
            return 'bet', round(random.uniform(0.3, 0.5), 2)
        elif 0.5 <= strength < 0.8:
            return 'bet', round(random.uniform(0.75, 1.0), 2)
        elif texture == 0.8:
            if random.random() < 0.3:
                return 'bluff', round(random.uniform(0.3, 0.5), 2)
        return 'check', 0

# Game loop
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
        decision = bot_decision(street, bot_strength, texture)
        if isinstance(decision, tuple):
            bot_action, size = decision
        else:
            bot_action, size = 0, 0

        if bot_action == 'fold':
            log.append(f"Bot {street}: fold")
            print("Bot folds. You win the pot.")
            player_stack += pot
            show_result(player_hand, bot_hand, board, pot, log)
            return
        elif bot_action in ['bet', 'bluff']:
            bot_bet = max(int(BIG_BLIND * size), MIN_BET)
            bot_bet = min(bot_bet, bot_stack)
            bot_stack -= bot_bet
            pot += bot_bet
            log.append(f"Bot {street}: {bot_action} {bot_bet}")
        else:
            bot_bet = 0
            log.append(f"Bot {street}: {bot_action}")
        print(f"Bot action: {bot_action} {bot_bet if bot_bet else ''}")

        def on_click(choice):
            global player_stack, bot_stack
            nonlocal pot
            if choice == "Fold":
                log.append("Player folds. Bot wins the pot.")
                bot_stack += pot
                show_result(player_hand, bot_hand, board, pot, log)
            elif choice == "Call":
                player_stack -= bot_bet
                pot += bot_bet
                next_street()
            elif choice == "Raise":
                raise_amt = min(player_stack, max(bot_bet * 2, MIN_BET))
                player_stack -= raise_amt
                pot += raise_amt
                log.append(f"Player raises to {raise_amt}")
                next_street()

        fold_btn = widgets.Button(description="Fold")
        call_btn = widgets.Button(description="Call")
        raise_btn = widgets.Button(description="Raise")
        fold_btn.on_click(lambda b: on_click("Fold"))
        call_btn.on_click(lambda b: on_click("Call"))
        raise_btn.on_click(lambda b: on_click("Raise"))
        display(widgets.HBox([fold_btn, call_btn, raise_btn]))

    next_street()

def show_result(player_hand, bot_hand, board, pot, log):
    global player_stack, bot_stack
    p_score = monte_carlo_strength(player_hand, board)
    b_score = monte_carlo_strength(bot_hand, board)
    p_rank_name = get_hand_rank_name(player_hand, board)
    b_rank_name = get_hand_rank_name(bot_hand, board)

    print("\n--- SHOWDOWN ---")
    print(f"Board: {board}")
    print(f"Your hand: {player_hand} ({p_score}, {p_rank_name})")
    print(f"Bot hand: {bot_hand} ({b_score}, {b_rank_name})")

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

