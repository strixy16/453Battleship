from MC2 import checkSunk

def ranodomAgent(h, w, ships, board):
    actionSet = [ i for i in range(h * w) ]
    sunkShips = 0
    while sunkShips != len(ships)
        action = random(tuple(actionSet))
        y = int(action/h)
        x = action % w
        if checkSunk([y,x], ships, board):
            sunkShips += 1
        actionSet.remove(action)
    
