from uno_game import GameState, GameDirector
from uno_controllers import UserPlayerTextController, BotPlayer
from uno_views import TextView, ColorTextView

def main():
    game = GameState()
    user_player = UserPlayerTextController(game, "User", "User")
    bot1 = BotPlayer(game, "Bot 1", "Bot")
    bot2 = BotPlayer(game, "Bot 2", "Bot")
    bot3 = BotPlayer(game, "Bot 3", "Bot")
    view = ColorTextView([user_player, bot1, bot2, bot3], game)
    director = GameDirector([user_player, bot1, bot2, bot3], game)

    while game.won is False:
        view.display(director.current_player(), always_show_card_count=True, show_bot_hands=True)
        # view.display_other_players_and_current_card()
        director.call_the_player()
        director.handle_reverse()
        director.go_to_next_player()


if __name__ == "__main__":
    main()
