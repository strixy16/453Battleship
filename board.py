import tkinter as tk
from math import floor

master = tk.Tk()
canvas_width = master.winfo_screenwidth()*(3/4)
canvas_height = master.winfo_screenheight()*(3/4)
window = tk.Canvas(master, width=canvas_width, height=canvas_height)

def tkinterInit():
	global master
	master.geometry("+%d+%d" % (master.winfo_screenwidth()/2 - canvas_width/2, master.winfo_screenheight()/2 - canvas_height/2))

#initialize the starting board
def bInit(p1, p2, h, w): #p1 and p2 are classes of type Agent, will probably change in the future to just take the array of ship locations
	#tkinter setup
	global master, window
	
	#the height and width of a square
	rHeight = min(canvas_height, canvas_width/2) * (3 / 4) / h
	
	#height at which the grid starts
	gridStartH = (canvas_height / 2) - ((rHeight * h) / 2)
	#starting xPos for the left and right grids
	lGridStartW = ((canvas_width / 4) - 10) - ((rHeight * w) / 2) #10 because the separator (black line) is 20 
	rGridStartW = ((canvas_width * 3 / 4) + 10) - ((rHeight * w) / 2)
	
	#draw ships for player 1
	for i in range(h):
		yPos = gridStartH + i*rHeight
		for j in range(w):
			xPos = lGridStartW + j*rHeight
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,outline='black')
	
	for i in range(len(p2.ships)):
		for j in range(len(p2.ships[i])):
			xPos = lGridStartW + ((p2.ships[i][j][1] * rHeight))
			yPos = gridStartH + (p2.ships[i][j][0] * rHeight)
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,fill='#00e0f0')

	#separator for the a e s t h e t i c c 
	window.create_line(canvas_width/2,0,canvas_width/2,canvas_height, width=20)
	
	#draw ships for player 2
	for i in range(h):
		yPos = gridStartH + i*rHeight
		for j in range(w):
			xPos = rGridStartW + j*rHeight
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,outline='black')

	for i in range(len(p1.ships)):
		for j in range(len(p1.ships[i])):
			xPos = rGridStartW + ((p1.ships[i][j][1] * rHeight))
			yPos = gridStartH + (p1.ships[i][j][0] * rHeight)
			window.create_rectangle(xPos, yPos, xPos+rHeight, yPos+rHeight, fill='#bc4fff')

	window.pack()

def drawBoard(b1, b2, h, w):
	global window
	window.delete("all")
	rHeight = min(canvas_height, canvas_width/2) * (3 / 4) / h
	
	#height at which the grid starts
	gridStartH = (canvas_height / 2) - ((rHeight * h) / 2)
	#starting xPos for the left and right grids
	lGridStartW = ((canvas_width / 4) - 10) - ((rHeight * w) / 2) #10 because the separator (black line) is 20 
	rGridStartW = ((canvas_width * 3 / 4) + 10) - ((rHeight * w) / 2)
	
	for i in range(h):
		yPos = gridStartH + i*rHeight
		for j in range(w):
			xPos = lGridStartW + j*rHeight
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,outline='black')
	
	yPos = gridStartH
	xPos = lGridStartW
	for i in range(h):
		yPos = gridStartH + i*rHeight
		for j in range(w):
			xPos = lGridStartW + j*rHeight
			if b1[i][j] == 1:
				window.create_oval(xPos, yPos, xPos+rHeight, yPos+rHeight, outline='black')
			elif b1[i][j] == 2:
				window.create_line(xPos, yPos, xPos+rHeight, yPos+rHeight, fill='red')
				window.create_line(xPos+rHeight, yPos, xPos, yPos+rHeight, fill='red')
	
	
	for i in range(h):
		yPos = gridStartH + i*rHeight
		for j in range(w):
			xPos = rGridStartW + j*rHeight
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,outline='black')
	
	yPos = gridStartH
	xPos = rGridStartW
	for i in range(h):
		yPos = gridStartH + i*rHeight
		for j in range(w):
			xPos = rGridStartW + j*rHeight
			if b2[i][j] == 1:
				window.create_oval(xPos, yPos, xPos+rHeight, yPos+rHeight, outline='black')
			elif b2[i][j] == 2:
				window.create_line(xPos, yPos, xPos+rHeight, yPos+rHeight, fill='red')
				window.create_line(xPos+rHeight, yPos, xPos, yPos+rHeight, fill='red')

	window.pack()

def tkMainLoop():
	tk.mainloop()
