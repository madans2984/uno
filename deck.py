import random

class Card:
    
    def __init__(self, suit, rank):
        """
        Args:
            suit: A string representing the suit.
            rank: An int represnting the rank of the card (11-13 is J, Q, K).
        """
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        if self.rank == 10:
            rank = "Skip"
        elif self.rank == 11:
            rank = "Reverse"
        elif self.rank == 12:
            rank = "Plus 2"
        elif self.rank == 13:
            rank = "Choose Color"
        elif self.rank == 14:
            rank = "Plus 4"
        else:
            rank = self.rank
           
        return f"{self.suit} {rank}"

class Deck:
    
    def __init__(self):
        self.cards = []
        for blank in range(2): 
            for suit in ["Red", "Blue", "Green", "Yellow"]:
                for rank in range(0,13):
                    self.cards.append(Card(suit,rank))
        for blank in range(4):
            for suit in ["Wild"]:
                for rank in range(13,15):
                    self.cards.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.cards)
        
    def draw(self):
        drawn_card = self.cards[0]
        self.cards = self.cards[1:]
        return drawn_card