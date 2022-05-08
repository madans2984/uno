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

def print_test_deck(name=None):
    deck = Deck()
    # deck.shuffle()
    unpacked_deck = unpack_deck(deck)

    if name != None:
        print(f"{name} = pack_deck([")
    else:
        print("[")

    i = 0
    for card in unpacked_deck:
        string = f"    {card}, "
        # string = string.ljust(27, " ")
        print(string, sep="")
        i +=1

    if name != None:
        print(f"    {unpacked_deck[-1]}])")
    else:
        print("]")
    
    print(deck.size())

# for i in range(1,6):
#     print_test_deck(f"test_deck{i}")
#     print()

print_test_deck()