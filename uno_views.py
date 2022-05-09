"""
Classes representing viewing modes for the uno game.
"""

from abc import ABC, abstractmethod
from uno_text_view_helpers import (
    put_in_card,
    get_big_card,
    color_card_rep,
    print_cards,
    other_players_as_big_card
)

class UnoView(ABC):
    """
    An abstract class for viewing the uno game.
    
    Attributes:
        players: A list of Player instances (either users or bots).
        game: A GameState instance representing the parts of the game that
            players can interact with.
    """

    def __init__(self, player_list, game_state):
        """
        Initialize a new game view instance.

        Args:
            players_list: A list of Player instances (either users or bots).
            game_state: A GameState instance for the new game.
        """
        self.players = player_list
        self.game = game_state

    def display(self, current_player, show_bot_hands=False):
        """
        Display the relevant information for this turn.

        Args:
            current_player: The Player instance whose turn it currently is.
            show_bot_hands: A bool that tells whether or not to show the hands
                of the bots playing (for testing) or False (default) to only
                show the hand of the user, as the game is meant to be played.
        """
        print("============================================================")
        self.display_other_players_and_current_card()
        print(f"It's {current_player.name}'s turn.")
        if ((show_bot_hands == True or current_player.player_type == "User")
            and self.game.current_action == None):
            self.display_hand(current_player)

    @abstractmethod
    def display_other_players_and_current_card(self):
        """
        An abstract method for showing the other players and their card count, as well as the current top card.
        """
    
    @abstractmethod
    def display_other_players(self):
        """
        An abstract method for showing the other players and their card count.
        """
    
    @abstractmethod
    def display_current_card(self):
        """
        An abstract method for showing the current top card.
        """

    @abstractmethod
    def display_hand(self, player):
        """
        An abstract method for showing the current player's hand.
        """


class TextView(UnoView):
    """
    An uno game viewing class (that inherits from UnoView) for displaying game information as plain text on the command line.
    """
    
    def display_other_players(self):
        """
        Print the names of the other players and the number of cards they have.
        """
        for player in self.players:
            print(f"{player.name} has {player.num_cards()} cards.")

    def display_current_card(self):
        """
        Print the current card as plain text.
        """
        print(f"The current card is {self.game.current_color()} {self.game.current_symbol()}.")

    def display_hand(self, player):
        """
        Print the player's hand as plain text.
        """
        print(f"{player.name}'s hand:")
        print(player.hand)

    def display_other_players_and_current_card(self):
        """
        Print the names of the other players and the number of cards they have
        as well as the current card.
        """
        self.display_other_players()
        self.display_current_card()

class ColorTextView(UnoView):
    """
    An uno game viewing class (that inherits from UnoView) for displaying game information as plain text and colorful ascii art in the terminal.
    """

    def display_other_players(self):
        """
        Print to the terminal the other players and the number of cards they
        have as an ascii art diamond with arrows indicating the direction of
        play.
        """
        full = self.make_other_players_diamond()
        for line in full:
            print(line)

    def display_current_card(self):
        """
        Print to the terminal a colored ascii art representation of the current
        card.
        """
        print(f"The current card is {self.game.current_color()} {self.game.current_symbol()}.")
        card_rep = get_big_card(self.game.current_symbol())
        card_rep = color_card_rep(card_rep, self.game.current_color())
        players_rep = self.display_other_players()
        players_big_card = other_players_as_big_card(players_rep)
        print_cards([card_rep, players_big_card])

    def display_other_players_and_current_card(self):
        """
        Print to the terminal a colored ascii art representation of the current
        card and the other players and the number of cards they have as an
        ascii art diamond in one block.
        """
        print(f"The current card is {self.game.current_color()} {self.game.current_symbol()}.")
        card_rep = get_big_card(self.game.current_symbol())
        card_rep = color_card_rep(card_rep, self.game.current_color())
        players_rep = self.make_other_players_diamond()
        players_big_card = other_players_as_big_card(players_rep)
        print_cards([card_rep, players_big_card])

    def display_hand(self, player):
        """
        Print to the terminal a colored ascii art representation of the cards
        in the player's hand.
        """
        print(f"{player.name}'s hand:")
        card_reps = []
        for card in player.hand:
            card_rep = put_in_card(card.symbol)
            card_rep = color_card_rep(card_rep, card.color)
            card_reps.append(card_rep)

        index_str = ""
        for i in range(1,len(player.hand)+1):
            index_str += str(i).center(6)

        print_cards(card_reps)
        print(index_str)

    def make_other_players_diamond(self):
        """
        Make a list of rows that when printed, shows the other players and the
        number of cards they have as an ascii art diamond with arrows
        indicating the direction of play.

        When printed, the result is like this:

                  Bot 2
                   (6)
               ↗        ↘
            Bot 1       Bot 3
             (5)         (1)
               ↖        ↙
                  Bot 0
                   (4)

        Returns:
            A list of strings.
        """
        # Define the unicode arrows and diamond width
        ne = "\u2197"
        se = "\u2198"
        sw = "\u2199"
        nw = "\u2196"
        half_width = 8

        # Create a list of string representations for the number of cards each
        # player has in their hand (formatted in parentheses)
        card_count_strings = []
        for player in self.players:
            card_str = "(" + str(player.num_cards()) + ")"
            card_str = card_str.center(len(player.name))
            card_count_strings.append(card_str)

        # Create centered blocks of two rows with the player names and card
        # counts with the first player on the bottom, and the second to the left
        top = [ self.players[2].name.center(half_width*2 + 1),
                card_count_strings[2].center(half_width*2 + 1) ]
        bottom = [ self.players[0].name.center(half_width*2 + 1),
                card_count_strings[0].center(half_width*2 + 1) ]
        left = [ self.players[1].name.ljust(half_width),
                card_count_strings[1].ljust(half_width) ]
        right = [ self.players[3].name.rjust(half_width),
                card_count_strings[3].rjust(half_width) ]

        # Create the arrow rows to point clockwise for forward, and
        # counterclockwise for backwards
        if self.game.direction == 1:
            arrows = [ne.center(half_width) + " " + se.center(half_width),
                      nw.center(half_width) + " " + sw.center(half_width)]
        else:
            arrows = [sw.center(half_width) + " " + nw.center(half_width),
                      se.center(half_width) + " " + ne.center(half_width)]

        # Assemble all of the blocks
        full = [top[0],
                top[1],
                arrows[0],
                left[0] + " " + right[0],
                left[1] + " " + right[1],
                arrows[1],
                bottom[0],
                bottom[1]]
        # Return the assembled string list
        return full