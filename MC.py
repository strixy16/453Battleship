import random
import numpy as np
import statistics
# initialize all 
# assume we have the board and all of the ships

# make a policy (of 9 for each square)
num = 25 # width of board * height of board, get from Kenny's thing
w = 5
h = 5
epsilon = 0.05
policy = [[[0.125 for y in range(3)] for x in range(3)] for z in range(num)]
#allPolicies = [np.reshape(np.array(i), (3,3)) for i in itertools.product([0,1,2], repeat = 9)] # all possible combinations of the 3x3 board
q = np.zeros(shape=(3,3,3,3,3,3,3,3,8))
returns = np.zeros(shape = (3,3,3,3,3,3,3,3,8,1)) # holds all G values for a given action/state
for i in policy:
    i[1][1] = 0 # middle one is 0, only access when middle is hit


#qTable = dict() # key = state, value = [action1, action2,..., action8]
# just store as they occur? Start with 0? Will be tupples and linked list? ((state, action):value) = (([board],tile):value)

#returns = dict() # will average for qTable
start = 0 # keeps track of where prev episode was in qTable/tracker

action = random.randint(0,num)
forever = 15000
mode = "random"
for i in range(forever):
    tracker = [] # keeps track of policies
    trackAction = [] # tracks actions taken
    t = 0 # to keep track of steps
    # refreshes every time a game is won, keeps track of states and actions (probably don't need it since you keep track of t, the key)
    possibleStates = [i for i in range(num)]
    while mode != "win":
        if mode == "random":
            # must convert action, maybe have a get function that converts and returns that slot?
            action = random.choice(possibleStates)
            possibleStates.remove(action)
            # change policy to 0 for this square, modify surrounding ones too
            x = int(action/w)
            y = action%h
            # need to modify +-x, +-y and every combo thereof
            neighbours = [[x-1, y-1],[x-1,y],[x-1, y+1],
                          [x,y-1],[x, y+1],[x+1, y-1],[x+1, y],[x+1, y+1]]
            for j in neighbours:
                if j[0] >= 0 and j[0] < w and j[1] >= 0 and j[1] < h:
                    if j[0] == x-1:
                        newX = x + 1
                    elif j[0] == x+1:
                        newX = x - 1
                    elif j[0] == x:
                        newX = x
                    if j[1] == y-1:
                        newY = y + 1
                    elif j[1] == y+1:
                        newY = y - 1
                    elif j[1] == y:
                        newY = y
                # the policy for a place for all its neighbours
                temp = policy[w*j[0] + j[1]][newX][newY]
                #policy[5*j[0] + j[1]] # neighbouring spot's policy
                policy[w*j[0] + j[1]][newX][newY] = 0
                for k in range(3):
                    for m in range(3):
                        hold = policy[w*j[0] + j[1]][k][m] # just to make it shorter
                        policy[w*j[0] + j[1]][k][m] = hold + temp*hold # modify each
                summed = sum(sum(policy[w*j[0]+j[1]],[]))# summmed for normalization
                policy[w*j[0] + j[1]] = [[p/summed for p in q] for q in policy[w*j[0] + j[1]]]             
                # modifications should be done
                
            target = 0
            for i in ships: # check if hit MAY NOT BE NECESSARY!!!
                target += action in i
            if target == 1: # hit
                mode = "target"
                
                    
        elif mode == "target": # have hit, action based on max QValue - all 0s initially
            
            # state space is only 9 blocks around hit
            # get board
            b = getBoard(x,y) # ASSUME RETURNS 1x8 BOARD *padding = miss
            if [0] not in b:
                print("U fuked up")
            ##            qState = q[b[0]][b[1]][b[2]][b[3]][b[4]][b[5]][b[6]][b[7]] # values for all 8 actions of a given state
##            action = qState.index(max(qState))
            
            # get action based on policy (do this until sunk)
            myPolicy = policy[x][y]
            tempPolicy = [0 for _ in range(9)]
            count = 0
            countIn = 0
            for j in myPolicy:
                for k in j:
                    count += k # cumulative percent
                    tempPolicy[countIn] = count
                    countIn += 1 # index of tempPolicy

                    
            #action = max(qTable[str(board)])
            
            chance = random.random()
            index = 0
            # find where in tempPolicy chance falls in
            for i in tempPolicy:
                if chance > i:
                    break
                index += 1

            # convert action to board action
            base = x*w + y
            # convert mini policy to add or subtract
            tempX = int(index/3)
            tempY = index % 3
            # [x,y] is at [1,1]
            if tempX < 1: # 1 row up
                base = base - w
            elif tempX > 1:
                base = base + w
            if tempY > 1:
                base = base + 1
            elif tempY < 1:
                base = base - 1
            action = base # now in board reference
            
            ################
            # deleted code
            ################
            # we have our action. Need to take action -> modifying policies, checking if sunk/hit/miss
            # if sunk, check win, else mode = "random"
            # board should notify if sunk
            if sunk: # SUNK IS NOT INITIALIZED ### MAYBE CHECK AGAINST SHIPS? FIGURE OUT DURING INTEGRATION
                # GET REWARD, PROPAGATE BACK UNTIL START
                if win: # KEEP COUNTER OF SHIPS SUNK?
                    mode = "win"
                #### FIGURE OUT LATER
##                elif hit but not sunk:
##                    x = placeHitX
##                    y = placeHitY
                else:
                    # check if elsewhere hit
                    mode = "random"
                
                # THESE MAY NEED TO BE CHANGED
                actionReward = 10 # for sinking. reward is -1 for everything else
                # don't need to calculate, 1st one is just reward of 10
                G = 10
                # append to rewards
                returns[[b[0]][b[1]][b[2]][b[3]][b[4]][b[5]][b[6]][b[7]][b[index]]].append(G)
                gamma = 0.9
               
                actionReward = -1
                for j in range(t-1, start, -1): # go backwards, calculate G
                    k = tracker[j]
                    G = gamma*G + actionReward
                    returns[k[0]][k[1]][k[2]][k[3]][k[4]][k[5]][k[6]][k[7]][k[8]].append(G)
                    ave = statistics.mean([k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7], k[8]])
                    q[k[0]][k[1]][k[2]][k[3]][k[4]][k[5]][k[6]][k[7]][k[8]] = ave
                    qState = q[k[0]][k[1]][k[2]][k[3]][k[4]][k[5]][k[6]][k[7]][k[8]]
                    argMax = qState.index(max(qState))
                    # Now we do e-greedy
                    for a in range(8):
                        myX = int(action/w)
                        myY = action%h
                        if a == argMax:
                            policy[myX][myY][a] = 1 - epsilon + (epsilon/8)
                        else:
                            policy[myX][myY][a] = epsilon/8
                            
                # have goal, state action will not have already appeared for this episode, can skip.
                
                start = t
            # if hit ???? I have no clue
            elif hit:
                x = int(action/w)
                y = action%y

            # if miss, nothing happens! x is still x, y is still y
            # LITERALLY JUST COPY/PASTE. SHOULD PROBABLY MAKE INTO A FUNCTION
            # need to modify +-x, +-y and every combo thereof
##            elif miss: # still use policy - MISS IS NOT INITIALIZED
##                neighbours = [[x-1, y-1],[x-1,y],[x-1, y+1],
##                              [x,y-1],[x, y+1],[x+1, y-1],[x+1, y],[x+1, y+1]]
##                for j in neighbours:
##                    if j[0] >= 0 and j[0] < w and j[1] >= 0 and j[1] < h:
##                        if j[0] == x-1:
##                            newX = x + 1
##                        elif j[0] == x+1:
##                            newX = x - 1
##                        elif j[0] == x:
##                            newX = x
##                        if j[1] == y-1:
##                            newY = y + 1
##                        elif j[1] == y+1:
##                            newY = y - 1
##                        elif j[1] == y:
##                            newY = y
##                    # the policy for a place for all its neighbours
##                    temp = policy[w*j[0] + j[1]][newX, newY]
##                    #policy[5*j[0] + j[1]] # neighbouring spot's policy
##                    policy[w*j[0] + j[1]][newX][newY] = 0
##                    for k in range(3):
##                        for m in range(3):
##                            hold = policy[w*j[0] + j[1]][k][m] # just to make it shorter
##                            policy[w*j[0] + j[1]][k][m] = hold + temp*hold # modify each
##                    summed = sum(sum(policy[w*j[0]+j[1]],[]))# summmed for normalization
##                    policy[w*j[0] + j[1]] = [[p/summed for p in q] for q in policy[w*j[0] + j[1]]]             
##                    # modifications should be done
                # must set x and y to be chosen coordinate if hit. If miss, stays the same
                    
           # store state and action in tracker, which records all 
            # add every single move to tracker
            tracker[t] = [[b[0]][b[1]][b[2]][b[3]][b[4]][b[5]][b[6]][b[7]][b[index]]]
            trackerAction[t] = action
            t += 1
