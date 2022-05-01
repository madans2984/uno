from art import *

cards = "?"
PURPLE = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
GRAY = '\033[90m'
WHITE = '\033[0m'

styles=[BLUE, GREEN, YELLOW, RED, WHITE]

for i, c in enumerate(cards):
    Art = text2art(c, font='block')

    print(styles[i % len(styles)] + Art + WHITE)

# f= open('color_r.txt', 'r')
# letter = f.read()
# letter = letter.replace("W", WHITE)
# letter = letter.replace("C", PURPLE)
# print(letter)
# f.close()