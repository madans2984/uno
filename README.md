# UNO

This is a repository housing Shree and Jules's, final SoftDes project, a virtual version of **UNO**.

## Game Overview
The goal of the game is to get rid of your cards first and it's played against three CPU players. We have most of the same rules as UNO with a few notable differences. The two key difference are special cards cannot be stacked to create a cumulative effect and there is no rule about calling out UNO when you have one card left. See full rules [here](https://olincollege.github.io/uno/game-overview.html)

## Installation and setup
To run the game, the only thing required is a python installation. The game itself operates with the command line interface so no additional packages are required for visualizations.

While not required to run the game, the test framework uses pytest, which can be installed by running `$ pip install pytest`.

## File Structure
The primary file structure consists of the following `.py` files:
* `play_uno.py`: Run this to play the game!
* `uno_controllers.py`: Classes representing human and computer uno players.
* `uno_deck.py`: Classes representing uno cards and a deck of uno cards.
* `uno_game.py`: Classes representing the uno game state and the game director.
* `uno_views.py`: Classes representing viewing modes for the uno game.
* `uno_text_view_helpers.py`: Varibles holding string list representations of cards.

The following files are for testing purposes:
* `test_uno.py`: Test all aspects of the uno game, across all files and classes, using pytest.
* `testing_deck.py`: Sample decks (unpacked, i.e. represented as lists of lists, for easy copying and comparison) that can be used by test_uno.py after being re-packed by testing_helpers.pack_deck().
* `testing_helpers.py`: Helper functions for unit testing.

### Static files

The /ascii images folder has the files for the card graphics. This path is hard-coded so those specific files must be in that folder. If you're downloading straight from the repo, you shouldn't run into any issues.
