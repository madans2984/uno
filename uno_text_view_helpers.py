"""
Varibles holding string list representations of cards.
"""

# Define useful colors
WHITE = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"

# Define the symbol representations for cards in the hand
symbol_reps = { "0": "０",
                "1": "１",
                "2": "２",
                "3": "３",
                "4": "４",
                "5": "５",
                "6": "６",
                "7": "７",
                "8": "８",
                "9": "９",
                "Reverse": "\u27F2 ",
                "Skip": "Ｘ",
                "": (WHITE+"  "+BLUE), # Wild
                "+2": "+2",
                "+4": (WHITE+"+4"+BLUE) }

# Define the colors used for each card color
color_reps = {
    "Red": RED,
    "Green": GREEN,
    "Blue": BLUE,
    "Yellow": YELLOW,
}

# Define the locations of the ascii art for the big cards / representations of
# the current card
big_card_files = {"0": "zero.txt",
                    "1": "one.txt",
                    "2": "two.txt",
                    "3": "three.txt",
                    "4": "four.txt",
                    "5": "five.txt",
                    "6": "six.txt",
                    "7": "seven.txt",
                    "8": "eight.txt",
                    "9" : "nine.txt",
                    "Reverse": "reverse.txt",
                    "Skip": "skip.txt",
                    "": "wild_blank.txt", # Wild
                    "+2": "d2.txt",
                    "+4": "d4.txt" }

def put_in_card(symbol):
    """
    Return the small/hand card representation of the given symbol.

    Args:
        symbol: A string representing the a symbol on an uno card (as it
            appears in the Card object).
    Returns:
        A list of strings representing even rows of ascii art.
    """
    card = [" ____ ",
            "|    |",
            "|    |",
            "|____|"]
    symbol_rep = symbol_reps[symbol]
    card[2] = "| " + symbol_rep + " |"
    return card

def get_big_card(symbol):
    """
    Return the big/current card representation of the given symbol.

    Args:
        symbol: A string representing the a symbol on an uno card (as it
            appears in the Card object).
    Returns:
        A list of strings representing even rows of ascii art.
    """
    # Pull the filepath from the dictionary
    filename = "ascii images/" + big_card_files[symbol]
    # Get each line of the file as a string in a list
    with open(filename, "r") as file:
        card = file.readlines()
    # Strip off the newlines
    for line_num in range(len(card)):
        card[line_num] = card[line_num].strip("\n")
    return card

def color_card_rep(card_rep, color):
    """
    Color the card representation by adding color escape codes to the beginning
    and end of each string in the list.

    Args:
        color: A string representing the the color of an uno card (as it
            appears in the Card object).
    Returns:
        A list of strings representing even rows of ascii art with color escape
        codes.
    """
    if color == "Wild":
        row_num = 0
        while True:
            for color_key in color_reps:
                card_rep[row_num] = (color_reps[color_key] +
                                        card_rep[row_num] + WHITE)
                row_num += 1
                if row_num >= len(card_rep):
                    return card_rep
    else:
        for row_num in range(len(card_rep)):
            card_rep[row_num] = color_reps[color] + card_rep[row_num] + WHITE
        return card_rep

def print_cards(card_list):
    """
    Print a list of card representations side by side to the terminal.

    Args:
        card_list: A list of lists of strings, where each sublist represents a
            card. All of the sublists must be the same length and all of the
            strings in a sublist are the same length.
    """
    print_rows = []
    num_rows = len(card_list[0])
    for i in range(num_rows):
        new_row = ""
        for card in card_list:
            new_row = new_row + card[i]
        print_rows.append(new_row)

    for row in print_rows:
        print(row)

def other_players_as_big_card(players_rep):
    """
    Add more blank lines to the top and bottom of a list of strings in order to
    make it the same size as a big card.

    This is used for displaying the current card and player diamond next to each other.
    """
    big_card_lines = 11
    big_card_players_rep = []
    blank_line = " " * 21
    space = " "*6
    while len(big_card_players_rep) < (big_card_lines - len(players_rep))/2:
        big_card_players_rep.append(blank_line)

    for line in players_rep:
        big_card_players_rep.append(space+line)

    while len(big_card_players_rep) < big_card_lines:
        big_card_players_rep.append(blank_line)

    return big_card_players_rep
