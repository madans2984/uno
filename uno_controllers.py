"""
Classes representing human and computer uno players.
"""

import random
import time
from abc import ABC, abstractmethod


class Player(ABC):
    """
    An abstract representation of an uno player.

    Attributes:
        player_type: A class attribute representing the type of player
        (bot or user) as a string ("Bot" or "User").
        default_delay: A class attribute representing the default number of
            seconds a player should wait after playing their card before ending
            their turn, to make it easier to see what bots play. This is only
            used if play_card_delay is not defined when initializing the player.
        game: A GameState instance representing the uno game the player is in.
        name: A string representing the player's name.
        play_card_delay: a float representing the number of seconds the player
            should wait after playing their card before ending their turn.
    """
    player_type = None
    default_delay = None

    def __init__(self, game_state, player_name, play_card_delay=None):
        """
        The inherited method for initializing a Player instance.

        Args:
            game: A GameState instance representing the uno game the player is
                in.
            name: A string representing the player's name.
            hand: A list of Cards that the player has to play.
            play_card_delay: (optional) an float greater than 0 representing
                the number of seconds the player should wait after playing
                their card before turn, to make it easier to see what bots play.
        """
        self.game = game_state
        self.name = player_name
        self.hand = self.game.draw(7)
        self.play_card_delay = self.get_play_card_delay(play_card_delay)

    def take_turn(self):
        """
        Do the steps involved in this player's turn.
        """
        # Handle any outstanding actions
        if self.handle_action():
            # All player-handled actions ("Skip", "+2", "+4") involve missing
            # the player's turn, so if an action is handled, end the turn.
            return

        if self.can_play():
            # If the player has a card in their hand that can be played, have
            # them choose a card to play
            self.choose_card()
            # After playing the card, if they have no more cards, flag the game
            # as won and congratulate the winner
            if self.num_cards() == 0:
                self.game.won = True
                print(f"{self.name} won!")
        else:
            # If the player has no playable cards in their hand, announce this
            # and have them draw 1 card.
            print(f"No play possible - {self.name} draws 1 card.")
            self.draw(1)
            return

    def handle_action(self):
        """
        Handle any actions (like "Skip", "+2", "+4") created by the last player.

        Uses the current_action attribute of the game GameState instance, and
        resets it to None after an action is handled.

        Returns:
            True if an action was handled (the player should end their turn) or
            False if no action was handled (the player can continue).
        """
        if self.game.current_action == "Skip":
            print(f"{self.name} was skipped.")
            self.game.current_action = None
            return True

        if self.game.current_action == "+2":
            self.draw(2)
            print(f"{self.name} drew 2 cards and misses their turn.")
            self.game.current_action = None
            return True

        if self.game.current_action == "+4":
            self.draw(4)
            print(f"{self.name} drew 4 cards and misses their turn.")
            self.game.current_action = None
            return True

        return False

    def play_card(self, card, choose_manual_input=None):
        """
        Have the player play the specified card onto the top of the game's discard pile.

        Args:
            card: A Card instance the player has in their hand and will attempt
                to play.
            choose_manual_input: (optional, for testing) A string ("r", "g",
                "b", or "y") representing what color the player wants to
                declare the wild card to be if it is played. If the card is not
                a wild card, this is ignored.
        """
        if self.check_play(card):  # If the play is valid
            # Announce the played card
            print(f"{self.name} played {card}.")

            # If the card is Wild, allow the player to choose the color
            if card.color == "Wild":
                card = self.choose_color(card, choose_manual_input)

            # If the card is an action card, set the game's current_action to
            # the card's symbol
            if (card.symbol == "Reverse" or
                card.symbol == "Skip" or
                card.symbol == "+2" or
                    card.symbol == "+4"):
                self.game.current_action = card.symbol

            # Add the card to the top of the game's discard pile
            self.game.play_card(card)
            # Remove the card from the player's hand
            self.hand.remove(card)
            # Return True to indicate a sucessful play
            return True
        return False

    def check_play(self, card):
        """
        Determine if the card can be played now.

        Returns:
            True if the play is valid, False if it is not allowed.
        """
        if (card.color == self.game.current_card().color or
            card.symbol == self.game.current_card().symbol or
                card.color == "Wild"):
            return True
        return False

    def num_cards(self):
        """
        Return the number of cards the player has in their hand.
        """
        return len(self.hand)

    def draw(self, num_cards=1):
        """
        Draw cards from the game's draw_pile deck and add them to the player's
        hand.

        Args:
            num_cards: (optional) An int representing how many cards to draw
                from the deck, default is 1.
        """
        self.hand.extend(self.game.draw(num_cards))

    def can_play(self):
        """
        Determine if the player has at least 1 card in their hand that can be
        played this turn.

        Returns:
            True if the player has a card that can be played, False if they
            don't (and will need to draw a card and end their turn).
        """
        for card in self.hand:
            if self.check_play(card):
                return True
        return False

    def get_play_card_delay(self, delay):
        """
        Determine the players play_card_delay (the number of seconds the player
        will wait between playing a card and ending their turn).

        Args:
            delay: A float representing the number of seconds this player
                should wait every turn, or None if the delay wasn't specified
                when the instance was initialized and the subclass'
                default_delay should be used instead.

        Returns:
            A float representing the number of seconds this player should wait.
        """
        if delay is None:
            return self.default_delay
        return delay

    @abstractmethod
    def choose_card(self):
        """
        An abstract method for the player to choose the card they will play
        during a turn.
        """

    @abstractmethod
    def choose_color(self, card, manual_input=None):
        """
        An abstract method for the player to choose the color of their Wild
        card when they play one.

        Args:
            card: A "Wild" colored Card instance whose color should be chosen.
            manual_input: (optional, for testing) A string ("r", "g",
                "b", or "y") representing what color the player wants to
                declare the wild card to be.
        Returns:
            The card with the chosen_color changed to the player's choice.
        """

    def __repr__(self):
        return f"{self.__class__.__name__} player {self.name} with " \
            f"cards: {self.hand}"


class UserPlayerTextController(Player):
    """
    A representation of a user player using a command line interface,
    inheriting from the Player class.
    """
    player_type = "User"
    default_delay = 0

    def choose_card(self):
        """
        Get command line input from the user to let them choose the card they
        will play during a turn, and play that card if it is valid.
        """
        while True:
            try:
                index = int(
                    input(f"Enter the index of the card you want to play (1-{self.num_cards()}): "))
                if self.play_card(self.hand[int(index-1)]):
                    return
                print("Invalid play. Your card must match the color or the"
                      " symbol of the current card, \n"
                      "or be a Wild card. Please try again.")
            except (IndexError, ValueError):
                print(f"Invalid input. Please enter an integer between 1 and"
                      f" {self.num_cards()}.")

    def choose_color(self, card, manual_input=None):
        """
        Get command line input from the user to let them choose the color of
        their Wild card.

        Args:
            card: A "Wild" colored Card instance whose color should be chosen.
            manual_input: (optional, for testing) A string ("r", "g",
                "b", or "y") representing what color the player wants to
                declare the wild card to be.
        Returns:
            The card with the chosen_color changed to the player's choice.
        """
        while True:
            if manual_input is None:
                text = input("What color should the new card be?"
                             " (r/g/b/y): ")
            else:
                text = manual_input

            if text == "r":
                card.set_chosen_color("Red")
                return card
            elif text == "g":
                card.set_chosen_color("Green")
                return card
            elif text == "b":
                card.set_chosen_color("Blue")
                return card
            elif text == "y":
                card.set_chosen_color("Yellow")
                return card
            else:
                print("That is not a valid input. Please enter 'r' for"
                      " Red, 'g' for Green, 'b' for Blue, or 'y' for"
                      " Yellow.")


class BotPlayer(Player):
    """
    A representation of a bot player, inheriting from the Player class.
    """
    player_type = "Bot"
    default_delay = 1

    def choose_card(self):
        """
        Have the bot player play the first card in their hand that is a valid
        play.
        """
        for card in self.hand:
            if self.play_card(card):
                if self.play_card_delay > 0:
                    time.sleep(self.play_card_delay)
                return

    def choose_color(self, card, manual_input=None):
        """
        Get command line input from the user to let them choose the color of
        their Wild card.

        Args:
            card: A "Wild" colored Card instance whose color should be chosen.
            manual_input: This is for testing the UserPlayerTextController
                interface, and is not used here.
        Returns:
            The card with the chosen_color changed to the player's choice.
        """
        card.set_chosen_color(random.choice(
            ["Red", "Blue", "Green", "Yellow"]))
        print(f"{self.name} chose {card.color}.")
        return card
