"""
Test all aspects of the uno game, across all files and classes, using pytest.
"""

import pytest
from testing_decks import (
    normal_test_deck1,
    normal_test_deck2,
    normal_test_deck3,
    normal_test_deck4,
    one_action_on_top_test_deck,
    five_actions_on_top_test_deck
)
from testing_helpers import (
    unpack_cards,
    pack_cards,
    unpack_deck,
    pack_deck
)
from uno_deck import Card, Deck
from uno_game import GameState, GameDirector
from uno_controllers import BotPlayer, UserPlayerTextController


def test_deck_packing():
    deck = Deck()
    deck.shuffle()
    unpacked_deck = unpack_deck(deck)
    packed_deck = pack_deck(unpacked_deck)
    re_unpacked_deck = unpack_deck(packed_deck)
    assert unpacked_deck == re_unpacked_deck

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
    (normal_test_deck1, 1, [['Green', '2']]),
    (normal_test_deck2, 2, [['Red', '3'], ['Green', '9']]),
    (normal_test_deck3, 4, [['Green','5'], ['Yellow','3'],
        ['Blue','1'], ['Yellow','5']]),
    (five_actions_on_top_test_deck, 4,[['Wild', ''], ['Red', 'Skip'],
        ['Blue', 'Reverse'], ['Wild', '+4']])
]

@pytest.mark.parametrize("test_deck_list,num_cards,drawn_cards",
    draw_cards_cases)
def test_user_draw_cards(test_deck_list, num_cards, drawn_cards):
    test_deck = pack_deck(test_deck_list)
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

@pytest.mark.parametrize("test_deck_list,num_cards,drawn_cards",
    draw_cards_cases)
def test_bot_draw_cards(test_deck_list, num_cards, drawn_cards):
    test_deck = pack_deck(test_deck_list)
    orig_deck_len = test_deck.size()
    orig_deck_list = unpack_cards(test_deck.cards)
    game = GameState()
    bot_player = UserPlayerTextController(game, "Bot", "Bot")
    bot_player.hand = []
    game.draw_pile = test_deck
    bot_player.draw(num_cards)
    if num_cards == None:
        num_cards = 1

    assert len(bot_player.hand) == num_cards
    assert game.draw_pile.size() == orig_deck_len-num_cards
    assert unpack_cards(bot_player.hand) == drawn_cards
    assert unpack_deck(game.draw_pile) == orig_deck_list[num_cards:]

setup_dealing_cases = [
    (normal_test_deck4,['Red', '8'],[ [['Green', '2'],
                                ['Green', '7'],
                                ['Red', '7'],
                                ['Wild', ''],
                                ['Blue', 'Skip'],
                                ['Red', 'Skip'],
                                ['Red', '0']],
                               [['Green', '9'],
                                ['Wild', ''],
                                ['Green', '6'],
                                ['Wild', '+4'],
                                ['Blue', '+2'],
                                ['Yellow', '8'],
                                ['Yellow', '3']],
                               [['Blue', '8'],
                                ['Blue', '+2'],
                                ['Green', '7'],
                                ['Wild', '+4'],
                                ['Red', '6'],
                                ['Red', '2'],
                                ['Yellow', '5']],
                               [['Red', '5'],
                                ['Green', '6'],
                                ['Green', 'Reverse'],
                                ['Green', '4'],
                                ['Yellow', '6'],
                                ['Green', '5'],
                                ['Green', '0']] ])
]

@pytest.mark.parametrize("test_deck_list,discard,player_hands", setup_dealing_cases)
def test_setup_dealing(test_deck_list,discard,player_hands):
    test_deck = pack_deck(test_deck_list)
    game = GameState(def_deck=test_deck)
    
    assert unpack_cards([game.discard_pile.show_top()]) == [discard]

    user_player = UserPlayerTextController(game, "User", "User")
    bot1 = BotPlayer(game, "Bot 1", "Bot")
    bot2 = BotPlayer(game, "Bot 2", "Bot")
    bot3 = BotPlayer(game, "Bot 3", "Bot")
    player_list = [user_player, bot1, bot2, bot3]

    for index in range(len(player_list)):
        print(player_hands[index])
        print(unpack_cards(player_list[index].hand))
        assert player_hands[index] == unpack_cards(player_list[index].hand)

    assert unpack_deck(game.draw_pile) == test_deck_list[29:]


discard_pile_setup_cases = [
    (pack_deck(normal_test_deck1),['Green', '2']),
    (pack_deck(normal_test_deck2),['Red', '3']),
    (pack_deck(one_action_on_top_test_deck),['Red', '9']),
    (pack_deck(five_actions_on_top_test_deck),['Blue', '5'])
]

@pytest.mark.parametrize("test_deck,discard", discard_pile_setup_cases)
def test_setup_discard_pile(test_deck,discard):
    game = GameState(def_deck=test_deck)
    assert unpack_cards([game.discard_pile.show_top()]) == [discard]


play_card_cases = [
    (Card("Red","0"), Card("Red", "0"), True),
    (Card("Green","2"), Card("Green", "0"), True),
    (Card("Yellow","3"), Card("Red", "3"), True),
    (Card("Red","4"), Card("Wild", ""), True),
    (Card("Blue","5"), Card("Blue", "+2"), True),
    (Card("Green","6"), Card("Wild", "+4"), True),
    (Card("Yellow","0"), Card("Yellow", "Reverse"), True),
    (Card("Red","Reverse"), Card("Blue", "Reverse"), True),
    (Card("Blue","+2"), Card("Yellow", "+2"), True),
    (Card("Green","+4"), Card("Blue", "+4"), True),
    (Card("Blue","1"), Card("Red", "0"), False),
    (Card("Green","+4"), Card("Yellow", "Reverse"), False),
    (Card("Blue","5"), Card("Green", "+2"), False),
    (Card("Yellow","0"), Card("Blue", "Reverse"), False),
    (Card("Blue","+2"), Card("Yellow", "Reverse"), False)

]

@pytest.mark.parametrize("current_card,played_card,result", play_card_cases)
def test_play_card(current_card,played_card,result):
    game = GameState()
    game.discard_pile = Deck(def_cards=[current_card])
    player = BotPlayer(game, "Bot", "Bot")
    player.hand = [played_card]
    assert player.play_card(played_card) == result

def test_playing_draw2():
    card = Card("Red", "+2")
    game = GameState()
    game.discard_pile = Deck(def_cards=[Card(card.color, "0")])
    bot0 = BotPlayer(game, "Bot 0", "Bot", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", "Bot", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", "Bot", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", "Bot", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    for player in player_list:
        player.hand = []

    bot3.hand = [card]
    bot3.play_card(card)

    director.call_the_player()
    director.handle_reverse()

    assert len(bot0.hand) == 2

    director.go_to_next_player()

    assert director.current_player() == bot1
    

def test_playing_draw4():
    card = Card("Wild", "+4")
    game = GameState()
    bot0 = BotPlayer(game, "Bot 0", "Bot", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", "Bot", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", "Bot", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", "Bot", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    for player in player_list:
        player.hand = []

    bot3.hand = [card]
    bot3.play_card(card)

    director.call_the_player()
    director.handle_reverse()

    assert len(bot0.hand) == 4

    director.go_to_next_player()

    assert director.current_player() == bot1

def test_playing_reverse():
    game = GameState()
    bot0 = BotPlayer(game, "Bot 0", "Bot", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", "Bot", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", "Bot", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", "Bot", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    bot0.hand.insert(0, Card("Red", "Reverse"))
    bot3.hand.insert(0, Card("Red", "0"))
    bot2.hand.insert(0, Card("Blue", "0"))
    bot1.hand.insert(0, Card("Blue", "Reverse"))
    game.discard_pile = Deck(def_cards=[Card(bot0.hand[0].color, "0")])

    # Call Bot 0, who plays Red Reverse
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()

    assert director.current_player() == bot3

    # Call Bot 3 who plays Red 0
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()

    assert director.current_player() == bot2

    # Call Bot 2 who plays Blue 0
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()

    assert director.current_player() == bot1

    # Call Bot 1 who plays Blue Reverse
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()

    assert director.current_player() == bot2

def test_playing_skip():
    game = GameState()
    bot0 = BotPlayer(game, "Bot 0", "Bot", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", "Bot", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", "Bot", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", "Bot", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    bot0.hand.insert(0, Card("Red", "Skip"))
    bot1.hand.insert(0, Card("Red", "0"))
    game.discard_pile = Deck(def_cards=[Card(bot0.hand[0].color, "0")])

    bot1_cards_orig = unpack_cards(bot1.hand)

    # Call Bot 0, who plays Red Skip
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()

    assert director.current_player() == bot1

    # Call Bot 1 who whould not get to do anything
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()

    assert unpack_cards(bot1.hand) == bot1_cards_orig

    assert director.current_player() == bot2


choose_color_cases = [
    (Card("Wild", ""), "r", "Red"),
    (Card("Wild", ""), "g", "Green"),
    (Card("Wild", ""), "b", "Blue"),
    (Card("Wild", ""), "y", "Yellow"),
    (Card("Wild", "+4"), "r", "Red"),
    (Card("Wild", "+4"), "g", "Green"),
    (Card("Wild", "+4"), "b", "Blue"),
    (Card("Wild", "+4"), "y", "Yellow"),
]

@pytest.mark.parametrize("card,manual_input,correct_color", choose_color_cases)
def test_choose_color(card, manual_input, correct_color):
    game = GameState()

    user_player = UserPlayerTextController(game, "User", "User")
    bot1 = BotPlayer(game, "Bot 1", "Bot", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", "Bot", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", "Bot", play_card_delay=0)
    player_list = [user_player, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    user_player.hand.insert(0, card)

    user_player.play_card(card,choose_manual_input=manual_input)

    assert game.current_color() == correct_color
    assert game.discard_pile.show_top().color == correct_color


win_testing_cases = [
    (Card("Red", "0"), 0),
    (Card("Green", "Reverse"), 1),
    (Card("Blue", "Skip"), 2),
    (Card("Yellow", "+2"), 3),
    (Card("Wild", ""), 0),
    (Card("Wild", "+4"), 1)
]

@pytest.mark.parametrize("card,player_index", win_testing_cases)
def check_win_condition(card, player_index):
    game = GameState()
    bot0 = BotPlayer(game, "Bot 0", "Bot", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", "Bot", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", "Bot", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", "Bot", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    winner = player_list[player_index]
    winner.hand = [card]
    game.discard_pile = Deck(def_cards=[Card(winner.hand[0].color, "0")])

    winner.play_card(card,"r")

    assert game.won == True