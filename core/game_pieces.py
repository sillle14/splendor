from __future__ import annotations

from enum import IntEnum
from typing import List, Optional, Dict


__all__ = ['Gem', 'Bundle', 'Card', 'Noble']


# The five types of gems in the game
class Gem(IntEnum):
    RED = 1  # Ruby #e0115f
    GREEN = 2  # Emerald #50c878
    BLUE = 3  # Sapphire #0f52ba
    WHITE = 4  # Diamond #b9f2ff
    BLACK = 5  # Onyx #696969
    # WILD = 6  # Gold #daa520 TODO


# A bundle of gems (one of the options for a turn)
class Bundle(object):

    def __init__(self,
                 gem_list: Optional[List[Gem]]=None,
                 bundle: Optional[Bundle]=None):
        self.gems = {}  # type: Dict[Gem, int]
        if gem_list:
            assert not bundle
            for name in gem_list:
                self.add(name)
        elif bundle:
            self.add_bundle(bundle)

    def __repr__(self):
        if len(self.gems) < 1:
            return 'Empty Bundle'
        else:
            representation = ''
            for gem, count in self.gems.items():
                representation += f"{count} {gem.name}(s); "
            return representation[:-2]
        
    def __eq__(self, other):
        if not set(self.gems.keys()) == set(other.gems.keys()):
            return False
        for gem, count in self.gems.items():
            if not count == other.gems.get(gem, 0):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def add(self, gem: Gem):
        self.add_multiple(gem, 1)

    def add_bundle(self, bundle: Bundle):
        for gem, count in bundle.gems.items():
            self.add_multiple(gem, count)

    def add_multiple(self, gem: Gem, count: int):
        assert count >= 0
        self.gems[gem] = self.gems.get(gem, 0)
        self.gems[gem] += count

    def amount(self, gem: Gem):
        return self.gems.get(gem, 0)

    def distinct_gems(self):
        return [gem for gem in self.gems if self.amount(gem) > 0]

    def subtract(self, gem: Gem):
        self.subtract_multiple(gem, 1)

    def subtract_bundle(self, bundle):
        for gem, count in bundle.gems.items():
            self.subtract_multiple(gem, count)

    def subtract_multiple(self, gem: Gem, count: int):
        assert count >= 0
        current_count = self.gems.get(gem, 0)
        if current_count < count:
            raise ValueError('Not enough gems to subtract.')
        elif count != 0:
            self.gems[gem] -= count

    def total(self):
        total = 0
        for _, count in self.gems.items():
            total += count
        return total

    def to_list(self):
        """Returns a list of integers representing this bundle to be used by the NN."""
        return [self.amount(gem) for gem in Gem]


class Card(object):

    def __init__(self,
                 tier: Optional[int]=None,  # 1, 2, or 3
                 gem: Optional[Gem]=None,  # which gem it gives you forever
                 cost: Optional[Bundle]=None,  # a bundle that makes up how many gems the card costs
                 points: Optional[int]=None, 
                 card: Optional[Card]=None): 
        if card:
            assert all([tier is None, gem is None, cost is None, points is None])
            self.tier = card.tier
            self.gem = card.gem
            self.cost = card.cost
            self.points = card.points
        else:
            assert not any([tier is None, gem is None, cost is None, points is None])
            self.tier = tier
            self.gem = gem
            self.cost = cost
            self.points = points

    def __repr__(self):

        return f"|*{self.points}* {self.gem.name}, Cost: {self.cost}|"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return all([
            self.tier == other.tier,
            self.gem == other.gem,
            self.cost == other.cost,
            self.points == other.points,
        ])

    def __lt__(self, other):
        return (self.tier, self.points) < (other.tier, other.points)

    def to_list(self):
        """Returns a list of integers representing this card to be read by the NN."""
        return self.cost.to_list() + [self.points] + [self.gem.value]


class Noble(object):
    def __init__(self,
                 cost: Optional[Bundle]=None,  # which cards the user must have in their tableau to gain the noble
                 noble: Optional[Noble]=None):
        self.points = 3  # all nobles are worth 3 points
        if noble:
            assert cost is None
            self.cost = noble.cost
        else:
            assert noble is None
            self.cost = cost

    def __repr__(self):
        return f"|{self.points}, Cost: {self.cost}|"

    def __eq__(self, other):
        if not isinstance(other, Noble):
            return False
        return all([
            self.cost == other.cost,
            self.points == other.points,
        ])
