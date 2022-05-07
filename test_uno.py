import pytest
from testing_helpers import *
from testing_decks import *
from uno_deck import *
from uno_game import *
from uno_controllers import *
from uno_views import *


# def test_deck_packing():
#     deck = Deck()
#     unpacked_deck = unpack_deck(deck)
#     packed_deck = pack_deck(unpacked_deck)
#     re_unpacked_deck = unpack_deck(packed_deck)
#     assert unpacked_deck == re_unpacked_deck

uno_card_creation_cases = [
    ("Red", "0"),
    ("Green", "Reverse"),
    ("Blue", "Skip"),
    ("Yellow", "+2"),
    ("Wild", ""),
    ("Wild", "+4"),
]

@pytest.mark.parametrize("color,symbol", uno_card_creation_cases)
def test_uno_card_creation(color, symbol):
    card = Card(color, symbol)
    assert card.color == color
    assert card.symbol == symbol


uno_chosen_color_cases = [
    ("Wild", "", "Red"),
    ("Wild", "+4", "Green"),
    ("Wild", "", "Blue"),
    ("Wild", "+4", "Yellow"),
]

@pytest.mark.parametrize("color,symbol,chosen_color", uno_chosen_color_cases)
def test_uno_card_chosen_color(color, symbol, chosen_color):
    card = Card(color, symbol)

    assert card.color == color
    assert card.symbol == symbol

    card.chosen_color = chosen_color

    assert card.color == chosen_color
    assert card.symbol == symbol

    card.strip_chosen_color()

    assert card.color == color
    assert card.symbol == symbol


def test_full_deck_creation():
    deck = Deck()
    reds = [card for card in deck.cards if card.color == "Red"]
    print("reds =", reds)
    assert len(reds) == 25
    greens = [card for card in deck.cards if card.color == "Green"]
    print("greens =", greens)
    assert len(greens) == 25
    blues = [card for card in deck.cards if card.color == "Blue"]
    print("blues =", blues)
    assert len(blues) == 25
    yellows = [card for card in deck.cards if card.color == "Yellow"]
    print("yellows =", yellows)
    assert len(yellows) == 25
    wilds = [card for card in deck.cards if card.color == "Wild"]
    print("wilds =", wilds)
    assert len(wilds) == 12

    nums = [card for card in deck.cards if card.symbol in "0123456789" and card.color != "Wild"]
    print("nums =", nums)
    assert len(nums) == 76
    reverses = [card for card in deck.cards if card.symbol == "Reverse"]
    print("reverses =", reverses)
    assert len(reverses) == 8
    skips = [card for card in deck.cards if card.symbol == "Skip"]
    print("skips =", skips)
    assert len(skips) == 8
    plus_2s = [card for card in deck.cards if card.symbol == "+2"]
    print("plus_2s =", plus_2s)
    assert len(plus_2s) == 8
    plus_4s = [card for card in deck.cards if card.symbol == "+4"]
    print("plus_4s =", plus_4s)
    assert len(plus_4s) == 6
    chooses = [card for card in deck.cards if card.symbol == ""]
    print("chooses =", chooses)
    assert len(chooses) == 6

    print("deck.cards =", deck.cards)
    assert len(deck.cards) == 112
    

def test_shuffle():
    deck = Deck()
    deck2 = Deck()
    deck2.shuffle()

    assert unpack_deck(deck) != unpack_deck(deck2)


draw_cards_cases = [
    (test_deck1, 1, [['Green', '2']]),
    (test_deck2, 2, [['Red', '3'], ['Green', '9']]),
    (test_deck3, 4, [['Green','5'],['Yellow','3'],['Blue','1'],['Yellow','5']])
]

@pytest.mark.parametrize("test_deck,num_cards,drawn_cards", draw_cards_cases)
def test_user_draw_card(test_deck, num_cards, drawn_cards):
    orig_deck_len = test_deck.size()
    orig_deck_list = unpack_cards(test_deck.cards)
    game = GameState()
    user_player = UserPlayerTextController(game, "User", "User")
    user_player.hand = []
    game.draw_pile = test_deck
    user_player.draw(num_cards)
    if num_cards == None:
        num_cards = 1

    assert len(user_player.hand) == num_cards
    assert game.draw_pile.size() == orig_deck_len-num_cards
    assert unpack_cards(user_player.hand) == drawn_cards
    assert unpack_deck(game.draw_pile) == orig_deck_list[num_cards:]