
from abc import ABC, abstractmethod

class UnoView(ABC):

    def __init__(self, player_list, game_state):
        self.players = player_list
        self.game = game_state

    def display(self, current_player, always_show_card_count=False,
        show_bot_hands=False):

        if (always_show_card_count == True or
            current_player.player_type == "User"):
            self.display_other_players()
        self.display_current_card()
        print(f"It's {current_player.name}'s turn.")
        if ((show_bot_hands == True or current_player.player_type == "User")
            and self.game.current_action == None):
            self.display_hand(current_player)
    
    @abstractmethod
    def display_other_players(self):
        pass
    
    @abstractmethod
    def display_current_card(self):
        pass

    @abstractmethod
    def display_hand(self, player):
        pass


class TextView(UnoView):
    
    def display_other_players(self):
        for player in self.players:
            print(f"{player.name} has {player.num_cards()} cards.")

    # def display_other_players(self): ## IN PROGRESS -- jules
    #     ne = "\u2197"
    #     se = "\u2198"
        # sw = "\u2199"
    #     nw = "\u2196"
    #     side_name_width = 7
    #     half_width = 8
    #     card_strings = []
    #     for player in self.players:
    #         card_str = "(" + str(player.num_cards()) + ")"
    #         card_str.center(len(player.name))
    #         card_strings.append(card_str)

    #     top = [ self.players[2].name.center(half_width*2 + 1),
    #             card_strings[2].center(half_width*2 + 1) ]
    #     bottom = [ self.players[0].name.center(half_width*2 + 1),
    #             card_strings[0].center(half_width*2 + 1) ]
    #     left = [ self.players[1].name.ljust(half_width),
    #             card_strings[1].ljust(half_width) ]
    #     right = [ self.players[3].name.rjust(half_width),
    #             card_strings[3].rjust(half_width) ]


    def display_current_card(self):
        print(f"The current card is {self.game.current_color()} {self.game.current_symbol()}")

    def display_hand(self, player):
        print(f"{player.name}'s hand:")
        print(player.hand)
