import pickle
import random
import time
from typing import Tuple

import numpy as np
from tqdm import trange

from core.game_state import GameState


def sigmoid(x):
    # To avoid overflow.
    if x < -100:
        return 0
    return 1 / (1 + np.exp(-x))


sigmoid = np.vectorize(sigmoid)


def sigmoid_derivative(x):
    if abs(x) > 100:
        return 0
    return x * (1 - x)


sigmoid_derivative = np.vectorize(sigmoid_derivative)


class Weights(object):

    input_node_count = 100  # n
    hidden_node_count = 50  # m

    def __init__(self):
        self.W1 = 2 * np.random.random((self.hidden_node_count, self.input_node_count)) - 1  # m x n
        self.bias_1 = 2 * np.random.random((self.hidden_node_count, 1)) - 1  # m x 1

        self.W2 = 2 * np.random.random((1, self.hidden_node_count)) - 1  # 1 x m
        self.bias_2 = 2 * np.random.random((1, 1)) - 1  # 1 x 1


class Network(object):

    def __init__(self, new_weights=False):
        if new_weights:
            self.weights = Weights()
            self.save_weights()
        else:
            self.weights = self.load_weights()
        self.lambda_ = 0.9
        self.e_t_b2_previous = np.zeros((1, 1))  # 1 x 1
        self.e_t_W2_previous = np.zeros((1, self.weights.hidden_node_count))  # 1 x m
        self.e_t_b1_previous = np.zeros((self.weights.hidden_node_count, 1))  # m x 1
        self.e_t_W1_previous = np.zeros((self.weights.hidden_node_count, self.weights.input_node_count))  # m x n

    @staticmethod
    def alpha():
        return 10**(-random.randint(1, 3))

    def save_weights(self):
        with open("weights.pickle", "wb") as f:
            pickle.dump(self.weights, f)

    @staticmethod
    def load_weights() -> Weights:
        with open("weights.pickle", "rb") as f:
            return pickle.load(f)

    def feed_forward(self, input_array: np.array) -> float:
        # If the input is less than 100, it means a deck has run out of cards, so we can give a loss.
        if input_array.size < 100:
            return 0
        layer_1 = sigmoid(self.weights.W1 @ input_array + self.weights.bias_1)  # m x 1
        output = sigmoid(self.weights.W2 @ layer_1 + self.weights.bias_2)  # 1 x 1

        # Return the score of the move.
        return output[0][0]

    def back_propagate(self, current_input: np.array, next_score: float):

        alpha = self.alpha()

        # z_k is the pre sigmoid output of each layer.
        # v_k is the output of the kth layer.

        z_1 = self.weights.W1 @ current_input + self.weights.bias_1  # m x 1
        v_1 = sigmoid(z_1)  # m x 1
        z_2 = self.weights.W2 @ v_1 + self.weights.bias_2  # 1 x 1
        v_2 = sigmoid(z_2)  # 1 x 1

        current_score = v_2[0][0]

        # Here, we calculate the gradient of the result with respect to each param (biases, weights).
        gradient_b2 = sigmoid_derivative(z_2)  # 1 x 1
        gradient_W2 = sigmoid_derivative(z_2) @ v_1.T  # 1 x 1 @ (m x 1)^T = 1 x m (aka g_b2 @ v_1.T)
        # For below: m x 1 @ 1 x 1 * (element-wise) m x 1 = m x 1.
        gradient_b1 = self.weights.W2.T @ sigmoid_derivative(z_2) * sigmoid_derivative(z_1)
        gradient_W1 = gradient_b2 @ current_input.T  # m x 1 @ (n x 1)^T = m x n

        # Now, we need to calculate the eligibility trace.
        e_t_b2 = self.lambda_ * self.e_t_b2_previous + gradient_b2  # 1 x 1
        e_t_W2 = self.lambda_ * self.e_t_W2_previous + gradient_W2  # 1 x m
        e_t_b1 = self.lambda_ * self.e_t_b1_previous + gradient_b1  # m x 1
        e_t_W1 = self.lambda_ * self.e_t_W1_previous + gradient_W1  # m x n
        self.e_t_b2_previous = e_t_b2
        self.e_t_W2_previous = e_t_W2
        self.e_t_b1_previous = e_t_b1
        self.e_t_W1_previous = e_t_W1

        delta_t = next_score - current_score

        # Update weights.
        self.weights.bias_2 = self.weights.bias_2 + alpha * delta_t * e_t_b2
        self.weights.W2 = self.weights.W2 + alpha * delta_t * e_t_W2
        self.weights.bias_1 = self.weights.bias_1 + alpha * delta_t * e_t_b1
        self.weights.W1 = self.weights.W1 + alpha * delta_t * e_t_W1

    def take_turn(self, game_state: GameState) -> Tuple[GameState, int]:
        # First, we need to calculate the outcome of the next game states.
        possible_next_states, _ = game_state.get_possible_moves()
        next_scores = {self.feed_forward(state.to_1P_array()): state for state in possible_next_states}

        best_score = max(next_scores)
        next_score = best_score if (game_state.has_player_won() is None) else game_state.has_player_won()
        next_state = next_scores.get(best_score).copy()
        return next_state, next_score

    def run_game(self, game_state: GameState, game_id, debug=False):
        start_time = time.time()
        while not game_state.is_game_over():

            next_state, next_score = self.take_turn(game_state)
            # Back propagate for new weights.
            self.back_propagate(game_state.to_array(), next_score)
            game_state = next_state
            if debug:
                print(f"moved to state with score {best_score}")
        end_time = time.time()
        if debug:
            print(f"Game {game_id} ended with {game_state.has_player_won()}!"
                  f" Turns: {game_state.turns}, Time: {end_time-start_time}s")
        return game_state.has_player_won(), game_state.turns
        # self.save_weights()

    def run_epoch(self, length, debug=False):
        turns_per_game = []
        for i in trange(length, desc='Training...', unit='game', dynamic_ncols=True, smoothing=0):
            if i % 100 == 0 and i != 0:
                total = len(turns_per_game)
                avg = sum(turns_per_game) / total
                print(f"Games {i-100} to {i} ended with {total} wins in avg of {avg} turns per game.")
                self.save_weights()
                turns_per_game = []
            g = GameState(["Michael"])
            result = self.run_game(g, i, debug)
            if result[0]:
                turns_per_game.append(result[1])
        print("End of epoch")
