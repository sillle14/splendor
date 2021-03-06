from core.game_pieces import *

CARDS = {
    'TIER_1': [
        Card(1, Gem.BLACK, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE]), 1),
        Card(1, Gem.BLACK, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN]), 0),
        Card(1, Gem.BLACK, Bundle([Gem.GREEN, Gem.GREEN, Gem.RED]), 0),
        Card(1, Gem.BLACK, Bundle([Gem.GREEN, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK]), 0),
        Card(1, Gem.BLACK, Bundle([Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.RED]), 0),
        Card(1, Gem.BLACK, Bundle([Gem.WHITE, Gem.BLUE, Gem.GREEN, Gem.RED]), 0),
        Card(1, Gem.BLACK, Bundle([Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.RED]), 0),
        Card(1, Gem.BLACK, Bundle([Gem.WHITE, Gem.WHITE, Gem.GREEN, Gem.GREEN]), 0),
        Card(1, Gem.BLUE, Bundle([Gem.BLACK, Gem.BLACK, Gem.BLACK]), 0),
        Card(1, Gem.BLUE, Bundle([Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED]), 0),
        Card(1, Gem.BLUE, Bundle([Gem.GREEN, Gem.GREEN, Gem.BLACK, Gem.BLACK]), 0),
        Card(1, Gem.BLUE, Bundle([Gem.RED, Gem.RED, Gem.RED, Gem.RED]), 1),
        Card(1, Gem.BLUE, Bundle([Gem.WHITE, Gem.BLACK, Gem.BLACK]), 0),
        Card(1, Gem.BLUE, Bundle([Gem.WHITE, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED]), 0),
        Card(1, Gem.BLUE, Bundle([Gem.WHITE, Gem.GREEN, Gem.RED, Gem.BLACK]), 0),
        Card(1, Gem.BLUE, Bundle([Gem.WHITE, Gem.GREEN, Gem.RED, Gem.RED, Gem.BLACK]), 0),
        Card(1, Gem.GREEN, Bundle([Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 1),
        Card(1, Gem.GREEN, Bundle([Gem.BLUE, Gem.BLUE, Gem.RED, Gem.RED]), 0),
        Card(1, Gem.GREEN, Bundle([Gem.BLUE, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK]), 0),
        Card(1, Gem.GREEN, Bundle([Gem.RED, Gem.RED, Gem.RED]), 0),
        Card(1, Gem.GREEN, Bundle([Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN]), 0),
        Card(1, Gem.GREEN, Bundle([Gem.WHITE, Gem.BLUE, Gem.RED, Gem.BLACK, Gem.BLACK]), 0),
        Card(1, Gem.GREEN, Bundle([Gem.WHITE, Gem.BLUE, Gem.RED, Gem.BLACK]), 0),
        Card(1, Gem.GREEN, Bundle([Gem.WHITE, Gem.WHITE, Gem.BLUE]), 0),
        Card(1, Gem.RED, Bundle([Gem.BLUE, Gem.BLUE, Gem.GREEN]), 0),
        Card(1, Gem.RED, Bundle([Gem.WHITE, Gem.BLUE, Gem.GREEN, Gem.BLACK]), 0),
        Card(1, Gem.RED, Bundle([Gem.WHITE, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 0),
        Card(1, Gem.RED, Bundle([Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.GREEN, Gem.BLACK]), 0),
        Card(1, Gem.RED, Bundle([Gem.WHITE, Gem.WHITE, Gem.GREEN, Gem.BLACK, Gem.BLACK]), 0),
        Card(1, Gem.RED, Bundle([Gem.WHITE, Gem.WHITE, Gem.RED, Gem.RED]), 0),
        Card(1, Gem.RED, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE]), 1),
        Card(1, Gem.RED, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE]), 0),
        Card(1, Gem.WHITE, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLACK, Gem.BLACK]), 0),
        Card(1, Gem.WHITE, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE]), 0),
        Card(1, Gem.WHITE, Bundle([Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.BLACK]), 0),
        Card(1, Gem.WHITE, Bundle([Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.BLACK]), 0),
        Card(1, Gem.WHITE, Bundle([Gem.BLUE, Gem.GREEN, Gem.RED, Gem.BLACK]), 0),
        Card(1, Gem.WHITE, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN]), 1),
        Card(1, Gem.WHITE, Bundle([Gem.RED, Gem.RED, Gem.BLACK]), 0),
        Card(1, Gem.WHITE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLACK]), 0),
    ],
    'TIER_2': [
        Card(2, Gem.BLACK, Bundle([Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 3),
        Card(2, Gem.BLACK, Bundle([Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 2),
        Card(2, Gem.BLACK, Bundle([Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED]), 2),
        Card(2, Gem.BLACK, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.RED]), 2),
        Card(2, Gem.BLACK, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN]), 1),
        Card(2, Gem.BLACK, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.BLACK, Gem.BLACK]), 1),
        Card(2, Gem.BLUE, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE]), 3),
        Card(2, Gem.BLUE, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE]), 2),
        Card(2, Gem.BLUE, Bundle([Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.RED]), 1),
        Card(2, Gem.BLUE, Bundle([Gem.WHITE, Gem.WHITE, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 2),
        Card(2, Gem.BLUE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE]), 2),
        Card(2, Gem.GREEN, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN]), 2),
        Card(2, Gem.GREEN, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN]), 3),
        Card(2, Gem.GREEN, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN]), 2),
        Card(2, Gem.GREEN, Bundle([Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLACK, Gem.BLACK]), 1),
        Card(2, Gem.GREEN, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED]), 1),
        Card(2, Gem.GREEN, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLACK]), 2),
        Card(2, Gem.RED, Bundle([Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 2),
        Card(2, Gem.RED, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 1),
        Card(2, Gem.RED, Bundle([Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED]), 3),
        Card(2, Gem.RED, Bundle([Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN]), 2),
        Card(2, Gem.RED, Bundle([Gem.WHITE, Gem.WHITE, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 1),
        Card(2, Gem.RED, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 2),
        Card(2, Gem.WHITE, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK]), 1),
        Card(2, Gem.WHITE, Bundle([Gem.GREEN, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK]), 2),
        Card(2, Gem.WHITE, Bundle([Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 2),
        Card(2, Gem.WHITE, Bundle([Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED]), 2),
        Card(2, Gem.WHITE, Bundle([Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.RED, Gem.RED, Gem.RED]), 1),
        Card(2, Gem.WHITE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE]), 3),
    ],
    'TIER_3': [
        Card(3, Gem.WHITE, Bundle([Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 4),
        Card(3, Gem.WHITE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 5),
        Card(3, Gem.WHITE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 4),
        Card(3, Gem.WHITE, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 3),
        Card(3, Gem.BLUE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE]), 4),
        Card(3, Gem.BLUE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE]), 5),
        Card(3, Gem.BLUE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 4),
        Card(3, Gem.BLUE, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 3),
        Card(3, Gem.GREEN, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE]), 4),
        Card(3, Gem.GREEN, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN]), 5),
        Card(3, Gem.GREEN, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN]), 4),
        Card(3, Gem.GREEN, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 3),
        Card(3, Gem.RED, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN]), 4),
        Card(3, Gem.RED, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.RED]), 5),
        Card(3, Gem.RED, Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.RED]), 4),
        Card(3, Gem.RED, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 3),
        Card(3, Gem.BLACK, Bundle([Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED]), 4),
        Card(3, Gem.BLACK, Bundle([Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 5),
        Card(3, Gem.BLACK, Bundle([Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.RED, Gem.BLACK, Gem.BLACK, Gem.BLACK]), 4),
        Card(3, Gem.BLACK, Bundle([Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.GREEN, Gem.RED, Gem.RED, Gem.RED]), 3),
    ]
}

NOBLES = [Noble(Bundle([Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.RED, Gem.RED, Gem.RED, Gem.GREEN, Gem.GREEN, Gem.GREEN])),
          Noble(Bundle([Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.BLACK, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE])),
          Noble(Bundle([Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.BLUE, Gem.WHITE, Gem.WHITE, Gem.WHITE, Gem.WHITE]))]







