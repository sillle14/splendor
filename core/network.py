import numpy as np

from core.game_state import GameState


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


class Network(object):

    input_node_count = 3  # n
    hidden_node_count = 5  # m

    def __init__(self):
        np.random.seed(1)

        self.W1 = 2 * np.random.random((self.hidden_node_count, self.input_node_count)) - 1
        self.bias_1 = 2 * np.random.random((self.hidden_node_count, 1)) - 1

        self.W2 = 2 * np.random.random((1, self.hidden_node_count)) - 1
        self.bias_2 = 2 * np.random.random((1, 1)) - 1

        self.alpha = 0.5
        self.lambda_ = 0.7
        self.e_t_previous = 0  # TODO this is actually a vector of 0s for each param

    def feed_forward(self, input_array: np.array):
        layer_1 = sigmoid(np.dot(self.W1, input_array) + self.bias_1)
        output = sigmoid(np.dot(self.W2, layer_1) + self.bias_2)

        # Return the score of the move.
        return output[0]

    def back_propagate(self, game_state: GameState):
        # First, we need to calculate the outcome of the next game state.
        possible_next_states, _ = game_state.get_possible_moves()
        scores = [self.feed_forward(state.to_array()) for state in possible_next_states]
        # This is assuming there is just one player so if the game is over then they have won.
        next_score = max(scores) if not game_state.is_game_over() else 1
        current_score = self.feed_forward(game_state.to_array())
        delta_t = next_score - current_score

        # Here, we calculate the gradient of the result with respect to each param (biases, weights)
        gradient = 3

        # Now, we need to calculate the eligibility trace.
        e_t = self.lambda_ * self.e_t_previous + gradient
        self.e_t_previous = e_t

        # Finally, we update each weight.
        # new_weights = old_weights + self.alpha * delta_t * e_t





