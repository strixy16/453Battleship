# Let's try MC again
import random
import numpy as np
from agents import Agent
import copy

q = np.zeros(shape=(3,3,3,3,3,3,3,3,8))
records = [] # records all states and actions, will have a bunch of 1x9 arrays

def checkWin(ships):
    if ships == []:
        return True
    return False

def checkSunk(ships):
    if [] in ships:
        ships.remove([])    
        return True
    return False        

def checkHit(action, ships, board):
    for i in range(len(ships)):
        for j in range(len(ships[i])):
            if action in ships[j]:
                board[action[0]][action[1]] = 2
                ships[j].remove(action)
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
            elif i >=4:
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
        
def monteCarlo(action, ships, board, e, w, h, gamma):
    global records, q
    if checkSunk(ships):
        # update q table
        g = 10
        for i in records:
            print(i)
            q[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]][i[7]][i[8]] = g
            g = gamma*g -1
        records = [] # reset 
        if checkWin(ships):
            return True, board
        return False, board
    
    state = getState(action, board, w, h)
    # use e soft to get action
    # we have the state (action)
    # should be list of 8 actions
    myActions = getActions(state)
    actionInd = eSoft(myActions,e)
    records.append(state.append(actionInd))
    myY = int(actionInd/3)
    myX = actionInd%3
    oldAction = [0,0]
    oldAction[0] = action[0]
    oldAction[1] = action[1]
    if myX == 0:
        action[1] += 1
    elif myX == 1:
        action[1] += 0
    elif myX == 2:
        action[1] -= 1 
    if myY == 0:
        action[0] += 1*w
    elif myY == 1:
        action[0] += 0*w
    elif myY == 2:
        action[0] -= 1*w
    
    # have new action
    if checkHit(action, ships, board):
        return monteCarlo(action, ships, board, e, w, h, gamma)
    else:
        board[myY][myX] = 1
        return monteCarlo(oldAction, ships, board, e, w, h, gamma)
        
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
            #pick random action
            action = random.choice(tuple(actionSet))
            actionSet.remove(action)
            y = int(action/w)
            x = action%h
            hit = checkHit([y,x], ships, board)
            state = getState([x,y], board, w, h)
            if hit:
                # will return ~3 times, last time win should be true
                win, board = monteCarlo([y,x], ships, board, e, w, h, gamma)                
            else:
                board[y][x] = 1    
        if i == forever - 1:
            return board
            
             

def main():
    w = 5
    h = 5
    forever = 1000
    board = play(forever, w, h)
    for i in board:
        print(i)

main()
