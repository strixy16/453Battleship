import numpy as np
import random

class Agent:
	def __init__(self,h,w):
		self.ships = setShips(h,w)
		self.q = np.zeros(shape=(3,3,3,3,3,3,3,3,8))
		self.enemyBoard = np.full((h,w), 'u')

def setShips(h, w):
	shipLen = [2,2,2]
	squares = {i for i in range(h * w)}
	ships = []

	while shipLen:
		shipIndex = random.randint(0, len(shipLen) - 1)
		shipToPlace = shipLen[shipIndex]
		placed = False
		while not placed:
			sSquare = random.choice(tuple(squares))
			directions = {-1, 1, w, -w}	
			while directions:
				d = random.choice(tuple(directions))
				tempB = True
				for i in range(1, shipToPlace + 1):
					tempB = tempB and ((sSquare + d * i) in squares)
					if d == 1: #not very elegant
						if (sSquare + d*i) % h == 0:
							tempB = False
							break
					elif d == -1:
						if (sSquare + d*i + 1) % h == 0:
							tempB = False
							break
				if tempB:
					tempA = []
					for i in range(1, shipToPlace + 1):
						tempA.append(sSquare + d * i)
						squares.remove(sSquare + d * i)
					ships.append(tempA)
					placed = True
					break
				else:
					directions.remove(d)
		del(shipLen[shipIndex])
	
	return(ships)

