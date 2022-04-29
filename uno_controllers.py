import random
from abc import ABC, abstractmethod

class Player(ABC):

    def __init__(self, game_state, player_name, player_type):
        self.game = game_state
        self.name = player_name
        self.player_type = player_type
        self.hand = self.game.draw_pile.draw(7)

    def take_turn(self):
        if self.handle_action():
            return

        if self.can_play():
            self.choose_card()
            if self.num_cards() == 0:
                self.game.won = True
                print(f"{self.name} won!")
        else:
            print(f"No play possible - {self.name} draws 1 card.")
            self.draw(1)
            return

    def handle_action(self):
        if self.game.current_action == "Skip":
            print(f"{self.name} was skipped.")
            self.game.current_action = None
            return True

        if self.game.current_action == "+2":
            self.draw(2)
            print(f"{self.name} drew 2 cards and misses their turn.")
            self.game.current_action = None
            return True

        if self.game.current_action == "+4":
            self.draw(4)
            print(f"{self.name} drew 4 cards and misses their turn.")
            self.game.current_action = None
            return True

        return False

    def play_card(self, card):
        if self.check_play(card):
            print(f"{self.name} played {card}.")
            if card.color == "Wild":
                card = self.choose_color(card)

            if (card.symbol == "Reverse" or
                card.symbol == "Skip" or
                card.symbol == "+2" or
                card.symbol == "+4"):
                self.game.current_action = card.symbol
                print(f"The current action is now {self.game.current_action}.")
 
            self.game.discard_pile.add_to_top(card)
            self.hand.remove(card)
            return True
        else:
            return False

    def check_play(self, card):
        if (card.color == self.game.current_color() or 
            card.symbol == self.game.current_symbol() or card.color == "Wild"):
            return True
        return False

    def num_cards(self):
        return len(self.hand)
    
    def draw(self, num_cards):
        self.hand.extend(self.game.draw_pile.draw(num_cards))

    def can_play(self):
        for card in self.hand:
            if self.check_play(card):
                return True
        return False

    @abstractmethod
    def choose_card(self):
        """
        """

    @abstractmethod
    def choose_color(self, card):
        pass

    def __repr__(self):
        return f"Player {self.name} with cards: {self.hand}"

class UserPlayerTextController(Player):
    """
    """
    def choose_card(self):
        while True:
            try:
                index = int(input("Enter the index of the card you want to play: "))
                if self.play_card(self.hand[int(index)]):
                    return
                else:
                    print("Invalid play. Your card must match the color or the"
                        " symbol of the current card, \n"
                        "or be a Wild card. Please try again.")
            except (IndexError, ValueError):
                print(f"Invalid input. Please enter an integer between 0 and"
                    f" {self.num_cards()-1}.")

            

    def choose_color(self, card):
        while True:
                text = input("What color should the new card be?"
                    " (r/g/b/y):")
                if text == "r":
                    card.chosen_color = "Red"
                    return card
                elif text == "g":
                    card.chosen_color = "Green"
                    return card
                elif text == "b":
                    card.chosen_color = "Blue"
                    return card
                elif text == "y":
                    card.chosen_color = "Yellow"
                    return card
                else:
                    print("That is not a valid input. Please enter 'r' for"
                        " Red, 'g' for Green, 'b' for Blue, or 'y' for"
                        " Yellow.")

class BotPlayer(Player):
    """
    """
    def choose_card(self):
        for card in self.hand:
            if self.play_card(card):
                return

    def choose_color(self, card):
        card.chosen_color = random.choice(["Red", "Blue", "Green", "Yellow"])
        return card
