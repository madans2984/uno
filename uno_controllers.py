import random
from abc import ABC, abstractmethod

class Player(ABC):

    def __init__(self, game_state, player_name):
        self.game = game_state
        self.name = player_name
        self.hand = self.game.draw_pile.draw(7)

    def play_card(self, card):
        if self.check_play(card):
            self.game.discard_pile.add_to_top(card)
            self.hand.remove(card)
            print(f"Playing {card}.")
            return True
        else:
            return False

    def check_play(self, card):
        if ( card.color == self.game.current_color() or 
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

    # @abstractmethod
    # def choose_color(self):
    #     pass
    
    @abstractmethod
    def take_turn(self):
        """
        """

    def __repr__(self):
        return f"Player {self.name} with cards: {self.hand}"

class UserPlayerTextController(Player):
    """
    """
    def take_turn(self):
        if self.can_play():
            while self.can_play():
                index = input("Enter the index of the card you want to play: ")
                self.play_card(self.hand[int(index)])
                if self.num_cards() == 0:
                    print(f"{self.name} wins!")
                    return True
                print(self.hand)
            else:
                print("No more plays possible.")
        else:
            print("No play possible - player draws 1 card.")
            self.draw(1)
            return
        

class BotPlayer(Player):
    """
    """
    def take_turn(self):
        for card in self.hand:
            if self.play_card(card):
                break

    # def choose_color(self):
    #     return random.choice(["Red", "Blue", "Green", "Yellow"])
