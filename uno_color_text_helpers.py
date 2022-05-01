"""
Varibles holding string list representations of cards.
"""

WHITE = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
PURPLE = '\033[95m'
GRAY = '\033[90m'

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
                "": (WHITE+"\u2B56 "+BLUE), # Wild
                "+2": "+2",
                "+4": (WHITE+"+4"+BLUE) }

color_reps = {
    "Red": RED,
    "Green": GREEN,
    "Blue": BLUE,
    "Yellow": YELLOW,
}

big_card_files = {"0": "color_zero.txt",
                    "1": "color_one.txt",
                    "2": "color_two.txt",
                    "3": "color_three.txt",
                    "4": "color_four.txt",
                    "5": "color_five.txt",
                    "6": "color_six.txt",
                    "7": "color_seven.txt",
                    "8": "color_eight.txt",
                    "9" : "color_nine.txt",
                    "Reverse": "color_reverse.txt",
                    "Skip": "color_skip.txt",
                    "": "color_wild.txt", # Wild
                    "+2": "color_d2.txt",
                    "+4": "color_d4.txt" }

def put_in_card(symbol):
    card = [" ____ ",
            "|    |",
            "|    |",
            "|____|"]
    symbol_rep = symbol_reps[symbol]
    card[2] = "| " + symbol_rep + " |"
    return card

def get_big_card(symbol):
    filename = "ascii images/" + big_card_files[symbol]
    with open(filename, "r") as file:
        card = file.readlines()
    for line_num in range(len(card)):
        card[line_num] = card[line_num].strip("\n")
    return card

def color_card_rep(card_rep, color):
    if color == "Wild":
        row_num = 0
        while True:
            for color_key in color_reps:
                card_rep[row_num] = color_reps[color_key] + card_rep[row_num] +WHITE
                row_num += 1
                if (row_num >= len(card_rep)):
                    return card_rep
        return card_rep
    else:
        for row_num in range(len(card_rep)):
            card_rep[row_num] = color_reps[color] + card_rep[row_num] + WHITE
        return card_rep

def print_cards(card_list):
    print_rows = []
    num_rows = len(card_list[0])
    for i in range(num_rows):
        new_row = ""
        for card in card_list:
            new_row = new_row + card[i]
        print_rows.append(new_row)

    for row in print_rows:
        print(row)


card1 = put_in_card("0")
card1 = color_card_rep(card1, "Red")
card2 = put_in_card("Reverse")
card3 = put_in_card("Skip")
card4 = put_in_card("")
card4 = color_card_rep(card4, "Wild")
card5 = put_in_card("+4")
card5 = color_card_rep(card5, "Wild")

print_cards([card1,card2,card3,card4,card5])

big_card = get_big_card("")
big_card = color_card_rep(big_card, "Wild")
# print(big_card)
print_cards([big_card])