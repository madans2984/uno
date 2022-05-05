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

def print_test_deck(name):
    deck = Deck()
    deck.shuffle()
    unpacked_deck = unpack_deck(deck)
    print(f"{name} = pack_deck([")
    for card in unpacked_deck[:-1]:
        print("    ", card, ",", sep="")
    print(f"    {unpacked_deck[-1]}])")

for i in range(1,6):
    print_test_deck(f"test_deck{i}")
    print()

test_deck1 = pack_deck([
    ['Blue', 'Skip'],
    ['Green', '0'],
    ['Blue', '9'],
    ['Red', '8'],
    ['Red', 'Reverse'],
    ['Yellow', 'Skip'],
    ['Green', '9'],
    ['Green', '2'],
    ['Green', '3'],
    ['Yellow', '3'],
    ['Wild', '+4'],
    ['Wild', '+4'],
    ['Red', '2'],
    ['Blue', '+2'],
    ['Red', '9'],
    ['Yellow', '1'],
    ['Yellow', '2'],
    ['Blue', '3'],
    ['Yellow', '+2'],
    ['Red', '7'],
    ['Blue', '5'],
    ['Wild', ''],
    ['Green', '2'],
    ['Blue', '4'],
    ['Red', '8'],
    ['Green', '4'],
    ['Red', '4'],
    ['Green', '3'],
    ['Blue', '6'],
    ['Blue', '9'],
    ['Yellow', '7'],
    ['Red', '3'],
    ['Yellow', '7'],
    ['Yellow', '8'],
    ['Red', '1'],
    ['Yellow', '5'],
    ['Red', '9'],
    ['Green', '7'],
    ['Green', '5'],
    ['Wild', ''],
    ['Blue', '1'],
    ['Yellow', '9'],
    ['Blue', 'Skip'],
    ['Wild', ''],
    ['Yellow', '8'],
    ['Yellow', '1'],
    ['Red', '7'],
    ['Green', '1'],
    ['Red', '5'],
    ['Wild', ''],
    ['Red', '0'],
    ['Red', '2'],
    ['Blue', '7'],
    ['Blue', '4'],
    ['Blue', '8'],
    ['Green', '6'],
    ['Green', '9'],
    ['Wild', ''],
    ['Yellow', '4'],
    ['Red', '3'],
    ['Blue', '+2'],
    ['Green', '5'],
    ['Yellow', '5'],
    ['Green', '1'],
    ['Green', 'Skip'],
    ['Green', '+2'],
    ['Red', 'Skip'],
    ['Red', '6'],
    ['Yellow', '6'],
    ['Blue', '7'],
    ['Red', '+2'],
    ['Blue', 'Reverse'],
    ['Blue', 'Reverse'],
    ['Red', '4'],
    ['Wild', '+4'],
    ['Green', 'Reverse'],
    ['Blue', '8'],
    ['Wild', '+4'],
    ['Green', 'Skip'],
    ['Wild', '+4'],
    ['Green', '8'],
    ['Blue', '2'],
    ['Green', '4'],
    ['Yellow', '0'],
    ['Red', '1'],
    ['Yellow', '3'],
    ['Green', '+2'],
    ['Yellow', '9'],
    ['Red', '6'],
    ['Wild', '+4'],
    ['Blue', '0'],
    ['Blue', '5'],
    ['Red', '5'],
    ['Blue', '6'],
    ['Yellow', '+2'],
    ['Blue', '1'],
    ['Wild', ''],
    ['Yellow', '2'],
    ['Blue', '2'],
    ['Green', '7'],
    ['Red', '+2'],
    ['Green', '8'],
    ['Yellow', '4'],
    ['Green', 'Reverse'],
    ['Green', '6'],
    ['Yellow', 'Reverse'],
    ['Red', 'Skip'],
    ['Red', 'Reverse'],
    ['Blue', '3'],
    ['Yellow', 'Reverse'],
    ['Yellow', '6'],
    ['Yellow', 'Skip'], ])

