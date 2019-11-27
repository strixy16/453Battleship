# Let's try MC again
import random
import numpy as np
from agents import Agent
#import copy
import matplotlib.pyplot as plt
import statistics

q = np.zeros(shape=(3,3,3,3,3,3,3,3,8))
returns = np.zeros(shape=(3,3,3,3,3,3,3,3,8,1)) # stores rewards for each action/state
returnsBool = np.zeros(shape=(3,3,3,3,3,3,3,3,8))
# each action has a bool value that says if its been visited already
returns = returns.tolist()
records = [] # records all states and actions, will have a bunch of 1x9 arrays
steps = 0 # for graphing purposes

numberOfHits = 0
#shipsSunk = 0


def calculate(gamma):
    global q, records, returns, returnsBool
    g = 5 # set reward for sinking to be 0, -1 for everything else
    for i in reversed(records): # includes the 1x8 state and the action
        #print(i)
        act = i[-1] # the action taken
        
        if returnsBool[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act] == 0:
            # won't visit for rest of game
            returnsBool[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act] = 1
            returns[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act].append(g)            
            myRewards = returns[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act]
        #print(myRewards)
            q[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][act] = statistics.mean(myRewards)
            g = gamma*g -1
        # esoft handled elsewhere
    records = [] # clear records
        
        
    
        
def checkSunk(action, ships, board):
    global numberOfHits
    for i in range(len(ships)):
        for j in range(len(ships[i])):
            if action == ships[i][j]:
                # go through all coords in ship, confirm if all hit
                for k in ships[i]:
                    if board[k[0]][k[1]] != 2:
                        return False
                return True
                #return (board[ships[i][j-1][0]][ships[i][j-1][1]] == 2)

def checkHit(action, ships, board):
    for i in range(len(ships)):
        for j in range(len(ships[i])):
            if action == ships[i][j]:
                board[action[0]][action[1]] = 2
                return True
    return False

# returns 3x3 board
def getState(action, board, w, h):
    state = [0 for _ in range(8)]    
    b = 0
    x = action[0]
    y = action[1]
##    print("x,y:")
##    print(x,y)
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
##                print(i,j)
##                print(board[i][j])
                if i == x and j == y:
                    b -= 1
                else:
                    state[b] = int(board[i][j])
##                    print("added")
##                    print(state[b])
##                else:
##                    b -= 1
            b += 1
        
    return state

def getActions(state):
    global q
    return q[state[0]][state[1]][state[2]][state[3]][state[4]][state[5]][state[6]][state[7]]

            
#returns the index of the action chosen by e-soft
def eSoft(actions, e):
        maxIndices = []
        maxVal = float('-inf')
        lenActions = len(actions)
        actionIndices = [ i for i in range(lenActions) ]
        for i in range(lenActions):
            if actions[i] > maxVal:
                maxIndices.clear()
                maxIndices.append(i)
                maxVal = actions[i]
            elif actions[i] == maxVal:
                maxIndices.append(i)
                
        probArray = [ (e/lenActions) for _ in range(lenActions) ]

        for i in range(len(maxIndices)):
            probArray[maxIndices[i]] = ((1 - e) + ( len(maxIndices) * e / lenActions)) / len(maxIndices)

        return np.random.choice(actionIndices, p=probArray)


def convert(actionInd):
##    newY = int((actionInd + 1) / 3)
##    if actionInd >= 0 and actionInd < 4:
##        newX = actionInd % 3
##    elif actionInd >= 4 and actionInd < 8:
##        newX = (actionInd + 1) % 3
##    else:
##        newX = 2
##    return newY, newX
    if actionInd >= 0 and actionInd < 3:
        newY = 0
    elif actionInd >= 3 and actionInd < 6:
        newY = 1
    elif actionInd >= 6:
        newY = 2
    else:
        print('u done fuked up')
        
    if actionInd % 3 == 0:
        newX = 0
    elif actionInd % 3 == 1:
        newX = 1
    elif actionInd % 3 == 2:
        newX = 2
    return newY, newX

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
            
def monteCarlo(action, ships, board, e, w, h, gamma):
    global steps, numberOfHits
    steps += 1
##    print(board)
##    print()
    #print(shipsSunk)
    global records, q
    if totalSunk(ships, board)== len(ships):
        return True
    elif checkSunk(action, ships, board):
##        print(numberOfHits)
        numberOfHits = 0
        calculate(gamma)
        return False
##    print("action:")
##    print(action)
    state = getState(action, board, w, h)
    if 0 not in state:
        return False
    #print(state)
    # use e soft to get action
    # we have the state (action)
    # should be list of 8 actions
    myActions = getActions(state)
    # check if state is hit, if hit set action to be -inf
##    print(state)
    for i in range(8): # state is 1x8
        if state[i]!= 0:
            myActions[i] = '-inf'
    actionInd = eSoft(myActions,e)
        
    state.append(actionInd)
    records.append(state)
    
    if actionInd >= 4: # skip index 4 - is self, for conversion purposes
        actionInd += 1
##    print(actionInd)
    
    
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
        numberOfHits += 1
        #print(state)
        #print(getActions(state))

        return monteCarlo([newY,newX], ships, board, e,w,h, gamma)
        # if current ship is sunk, move to next
        # else, retrun monteCarlo with old again
##        if checkSunk([action[0], action[1]], ships, board, gamma):
##            return monteCarlo([newY,newX], ships, board, e, w, h, gamma)
##        else:
##            return monteCarlo([action[0], action[1]], ships, board, e, w, h, gamma)
    else:
##        print("!!!" + str(action[0]) +", " + str(action[1]))
        numberOfHits += 1
        board[newY][newX] = 1
        return monteCarlo([action[0],action[1]], ships, board, e, w, h, gamma)


# DONT ACTUALLY USE THIS - NOT REINFORCEMENT LEARNING
def hitNotSunk(ships, board, w,h, gamma):
    # go through all board coordinates, for all hits, check sunk
    allHit = [] # all hits of the boat for which the thing belongs
    for i in range(h):
        for j in range(w):
            if board[i][j] == 2:
                # check sunk
                if not checkSunk([i,j], ships, board):
                    allHit.append([i,j])
                    #return True, [i,j]
    # no hit but unsunk ships
    
    if allHit != []:
        # pick any random one that was hit and not sunk
        choice = random.choice(allHit)
        return True, choice
    return False, [0,0]
        
def play(forever,w,h):
    global records, returnsBool, steps
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
        agent = Agent(w,h)
        ships = agent.ships
        board = agent.enemyBoard
        # set up game, get ships and board

        # keep track of which ships were hit
        #boolShips = np.copy(ships)
        #numShips = len(boolShips) # should be 3
        #for i in range(numShips):            
        #    lenShips = length(boolShips[i])            
        #    for j in range(lenShips):
        #        boolShips[j] = 0
            
        
        actionSet = {i for i in range(num)}

        win = False
        while not win:
            # check to make sure there is nothing hit that wasn't sunk
            # returns bool, if true take action, action is random among all hit
            notSunkYet, action = hitNotSunk(ships, board, w,h, gamma)
            if notSunkYet:
                win = monteCarlo([action[0], action[1]], ships, board, e, w, h ,gamma)
            else:
                #pick random action
                action = random.choice(tuple(actionSet))
                actionSet.remove(action)
                y = int(action/w)
                x = action%h
                hit = checkHit([y,x], ships, board)
##                print("??")
                state = getState([y,x], board, w, h)
                if hit:
                    # will return ~3 times, last time win should be true
                    records = [] # reset
                    win = monteCarlo([y,x], ships, board, e, w, h, gamma)                
                else:
                    board[y][x] = 1 

        counter[countTo10] = steps
        countTo10 += 1
        steps = 0
        if countTo10 == 10:
            countTo10 = 0
            pts[myCount] = statistics.mean(counter)
            myCount += 1
    # plot pts and i
    #print(pts)
    
    episodes = np.array([i for i in range(1, forever+1,10)])
    pts = np.array(pts)
    #print(episodes)
    plt.figure(1)
    plt.plot(episodes, pts)
##    plt.scatter(episodes, pts, alpha = 0.2, s = 10)
    
    plt.xlabel('Number of Episodes')
    plt.ylabel('Time Steps')
    plt.title('Convergence of Monte Carlo')
    plt.show()
    return board        

def main():
    w = 5
    h = 5
    
    global q
    forever = 100
    
    for i in range(1):
        board = play(forever, w, h)
        for i in board:
            print(i)
        print()
    

main()
