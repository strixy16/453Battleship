from board import Board, bInit
from agents import setShips

w = 10
h = 10

if __name__ == "__main__":
	agent1 = Board(h, w, setShips(h,w))
	agent2 = Board(h, w, setShips(h,w))
	bInit(agent1, agent2, h, w)
