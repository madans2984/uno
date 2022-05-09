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
    """
    Test the deck packing and unpacking testing helper functions in
    testing_helpers.py.
    """
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
    """
    Test Card creation and private attributes

    Args:
        color: A string representing the color to set the card to.
        symbol: A string representing the symbol to set the card to.
    """
    card = Card(color, symbol)
    assert card.color == color
    assert card.symbol == symbol
    try:
        card.symbol = "wrong"
        card.color = "wrong"
    except AttributeError:
        print("Setting private attributes failed properly.")
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
    """
    Test setting a wild card's chosen color attribute.

    Args:
        color: A string representing the test card's color.
        symbol: A string representing the test card's symbol.
        chosen_color: A string representing the color to set the card to.
    """
    card = Card(color, symbol)

    assert card.color == color
    assert card.symbol == symbol

    card.set_chosen_color(chosen_color)

    assert card.color == chosen_color
    assert card.symbol == symbol

    card.strip_chosen_color()

    assert card.color == color
    assert card.symbol == symbol


def test_full_deck_creation():
    """
    Check that the deck has the right number of each type of card.
    """
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
    """
    Test that shuffling the deck changes the order of the cards.
    """
    deck = Deck()
    deck2 = Deck()
    deck2.shuffle()

    assert unpack_deck(deck) != unpack_deck(deck2)


draw_cards_cases = [
    (normal_test_deck1, 1, [["Green", "2"]]),
    (normal_test_deck2, 2, [["Red", "3"], ["Green", "9"]]),
    (normal_test_deck3, 4, [["Green","5"], ["Yellow","3"],
        ["Blue","1"], ["Yellow","5"]]),
    (five_actions_on_top_test_deck, 4,[["Wild", ""], ["Red", "Skip"],
        ["Blue", "Reverse"], ["Wild", "+4"]])
]

@pytest.mark.parametrize("test_deck_list,num_cards,drawn_cards",
    draw_cards_cases)
def test_user_draw_cards(test_deck_list, num_cards, drawn_cards):
    """
    Test that a user player drawing cards from a deck removes the correct cards from the deck and adds the correct cards to the user player's hand.

    Args:
        test_deck_list: A list of cards represented by lists of strings to be
            packed into a new draw_pile deck.
        num_cards: An int representing the number of cards to draw.
        drawn_cards: A list of cards represented by lists of strings that
            represent the cards expected to be drawn from the deck into the
            player's hand.
    """
    # Pack the deck into a Deck instance
    test_deck = pack_deck(test_deck_list)
    # Record the original deck size
    orig_deck_len = test_deck.size()

    # Start a game and replace the draw pile with the test deck
    game = GameState()
    user_player = UserPlayerTextController(game, "User")
    game.draw_pile = test_deck

    # Empty the player's hand and draw the cards
    user_player.hand = []
    user_player.draw(num_cards)

    # Check that the right number of cards have moved
    assert len(user_player.hand) == num_cards
    assert game.draw_pile.size() == orig_deck_len-num_cards

    # Check that the intended cards moved
    assert unpack_cards(user_player.hand) == drawn_cards
    assert unpack_deck(game.draw_pile) == test_deck_list[num_cards:]

@pytest.mark.parametrize("test_deck_list,num_cards,drawn_cards",
    draw_cards_cases)
def test_bot_draw_cards(test_deck_list, num_cards, drawn_cards):
    """
    Test that a bot player drawing cards from a deck removes the correct cards from the deck and adds the correct cards to the bot player's hand.

    Args:
        test_deck_list: A list of cards represented by lists of strings to be
            packed into a new draw_pile deck.
        num_cards: An int representing the number of cards to draw.
        drawn_cards: A list of cards represented by lists of strings that
            represent the cards expected to be drawn from the deck into the
            player's hand.
    """
    # Pack the deck into a Deck instance
    test_deck = pack_deck(test_deck_list)
    # Record the original deck size
    orig_deck_len = test_deck.size()

    # Start a game and replace the draw pile with the test deck
    game = GameState()
    bot_player = BotPlayer(game, "Bot")
    game.draw_pile = test_deck

    # Empty the player's hand and draw the cards
    bot_player.hand = []
    bot_player.draw(num_cards)

    # Check that the right number of cards have moved
    assert len(bot_player.hand) == num_cards
    assert game.draw_pile.size() == orig_deck_len-num_cards

    # Check that the intended cards moved
    assert unpack_cards(bot_player.hand) == drawn_cards
    assert unpack_deck(game.draw_pile) == test_deck_list[num_cards:]

setup_dealing_cases = [
    (normal_test_deck4,["Red", "8"],[ [["Green", "2"],
                                ["Green", "7"],
                                ["Red", "7"],
                                ["Wild", ""],
                                ["Blue", "Skip"],
                                ["Red", "Skip"],
                                ["Red", "0"]],
                               [["Green", "9"],
                                ["Wild", ""],
                                ["Green", "6"],
                                ["Wild", "+4"],
                                ["Blue", "+2"],
                                ["Yellow", "8"],
                                ["Yellow", "3"]],
                               [["Blue", "8"],
                                ["Blue", "+2"],
                                ["Green", "7"],
                                ["Wild", "+4"],
                                ["Red", "6"],
                                ["Red", "2"],
                                ["Yellow", "5"]],
                               [["Red", "5"],
                                ["Green", "6"],
                                ["Green", "Reverse"],
                                ["Green", "4"],
                                ["Yellow", "6"],
                                ["Green", "5"],
                                ["Green", "0"]] ])
]

@pytest.mark.parametrize("test_deck_list,discard,player_hands", setup_dealing_cases)
def test_setup_dealing(test_deck_list,discard,player_hands):
    """
    Test that the players are dealt the correct cards at the beginning of the
    game.

    Args:
        test_deck_list: A list of cards represented by lists of strings to be
            packed into a new draw_pile deck.
        discard: A list representing the card that should be the top of the
            discard pile.
        drawn_cards: A list of lists of cards represented by lists of strings
            that represent the cards expected to be drawn from the deck into
            each player's hand.
    """
    test_deck = pack_deck(test_deck_list)
    game = GameState(def_deck=test_deck)

    assert unpack_cards([game.discard_pile.show_top()]) == [discard]

    user_player = UserPlayerTextController(game, "User")
    bot1 = BotPlayer(game, "Bot 1")
    bot2 = BotPlayer(game, "Bot 2")
    bot3 = BotPlayer(game, "Bot 3")
    player_list = [user_player, bot1, bot2, bot3]

    for index in range(len(player_list)):
        print(player_hands[index])
        print(unpack_cards(player_list[index].hand))
        assert player_hands[index] == unpack_cards(player_list[index].hand)

    assert unpack_deck(game.draw_pile) == test_deck_list[29:]


discard_pile_setup_cases = [
    (pack_deck(normal_test_deck1),["Green", "2"]),
    (pack_deck(normal_test_deck2),["Red", "3"]),
    (pack_deck(one_action_on_top_test_deck),["Red", "9"]),
    (pack_deck(five_actions_on_top_test_deck),["Blue", "5"])
]

@pytest.mark.parametrize("test_deck,discard", discard_pile_setup_cases)
def test_setup_discard_pile(test_deck,discard):
    """
    Check that the first non-special card in the deck starts at the top of the discard pile.

    Args:
        test_deck_list: A list of cards represented by lists of strings to be
            packed into a new draw_pile deck.
        discard: A list representing the card that should be the top of the
            discard pile.
    """
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
    """
    Check that the player.play_card() function properly allows and refuses cards that are and aren't allowed to be played during that turn.

    Args:
        current_card: A Card instance representing the card on the top of the
            discard pile / the current card.
        played_card: A Card instance representing the card for player to
            attempt to play.
        result: A bool representing the expected output from the play_card()
            function (True for played, False for invalid).
    """
    game = GameState()
    game.discard_pile = Deck(def_cards=[current_card])
    player = BotPlayer(game, "Bot")
    player.hand = [played_card]
    assert player.play_card(played_card) == result

def test_playing_draw2():
    """
    Check that playing a "+2" card makes the next player draw 2 cards.
    """
    card = Card("Red", "+2")

    # Setup a game of bots with no delay time, and rig the deck to be able to
    # play the card.
    game = GameState()
    game.discard_pile = Deck(def_cards=[Card(card.color, "0")])
    bot0 = BotPlayer(game, "Bot 0", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    # Empty all of the hands to make it easy to tell if cards were drawn.
    for player in player_list:
        player.hand = []

    # Add the +2 card to bot3's hand and have them play it
    bot3.hand = [card]
    bot3.play_card(card)

    # Have the director simulate the rest of a turn cycle
    director.call_the_player()
    director.handle_reverse()

    # Check that the next player (bot0) now has 2 cards
    assert len(bot0.hand) == 2

    # Have the director complete the turn cycle
    director.go_to_next_player()

    # Check that it is now the next player's turn, (not the player that was
    # skipped by the +2)
    assert director.current_player() == bot1
    

def test_playing_draw4():
    """
    Check that playing a "+4" card makes the next player draw 4 cards.
    """
    card = Card("Wild", "+4")

    # Setup a game of bots with no delay time
    game = GameState()
    bot0 = BotPlayer(game, "Bot 0", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    # Empty all of the hands to make it easy to tell if cards were drawn.
    for player in player_list:
        player.hand = []

    # Add the +2 card to bot3's hand and have them play it
    bot3.hand = [card]
    bot3.play_card(card)

    # Have the director simulate the rest of a turn cycle
    director.call_the_player()
    director.handle_reverse()

    # Check that the next player (bot0) now has 2 cards
    assert len(bot0.hand) == 4

    # Have the director complete the turn cycle
    director.go_to_next_player()

    # Check that it is now the next player's turn, (not the player that was
    # skipped by the +4)
    assert director.current_player() == bot1

def test_playing_reverse():
    """
    Check that playing a "Reverse" makes the turn order switch.
    """
    # Setup a game of bots with no delay time
    game = GameState()
    bot0 = BotPlayer(game, "Bot 0", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    # Plant cards at the front of the player's hands
    bot0.hand.insert(0, Card("Red", "Reverse"))
    bot3.hand.insert(0, Card(bot0.hand[0].color, "0"))
    bot2.hand.insert(0, Card("Blue", bot3.hand[0].symbol))
    bot1.hand.insert(0, Card(bot2.hand[0].color, "Reverse"))
    # Rig the discard pile to allow the first player's card.
    game.discard_pile = Deck(def_cards=[Card(bot0.hand[0].color, "0")])

    # Call Bot 0, who plays Red Reverse
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()
    # Check that the next player is Bot 3
    assert director.current_player() == bot3

    # Call Bot 3 who plays Red 0
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()
    # Check that the next player is Bot 2
    assert director.current_player() == bot2

    # Call Bot 2 who plays Blue 0
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()
    # Check that the next player is Bot 1
    assert director.current_player() == bot1

    # Call Bot 1 who plays Blue Reverse
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()
    # Check that the next player is Bot 2
    assert director.current_player() == bot2

def test_playing_skip():
    """
    Check that playing a "Skip" makes the next player miss their turn.
    """
    # Setup a game of bots with no delay time
    game = GameState()
    bot0 = BotPlayer(game, "Bot 0", play_card_delay=0)
    bot1 = BotPlayer(game, "Bot 1", play_card_delay=0)
    bot2 = BotPlayer(game, "Bot 2", play_card_delay=0)
    bot3 = BotPlayer(game, "Bot 3", play_card_delay=0)
    player_list = [bot0, bot1, bot2, bot3]
    director = GameDirector(player_list, game)

    # Plant cards at the front of the player's hands
    bot0.hand.insert(0, Card("Red", "Skip"))
    bot1.hand.insert(0, Card("Red", "0"))
    # Rig the discard pile to allow the first player's card.
    game.discard_pile = Deck(def_cards=[Card(bot0.hand[0].color, "0")])

    # Record Bot 1's hand to make sure they don't play anything
    bot1_cards_orig = unpack_cards(bot1.hand)

    # Call Bot 0, who plays Red Skip
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()
    # Check that the next player is Bot 1
    assert director.current_player() == bot1

    # Call Bot 1 who would not get to do anything
    director.call_the_player()
    director.handle_reverse()
    director.go_to_next_player()
    # Check that Bot 1 did not play or draw any cards
    assert unpack_cards(bot1.hand) == bot1_cards_orig

    # Check that the next player is Bot 2
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
    """
    Test that hypothetical user input for Wild card color choosing is processed
    properly.

    Arg:
        card: A wild Card instance to choose the color of.
        manual_input: A string representing a user input for color choosing.
        correct_color: A string representing what card.color should return if
            choosing is done properly.
    """
    game = GameState()
    user_player = UserPlayerTextController(game, "User")
    user_player.hand.insert(0, card)
    user_player.play_card(card,choose_manual_input=manual_input)

    assert game.current_color() == correct_color
    assert game.discard_pile.show_top().color == correct_color


win_testing_cases = [
    Card("Red", "0"),
    Card("Green", "Reverse"),
    Card("Blue", "Skip"),
    Card("Yellow", "+2"),
    Card("Wild", ""),
    Card("Wild", "+4")
]

@pytest.mark.parametrize("card", win_testing_cases)
def test_win_condition(card):
    """
    Check that a player playing their last card results in a win being flagged.

    Args:
        card: A Card instance that is the last/only card that a player plays to win.
    """
    game = GameState()
    player = BotPlayer(game, "Bot 0", play_card_delay=0)
    player.hand = [card]
    game.discard_pile = Deck(def_cards=[Card(player.hand[0].color, "0")])

    player.take_turn()
    assert game.won == True


def test_reuse_discard_pile():
    """
    Test the GameState.reuse_discard_pile() function.
    """
    # Start a game
    game = GameState()
    # Make the draw pile empty
    game.draw_pile = Deck(is_empty=True)
    # Make the discard pile full of cards
    game.discard_pile = Deck(def_cards=[pack_cards(normal_test_deck1)])
    # Record the old discard and draw pile sizes
    orig_discard_size = game.discard_pile.size()
    orig_draw_size = game.draw_pile.size()

    game.reuse_discard_pile()

    # Check sizes of the new draw and discard piles
    assert game.draw_pile.size() == orig_draw_size + orig_discard_size - 1
    assert game.discard_pile.size() == 1