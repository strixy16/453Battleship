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

# Main Q-learning function
# Input: number of episodes to run, width and height of battleship board
# Output: Final board at end of forever, array containing # of time steps averaged every 10 episodes
def QLearning(forever, width, height):
    # Reward matrix, with values for unchecked, miss, hit, and sink
    rewardMatrix = [0, -1, 0, 1] # unchecked value there because unchecked value on board is 0

    # Step size
    alpha = 0.1
    # Epsilon for epsilon-greedy action selection
    epsilon = 0.05
    # Discount factor
    gamma = 0.9

    # Q-table initialization
    q = np.zeros(shape=(3, 3, 3, 3, 3, 3, 3, 3, 8))

    # Generating Agent object to train
    w = width
    h = height
    agent = Agent(w, h)

    # Array to save number of steps to sink a ship every 10 episodes
    time_steps = []
    # Counter to check when 10 episodes have passed to save time_steps out
    episode_count = 0
    # Stores number of steps to sink a ship for every episode
    temp_time_steps = []

    # Loop for each episode in forever
    for i in range(forever):
        episode_count += 1
        # Resetting board each episode
        board = np.zeros((h, w))
        # Padding board with 1s to handle shots fired at edge needing a 3x3 surrounding
        board = np.pad(board, 1, 'constant', constant_values=(1, 1))
        # Setting ships randomly on board
        agent.ships = setShips(h, w)
        ships = agent.ships
        # Add 1 to ship indexes to account for board padding
        ships = [[[z + 1 for z in y] for y in x] for x in ships]
        # Boolean for terminal state
        win = False
        # Ship counter to figure out when game has been won
        shipCount = 0
        # Randomly choosing first space to fire at
        location = chooseAction(board, h, w)
        # Boolean to decide which policy to follow, random or "hit policy"
        hit = False
        # Counter for number of steps to finish a game, will be divided by 3 to approximate # of steps to sink a ship
        time_steps_episode = 0
        # Looping while not at terminal state
        while not win:
            # If hit occurred, move into Q-learning
            if hit:
                # Only counting steps to finish a game when in hit policy
                time_steps_episode += 1
                # Getting current state by looking at board around location that was just hit and getting a size 8 array
                tempState = []
                for y in range(location[1] - 1, location[1] + 2):
                    for x in range(location[0] - 1, location[0] + 2):
                        if [x, y] != location: # ignores square we just hit, only need locations around it
                            tempState.append(int(copy(board[x][y])))
                # Extracting policy array from q-table using S
                S = copy(
                    q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][
                        tempState[7]])
                # Call to bestChoice to choose A from S using epsilon-greedy
                # qA is the action index to update S (the q table)
                # bA is the action to compare to the whole board
                (qA, bA) = bestChoice(S, location, epsilon, board)
                # Take chosen action and update board
                result = takeAction(board, bA, ships)
                # Determine reward to be given based on result
                reward = rewardMatrix[result]

                # Get new state indices for q-table based on action taken
                temp2State = copy(tempState)
                # If result is sunk, the value to be put in q-table is 2. 3 was only for reward indexing
                if result == 3:
                    temp2State[qA] = 2
                else:
                    temp2State[qA] = result

                # Get S' from q-table using temp2State
                newS = q[temp2State[0]][temp2State[1]][temp2State[2]][temp2State[3]][temp2State[4]][temp2State[5]][
                    temp2State[6]][temp2State[7]]
                # From S', observe what optimal value will be for max(a)Q(S',a)
                maxnewS = max(newS)

                # Q update
                q[tempState[0]][tempState[1]][tempState[2]][tempState[3]][tempState[4]][tempState[5]][tempState[6]][
                    tempState[7]][qA] \
                    = S[qA] + alpha * (reward + gamma * maxnewS - S[qA])

                # If action was miss, do not shift 3x3
                if result == 1:
                    S = newS
                # If action was hit but not sink, recenter S on the new hit
                elif result == 2:
                    location = bA
                # If action was a sink
                elif result == 3:
                    # Sunk ship count increases
                    shipCount = shipCount + 1
                    # Checking if game has been won (always use 3 ships right now)
                    if shipCount == 3:
                        # Terminal state has been reached
                        win = True
                        # Average total steps taken to figure out how long it takes to sink 1 ship
                        temp_time_steps.append(time_steps_episode / 3)
                        # Average step count over 10 episodes for graphs
                        if episode_count == 10:
                            time_steps.append(np.mean(temp_time_steps))
                            # Reset values for next 10 episodes
                            temp_time_steps = []
                            episode_count = 0
                    # Game hasn't ended yet, still ships to sink
                    else:
                        # Return to random policy when ship has been sunk
                        hit = False
                        # Choosing an action to take next time step
                        location = chooseAction(board, h, w)

            # If miss occurred or first iteration, use random policy
            else:
                # Take random chosen action and get result as hit, miss, or sink
                result = takeAction(board, location, ships)
                # If action was hit but not sink, set hit to true so we move into Q-learning policy
                if result == 2:
                    hit = True
                # If action was a sink
                elif result == 3:
                    # Sunk ship count increases
                    shipCount = shipCount + 1
                    # It took 1 attempt to sink the ship
                    time_steps_episode += 1
                    # Checking if game has been won (always use 3 ships right now)
                    if shipCount == 3:
                        # Terminal state has been reached
                        win = True
                        # Average total steps taken to figure out how long it takes to sink 1 ship
                        temp_time_steps.append(time_steps_episode / 3)
                        # Average step count over 10 episodes for graphs
                        if episode_count == 10:
                            time_steps.append(np.mean(temp_time_steps))
                            # Reset values for next 10 episodes
                            temp_time_steps = []
                            episode_count = 0
                # If action was miss, randomly choose next action
                else:
                    location = chooseAction(board, h, w)

    return board, time_steps

# Main function, returns the final board
def main():
    # Number of episodes to train with
    forever = 1000
    # Size of board
    width = 20
    height = 20
    # Run Q-learning
    board, time_steps = QLearning(forever, width, height)
    # Print out mean of all the time step measurements
    print(np.mean(time_steps))

    # Plotting convergence
    # Generating values for x axis
    x = np.array([i for i in range(1, forever + 1, 10)])
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

# Statistical collection - leave commented out
# mts = []
# for _ in range(5):
#     print(main())
#     mts.append(main())
#
# x = np.mean(mts)
# print(x)

