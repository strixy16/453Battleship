import tkinter as tk
from math import floor

def bInit(p1, p2, h, w): #p1 and p2 are Board classes
	global master
	master = tk.Tk()
	canvas_width = master.winfo_screenwidth()*(3/4)
	canvas_height = master.winfo_screenheight()*(3/4)

	window = tk.Canvas(master, width=canvas_width, height=canvas_height)
	master.geometry("+%d+%d" % (master.winfo_screenwidth()/2 - canvas_width/2, master.winfo_screenheight()/2 - canvas_height/2))
	
	rHeight = min(canvas_height, canvas_width/2) * (3 / 4) / h

	gridStartH = (canvas_height / 2) - ((rHeight * h) / 2)
	lGridStartW = ((canvas_width / 4) - 10) - ((rHeight * w) / 2) #10 because the separator (black line) is 20 
	rGridStartW = ((canvas_width * 3 / 4) + 10) - ((rHeight * w) / 2)
	#player 1
	for i in range(h):
		yPos = gridStartH + i*rHeight
		for j in range(w):
			xPos = lGridStartW + j*rHeight
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,outline='black')
	
	for i in range(len(p1.ships)):
		for j in range(len(p1.ships[i])):
			xPos = lGridStartW + ((p1.ships[i][j] % h)*rHeight)
			yPos = gridStartH + (floor(p1.ships[i][j] / h)*rHeight)
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,fill='#00e0f0')

	window.create_line(canvas_width/2,0,canvas_width/2,canvas_height, width=20)
	#player 2
	for i in range(h):
		yPos = gridStartH + i*rHeight
		for j in range(w):
			xPos = rGridStartW + j*rHeight
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,outline='black') 
	
	for i in range(len(p2.ships)):
		for j in range(len(p2.ships[i])):
			xPos = rGridStartW + ((p2.ships[i][j] % h)*rHeight)
			yPos = gridStartH + (floor(p2.ships[i][j] / h)*rHeight)
			window.create_rectangle(xPos,yPos,xPos+rHeight,yPos+rHeight,fill='#bc4fff')

	window.pack()

	tk.mainloop()

		
