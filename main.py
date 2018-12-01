from core.network import Network
from core.game_state import GameState

# print("hello")
n = Network()

g1 = GameState(["Michael"])

n.run_epoch(1000)

