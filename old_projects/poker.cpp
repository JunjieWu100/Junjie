#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <ctime>
#include <map>

// Card struct represents each card with a suit and a rank
struct Card {
    std::string suit;
    std::string rank;
};

// Function to create a deck of cards
std::vector<Card> createDeck() {
    std::vector<Card> deck;
    std::string suits[] = {"Hearts", "Diamonds", "Clubs", "Spades"};
    std::string ranks[] = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"};

    for (const auto& suit : suits) {
        for (const auto& rank : ranks) {
            deck.push_back({suit, rank});
        }
    }
    return deck;
}

// Shuffle the deck
void shuffleDeck(std::vector<Card>& deck) {
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(deck.begin(), deck.end(), g);
}

// Player struct
struct Player {
    std::string name;
    std::vector<Card> hand;
    int bankroll;
    bool isInRound;

    Player(const std::string& n, int b) : name(n), bankroll(b), isInRound(true) {}
};

// Deal a card from the deck
Card dealCard(std::vector<Card>& deck) {
    Card dealtCard = deck.back();
    deck.pop_back();
    return dealtCard;
}

// Function to print a card
void printCard(const Card& card) {
    std::cout << card.rank << " of " << card.suit;
}

// Function to evaluate hands and determine the winner (basic comparison)
std::string determineWinner(Player& p1, Player& p2, const std::vector<Card>& board) {
    // Simplified: Just compares first card rank as a placeholder
    if (p1.hand[0].rank > p2.hand[0].rank) {
        return p1.name;
    } else if (p1.hand[0].rank < p2.hand[0].rank) {
        return p2.name;
    }
    return "Draw";
}

// Game function
void playGame() {
    std::vector<Card> deck = createDeck();
    shuffleDeck(deck);

    Player player1("Player 1", 1000);
    Player player2("Player 2", 1000);
    std::vector<Card> board;

    // Deal two cards to each player
    player1.hand.push_back(dealCard(deck));
    player1.hand.push_back(dealCard(deck));
    player2.hand.push_back(dealCard(deck));
    player2.hand.push_back(dealCard(deck));

    // Display players' hands
    std::cout << player1.name << "'s hand: ";
    printCard(player1.hand[0]);
    std::cout << ", ";
    printCard(player1.hand[1]);
    std::cout << "\n";

    std::cout << player2.name << "'s hand: ";
    printCard(player2.hand[0]);
    std::cout << ", ";
    printCard(player2.hand[1]);
    std::cout << "\n";

    // Deal the board cards (community cards)
    std::cout << "Dealing the board...\n";
    for (int i = 0; i < 5; ++i) {
        board.push_back(dealCard(deck));
    }

    std::cout << "Board cards: ";
    for (const auto& card : board) {
        printCard(card);
        std::cout << " | ";
    }
    std::cout << "\n";

    // Determine the winner
    std::string winner = determineWinner(player1, player2, board);
    if (winner == "Draw") {
        std::cout << "The round is a draw!\n";
    } else {
        std::cout << winner << " wins the round!\n";
    }
}

int main() {
    std::cout << "Welcome to Heads-Up No-Limit Texas Hold'em!\n";
    playGame();
    return 0;
}
