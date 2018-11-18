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
        self.player_names = player_names
        self.players = [Player(name) for name in player_names]

        self.cur_player_idx = 0
        self.cur_player = self.players[self.cur_player_idx]

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


    def remove_card(self, player: Player, card: Card):
        if (card not in self.display):
            raise ValueError("Card not in display")
        self.display.remove(card)
        tier = card.tier
        self.display.append(self.deck[tier].pop())

    def remove_gems(self, gems: Bundle):
        self.gems.subtract_bundle(gems)

    def add_gems(self, gems: Bundle):
        self.gems.add_bundle(gems)

    def get_display(self):
        return self.display

    def get_player(self, name: str):
        return self.players[self.player_names.index(name)]

    def get_cur_player(self):
        return self.cur_player

    def next_player(self):
        self.cur_player_idx = (self.cur_player_idx + 1) % len(self.players)
        self.cur_player = self.players[self.cur_player_idx]




