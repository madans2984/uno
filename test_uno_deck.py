import pytest
from uno_deck import *

uno_card_creation_cases = [
    ("Red", "0"),
    ("Green", "Reverse"),
    ("Blue", "Skip"),
    ("Yellow", "+2"),
    ("Wild", ""),
    ("Wild", "+4"),
]

@pytest.mark.parametrize("color,symbol", uno_card_creation_cases)
def test_uno_card_creation(color, symbol):
    card = Card(color, symbol)
    assert card.color == color
    assert card.symbol == symbol
