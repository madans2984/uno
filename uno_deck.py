"""
Classes representing uno cards and a deck of uno cards.
"""

import random

class Card:
    """
    A representation of an Uno card.
    """
    def __init__(self, color, symbol):
        """
        Create an Uno card object with a color and symbol/action.

        Color options: "Red", "Blue", "Green", "Yellow", and "Wild"
        Symbol options: "", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "Reverse", "Skip", "+2", and "+4"

        Args:
            _color: A string representing the color.
            symbol: A string represening the number or action on the card
            chosen_color: A string representing the color chosen by the player
                when _color is "Wild"
        """
        self._color = color
        self._symbol = symbol
        self.chosen_color = ""

    def strip_chosen_color(self):
        """
        Reset chosen_color back to "", in case it had been defined by a player
        before.
        """
        self.chosen_color = ""

    def is_special(self):
        if (self.symbol == "Reverse" or self.symbol == "Skip"
            or self.symbol == "+2" or self.symbol == "+4"
            or self.symbol == ""):
            return True
        return False

    @property
    def color(self):
        if self._color == "Wild" and self.chosen_color != "":
            return self.chosen_color
        return self._color

    @property
    def symbol(self):
        return self._symbol

    def __repr__(self):
        if self.symbol == "":
            return f"{self.color}"
        else:
            return f"{self.color} {self.symbol}"

class Deck:
    """
    A representation of an Uno deck.
    """
    def __init__(self, def_cards=None, is_empty=False):
        """
        Initialize a deck object.

        Default is a full (unshuffled) deck with 112 cards.
            - 25 of each color (of Red, Green, Blue, and Yellow).
              Within each color:
                - One "0"
                - Two of each number 1-9
                - Two of each of "Reverse", "Skip", and "+2"
            - 12 "Wild" cards
                - Six "", where the color is chosen by the player
                - Six "+4", where the color is chosen by the player and the
                  next player must draw 4 cards and miss their turn

        Args:
            def_cards: A list of Card objects, in case the deck should be
                defined manually (e.g. reusing discards, running tests)
            is_empty: A boolean denoting if the Deck should be initialized as
                an empty list with no Cards in it (e.g. the discard pile)
        """

        # Use only the defined cards if they are given
        if def_cards is not None:
            self.cards = def_cards
            return

        # Initialize the cards attribute as an empty list
        self.cards = []

        # If the deck is meant to be empty (e.g. the discard pile during setup)
        # then stop now
        if is_empty: return

        # Add the 112 cards in a normal uno deck
        for color in ["Red", "Blue", "Green", "Yellow"]:
            self.cards.append(Card(color,"0"))
            for _ in range(2):
                for num in range(1,10):
                    self.cards.append(Card(color,str(num)))
                self.cards.append(Card(color,"Reverse"))
                self.cards.append(Card(color,"Skip"))
                self.cards.append(Card(color,"+2"))
        self.cards.extend([Card("Wild","")]*6)
        self.cards.extend([Card("Wild","+4")]*6)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self,num_cards=1):
        """
        Remove an return a list of a specified number of Cards from the Deck.

        Args:
            num_cards: An int specifying how many cards to draw (optional, default is 1 card)
        Returns:
            A list of Cards (even if only one card is requested).
        """
        drawn_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return drawn_cards

    def show_top(self):
        return self.cards[0]

    def add_to_top(self, new_card):
        """
        Args:
            new_card: A single Card object to be added to the top/beginning
                of the Deck/list.
        """
        self.cards.insert(0,new_card)

    def add_to_bottom(self, new_cards):
        """
        Args:
            new_cards: A list of Cards to be added to the bottom/end of the
                Deck/list
        """
        self.cards.extend(new_cards)

    def size(self):
        return len(self.cards)

    def __repr__(self):
        return f"Deck with cards {self.cards}"
