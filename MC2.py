# Let's try MC again
import random
import numpy as np
from agents import Agent
import copy


q = np.zeros(shape=(3,3,3,3,3,3,3,3,8))
records = [] # records all states and actions, will have a bunch of 1x9 arrays
#shipsSunk = 0


def checkSunk(action, ships, board):
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

def getState(action, board, w, h):
    state = [0 for _ in range(8)]    
    b = 0
    x = action[1]
    y = action[0]
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
                if i != x and j != y:
                    state[b] = int(board[i][j])
                else:
                    b -= 1
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
        print('u dont fuked up')
        
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
    #print(board)
    #print()
    #print(shipsSunk)
    global records, q
    if totalSunk(ships, board)==3:
        return True
    elif checkSunk(action, ships, board):
        return False
    
    state = getState(action, board, w, h)
    # use e soft to get action
    # we have the state (action)
    # should be list of 8 actions
    myActions = getActions(state)
    actionInd = eSoft(myActions,e)
    if actionInd >= 4: # skip index 4 - is self
        actionInd += 1
    #print(actionInd)
    records.append(state.append(actionInd))
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
        
        # if current ship is sunk, move to next
        # else, retrun monteCarlo with old again
        if checkSunk([action[0], action[1]], ships, board):
            return monteCarlo([newY,newX], ships, board, e, w, h, gamma)
        else:
            return monteCarlo([action[0], action[1]], ships, board, e, w, h, gamma)
    else:
        board[newY][newX] = 1
        return monteCarlo([action[0],action[1]], ships, board, e, w, h, gamma)

def hitNotSunk(ships, board, w,h):
    # go through all board coordinates, for all hits, check sunk
    for i in range(h):
        for j in range(w):
            if board[i][j] == 2:
                # check sunk
                if not checkSunk([i,j], ships, board):
                    return True, [i,j]
    # no hit but unsunk ships
    return False, [0,0]
        
def play(forever,w,h):
    global records
    num = w*h
    gamma = 0.9
    e = 0.05
    for i in range(forever):
        
        records = [] # reset
        # set up game, get ships and board
        agent = Agent(w,h)
        board = agent.enemyBoard
        ships = agent.ships
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
            # returns bool, if true take action
            notSunkYet, action = hitNotSunk(ships, board, w,h)
            if notSunkYet:
                win = monteCarlo([action[0], action[1]], ships, board, e, w, h ,gamma)
            else:
                #pick random action
                action = random.choice(tuple(actionSet))
                actionSet.remove(action)
                y = int(action/w)
                x = action%h
                hit = checkHit([y,x], ships, board)
                state = getState([x,y], board, w, h)
                if hit:
                    # will return ~3 times, last time win should be true
                    records = [] # reset
                    win = monteCarlo([y,x], ships, board, e, w, h, gamma)                
                else:
                    board[y][x] = 1 
            
    return board        

def main():
    w = 15
    h = 15
    forever = 1000
    board = play(forever, w, h)
    for i in board:
        print(i)
    

main()
