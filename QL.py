# Implementing Q-learning agent
import numpy as np
import random
from copy import copy



# note: need to pass in board with all the places that have been shot at already by agent
def chooseAction():
    chosen = False
    while not chosen:
        x = random.randint(0,25)
        if not board(x).shot:
            return x

# function to find best choice based on current 3x3 state
def bestChoice():
    # Has to return value between 0-7 to update into q-table AND the board index
    # epsilon will be used in here
    pass

def takeAction(boardAction, board, qAction):
    #will need to pass in board
    # if action results in a miss, then reward is -1
    # if action taken is a hit, need to check whole board for sunk
        # if sunk, give reward that
    pass

def wasSunk(board):
    pass

def QLearning():
    w = 5
    h = 5

    # in order: unchecked, miss, hit, sink
    rewardMatrix = [0, -1, 0, 4]

    alpha = 0.1
    epsilon = 0.1
    gamma = 0.9

    # Q-table initialization
    q = np.zeros(shape=(3, 3, 3, 3, 3, 3, 3, 3, 8))
    print(q[0][0][0][0][0][0][0][0])

    # state representation is
    # b) if the last missile was a hit or a miss

    board = np.zeros((w, h))
    board = board + 0.04
    forever = 15000
    shipcount = 0
    # location = chooseAction() # needs to be an x,y
    hit = False
    tempState = []
    for y in range(location[1] - 1, location[1] + 2):
        for x in range(location[0] - 1, location[0] + 2):
            if x != location[0] and y != location[1]:
                tempState.(boardVal(x, y))

    for i in range(forever):
        if hit:
            # we think this is a reference?
            S = copy(q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][tempState[7]])
            # update board to have hit where we just hit
            # choose Action from this board currQ
            (bA, qA) = bestChoice(S)
            #qA is the action index to update S (the q table)
            #ba is the action to compare to the whole board

            # take chosen Action, observe reward and next state
            result = board(bA) # either be a hit or miss
            if result == 2:
                # need to check whole board to see if sink
                if wasSunk:
                    result = 3
                pass

            reward = rewardMatrix[result]
            temp2State = copy(tempState)
            temp2State = temp2State[qA]

            newS = q[temp2State[0]][temp2State[1]][temp2State[2]][temp2State[3]][temp2State[4]][temp2State[5]][temp2State[6]][temp2State[7]]
            # from next state, observe what optimal value can be
            maxnewS = max(newS)

            # Q update
            q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][tempState[7]]\
                = S[qA] + alpha[reward + gamma*maxnewS - S[qA]]

            # if miss, 3x3 does not shift
            if reward == 1:
                S = newS
            elif reward == 2:
                tempState = []
                for y in range(bA[1] - 1, bA[0] + 2):
                    for x in range(bA[0] - 1, bA[0] + 2):
                        if x != bA[0] and y != bA[1]:
                            tempState.(boardVal(x, y))
            else: # sunk the ship
                hit = False

        else:
            # randomly choose an action
            chooseAction()
            # check if action was hit or miss and update board accordingly and hit boolean


            # currState = nextState


    # for i in range(forever):
    #
    #     while not won:
    #         # only run this for hit
    #         action = random(x,y)
    #         next_state = [hitbool]
    #         reward = take_action(action)
    #         Q(state,action) = Q(state,action) + alpha(reward + 0.9*max(Q(state,action)) - Q(state,action))
    #
    #         if reward == 1:
    #             shipcount += 1
    #         if shipcount == 3:
    #             won = True
    #
    #         state = next_state

QLearning()