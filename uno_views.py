
from abc import ABC, abstractmethod

class UnoView(ABC):

    def __init__(self, player_list, game_state):
        self.players = player_list
        self.game = game_state

    @abstractmethod
    def display(self):
        pass


class TextView(UnoView):
    
    def display(self, current_player):
        self.display_other_players()
        print(f"The current card is {self.game.current_color()} {self.game.current_symbol()}")
        self.display_hand(current_player)

    def display_other_players(self):
        for player in self.players:
            print(f"{player.name} has {player.num_cards()} cards.")

    def display_hand(self, player):
        print(player.hand)
