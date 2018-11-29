import pickle
import time
from typing import List, Optional, Dict

import numpy as np

from core.game_state import GameState


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


class Weights(object):

    input_node_count = 100  # n
    hidden_node_count = 20  # m

    def __init__(self):
        np.random.seed(1)

        self.W1 = 2 * np.random.random((self.hidden_node_count, self.input_node_count)) - 1
        self.bias_1 = 2 * np.random.random((self.hidden_node_count)) - 1

        self.W2 = 2 * np.random.random((1, self.hidden_node_count)) - 1
        self.bias_2 = 2 * np.random.random((1)) - 1


class Network(object):

    def __init__(self, newWeights=False):
        if newWeights:
            self.weights = Weights()
            self.saveWeights()
        else:
            self.weights = self.loadWeights()
        self.alpha = 0.5
        self.lambda_ = 0.7
        self.e_t_previous = 0  # TODO this is actually a vector of 0s for each param

    def saveWeights(self):
        with open("weights.pickle", "wb") as f:
            pickle.dump(self.weights, f)

    def loadWeights(self):
        with open("weights.pickle", "rb") as f:
            return pickle.load(f)

    def feed_forward(self, input_array: np.array):
        temp_1 = np.dot(self.weights.W1, input_array)
        temp_2 = temp_1 + self.weights.bias_1
        layer_1 = sigmoid(temp_2)
        output = sigmoid(np.dot(self.weights.W2, layer_1) + self.weights.bias_2)

        # Return the score of the move.
        return output[0]

    def back_propagate(self, current_score: int, next_scores: List[int], done: bool):
        # This is assuming there is just one player so if the game is over then they have won.
        next_score = max(next_scores) if (not done) else 1
        delta_t = next_score - current_score

        # Here, we calculate the gradient of the result with respect to each param (biases, weights)
        gradient = 3

        # Now, we need to calculate the eligibility trace.
        e_t = self.lambda_ * self.e_t_previous + gradient
        self.e_t_previous = e_t

        # Finally, we update each weight.
        # new_weights = old_weights + self.alpha * delta_t * e_t

        # update weights 

        self.weights.W1 = self.weights.W1 + self.alpha * delta_t * e_t
        self.weights.W2 = self.weights.W2 + self.alpha * delta_t * e_t

    def run_game(self, game_state: GameState, debug=False):
        start_time = time.time()
        while not game_state.is_game_over():
            # First, we need to calculate the outcome of the next game state.
            possible_next_states, possible_next_moves = game_state.get_possible_moves()
            current_score = self.feed_forward(game_state.to_array())
            next_scores = [self.feed_forward(state.to_array()) for state in possible_next_states]
            # get arg_max of best next state and choose it
            best_score_idx = np.argmax(next_scores)
            next_state = possible_next_states[best_score_idx].copy()
            # back propogate for new weights
            self.back_propagate(current_score, next_scores, game_state.is_game_over())
            game_state = next_state
            if debug:
                print("next move: " + possible_next_moves[best_score_idx])
        end_time = time.time()
        print(f'Game ended! Turns: {game_state.turns}, Time: {end_time-start_time}s')

    def run_epoch(self, length, debug=False):
        for i in range(length):
            g = GameState(["Michael"])
            self.run_game(g, debug)
        print("End of epoch")


        

    





