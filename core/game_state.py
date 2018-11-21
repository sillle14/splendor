import random
from copy import deepcopy
from typing import List, Dict

from core.game_pieces import *
from core.player import Player
from core.static import CARDS

GEM_COUNT = 4
MAX_GEM_HAND_SIZE = 10


class InvalidMoveError(Exception):
    pass


class GameState(object):

    def __init__(self, player_names: List[str]):
        # Add players.
        assert len(player_names) <= 2
        self.player_names = player_names
        self.players = [Player(name) for name in player_names]

        self.cur_player_idx = 0
        self.cur_player = self.players[self.cur_player_idx]

        # Add gems.
        self.gems = Bundle()
        for gem in Gem:
            self.gems.add_multiple(gem, GEM_COUNT)

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
            if player == self.cur_player:
                representation += "Current "
            representation += f"{player}\n\n"
        return representation

    def get_possible_moves(self):
        """
        Gets all the moves that can be performed from this game state, as well as the resulting states.

        Returns:
            A list of all the possible GameStates
            A dict in the form {'buy': [list of cards that can be bought],
                                'take': [list of bundles that can be taken]}
        """
        states = []  # type: List[GameState]
        moves = {'buy': [], 'take': []}

        # Find all possible 3 gem draws.
        for gem_1 in Gem:
            for gem_2 in [gem for gem in Gem if (gem > gem_1)]:
                for gem_3 in [gem for gem in Gem if (gem > gem_2)]:
                    gems = Bundle(gem_list=[gem_1, gem_2, gem_3])
                    try:
                        new_state = deepcopy(self)  # TODO: We should implement our own copy method which copies the correct things
                        new_state.draw_gems(gems)
                        states.append(new_state)
                        moves['take'].append(gems)
                    except InvalidMoveError:
                        pass

        # Find all possible 2 gem draws.
        for gem in Gem:
            gems = Bundle(gem_list=[gem, gem])
            try:
                new_state = deepcopy(self)
                new_state.draw_gems(gems)
                states.append(new_state)
                moves['take'].append(gems)
            except InvalidMoveError:
                pass

        # Find all possible cards to buy.
        for card in self.display:
            try:
                new_state = deepcopy(self)
                new_state.buy_card(card)
                states.append(new_state)
                moves['buy'].append(card)
            except InvalidMoveError:
                pass

        return states, moves

    def to_array(self):
        """Converts the gamestate into an array which can be read by the NN."""
        pass

    # ===========
    #    MOVES
    # ===========

    def buy_card(self, card: Card, player: Player=None):
        """Buy a card on behalf of the given player. Uses the current player if none is given."""

        # Set the player if none is given.
        if not player:
            player = self.cur_player

        # Check that the card is available for purchase.
        if card not in self.display:
            raise InvalidMoveError('This card is not available to be bought.')

        # Buy the card for the player, if possible.
        try:
            self.gems.add_bundle(player.buy_card(card))
        except ValueError:
            raise InvalidMoveError('Player cannot afford this card.')
        self.remove_card(card)
        self.next_player()

    def draw_gems(self, gems: Bundle, player: Player=None):
        """Collect a given bundle of gems on behalf of the given player. Uses the current player if none is given."""

        # Set the player if none is given.
        if not player:
            player = self.cur_player

        # Check that it is allowed to take the given gems.
        if player.gems.total() + gems.total() > MAX_GEM_HAND_SIZE:
            raise InvalidMoveError('These gems will violate the handsize limit.')
        if gems.total() == 2:
            if len(gems.distinct_gems()) != 1:
                raise InvalidMoveError("Can't 2 gems of different colors.")
            if self.gems.amount(gems.distinct_gems()[0]) < 4:
                raise InvalidMoveError("Can't take 2 gems when there are less than 4 left in the supply.")
        elif gems.total() == 3:
            if len(gems.distinct_gems()) != 3:
                raise InvalidMoveError("Can't take three gems unless they are all different.")
        else:
            raise InvalidMoveError(f"Can't take a total of {gems.total()} gems.")

        # If we get to here, the move is valid, unless there are not enough gems in the supply.
        try:
            self.gems.subtract_bundle(gems)
        except ValueError:
            raise InvalidMoveError("Can't take these gems as there are not enough left in the supply.")
        player.draw_gems(gems)
        self.next_player()

    # =============
    #    HELPERS
    # =============

    def remove_card(self, card: Card):
        if card not in self.display:
            raise ValueError("Card not in display")
        self.display.remove(card)
        self.display.append(self.deck[f"TIER_{card.tier}"].pop())

    def next_player(self):
        self.cur_player_idx = (self.cur_player_idx + 1) % len(self.players)
        self.cur_player = self.players[self.cur_player_idx]

    def is_game_over(self):
        for player in self.players:
            if player.points >= 15 and self.cur_player_idx == 0:
                return True
        return False

    def get_winner(self):
        if self.is_game_over():
            return self.players.sort(key=lambda x: x.points, reverse=True)[0]
