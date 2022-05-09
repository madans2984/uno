"""
Helper functions for unit testing.
"""

from uno_deck import *

def unpack_cards(card_obj_list):
    return [[card.color, card.symbol] for card in card_obj_list]

def pack_cards(color_symbol_list):
    cards = []
    for row in color_symbol_list:
        cards.append(Card(row[0],row[1]))
    return cards

def unpack_deck(deck):
    return unpack_cards(deck.cards)

def pack_deck(color_symbol_list):
    cards = pack_cards(color_symbol_list)
    return Deck(def_cards=cards)