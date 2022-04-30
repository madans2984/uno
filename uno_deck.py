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
        self.symbol = symbol
        self.chosen_color = ""

    def strip_chosen_color(self):
        """
        Reset chosen_color back to "", in case it had been defined by a player
        before.
        """
        self.chosen_color = ""
    
    @property
    def color(self):
        if self._color == "Wild" and self.chosen_color != "":
            return self.chosen_color
        return self._color
    
    def __repr__(self):
        return f"{self.color} {self.symbol}"

class Deck:
    """
    A representation of an Uno deck.
    """
    def __init__(self, def_cards=None, include_reverse=True,
        include_wilds=True, include_skips=True, include_draws=True,
        is_empty=False):
        """
        Args:
            def_cards: A list of Card objects, in case the deck should be
                defined manually (e.g. reusing discards)
            include_reverse: A boolean denoting if Cards with the symbol/action
                "Reverse" should be included in the deck
            include_wilds: A boolean denoting if "Wild" cards should be
                included in the deck
            include_skips: A boolean denoting if Cards that make the next
                player skip their turn ("Skip", "+2", and "+4") should be
                included
            include_draws: A boolean denoting if Cards that make the next
                player draw cards ("+2", "+4") should be included
            is_empty: A boolean denoting if the Deck should be initialized as
                an empty list with no Cards in it (e.g. the discard pile)
        """
        if def_cards is not None:
            self.cards = def_cards
            return

        self.cards = []
        if not is_empty:
            for _ in range(2): 
                for color in ["Red", "Blue", "Green", "Yellow"]:
                    for symbol in range(0,10):
                        self.cards.append(Card(color,str(symbol)))
                    if include_reverse:
                        self.cards.append(Card(color,"Reverse"))
                    if include_skips:
                        self.cards.append(Card(color,"Skip"))
                    if include_draws and include_skips:
                        self.cards.append(Card(color,"+2"))
            for _ in range(6):
                if include_wilds:
                    self.cards.append(Card("Wild",""))
                if include_draws and include_skips and include_wilds:
                    self.cards.append(Card("Wild","+4"))

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