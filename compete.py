import MC
import QL
from agents import Agent
import random
from statistics import mean
import matplotlib.pyplot as plt

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
		if not MC.checkHit([y,x], agent.ships, agent.enemyBoard):
			agent.enemyBoard[y][x] = 1		
		win = checkWin(agent.ships, agent.enemyBoard)
		actionSet.remove(action)

def totalMoves(board):
	tMoves = 0
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] != 0:
				tMoves += 1
	return tMoves

def plotWinPercent(a1Name, a2Name, a1Moves, a2Moves, episodes):
	a1WinPercent = []
	a2WinPercent = []
	eps = [ i for i in range(150,3001,150) ]
	
	for i in range(len(a1Moves)):
		a1WinSum = 0
		a2WinSum = 0
		for j in range(len(a1Moves[0])):
			if a1Moves[i][j] < a2Moves[i][j]:
				a1WinSum += 1
			elif a2Moves[i][j] < a1Moves[i][j]:
				a2WinSum += 1
			else:
				if random.random() >= 0.5:
					a1WinSum += 1
				else:
					a2WinSum += 1
		a1WinPercent.append((a1WinSum/len(a1Moves[0])))
		a2WinPercent.append((a2WinSum/len(a1Moves[0])))
	
	fig = plt.figure()
	g1 = fig.add_subplot(111) 
	g1.scatter(eps, a1WinPercent, c="r", marker = "s", label = a1Name)
	g1.scatter(eps, a2WinPercent, c="b", marker = "s", label = a2Name)
	plt.xlabel('Episodes')
	plt.ylabel('Win Rate')
	plt.title('Summary of ' + a1Name + ' and ' + a2Name + ' over episodes')
	plt.legend(loc="upper left")
	plt.show()

if __name__ == '__main__':
	mcAverageMoves = []
	qlAverageMoves = []
	rAverageMoves = []
	for i in range(50,1001,50):
		aveMC = []
		aveQL = []
		aveR = []
		for j in range(20):
			b1 = MC.main(i)
			mcMoves = totalMoves(b1)
			aveMC.append(mcMoves)
			
			b2 = QL.main(i)
			qlMoves = totalMoves(b2)
			aveQL.append(qlMoves)
			
			rAgent = Agent(h,w)
			randomAgent(rAgent)
			rMoves = totalMoves(rAgent.enemyBoard)
			aveR.append(rMoves)

		mcAverageMoves.append(aveMC)
		qlAverageMoves.append(aveQL)
		rAverageMoves.append(aveR)
	plotWinPercent("MC", "QL", mcAverageMoves, qlAverageMoves, 1000)
	plotWinPercent("MC", "Random", mcAverageMoves, rAverageMoves, 1000)
	plotWinPercent("QL", "Random", qlAverageMoves, rAverageMoves, 1000)
	#tkinterInit()
	#drawBoard(b1, b2, h, w)
	#tkMainLoop()
