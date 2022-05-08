"""
Main method for playing the uno game.
"""

from uno_game import GameState, GameDirector
from uno_controllers import UserPlayerTextController, BotPlayer
from uno_views import TextView, ColorTextView
import textwrap

welcome_message = (
    "\nWelcome to UNO! In this game, each player is dealt seven cards with the gameplay goal being the first to get rid of all of your cards. Each player attempts to match the card in the Discard Pile by the symbol, color, or using a Wild card to change the color of the pile. An example would be if the Discard Pile has a 'Red 0' then players can play either a red card or a 0. If the player was to put down a Wild card they can choose the current color in play. If a player cannot play any cards, they draw one from the pile and it moves to the next person's turn. \n \n"
    "We made two main modifications to our game rules compared to how UNO is typically played. First, we don't have a rule where you need to call UNO once you have your last card. Additionally we decided that special cards cannot be stacked meaning that there would be no cumulative effect for them. \n \n"
    "The big card in the middle of the screen is the current top card and the smaller cards below it are the cards you are able to play. Next to the large card is a graphic which will tell you the current order for the gameplay. To play a card, enter the index of the card (listed below it). \n"
    )

def main():
    tw = textwrap.TextWrapper(width=80,break_long_words=False,replace_whitespace=False)
    print(tw.fill(welcome_message))
    print()
    
    game = GameState()

    user_player = UserPlayerTextController(game, "User", "User")
    bot0 = BotPlayer(game, "Bot 0", "Bot")
    bot1 = BotPlayer(game, "Bot 1", "Bot")
    bot2 = BotPlayer(game, "Bot 2", "Bot")
    bot3 = BotPlayer(game, "Bot 3", "Bot")
    player_list = [user_player, bot1, bot2, bot3]

    view = ColorTextView(player_list, game)
    director = GameDirector(player_list, game)

    while game.won is False:
        view.display(director.current_player())
        director.call_the_player()
        director.handle_reverse()
        director.go_to_next_player()


if __name__ == "__main__":
    main()
