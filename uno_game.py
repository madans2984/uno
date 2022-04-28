import random
from uno_deck import Card, Deck

class GameState:
    
    def __init__(self):
        self.discard_pile = Deck(is_empty=True)
        self.draw_pile = Deck(include_reverse=False, include_wilds=False, include_skips=False, include_draws=False)
        self.draw_pile.shuffle()
        self.direction = 1
        self.current_action = None
        self.discard_pile.add_to_top(Card("Red","0"))
        self.won = False

    def reuse_discard_pile(self):
        top_card = self.discard_pile.draw()
        self.discard_pile.shuffle()
        useable_cards = self.discard_pile.cards
        for card in useable_cards:
            card.strip_chosen_color()
        self.draw_pile.add_to_bottom(useable_cards)
        self.discard_pile = Deck(def_cards=top_card)

    def current_color(self):
        return self.discard_pile.show_top().color

    def current_symbol(self):
        return self.discard_pile.show_top().symbol

    def __repr__(self):
        pass

class GameDirector:

    def __init__(self, player_list, game_state):
        self.game = game_state
        self.players = player_list
        self.current_player_index = 0
    
    def call_the_player(self):
        if self.game.current_action == "Reverse":
            self.game.direction = -self.game.direction
            print("Reverse!")
            self.game.current_action = None

        # elif self.game.current_action == "Skip":
        #     self.next_player()
        #     print(f"{self.current_player()} was skipped.")
        #     self.game.current_action = None

        # elif self.game.current_action == "Draw 2":
        #     self.next_player()
        #     self.current_player().draw(2)
        #     print(f"{self.current_player()} drew 2 cards.")
        #     self.game.current_action = None

        # elif self.game.current_action == "Draw 4":
        #     self.next_player()
        #     self.current_player().draw(4)
        #     print(f"{self.current_player()} drew 4 cards.")
        #     self.game.current_action = None
        print(f"It's {self.current_player().name}'s turn.")
        self.current_player().take_turn()
    
    def current_player(self):
        return self.players[self.current_player_index]

    def go_to_next_player(self):
        if self.current_player_index > 2:
            self.current_player_index = 0
        else:
            self.current_player_index += self.game.direction
        # return self.players[self.current_player_index]

    
