import random
from typing import List, Dict

from game_state import GameState
from game_pieces import *

### Implements the Game Logic for Splendor ###

newGame = GameState(["Michael","Lewis"])

print(newGame)
newGame.draw_gems(newGame.get_cur_player(), Bundle([Gem.WHITE, Gem.BLACK, Gem.GREEN]))
print(newGame)
