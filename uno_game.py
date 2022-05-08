"""
Classes representing the uno game state and the game director.
"""

from uno_deck import Deck

class GameState:
    """
    A representation of the uno game's state.

    Attributes:
        draw_pile: A Deck of Cards to be drawn from during the game.
        discard_pile: A Deck of Cards to add played cards to.
        _direction: A int that is either 1 or -1 indicating which direction
            play is currently moving. 1 means that the GameDirector should go
            forwards through the list of players when calling the next player,
            and -1 means that the the GameDirector should go backwards through
            the list.
        current_action: A string representing the symbol of an action card
            (either "Reverse", "Skip", "+2", or "+4") whose action has not yet
            been implemented (the next player has not yet drawn, been skipped,
            etc.)
        won: A bool changed by a player to indicate they they won (True for
            someone has won, False for nobody has declared a win yet.)
    """

    def __init__(self, def_deck=None):
        """
        Initialize an uno gamestate and make the game ready to play.

        Args:
            def_deck: (optional) a Deck to be used as the draw deck and not
                shuffled prior to using (for testing).
        """
        self._direction = 1
        self.current_action = None
        self.won = False

        # Set up the draw pile
        if def_deck == None:
            self.draw_pile = Deck()
            self.draw_pile.shuffle()
        else:
            self.draw_pile = def_deck

        # Set up the discard pile
        self.discard_pile = Deck(is_empty=True)
        # To set up the discard pile, find the first non-action card, make it
        # the current card (top of discard pile), put all cards before the
        # first non-action card at the bottom of the deck, and shuffle.
        cards = self.draw(1)
        if cards[0].is_special():
            while cards[-1].is_special():
                cards.extend(self.draw(1))
            self.draw_pile.add_to_bottom(cards[:-1])
            self.draw_pile.shuffle()
        self.discard_pile.add_to_top(cards[-1])

    def play(self, card):
        """
        Play a Card onto the top of the discard_pile Deck.
        
        Args:
            card: A Card instance to be added to the top of the discard pile.
        """
        self.discard_pile.add_to_top(card)

    def draw(self, num_cards=1):
        """
        Draw a Card from the top of the draw_pile Deck.

        Args:
            num_cards: An int representing the number of cards to draw.
        Returns:
            The drawn Card.
        """
        if self.draw_pile.size() < 5:
            self.reuse_discard_pile()
        return self.draw_pile.draw(num_cards)

    def reuse_discard_pile(self):

        top_card = self.discard_pile.draw()
        self.discard_pile.shuffle()

        # 
        useable_cards = self.discard_pile.cards
        for card in useable_cards:
            card.strip_chosen_color()
        self.draw_pile.add_to_bottom(useable_cards)
        self.discard_pile = Deck(def_cards=top_card)
    
    def current_card(self):
        return self.discard_pile.show_top()

    def current_color(self):
        return self.current_card().color

    def current_symbol(self):
        return self.current_card().symbol

    def reverse_direction(self):
        self._direction = -self._direction

    @property
    def direction(self):
        return self._direction

    def __repr__(self):
        return (f"Uno GameState with current_card(): {self.current_card()} \n"
            f"draw_pile ({self.draw_pile.size()} card): {self.draw_pile} \n"
            f"and discard_pile ({self.discard_pile.size()} card): "
            f"{self.discard_pile}")

class GameDirector:

    def __init__(self, player_list, game_state):
        self.game = game_state
        self.players = player_list
        self.current_player_index = 0

    def current_player(self):
        return self.players[self.current_player_index]

    def handle_reverse(self):
        if self.game.current_action == "Reverse":
            self.game.reverse_direction()
            self.game.current_action = None

    def call_the_player(self):
        self.current_player().take_turn()

    def go_to_next_player(self):
        new_index = self.current_player_index + self.game.direction
        if new_index > 3:
            self.current_player_index = 0
        elif new_index < 0:
            self.current_player_index = 3
        else:
            self.current_player_index = new_index


game = GameState()

print(game)