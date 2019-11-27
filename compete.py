import MC
import QL
from board import tkinterInit, drawBoard, tkMainLoop
from agents import Agent
import random

h = 15
w = 15

def checkWin(ships, board):
	win = True
	for i in range(len(ships)):
		for j in range(len(ships[i])):
			win = win and board[ships[i][j][0]][ships[i][j][1]] == 2
	return win

def randomAgent(agent):
	win = False
	actionSet = { i for i in range(w*h)}
	while not win:
		action = random.choice(tuple(actionSet))
		y = int(action/h)
		x = action % w
		if not MC2.checkHit([y,x], agent.ships, agent.enemyBoard):
			agent.enemyBoard[y][x] = 1		
		win = checkWin(agent.ships, agent.enemyBoard)
		actionSet.remove(action)
	
if __name__ == '__main__':
	b1 = MC.main()
	b2 = QL.main()
	rAgent = Agent(h,w)
	randomAgent(rAgent)
	print(rAgent.enemyBoard)
	tkinterInit()
	drawBoard(b1, b2, h, w)
	tkMainLoop()
