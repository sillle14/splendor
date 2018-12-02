from __future__ import annotations

from typing import Optional

from core.game_pieces import Bundle, Card


class Player(object):

    def __init__(self, name: Optional[str]=None, player: Optional[Player]=None):
        if name:
            assert not player
            self.name = name
            self.gems = Bundle()
            self.tableau = Bundle()
            self.tableau_cards = []  # type: List[Card]
            # self.reserves = []  # type: List[Card]  TODO
            self.points = 0
            self.my_turn = False
        else:
            assert player
            self.name = player.name
            self.gems = player.gems
            self.tableau = player.tableau
            self.tableau_cards = []  # type: List[Card]
            # self.reserves = player.reserves  TODO
            self.points = player.points
            self.my_turn = player.my_turn

    def __repr__(self):
        return f"Player {self.name}\nPoints: {self.points}\nTableau: {self.tableau}\nGems: {self.gems}"

    def draw_gems(self, new_gems: Bundle):
        self.gems.add_bundle(new_gems)

    def add_card(self, card: Card):
        self.points += card.points
        self.tableau.add(card.gem)
        self.tableau_cards.append(card)

    def buy_card(self, card: Card):
        """Buys a card for the player. Returns the gems spent."""
        spent_gems = Bundle()
        for gem, count in card.cost.gems.items():
            real_cost = max(count - self.tableau.amount(gem),0)
            if self.gems.amount(gem) < real_cost:
                raise ValueError('Not enough gems to buy this card')
            else:
                spent_gems.add_multiple(gem, real_cost)
        self.add_card(card)
        self.gems.subtract_bundle(spent_gems)
        return spent_gems

    def to_list(self):
        """Returns a list of integers to be read by the NN."""
        return self.tableau.to_list() + self.gems.to_list() + [self.points / 12]
