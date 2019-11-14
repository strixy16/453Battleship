import random
# assume we have the board and all of the ships

# make a policy (of 9 for each square)
num = 25 # width of board * height of board, get from Kenny's thing
w = 5
h = 5
policy = [[[0.125 for y in range(3)] for x in range(3)] for z in range(num)]
for i in policy:
    i[1][1] = 0 # middle one is 0, only access when middle is hit


qTable = dict() # key = state, value = [action1, action2,..., action8]
# just store as they occur? Start with 0? Will be tupples and linked list? ((state, action):value) = (([board],tile):value)

returns = dict() # will average for qTable
start = 0 # keeps track of where prev episode was in qTable/tracker

action = random.randint(0,num)
forever = 15000
mode = "random"
for i in range(forever):
    t = 0 # to keep track of steps
    # refreshes every time a game is won, keeps track of states and actions (probably don't need it since you keep track of t, the key)
    tracker = dict() # key = (state, action), value = t 
    while mode != "win":
        if mode == "random":
            # must convert action, maybe have a get function that converts and returns that slot?
            while board[action] != 'X' and board[action] != 'O':
                action = random.randint(0,num)

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
                temp = policy[w*j[0] + j[1]][newX, newY]
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
                target += a in i
            if target == 1: # hit
                mode = "target"
                    
        elif mode == "target": # have hit, action based on policy
            ### Need to change this based on e soft policy ####
            # THIS DOESNT TAKE MAX WITH ESOFT, MUST FIX, TOO TIRED TO DO IT NOW
            # state space is only 9 blocks around hit
            myPolicy = policy[x][y]
            tempPolicy = [0 for _ in range(9)]
            count = 0
            countIn = 0
            for j in myPolicy:
                for k in j:
                    count += k # cumulative percent
                    tempPolicy[countIn] = count
                    countIn += 1 # index of tempPolicy
                    
            chance = random.random()
            count = 0 # tracks index of tempPolicy
            for j in tempPolicy:
                if chance < j:
                    if count < 3:
                        tempX = x-1
                    elif count > 5:
                        tempX = x+1
                    else:
                        tempX = x
                    if count%3 == 0:
                        tempY = y-1
                    elif count%3 == 2:
                        tempY = y+1
                    else:
                        tempY = y
                    action = w*tempX + tempY # action of board frame of reference               
                    break
                count += 1
            # we have our action. Need to take action -> modifying policies, checking if sunk/hit/miss
            # if sunk, check win, else mode = "random"
            # board should notify if sunk
            if sunk: # SUNK IS NOT INITIALIZED
                # GET REWARD, PROPAGATE BACK UNTIL START
                if win:
                    mode = "win"
                else:
                    mode = "random"
                
                # THESE MAY NEED TO BE CHANGED
                reward = 10 # for sinking. reward is -1 for everything else
                gamma = 0.9
                G = 0
                G = gamma*G + reward
                reward = -1
                for j in range(t, start, -1): # go backwards, calculate G
                    G = gamma*G + reward
                # have goal, state action will not have already appeared for this episode, can skip.
                
                # need to find terminating state and action. Will be t -> most recent state
                if tracker[t] in returns:
                    returns[tracker[t]].append(G)
                else:
                    returns[tracker[t]] = [G]
                # find out which square was hit on the 3x3    
                qTable[t][3*tempX + tempY] = statistics.mean(returns[tracker[t]])
                start = t
                # t increments below again
                
            
            # if hit ???? I have no clue
            elif hit:
                pass

            # if miss, adjust policy same as random
            # LITERALLY JUST COPY/PASTE. SHOULD PROBABLY MAKE INTO A FUNCTION
            # need to modify +-x, +-y and every combo thereof
            elif miss: # still use policy - MISS IS NOT INITIALIZED
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
                    temp = policy[w*j[0] + j[1]][newX, newY]
                    #policy[5*j[0] + j[1]] # neighbouring spot's policy
                    policy[w*j[0] + j[1]][newX][newY] = 0
                    for k in range(3):
                        for m in range(3):
                            hold = policy[w*j[0] + j[1]][k][m] # just to make it shorter
                            policy[w*j[0] + j[1]][k][m] = hold + temp*hold # modify each
                    summed = sum(sum(policy[w*j[0]+j[1]],[]))# summmed for normalization
                    policy[w*j[0] + j[1]] = [[p/summed for p in q] for q in policy[w*j[0] + j[1]]]             
                    # modifications should be done
                # must set x and y to be chosen coordinate if hit. If miss, stays the same
                    
           # store state and action in tracker, which records all 
           if board not in qTable: # only add new states for all
               # yikes
               qTable[str(board)] = [0,0,0,0,0,0,0,0] # all possible targets
            # add every single move to tracker
            tracker[t] = board 
            t += 1
