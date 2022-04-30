"""
Varibles holding string list representations of cards.
"""
symbol_reps = { "0": "０",
                "1": "１",
                "2": "２",
                "3": "３",
                "4": "４",
                "5": "５",
                "6": "６",
                "7": "７",
                "8": "８",
                "9" :"９",
                "Reverse": "\u27F2 ",
                "Skip": "Ｘ",
                "": "\u2B56 ", # Wild
                "+2": "+2",
                "+4": "+4" }

def put_in_card(symbol):
    card = [" ____ ",
            "|    |",
            "|    |",
            "|____|"]
    
    symbol_rep = symbol_reps[symbol]
    card[2] = "| " + symbol_rep + " |"
    return card

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
card2 = put_in_card("Reverse")
card3 = put_in_card("Skip")
card4 = put_in_card("")

print_cards([card1,card2,card3,card4])
