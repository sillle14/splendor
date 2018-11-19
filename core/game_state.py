import random
from typing import List, Dict

from game_pieces import *
from player import Player
from static import CARDS


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
        self.display.sort()

    def __repr__(self):
        representation = "~~ SPLENDOR BOARD ~~\n\n"
        representation += f"Gems: {self.gems}\n\n"
        representation += f"Display:\n"
        for card in self.display:
            representation += f"{card.tier}: {card}\n"
        representation += "\n"
        for player in self.players:
            if player == self.cur_player: representation += "Current "
            representation += f"{player}\n\n"
        return representation

    def buy_card(self, player: Player, card: Card):
        self.remove_card(card)
        player.buy_card(card)
        self.gems.add_bundle(card.cost)

    def remove_card(self, card: Card):
        if (card not in self.display):
            raise ValueError("Card not in display")
        self.display.remove(card)
        tier = card.tier
        self.display.append(self.deck[tier].pop())

    def draw_gems(self, player: Player, gems: Bundle):
        self.gems.subtract_bundle(gems)
        player.draw_gems(gems)


    def get_display(self):
        return self.display

    def get_player(self, name: str):
        return self.players[self.player_names.index(name)]

    def get_cur_player(self):
        return self.cur_player

    def next_player(self):
        self.cur_player_idx = (self.cur_player_idx + 1) % len(self.players)
        self.cur_player = self.players[self.cur_player_idx]

    def is_game_over(self):
        for player in self.players:
            if player.score >= 15:
                return True
        return False

    def get_winner(self):
        for player in self.players:
            if player.score >= 15:
                return player
        return None



