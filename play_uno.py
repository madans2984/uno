"""
Main method for playing the uno game.
"""

import textwrap
from uno_game import GameState, GameDirector
from uno_controllers import UserPlayerTextController, BotPlayer
from uno_views import ColorTextView


def main():
    """
    Have the user play an UNO game against 3 computer opponents.
    """
    # Print the welcome message
    with open("welcome_message.txt", "r") as file:
        welcome_message = file.readlines()
    text = textwrap.TextWrapper(width=80, break_long_words=False,
                                replace_whitespace=False)
    print()
    for line in welcome_message:
        print(text.fill(line))
    print()

    # Initialize the GameState (contains draw pile, discard pile, and direction)
    game = GameState()

    # Initialize the players with their hands of 7 cards
    user_player = UserPlayerTextController(game, "User")
    bot1 = BotPlayer(game, "Bot 1")
    bot2 = BotPlayer(game, "Bot 2")
    bot3 = BotPlayer(game, "Bot 3")
    player_list = [user_player, bot1, bot2, bot3]

    # Initialize the viewer
    view = ColorTextView(player_list, game)

    # Intialize the GameDirector (handles reverses, determines who goes next)
    director = GameDirector(player_list, game)

    # Continue the game turn cycle until a player wins
    while game.won is False:
        # Display the game information (current card, the other players and how
        # many cards they have, and the user's hand if it's their turn)
        view.display(director.current_player())
        # Have the current player handle any card actions (skip, +2, +4), play
        # a card, or draw a card from the draw pile if they can't play anything
        director.call_the_player()
        # Check if a reverse was played, and if it was, then reverse the
        # direction attribute of game
        director.handle_reverse()
        # Use the game.direction and the player list to move to the next player
        director.go_to_next_player()


if __name__ == "__main__":
    main()
