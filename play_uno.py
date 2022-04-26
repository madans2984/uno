from uno_game import GameState, GameDirector
from uno_controllers import UserPlayerTextController, BotPlayer
from uno_views import TextView

def main():
    game = GameState()
    user_player = UserPlayerTextController(game, "User")
    bot1 = BotPlayer(game, "Bot1")
    bot2 = BotPlayer(game, "Bot2")
    bot3 = BotPlayer(game, "Bot3")
    view = TextView([user_player, bot1, bot2, bot3], game)
    director = GameDirector([user_player, bot1, bot2, bot3], game)

    for _ in range(12):
        view.display(director.current_player())
        director.call_the_player()
        director.go_to_next_player()


if __name__ == "__main__":
    main()