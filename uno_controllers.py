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
            return True
        else:
            return False

    def check_play(self, card):
        if ( card.color == self.game.current_color() or 
            card.symbol == self.game.current_symbol() or card.color == "Wild"):
            return True
    
    def num_cards(self):
        return len(self.hand)
    
    def draw2(self):
        self.hand.extend(self.game.draw_pile.draw(2))

    def draw4(self):
        self.hand.extend(self.game.draw_pile.draw(4))

    @abstractmethod
    def choose_color(self):
        pass
    
    @abstractmethod
    def take_turn(self):
        pass

    def __repr__(self):
        return f"Player {self.name} with cards: {self.hand}"

class UserPlayerTextController(Player):
    """
    """
    def take_turn(self):
        pass

class BotPlayer(Player):
    """
    """
    def take_turn(self):
        for card in self.hand:
            if self.play_card(card):
                break

    def choose_color(self):
        return random.choice(["Red", "Blue", "Green", "Yellow"])
