import random
# assume we have the board and all of the ships

# make a policy (of 9 for each square)
num = 25 # width of board * height of board, get from Kenny's thing
w = 5
h = 5
policy = [[[0.125 for y in range(3)] for x in range(3)] for z in range(num)]
for i in policy:
    i[1][1] = 0 # middle one is 0, only access when middle is hit
    
##for i in policy:
##    print(i)
action = random.randint(0,num)
forever = 15000
mode = "random"
for i in range(forever):
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
                
            t = 0
            for i in ships: # check if hit
                t += a in i
            if t == 1: # hit
                mode = "target"
                    
        elif mode == "target": # have hit, action based on policy
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
                # GET REWARD?
                mode = "random"
            
            # if hit ???? I have no clue
            if hit:
                pass

            # if miss, adjust policy same as random
            # LITERALLY JUST COPY/PASTE. SHOULD PROBABLY MAKE INTO A FUNCTION
            # need to modify +-x, +-y and every combo thereof
            if miss: # still use policy - MISS IS NOT INITIALIZED
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
                    
            
            
