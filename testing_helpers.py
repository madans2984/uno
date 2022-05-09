"""
Helper functions for unit testing.

It's difficult to compare lists of Cards and Deck instances to know if they are
identical, and once an imported Deck is modified by a test, it remains in that
state for the rest of the tests (so imported Decks can be reused). These
"packing" (turning a list of lists into a Deck or list of Cards) and
"unpacking" (turning a Deck or list of Cards into a list of lists) functions
create list-based representations of these objects and lists of objects, and
allow the important aspects of these objects (the color and symbol) to be
compared easily.
"""

from uno_deck import Card, Deck


def unpack_cards(card_obj_list):
    """
    Return the list-based representation of the list of Card instances.

    Args:
        card_obj_list: A list of Card instances.
    """
    return [[card.color, card.symbol] for card in card_obj_list]


def pack_cards(color_symbol_list):
    """
    Return the list of Card instances indicated by the list-based
    representation.

    Args:
        color_symbol_list: A list of cards represented as [<color>, <symbol>].
    """
    cards = []
    for row in color_symbol_list:
        cards.append(Card(row[0], row[1]))
    return cards


def unpack_deck(deck):
    """
    Return the list-based representation of the Deck instance.

    Args:
        card_obj_list: A list of Card instances.
    """
    return unpack_cards(deck.cards)


def pack_deck(color_symbol_list):
    """
    Return the Deck indicated by the list-based representation.

    Args:
        color_symbol_list: A list of cards represented as [<color>, <symbol>].
    """
    cards = pack_cards(color_symbol_list)
    return Deck(def_cards=cards)
