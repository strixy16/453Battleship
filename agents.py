import numpy as np
import random

class Agent:
	def __init__(self,h,w):
		self.ships = setShips(h,w) #positions of the ships, array shape = (3,2)
		self.q = np.zeros(shape=(3,3,3,3,3,3,3,3,8)) #general 3x3 policy
		self.enemyBoard = np.zeros((h,w)) #what we know about the enemy board, everything is unchecked to start

def setShips(h, w):
	shipLen = [2,2,2] #length of every ship
	squares = {i for i in range(h * w)} #we make a set of every tile, and when we place a ship we remove the positions from the set.
	ships = [] #positions of the ships, shape=(3,2)

	while shipLen:
		shipIndex = random.randint(0, len(shipLen) - 1) #randomly get the index of a ship we want to place
		shipToPlace = shipLen[shipIndex] #shipToPlace is the length of the ship we will place
		placed = False 
		while not placed:
			sSquare = random.choice(tuple(squares)) #starting square, we place each ship one square at a time
			directions = {-1, 1, w, -w}	#directions to place the next square of the ship
			while directions: #while we have not tried to place the next square in every direction
				d = random.choice(tuple(directions)) #get random direction
				tempB = True #temporary boolean to check if placing the next square is legal
				for i in range(1, shipToPlace + 1): #we use 1 as the initial value because we are placing the square of the ship 1 tile away
					tempB = tempB and ((sSquare + d * i) in squares) #check if legal move
					if d == 1: #if we are placing towards the right, and try to place on the leftmost square 1 row down, not a legal move
						if (sSquare + d*i) % h == 0:
							tempB = False
							break
					elif d == -1: #same idea as above but opposite scenario
						if (sSquare + d*i + 1) % h == 0:
							tempB = False
							break
				if tempB: #if we do place every square of the ship
					tempA = [] #temporary array we will append to ships
					for i in range(1, shipToPlace + 1):
						tempA.append(sSquare + d * i) #appending the positions of each square
						squares.remove(sSquare + d * i) #removing the tiles from the set 
					ships.append(tempA)
					placed = True
					break
				else:
					directions.remove(d) 
		del(shipLen[shipIndex]) 
	
	return(ships)

