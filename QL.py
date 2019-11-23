# Implementing Q-learning agent
import numpy as np
import random
from copy import copy
from agents import Agent
from agents import setShips
import matplotlib.pyplot as plt

# note: need to pass in board with all the places that have been shot at already by agent
def chooseAction(board, h, w):
    chosen = False
    while not chosen:
        x = random.randint(1,h)
        y = random.randint(1,w)
        if board[x][y] == 0:
            return [x, y]

# function to find best choice based on current 3x3 state
# NEEDS TO BE TESTED
def bestChoice(state, shotLocation, epsilon, board):
    # Has to return value between 0-7 to update into q-table AND the board index
    # epsilon will be used in here
    explore = random.random()
    acceptable = False
    while not acceptable:
        explore = False
        if explore > epsilon:
            explore = True
            tempState = copy(state)
            qA = np.argmax(tempState) #this will never be a state already selected
        else:
            qA = random.randint(0, 7)

        # Convert q-table indexing to full board indexing
        convert = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
        bX = shotLocation[0] + convert[qA][0]
        bY = shotLocation[1] + convert[qA][1]
        bA = [bX, bY]

        if board[bX,bY] == 0:
            acceptable = True
        if explore == True and acceptable == False:
            tempState[qA] = '-inf'

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
                    board[boardAction[0]][boardAction[1]] = 2
                    return 3
            else:
                shipLocations[i][1] = 'hit'
                if shipLocations[i][0] == 'hit':
                    board[boardAction[0]][boardAction[1]] = 2
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

def QLearning(forever):
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
    w = 8
    h = 8
    agent = Agent(w, h)
    board = agent.enemyBoard  # enemy board
    # forever = 50000
    time_steps = []
    for i in range(forever):
        # print('WE DID IT BITCHES')
        board = np.zeros((h, w))
        agent.ships = setShips(h, w)
        ships = agent.ships
        ships = [[[z+1 for z in y] for y in x] for x in ships]
        # ships = agent.ships
        board = np.pad(board, 1, 'constant', constant_values=(1, 1))
        # ships = [[[1, 2], [1, 3]], [[4, 5], [3, 5]], [[3, 4], [2, 4]]] # agent.ships  # enemy ships
        win = False
        shipCount = 0
        location = chooseAction(board, h, w) # needs to be an x,y
        hit = False
        time_steps_episode = 1
        while not win:
            if hit:
                time_steps_episode += 1
                tempState = []
                for y in range(location[1] - 1,location[1] + 2):
                    for x in range(location[0] - 1, location[0] + 2):
                        if [x,y] != location:
                            tempState.append(int(copy(board[x][y])))

                S = copy(q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][tempState[7]])
                # update board to have hit where we just hit
                # choose Action from this board currQ
                (qA, bA) = bestChoice(S, location, epsilon,board)
                #qA is the action index to update S (the q table)
                #ba is the action to compare to the whole board
                # take chosen Action, observe reward and next state
                result = takeAction(board, bA, ships)
                reward = rewardMatrix[result]

                # get new state indices for q-table based on action taken
                temp2State = copy(tempState)
                if result == 3:
                    temp2State[qA] = 2
                else:
                    temp2State[qA] = result


                newS = q[temp2State[0]][temp2State[1]][temp2State[2]][temp2State[3]][temp2State[4]][temp2State[5]][temp2State[6]][temp2State[7]]
                # from next state, observe what optimal value can be
                maxnewS = max(newS)

                # Q update
                # print('before:', q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][
                #         tempState[7]])
                q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][tempState[7]][qA]\
                    = S[qA] + alpha*(reward + gamma*maxnewS - S[qA])
                # print('after', q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][tempState[7]])


                # if miss, 3x3 does not shift
                if result == 1: #miss
                    S = newS
                elif result == 2: #hit but not a sink
                    location = bA
                elif result == 3: # sunk the ship
                    shipCount = shipCount + 1
                    if shipCount == 3:
                        win = True # terminal state has been reached
                        time_steps.append(time_steps_episode/3) # the game episode is over so average for all ships
                        hit = True
                    else:
                        hit = False
                        temp_time_steps = 1 # reset temp time steps for next ship
                        location = chooseAction(board, h, w)
            # MISS
            else:
                # randomly choose an action
                result = takeAction(board, location, ships)
                if result == 2: #hit
                    time_steps_episode += 1
                    hit = True
                elif result == 3: #sunk
                    shipCount = shipCount + 1
                    time_steps_episode += 1  # it took 1 attempt to sink the ship
                    if shipCount == 3:
                        win = True  # terminal state has been reached
                        time_steps.append(time_steps_episode/3)# the game episode is over so average for all ships
                        hit = True
                else:
                    location = chooseAction(board, h, w)

                # check if action was hit or miss and update board accordingly and hit boolean
    return board, time_steps, q[1][0][1][1][0][1][0][0]


forever = 5000
board, time_steps,q_table = QLearning(forever)
print(board)
print(q_table)
x = [t for t in range(1, forever + 1)]

plt.figure(1)
plt.plot(x, time_steps)
plt.xlabel('Number of Episodes')
plt.ylabel('Time Steps')
plt.title('Convergence of Q-Learning')
plt.show()

