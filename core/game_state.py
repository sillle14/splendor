import random
from typing import List, Dict

from core.game_pieces import *
from core.player import Player
from core.static import CARDS


class GameState(object):

    GEM_COUNT = 4
    MAX_GEM_HAND_SIZE = 10

    def __init__(self, player_names: List[str]):
        # Add players.
        assert len(player_names) == 2
        self.players = [Player(name) for name in player_names]

        # Add gems.
        self.gems = Bundle()
        for gem in Gem:
            self.gems.add_multiple(gem, self.GEM_COUNT)

        # Add cards.
        self.deck = {}  # type: Dict[str, List[Card]]
        for tier, cards in CARDS.items():
            self.deck[tier] = cards
            random.shuffle(self.deck[tier])

        # Display cards.
        self.display = []  # type: List[Card]
        for _ in range(4):
            for tier in self.deck:
                self.display.append(self.deck[tier].pop())


