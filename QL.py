# Implementing Q-learning agent
import numpy as np
import random
from copy import copy
from agents import Agent


# note: need to pass in board with all the places that have been shot at already by agent
def chooseAction(board):
    chosen = False
    while not chosen:
        x = random.randint(0,4)
        y = random.randint(0,4)
        if board[x][y] == 0:
            return x, y

# function to find best choice based on current 3x3 state
# NEEDS TO BE TESTED
def bestChoice(state, shotLocation, epsilon):
    # Has to return value between 0-7 to update into q-table AND the board index
    # epsilon will be used in here
    explore = random(0,1)
    if explore <= epsilon:
        qA = np.argmax(state)
    else:
        qA = random.randint(0,7)

    # Convert q-table indexing to full board indexing
    convert = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
    bX = shotLocation[0] + convert[qA][0]
    bY = shotLocation[1] + convert[qA][1]
    bA = [bX, bY]

    return qA, bA


def takeAction(board, boardAction, shipLocations):
    result = 0
    shipCount = len(shipLocations)
    for i in range(shipCount):
        # Checking if hit location is one of the ship coordinates
        if boardAction in shipLocations[i]:
            # checking if other ship coordinate has been hit already
            if boardAction == shipLocations[i][0]:
                shipLocations[i][0] = 'hit'

                # if so, return sunk = 3
                if shipLocations[i][1] == 'hit':
                    board[boardAction[0]][boardAction[1]] = 3
                    return 3
            else:
                shipLocations[i][1] = 'hit'
                if shipLocations[i][0] == 'hit':
                    board[boardAction[0]][boardAction[1]] = 3
                    return 3
            # if not, return hit = 2
            board[boardAction[0]][boardAction[1]] = 2
            return 2

    board[boardAction[0]][boardAction[1]] = 1
    return 1

    # if action results in a miss, then reward is -1
    # if action taken is a hit, need to check whole board for sunk
        # if sunk, give reward that
    pass

def wasSunk(board):
    pass

def QLearning():


    # in order: unchecked, miss, hit, sink
    rewardMatrix = [0, -1, 0, 4]

    alpha = 0.1
    epsilon = 0.1
    gamma = 0.9

    # Q-table initialization
    q = np.zeros(shape=(3, 3, 3, 3, 3, 3, 3, 3, 8))

    # state representation is
    # b) if the last missile was a hit or a miss

    # board = np.zeros((w, h))
    # board = board + 0.04
    # forever = 15000
    # shipCount = 0
    # location = chooseAction(board) # needs to be an x,y
    # hit = False
    forever = 2
    for i in range(forever):
        agent = Agent(5, 5)
        board = agent.enemyBoard  # enemy board
        ships = [[[0, 1], [0, 2]], [[3, 4], [2, 4]], [[2, 3], [1, 3]]] # agent.ships  # enemy ships
        print(ships)
        win = False
        shipCount = 0
        location = chooseAction(board)  # needs to be an x,y
        hit = False
        print("First location guess:", location)
        while not win:
            if hit:
                tempState = []
                for y in range(location[1] - 1,location[0] + 2):
                    for x in range(location[0] - 1, location[0] + 2):
                        if x != location[0] and y != location[1]:
                            tempState.append(board[x][y])

                S = copy(q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][tempState[7]])
                # update board to have hit where we just hit
                # choose Action from this board currQ
                (bA, qA) = bestChoice(S, location, epsilon)
                #qA is the action index to update S (the q table)
                #ba is the action to compare to the whole board

                # take chosen Action, observe reward and next state
                result = takeAction(bA, board, ships)
                reward = rewardMatrix[result]

                # get new state indices for q-table based on action taken
                temp2State = copy(tempState)
                temp2State = temp2State[qA]

                newS = q[temp2State[0]][temp2State[1]][temp2State[2]][temp2State[3]][temp2State[4]][temp2State[5]][temp2State[6]][temp2State[7]]
                # from next state, observe what optimal value can be
                maxnewS = max(newS)

                # Q update
                q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][tempState[7]]\
                    = S[qA] + alpha[reward + gamma*maxnewS - S[qA]]

                # if miss, 3x3 does not shift
                if result == 1:
                    S = newS
                elif result == 2:
                    location = bA
                else: # sunk the ship
                    shipCount += 1
                    if shipCount == 3:
                        win = True # terminal state has been reached
                    hit = False
            else:
                # randomly choose an action
                location = chooseAction(board)
                print("We missed, here's our new location:",location)
                # check if action was hit or miss and update board accordingly and hit boolean
                result = takeAction(board, location, ships)
                if result == 2:
                    hit = True

        return board


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

# result = board[bA[0]][bA[1]] # either be a hit or miss
#             if result == 2:
#                 # need to check whole board to see if sink
#                 if wasSunk:
#                     result = 3
#                 pass

QLearning()