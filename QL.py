# Implementing Q-learning agent
import numpy as np
import random

# note: need to pass in board with all the places that have been shot at already by agent
def chooseAction():
    chosen = False
    while not chosen:
        x = random.randint(0,25)
        if not board(x).shot:
            return x

def QLearning(board):
    w = 5
    h = 5

    alpha = 0.1
    epsilon = 0.1
    gamma = 0.9

    # state representation is
    # b) if the last missile was a hit or a miss

    board = np.zeros((w, h))
    board = board + 0.04
    forever = 15000
    shipcount = 0
    for i in range(forever):
        state = [hitbool]
        while not won:
            action = random(x,y)
            next_state = [hitbool]
            reward = take_action(action)
            Q(state,action) = Q(state,action) + alpha(reward + 0.9*max(Q(state,action)) - Q(state,action))

            if reward == 1:
                shipcount += 1
            if shipcount == 3:
                won = True

            state = next_state

