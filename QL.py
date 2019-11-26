# Implementing Q-learning agent
import numpy as np
import random
from copy import copy
from agents import Agent
from agents import setShips
import matplotlib.pyplot as plt


# Function to randomly choose an space on the board to fire out
# Input: Board with all previous actions recorded, height and width of board
# Output: Location on board in [x,y] coordinates
def chooseAction(board, h, w):
    chosen = False
    while not chosen:
        # Generating random value for x and y
        x = random.randint(1, h)
        y = random.randint(1, w)
        if board[x][y] == 0:
            return [x, y]


# Function to select best action in the current 3x3 state
# Input: State from q-table, location of last fire in [x,y], epsilon for exploit/explore choice, full board
# Output: qA = action index in the 3x3 state, bA = action indexed onto board in [x,y]
def bestChoice(state, shotLocation, epsilon, board):
    qA = 0  # Will be set to action we select
    exp = random.random()  # Determine if you will exploit
    acceptable = False  # Boolean for if space has already been selected
    exploit = False  # Boolean for exploit or explore to be determined by comparison to exp
    # Epsilon-greedy method to determine if agent will explore or exploit
    if exp > epsilon:
        exploit = True
    # Copy of state to update if space is not an acceptable choice
    tempState = copy(state)

    # Keep generating action choice until space has not been chosen before
    while not acceptable:
        if exploit:
            qA = np.argmax(tempState)
        else:
            qA = random.randint(0, 7)  # randomly select a state

        # Convert q-table indexing to full board indexing
        convert = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        bX = shotLocation[0] + convert[qA][0]
        bY = shotLocation[1] + convert[qA][1]
        bA = [bX, bY]

        # Check if selected space has been fired at already
        if board[bX][bY] == 0:
            acceptable = True
        if exploit and not acceptable:
            tempState[qA] = '-inf'  # take the next best action

    return qA, bA

# Function to update board and determine result of an action
# Input: Whole board, space to be fired at, locations of enemy ships
# Output: result, where 1 = miss, 2 = hit, 3 = sink
def takeAction(board, boardAction, shipLocations):
    result = 0
    # Get total number of ships
    shipCount = len(shipLocations)
    # Iterate through each ship to see if boardAction hits any of them
    for i in range(shipCount):
        # Checking if hit location is one of the ship coordinates
        if boardAction in shipLocations[i]:
            # Checking first ship coordinate
            if boardAction == shipLocations[i][0]:
                # Update value for that ship location as 'hit'
                shipLocations[i][0] = 'hit'
                # Checking if other ship coordinate has been hit already
                if shipLocations[i][1] == 'hit':
                    # If so, ship has been sunk, return 3
                    board[boardAction[0]][boardAction[1]] = 2
                    return 3
            # Hit is on other ship coordinate
            else:
                shipLocations[i][1] = 'hit'
                # Checking if other ship coordinate has been hit already
                if shipLocations[i][0] == 'hit':
                    # If so, ship has been sunk, return 3
                    board[boardAction[0]][boardAction[1]] = 2
                    return 3
            # If the other coordinate in the ship hasn't been hit, return 2
            board[boardAction[0]][boardAction[1]] = 2
            return 2
    # If boardAction is not on one of the ships, return miss
    board[boardAction[0]][boardAction[1]] = 1
    return 1


def QLearning(forever, width, height):
    # in order: unchecked, miss, hit, sink
    rewardMatrix = [0, -1, 0, 1]

    alpha = 0.1
    epsilon = 0.05
    gamma = 0.9

    # Q-table initialization
    q = np.zeros(shape=(3, 3, 3, 3, 3, 3, 3, 3, 8))

    w = width
    h = height
    agent = Agent(w, h)

    time_steps = []
    episode_count = 0
    temp_time_steps = []

    for i in range(forever):
        episode_count += 1
        board = np.zeros((h, w))
        agent.ships = setShips(h, w)
        ships = agent.ships
        ships = [[[z + 1 for z in y] for y in x] for x in ships]
        board = np.pad(board, 1, 'constant', constant_values=(1, 1))
        win = False
        shipCount = 0
        location = chooseAction(board, h, w)
        hit = False
        time_steps_episode = 0
        while not win:
            if hit:
                time_steps_episode += 1
                tempState = []
                for y in range(location[1] - 1, location[1] + 2):
                    for x in range(location[0] - 1, location[0] + 2):
                        if [x, y] != location:
                            tempState.append(int(copy(board[x][y])))

                S = copy(
                    q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][
                        tempState[7]])
                # update board to have hit where we just hit
                # choose Action from this board currQ
                (qA, bA) = bestChoice(S, location, epsilon, board)
                # qA is the action index to update S (the q table)
                # ba is the action to compare to the whole board
                # take chosen Action, observe reward and next state
                result = takeAction(board, bA, ships)
                reward = rewardMatrix[result]

                # get new state indices for q-table based on action taken
                temp2State = copy(tempState)
                if result == 3:
                    temp2State[qA] = 2
                else:
                    temp2State[qA] = result

                newS = q[temp2State[0]][temp2State[1]][temp2State[2]][temp2State[3]][temp2State[4]][temp2State[5]][
                    temp2State[6]][temp2State[7]]
                # from next state, observe what optimal value can be
                maxnewS = max(newS)

                # Q update
                q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][
                    tempState[7]][qA] \
                    = S[qA] + alpha * (reward + gamma * maxnewS - S[qA])

                # if miss, 3x3 does not shift
                if result == 1:  # miss
                    S = newS
                elif result == 2:  # hit but not a sink
                    location = bA
                elif result == 3:  # sunk the ship
                    shipCount = shipCount + 1
                    if shipCount == 3:
                        win = True  # terminal state has been reached
                        temp_time_steps.append(time_steps_episode / 3)  # the game episode is over so average for all ships
                        hit = True
                        if episode_count == 10:
                            time_steps.append(np.mean(temp_time_steps))
                            temp_time_steps = []
                            episode_count = 0


                    else:
                        hit = False
                        location = chooseAction(board, h, w)
            # MISS
            else:
                # randomly choose an action
                result = takeAction(board, location, ships)
                if result == 2:  # hit
                    hit = True
                elif result == 3:  # sunk
                    shipCount = shipCount + 1
                    time_steps_episode += 1  # it took 1 attempt to sink the ship
                    if shipCount == 3:
                        win = True  # terminal state has been reached
                        temp_time_steps.append(time_steps_episode / 3)  # the game episode is over so average for all ships
                        hit = True
                        if episode_count == 10:
                            time_steps.append(np.mean(temp_time_steps))
                            temp_time_steps = []
                            episode_count = 0
                else:
                    location = chooseAction(board, h, w)

                # check if action was hit or miss and update board accordingly and hit boolean
    return board, time_steps


def main():
    forever = 5000
    width = 20
    height = 20
    board, time_steps= QLearning(forever, width, height)
    x = np.array([i for i in range(1, forever+1, 10)])
    print(np.mean(time_steps))
    # return np.mean(time_steps)

    plt.figure(1)
    plt.plot(x, time_steps)
    plt.xlabel('Number of Episodes')
    plt.ylabel('Time Steps')
    plt.title('Convergence of Q-Learning')
    plt.show()

    realBoard = []
    for i in range(1, len(board) - 1):
        realBoard.append(board[i][1:16])

    print(realBoard)
    return realBoard

main()
# mts = []
# for i in range(5):
#     print(main())
#     mts.append(main())
#
# x = np.mean(mts)
# print(x)

