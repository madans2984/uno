"""
Classes representing the uno game state and the game director.
"""

from uno_deck import Deck

class GameState:
    """
    A representation of the uno game's state, with the parts of the game that
    players can affect.

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

    def play_card(self, card):
        """
        Play a Card onto the top of the discard_pile Deck.
        
        Args:
            card: A Card instance to be added to the top of the discard pile.
        """
        self.discard_pile.add_to_top(card)

    def draw(self, num_cards=1):
        """
        Draw card(s) from the top of the draw_pile Deck.

        Args:
            num_cards: An int representing the number of cards to draw.
        Returns:
            A list of the drawn cards.
        """
        if self.draw_pile.size() < 5:
            self.reuse_discard_pile()
        return self.draw_pile.draw(num_cards)

    def reuse_discard_pile(self):
        """
        Add the shuffled discard pile cards to the bottom of the draw pile.
        """
        # Take off the top/current card in the discard pile
        top_card = self.discard_pile.draw()

        # Shuffle the remaining cards
        self.discard_pile.shuffle()

        # Go through each card in the pile and strip the chosen_color attribute
        # off the Wild cards
        useable_cards = self.discard_pile.cards
        for card in useable_cards:
            card.strip_chosen_color()

        # Add the cleaned cards to the bottom of the draw pile
        self.draw_pile.add_to_bottom(useable_cards)
        # Replace the original discard pile with just the top/current card
        self.discard_pile = Deck(def_cards=top_card)
    
    def current_card(self):
        """
        Return the current/top card in the discard pile, which is the card that
        future plays need to match.
        """
        return self.discard_pile.show_top()

    def current_color(self):
        """
        Return just the color (as a string) of the current/top card.
        """
        return self.current_card().color

    def current_symbol(self):
        """
        Return just the Symbol (as a string) of the current/top card.
        """
        return self.current_card().symbol

    def reverse_direction(self):
        """
        Reverse the current direction of play (CW/forwards vs. CCW/backwards).
        """
        self._direction = -self._direction

    @property
    def direction(self):
        """
        Return the private property _direction.

        Returns:
            An int that is either -1 or 1, indicating what direction play
            should proceed.
        """
        return self._direction

    def __repr__(self):
        """
        Overwrite the representation of the GameState class to include the
        current card, direction, and contents of the draw and discard piles.
        """
        return (f"Uno GameState with current_card(): {self.current_card()} and"
            f"direction: {self.direction}\n"
            f"draw_pile ({self.draw_pile.size()} card): {self.draw_pile} \n"
            f"and discard_pile ({self.discard_pile.size()} card): "
            f"{self.discard_pile}")

class GameDirector:
    """
    A representation of an uno game director, which tells players when they can
    play cards.

    Attributes:
        players: A list of Player instances (either users or bots).
        game: A GameState instance representing the parts of the game that
            players can interact with.
        current_player_index: The index in the players list (0-3) of the player
            being/to-be called.
    """

    def __init__(self, player_list, game_state):
        """
        Initialize the GameDirector instance.

        Args:
            players_list: A list of Player instances (either users or bots).
            game_state: A GameState instance for the new game.
        """
        self.players = player_list
        self.game = game_state
        self.current_player_index = 0

    def current_player(self):
        """
        Return the player instance refered to by the current_player_index.
        """
        return self.players[self.current_player_index]

    def handle_reverse(self):
        """
        Reverse the direction of the game if the action has not yet been
        handled (and do nothing if there is no reverse or it has already been
        handled).
        """
        if self.game.current_action == "Reverse":
            self.game.reverse_direction()
            self.game.current_action = None

    def call_the_player(self):
        """
        Get the current player to take their turn (handle action that refer to
        them like drawing card or being skipped, and if they don't have to do
        that, then play a card of their choice).
        """
        self.current_player().take_turn()

    def go_to_next_player(self):
        """
        Change current_player_index to the correct next int using the game's direction and loop at the bounds of the list.
        """
        new_index = self.current_player_index + self.game.direction
        if new_index > len(self.players)-1:
            self.current_player_index = 0
        elif new_index < 0:
            self.current_player_index = len(self.players)-1
        else:
            self.current_player_index = new_index
