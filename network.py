import random     # For sampling batches from the observations

import numpy as np
from keras.models import Sequential      # One layer after the other
from keras.layers import Dense, Flatten  # Dense layers are fully connected layers, Flatten layers flatten out multidimensional inputs
from collections import deque            # For storing moves 

from core.game_state import GameState

DEBUG = False

model = Sequential()
model.add(Dense(20, input_shape=(100,), init='uniform', activation='relu'))
model.add(Dense(18, init='uniform', activation='relu'))
model.add(Dense(10, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='linear')) 

model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])


# Parameters
D = deque()                                # Register where the actions will be stored

observetime = 500                          # Number of timesteps we will be acting on the game and observing results
epsilon = 0.7                              # Probability of doing a random move
gamma = 0.9                                # Discounted future reward. How much we care about steps further in time
mb_size = 500                              # Learning minibatch size

# FIRST STEP: Knowing what each action does (Observing)
observation = GameState(["Michael"])                   # Game begins
state = observation.to_array()
done = False
turns = 0
for t in range(observetime):
    possible_moves = observation.get_possible_moves()[0]
    if (DEBUG):
        if t < 10 or t % 20 == 0:
            print("t = "+str(t))
            print(observation)
            print("len = "+str(len(possible_moves)))
    if (t % 100 == 0 and turns >= 100):
        observation = GameState(["Michael"])                   # Game begins
        state = observation.to_array()
        done = False
        turns = 0
        print("RESTART: t = "+str(t))

    possible_states = np.array(list(map(lambda move: move.to_array(), possible_moves)))

    if np.random.rand() <= epsilon:
        action = np.random.randint(0, np.size(possible_states, 0))
    else:
        # predict_all = np.vectorize(lambda state: model.predict(state))
        Q = model.predict(possible_states)

        # Q = np.array(list(map(lambda state: model.predict(state), possible_states)))  # Q-values predictions
        action = np.argmax(Q)             # Move with highest Q-value is the chosen one
    observation_new = possible_moves[action]
    reward = observation_new.get_reward()
    done = observation_new.is_game_over()

    state_new = observation_new.to_array()     # Update the input with the new state of the game
    D.append((state, action, reward, state_new, done))         # 'Remember' action and consequence
    state = state_new         # Update state
    observation = observation_new
    if done:
        # print(observation_new.get_winner())
        print("END: t = "+str(t))
        observation = GameState(["Michael"])                   # Game begins
        state = observation.to_array()
        done = False
        turns = 0
    turns += 1
print('Observing Finished')

# SECOND STEP: Learning from the observations (Experience replay)
minibatch = random.sample(D, mb_size)                              # Sample some moves

inputs_shape = (mb_size,) + state.shape[0:]
inputs = np.zeros(inputs_shape)
targets = np.zeros((mb_size, 1))

for i in range(0, mb_size):
    state = minibatch[i][0]
    action = minibatch[i][1]
    reward = minibatch[i][2]
    state_new = minibatch[i][3]
    done = minibatch[i][4]
    
# Build Bellman equation for the Q function
    inputs[i:i+1] = np.expand_dims(state, axis=0)
    targets[i] = model.predict(np.expand_dims(state, axis=0))
    Q_sa = model.predict(np.expand_dims(state_new, axis=0))
    
    if done:
        targets[i, 0] = reward
    else:
        targets[i, 0] = reward + gamma * np.max(Q_sa)

# Train network to output the Q function
    model.train_on_batch(inputs, targets)
print('Learning Finished')

# THIRD STEP: Play!

observation = GameState(["Michael"])                   # Game begins
state = observation.to_array()
done = False
tot_reward = 0.0
turns = 0
while not done:
    turns += 1
    Q = model.predict(np.expand_dims(state, axis=0))        
    action = np.argmax(Q)     
    possible_moves = observation.get_possible_moves()[0]
    observation_new = possible_moves[action]
    reward = observation_new.get_reward()
    done = observation_new.is_game_over()
    state_new = observation_new.to_array()    
    tot_reward += reward
    observation = observation_new.copy()
    state = state_new
print(f'Game ended! Total reward: {reward}, Turns: {turns}')