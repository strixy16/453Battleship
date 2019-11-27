import random
import numpy as np
from agents import Agent
import matplotlib.pyplot as plt
import statistics

'''
This program applies on-policy first-visit Monte Carlo to the game Battleship.
CISC 453 - Reinforcement Learning
Final Project
'''


# Global Variables
q = np.zeros(shape=(3,3,3,3,3,3,3,3,8))
returns = np.zeros(shape=(3,3,3,3,3,3,3,3,8,1)) # stores rewards for each action/state
returnsBool = np.zeros(shape=(3,3,3,3,3,3,3,3,8))
# each action has a bool value that says if its been visited already
returns = returns.tolist()
records = [] # records all states and actions, will have a bunch of 1x9 arrays
steps = 0 # for graphing purposes



def calculate(gamma):
    global q, records, returns, returnsBool
    g = 1 # set reward for sinking to be 0, -1 for everything else
    for i in reversed(records): # includes the 1x8 state and the action
        act = i[-1] # the action taken
        
        if returnsBool[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act] == 0:
            # won't visit for rest of game
            returnsBool[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act] = 1
            returns[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act].append(g)            
            myRewards = returns[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act]
            q[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act] = statistics.mean(myRewards)
            g = gamma*g -1
        # esoft handled elsewhere
    records = [] # clear records
        
        
    
'''
This function determines if a ship has been sunk.
Paramaters: action taken, ship coordinates, current board
Return: True if all coordinates in ship have been hit
'''
def checkSunk(action, ships, board):
    global totalHits
    for i in range(len(ships)):
        for j in range(len(ships[i])):
            if action == ships[i][j]:
                # go through all coords in ship, confirm if all hit
                for k in ships[i]:
                    if board[k[0]][k[1]] != 2:
                        return False
                #numberOfHits = 0
                return True
            
'''
This function determines if a ship has been hit.
Paramaters: action taken, ship coordinates, current board
Return: True if the action is in ship coordinates
'''
def checkHit(action, ships, board):
    for i in range(len(ships)):
        for j in range(len(ships[i])):
            if action == ships[i][j]:
                board[action[0]][action[1]] = 2
                return True
    return False

'''
This function creates a 1x8 array to represent the 3x3 board surrounding the selected action.
Paramaters: action taken, current board, dimensions of the board.
Return: 3x3 board.
'''
def getState(action, board, w, h):
    state = [0 for _ in range(8)]    
    b = 0
    x = action[0]
    y = action[1]

    for i in range(x-1, x+2):    
        for j in range(y-1,y+2):
            
            # check if out of bounds
            if i < 0:
                state[b] = 1
            elif i >= w:
                state[b] = 1
            elif j < 0:
                state[b] = 1
            elif j >= h:
                state[b] = 1
            else:
                if i == x and j == y:
                    b -= 1
                else:
                    state[b] = int(board[i][j])

            b += 1
        
    return state

# gets all possible actions from a given state
def getActions(state):
    global q
    return q[state[0]][state[1]][state[2]][state[3]][state[4]][state[5]][state[6]][state[7]]

'''
This function selects an action using epsilon soft.
Paramaters: possible actions, epsilon
Return: selected action
'''
def eSoft(actions, e, state):
        maxIndices = []
        valid = []
        for i in range(len(state)):
            if state[i] == 0:
                valid.append(i)
        maxVal = float('-inf')
        lenActions = len(valid)
        actionIndices = [ i for i in range(len(actions))     ]
        for i in range(lenActions):
            if actions[valid[i]] > maxVal:
                maxIndices.clear()
                maxIndices.append(valid[i])
                maxVal = actions[valid[i]]
            elif actions[valid[i]] == maxVal:
                maxIndices.append(valid[i])
                
        probArray = [ 0 for _ in range(len(actions)) ]
        for i in range(lenActions):
            probArray[valid[i]] = e/lenActions
            
        for i in range(len(maxIndices)):
            probArray[maxIndices[i]] = ((1 - e) + ( len(maxIndices) * e / lenActions)) / len(maxIndices)
        return np.random.choice(actionIndices, p=probArray)
       
        #return np.random.choice(actionIndices, p=probArray)


def convert(actionInd):

    if actionInd >= 0 and actionInd < 3:
        newY = 0
    elif actionInd >= 3 and actionInd < 6:
        newY = 1
    elif actionInd >= 6:
        newY = 2

    if actionInd % 3 == 0:
        newX = 0
    elif actionInd % 3 == 1:
        newX = 1
    elif actionInd % 3 == 2:
        newX = 2
    return newY, newX

'''
This function calculates the total number of ships that have been sunk
by comparing hit locations to ship coordinates.
Paramaters: ship coordinates, current board
Return: number of ships sunk
'''
def totalSunk(ships, board):
    count = 0
    shipsSunk = 0
    for i in range(len(ships)):
        count = 0
        for j in range(len(ships[i])):
            if board[ships[i][j][0]][ships[i][j][1]] == 2:
                count += 1
        if count == len(ships[i]):
            shipsSunk += 1
    return shipsSunk


## ''' This function implements on-policy Monte Carlo to sink a ship once it has been hit.
##Paramaters: action, ship coordinates, current board, epsilon, board dimensions, gamma
##Return: number of ships sunk
##'''           
def monteCarlo(action, ships, board, e, w, h, gamma):
    #print("MC")
    global steps # numberOfHits
    steps += 1

    global records, q
    if totalSunk(ships, board)== len(ships):
        return True
    elif checkSunk(action, ships, board):
        calculate(gamma)
        return False

    state = getState(action, board, w, h)
    if 0 not in state:
        return False
    #print(state)
    # use e soft to get action
    # we have the state (action)
    # should be list of 8 actions
    myActions = getActions(state)
    
    actionInd = eSoft(myActions,e, state)
##    print(board)
##    print (action)
##    print(actionInd)
    state.append(actionInd)
    records.append(state)
    
    if actionInd >= 4: # skip index 4 - is self, for conversion purposes
        actionInd += 1
    
    newY, newX = convert(actionInd)
    newY -= 1
    newX -= 1
    if (newY + action[0]) >= 0 and (newY + action[0]) < w:
        newY += action[0]
    else:
        newY = action[0]
        
    if (newX + action[1]) >= 0 and (newX + action[1]) < h:
        newX += action[1]
    else:
        newX = action[1]
    # have new action
    if checkHit([newY, newX], ships, board):
        #numberOfHits += 1

        return monteCarlo([newY,newX], ships, board, e,w,h, gamma)

    else:
        # numberOfHits += 1
        board[newY][newX] = 1
        return monteCarlo([action[0],action[1]], ships, board, e, w, h, gamma)

'''
This function allows gameplay by playing randomly until a ship have been hit,
and then entering monte carlo. This continues until all ships have been sunk.
Paramaters: forever (epochs), ship dimensions
Return: board
'''        
def play(forever,w,h):
    global records, returnsBool, steps

    #variables for graphing
    countTo10 = 0
    myCount = 0
    counter = [0 for i in range(10)]
    
    num = w*h
    gamma = 0.9
    e = 0.3
    pts = [0 for i in range(int(forever/10))]
    
    for i in range(forever):
        # reset the rewards boolean value
        returnsBool = np.zeros(shape=(3,3,3,3,3,3,3,3,8))        
        records = [] # reset
        #intialize the board
        agent = Agent(w,h)
        ships = agent.ships
        board = agent.enemyBoard 
        actionSet = {i for i in range(num)}

        win = False
        while not win:
                # select a random action from the actionSet
                action = random.choice(tuple(actionSet))
                actionSet.remove(action)
                y = int(action/w)
                x = action%h
                hit = checkHit([y,x], ships, board)
                state = getState([y,x], board, w, h)
                #print("rand")
                if hit:
                    # if action was a hit, enter Monte Carlo guessing
                    records = [] # reset
                    win = monteCarlo([y,x], ships, board, e, w, h, gamma)

                else:
                    # update the board location to be a miss
                    board[y][x] = 1 

    # for graphing purposes
##        print(steps/3)
        counter[countTo10] = steps/3 # ave num of hits to sink a ship
        countTo10 += 1
        steps = 0
        if countTo10 == 10:
            countTo10 = 0
            pts[myCount] = statistics.mean(counter)
            myCount += 1
            
    episodes = np.array([i for i in range(1, forever+1,10)])
    pts = np.array(pts)

    plt.figure(1)
    plt.plot(episodes, pts)

    
    plt.xlabel('Number of Episodes')
    plt.ylabel('Time Steps to Sink a Ship')
    plt.title('Convergence of Monte Carlo')
    plt.show()
    
    return board        

def main():
    # set dimensions of the board
    w = 20
    h = 20
    
    global q
    # number of epochs
    forever = 3000

    # print final board
    # for i in range(1):
    #     board = play(forever, w, h)
    #     for i in board:
    #         print(i)
    #     print()
    

main()
