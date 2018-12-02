from __future__ import annotations

import random
from copy import deepcopy
from typing import List, Dict, Optional, Tuple

import numpy as np

from core.game_pieces import *
from core.player import Player
from core.static import CARDS

GEM_COUNT = 4
MAX_GEM_HAND_SIZE = 20
WINNING_SCORE = 12


class InvalidMoveError(Exception):
    pass


class GameState(object):

    def __init__(self, player_names: List[str]=None):
        if player_names:
            # Add players.
            assert len(player_names) <= 2
            self.turns = 0
            self.player_names = player_names
            self.players = [Player(name) for name in player_names]

            self.cur_player_idx = 0
            self.cur_player = self.players[self.cur_player_idx]
            self.cur_player.my_turn = True

            # Add gems.
            self.gems = Bundle()
            for gem in Gem:
                self.gems.add_multiple(gem, GEM_COUNT)

            # Add cards.
            self.deck = {}  # type: Dict[str, List[Card]]
            for tier, cards in deepcopy(CARDS).items():
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
        representation += str(len(self.to_array()))
        return representation

    def copy(self) -> GameState:
        """Copies the GameState in a safe way without duplicating everything."""
        new_state = GameState()

        # Copy players.
        new_state.players = deepcopy(self.players)  # Deep copy the player list because making a move changes players
        new_state.turns = self.turns
        new_state.cur_player_idx = self.cur_player_idx
        new_state.cur_player = new_state.players[new_state.cur_player_idx]
        new_state.cur_player.my_turn = True

        # Copy gems.
        new_state.gems = Bundle(gem_list=None, bundle=self.gems)

        # Copy the cards. Here we want a new dictionary, with new lists in it, but the same cards in those lists. So, we
        #  want to shallow copy the lists.
        new_state.deck = {'TIER_1': list(self.deck['TIER_1']),
                          'TIER_2': list(self.deck['TIER_2']),
                          'TIER_3': list(self.deck['TIER_3'])}

        new_state.display = list(self.display)  # Also shallow copy this list

        return new_state

    def get_possible_moves(self) -> Tuple[List[GameState], Dict[str, List[any]]]:
        """
        Gets all the moves that can be performed from this game state, as well as the resulting states.

        Returns:
            A list of all the possible GameStates
            A dict in the form {'buy': [list of cards that can be bought],
                                'take': [list of bundles that can be taken]}
        """
        states = []  # type: List[GameState]
        moves = {'buy': [], 'take': [], 'pass': False}

        # Find all possible 3 gem draws.
        for gem_1 in Gem:
            for gem_2 in [gem for gem in Gem if (gem > gem_1)]:
                for gem_3 in [gem for gem in Gem if (gem > gem_2)]:
                    gems = Bundle(gem_list=[gem_1, gem_2, gem_3])
                    if self.cur_player.gems.total() >= 8:
                        gems.subtract(gem_2)
                    if self.cur_player.gems.total() >= 9:
                        gems.subtract(gem_3)
                    try:
                        new_state = self.copy()
                        new_state.draw_gems(gems)
                        states.append(new_state)
                        moves['take'].append(gems)
                    except InvalidMoveError:
                        pass

        # Find all possible 2 gem draws.
        for gem in Gem:
            gems = Bundle(gem_list=[gem, gem])
            try:
                new_state = self.copy()
                new_state.draw_gems(gems)
                states.append(new_state)
                moves['take'].append(gems)
            except InvalidMoveError:
                pass

        # Find all possible cards to buy.
        for card in self.display:
            try:
                new_state = self.copy()
                new_state.buy_card(card)
                states.append(new_state)
                moves['buy'].append(card)
            except InvalidMoveError:
                pass
        
        # Add a pass only in the case no moves are possible. TODO: it will get stuck here, we need to change this.
        if len(states) == 0:
            new_state = self.copy()
            new_state.pass_turn()
            states.append(new_state)
            moves['pass'] = True

        return states, moves

    def to_array(self) -> np.array:
        """Converts the GameState into an array which can be read by the NN. (100 Nodes)"""
        # Nodes for the GameState gems:
        game_state_gems = self.gems.to_list()

        # Nodes for the GameState display cards:
        game_state_cards = [card.to_list() for card in self.display]  # List of lists
        # Flatten.
        game_state_cards = [item for sublist in game_state_cards for item in sublist]

        # Nodes for each player:
        players = [player.to_list() for player in self.players]  # List of lists
        # Flatten.
        players = [item for sublist in players for item in sublist]

        # Return as a column vector.
        return np.array(game_state_gems + game_state_cards + players, ndmin=2).T

    def to_1P_array(self) -> np.array:
        """Only for 1 player (doesn't include other players' hands"""
        # Nodes for the GameState gems:
        game_state_gems = self.gems.to_list()

        # Nodes for the GameState display cards:
        game_state_cards = [card.to_list() for card in self.display]  # List of lists
        # Flatten.
        game_state_cards = [item for sublist in game_state_cards for item in sublist]

        # Nodes for each player:
        players = [self.cur_player.to_list()]  # List of lists
        # Flatten.
        players = [item for sublist in players for item in sublist]

        # Return as a column vector.
        return np.array(game_state_gems + game_state_cards + players, ndmin=2).T

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
        if gems.total() == 2 and len(gems.distinct_gems()) == 1:
            if self.gems.amount(gems.distinct_gems()[0]) < 4:
                raise InvalidMoveError("Can't take 2 gems when there are less than 4 left in the supply.")
        elif gems.total() == 3:
            if len(gems.distinct_gems()) != 3:
                raise InvalidMoveError("Can't take three gems unless they are all different.")
        elif gems.total() > 3:
            raise InvalidMoveError(f"Can't take a total of {gems.total()} gems.")

        # If we get to here, the move is valid, unless there are not enough gems in the supply.
        try:
            self.gems.subtract_bundle(gems)
        except ValueError:
            raise InvalidMoveError("Can't take these gems as there are not enough left in the supply.")
        player.draw_gems(gems)
        self.next_player()
    
    def pass_turn(self):
        self.next_player()

    # =============
    #    HELPERS
    # =============

    # TODO: handle empty decks.
    def remove_card(self, card: Card):
        if card not in self.display:
            raise ValueError("Card not in display")
        self.display.remove(card)
        try:
            self.display.append(self.deck[f"TIER_{card.tier}"].pop())
        except IndexError:
            pass
            # print(f"Ran out of cards to draw in Tier{card.tier}")
        self.display.sort()

    def next_player(self):
        self.cur_player.my_turn = False
        self.cur_player_idx = (self.cur_player_idx + 1) % len(self.players)
        self.cur_player = self.players[self.cur_player_idx]
        self.cur_player.my_turn = True
        if self.cur_player_idx == 0:
            self.turns += 1

    def is_game_over(self) -> bool:
        """Checks for player score, cards in deck, and number of turns."""
        for player in self.players:
            if player.points >= WINNING_SCORE and self.cur_player_idx == 0:
                return True
        # If cards ran out in a pile, we call the game over for now. TODO
        if len(self.display) < 12:
            return True
        # If the game takes too long, we call it over.
        if self.turns > 100:
            return True
        return False

    def has_player_won(self) -> Optional[int]:
        """Checks if the player has won in the one player case."""
        if self.is_game_over():
            if len(self.display) < 12:
                return 0
            if self.turns > 100:
                return 0
            return 1
        return None

    def get_winner(self) -> Player:
        if self.is_game_over() and self.has_player_won():
            return self.players.sort(key=lambda x: x.points, reverse=True)[0]

    def get_reward(self) -> int:
        if self.is_game_over():
            return 100
            # if self.get_winner() == self.cur_player:
            #     return 100
        return 0
