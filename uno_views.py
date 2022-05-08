
from abc import ABC, abstractmethod
from uno_color_text_helpers import put_in_card, color_card_rep, print_cards, get_big_card, other_players_as_big_card

class UnoView(ABC):

    def __init__(self, player_list, game_state):
        self.players = player_list
        self.game = game_state

    def display(self, current_player, show_bot_hands=False):

        # if (always_show_card_count == True or
        #     current_player.player_type == "User"):
        #     self.display_other_players()
        print("============================================================")
        self.display_other_players_and_current_card()
        print(f"It's {current_player.name}'s turn.")
        if ((show_bot_hands == True or current_player.player_type == "User")
            and self.game.current_action == None):
            self.display_hand(current_player)

    @abstractmethod
    def display_other_players_and_current_card(self):
        pass
    
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

    def display_current_card(self):
        print(f"The current card is {self.game.current_color()} {self.game.current_symbol()}.")

    def display_hand(self, player):
        print(f"{player.name}'s hand:")
        print(player.hand)

    def display_other_players_and_current_card(self):
        pass

class ColorTextView(UnoView):

    def display_other_players(self):
        full = self.make_other_players_diamond()
        for line in full:
            print(line)

    def display_current_card(self):
        print(f"The current card is {self.game.current_color()} {self.game.current_symbol()}.")
        card_rep = get_big_card(self.game.current_symbol())
        card_rep = color_card_rep(card_rep, self.game.current_color())
        players_rep = self.display_other_players()
        players_big_card = other_players_as_big_card(players_rep)
        print_cards([card_rep, players_big_card])

    def display_other_players_and_current_card(self):
        print(f"The current card is {self.game.current_color()} {self.game.current_symbol()}.")
        card_rep = get_big_card(self.game.current_symbol())
        card_rep = color_card_rep(card_rep, self.game.current_color())
        players_rep = self.make_other_players_diamond()
        players_big_card = other_players_as_big_card(players_rep)
        print_cards([card_rep, players_big_card])

    def display_hand(self, player):
        print(f"{player.name}'s hand:")
        card_reps = []
        index_str = ""
        for i in range(1,len(player.hand)+1):
            index_str += str(i).center(6)
        for card in player.hand:
            card_rep = put_in_card(card.symbol)
            card_rep = color_card_rep(card_rep, card.color)
            card_reps.append(card_rep)
        print_cards(card_reps)
        print(index_str)

    def make_other_players_diamond(self):
        ne = "\u2197"
        se = "\u2198"
        sw = "\u2199"
        nw = "\u2196"
        side_name_width = 7
        half_width = 8
        card_strings = []
        for player in self.players:
            card_str = "(" + str(player.num_cards()) + ")"
            card_str = card_str.center(len(player.name))
            card_strings.append(card_str)

        top = [ self.players[2].name.center(half_width*2 + 1),
                card_strings[2].center(half_width*2 + 1) ]
        bottom = [ self.players[0].name.center(half_width*2 + 1),
                card_strings[0].center(half_width*2 + 1) ]
        left = [ self.players[1].name.ljust(half_width),
                card_strings[1].ljust(half_width) ]
        right = [ self.players[3].name.rjust(half_width),
                card_strings[3].rjust(half_width) ]
        if self.game.direction == 1:
            arrows = [ne.center(half_width) + " " + se.center(half_width),
                      nw.center(half_width) + " " + sw.center(half_width)]
        else:
            arrows = [sw.center(half_width) + " " + nw.center(half_width),
                      se.center(half_width) + " " + ne.center(half_width)]
        full = [top[0],
                top[1],
                arrows[0],
                left[0] + " " + right[0],
                left[1] + " " + right[1],
                arrows[1],
                bottom[0],
                bottom[1]]
        return full