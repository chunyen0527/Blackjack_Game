import tkinter as tk
import random

# Create a standard 52-card deck (4 copies of each card)
cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4

# Function to randomly deal a single card
def deal_card():
    return random.choice(cards)

# Function to convert a card to Blackjack point value
def card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return card

# Function to calculate the total score of a hand
# Adjusts Aces from 11 to 1 if the total exceeds 21
def calculate_score(hand):
    values = [card_value(card) for card in hand]
    total = sum(values)
    ace_count = hand.count('A')
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    return total

# BlackjackGame main code
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Practice")   # Window title
        self.root.geometry("300x205")           # Fixed window size
        self.create_widgets()                   # Set up GUI components
        self.new_game_prompt()                  # Initialize game state
        
    # Create GUI components (labels, buttons, layout)
    def create_widgets(self):
        self.info_label = tk.Label(self.root, text="Wecome to Blackjack Game!", font=("Trebuchet MS", 14))
        self.info_label.pack(pady=5)

        self.player_label = tk.Label(self.root, text="", font=("Trebuchet MS", 12))
        self.player_label.pack()

        self.dealer_label = tk.Label(self.root, text="", font=("Trebuchet MS", 12))
        self.dealer_label.pack()

        self.result_label = tk.Label(self.root, text="", font=("Trebuchet MS", 14), fg="blue")
        self.result_label.pack(pady=5)

        # Upper button row: Hit and Stand
        top_button_row = tk.Frame(self.root)
        top_button_row.pack(pady=5)

        self.hit_button = tk.Button(top_button_row, text="Hit", width=10, command=self.hit, state="disabled")
        self.hit_button.pack(side="left", padx=5)

        self.stand_button = tk.Button(top_button_row, text="Stand", width=10, command=self.stand, state="disabled")
        self.stand_button.pack(side="left", padx=5)
        
        # Bottom button row: Start, Play Again, Quit
        bot_button_row = tk.Frame(self.root)
        bot_button_row.pack()
        
        self.start_button = tk.Button(bot_button_row, text="Start", width=10, command=self.start_game, state="active")
        self.start_button.pack(side="left", padx=5)

        self.new_button = tk.Button(bot_button_row, text="Play Again", width=10, command=self.new_game_prompt, state="disabled")
        self.new_button.pack(side="left", padx=5)
        
        self.exit_button = tk.Button(bot_button_row, text="Quit Game", width=10, command=self.root.destroy)
        self.exit_button.pack(side="left", padx=5)

    # Reset buttons and labels to prepare a new round
    def new_game_prompt(self):
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.new_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.player_label.config(text="")
        self.dealer_label.config(text="")
        self.result_label.config(text="")

    # Start a new game to player and dealer
    def start_game(self):
        self.start_button.config(state="disabled")
        self.player_hand = [deal_card(), deal_card()]
        self.dealer_hand = [deal_card(), deal_card()]
        self.update_display()
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")
        # Check for Blackjack
        if calculate_score(self.player_hand) == 21:
            self.result_label.config(text="BLACKJACK! You Win!", fg="green")
            self.end_game()
            
    # Update the interface to show current hands and scores
    def update_display(self, reveal_dealer=False):
        self.player_label.config(text=f"Your Hand: {self.player_hand} (Total:{calculate_score(self.player_hand)})")
        if reveal_dealer:
            self.dealer_label.config(text=f"Dealer;s Hand:{self.dealer_hand} (Total:{calculate_score(self.dealer_hand)})")
        else:
            self.dealer_label.config(text=f"Dealer;s Hand:[?, {self.dealer_hand[1]}]")

    # When player chooses "Hit", add a card and check for bust
    def hit(self):
        self.player_hand.append(deal_card())
        self.update_display()
        if calculate_score(self.player_hand) > 21:
            self.result_label.config(text="Busted! Better luck next time!", fg="red")
            self.end_game()

    # When player chooses "Stand", dealer draws until at least 17
    def stand(self):
        while calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(deal_card())
        self.update_display(reveal_dealer=True)
        self.check_result()

    # Compare scores and determine the result of the game
    def check_result(self):
        player_score = calculate_score(self.player_hand)
        dealer_score = calculate_score(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            self.result_label.config(text="You Win!", fg="green")
        elif player_score < dealer_score:
            self.result_label.config(text="You Lose!", fg="red")
        else:
            self.result_label.config(text="Push!", fg="black")
        self.end_game()
        
    # End the game round and enable "Play Again" button
    def end_game(self):
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.new_button.config(state="normal")
        
# Initialize the main application window and start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
