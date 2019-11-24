from board import bInit, tkinterInit, drawBoard, tkMainLoop
from agents import Agent

#dimensions of the board
w = 5
h = 5

b1 = [[0,0,0,2,0],[1,2,0,0,1],[0,2,2,0,1],[1,1,1,2,0],[0,2,0,2,1]]
b2 = [[1,0,2,0,1],[2,2,2,2,2],[1,1,1,1,1],[0,0,0,0,0],[1,2,1,2,1]]

if __name__ == "__main__":
	agent1 = Agent(h, w)
	agent2 = Agent(h, w)
	tkinterInit()
	#bInit(agent1, agent2, h, w)
	drawBoard(b1, b2, h, w)
	tkMainLoop()
