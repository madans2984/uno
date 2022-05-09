# UNO

This is a repository housing Shree and Jules's, final SoftDes project, a virtual version of **UNO**.

## Game Overview
The goal of the game is to get rid of your hand first and it's played against three CPU players. We have most of the same rules as UNO with a few notable differences. The two key difference are special cards cannot be stacked to create a cumulative effect and there is no rule about calling out UNO when you have one card left.

## Installation and setup
To run the game, the only thing required is a python installation. The game itself operates with the command line interface so no additional packages are required for visualizations.

While not required to run the game, the test framework uses pytest, which can be installed by running `$ pip install pytest`.

## File Structure
The file structure consists of the following `.py` files:
* `play_uno.py`: Run this to play the game!
* `uno_controllers.py`: Varibles holding string list representations of cards.
* `uno_deck.py`: Classes representing uno cards and a deck of uno cards.
* `uno_game.py`: Classes representing the uno game state and the game director.
* `uno_views.py`: Classes representing viewing modes for the uno game.
* `uno_text_view_helpers.py`: Varibles holding string list representations of cards.

### Static files

The /ascii images folder has the files for the card graphics. This path is hard-coded so those specific files must be in that folder. If you're downloading straight from the repo, you shouldn't run into any issues.
