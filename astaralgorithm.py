'''
    File name: astaralgorithm.py
    Author: Trevor Tomlin
    Date created: 4/7/2020
    Date last modified: 4/7/2020
    Python Version: 3.7.3
'''

import pygame
import math

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

display_width = 800
display_height = 800
menu_bar_size = 300

grid_size = 10
line_width = 5
line_color = BLACK


class Grid():

	def __init__(self, size=None):
		self.size = size
		self.nodes = []

	def draw(self, screen):

		sizeInterval = int(display_height / grid_size)

		for node in self.nodes:
			node.draw(sizeInterval, screen)
	
		for x in range(0, grid_size + 1):
			pygame.draw.line(screen, line_color, (x * sizeInterval, 0), (x * sizeInterval, display_height), 5)
		for x in range(0, grid_size + 1 ):
			pygame.draw.line(screen, line_color, (0 , x * int(display_width / grid_size)), (display_height, x * sizeInterval), 5)

	def button_handler(self, screen, color):
		mousePos = pygame.mouse.get_pos()
		col = math.ceil(mousePos[0] / (display_height / grid_size)) - 1
		row = math.ceil(mousePos[1] / (display_height / grid_size)) - 1

		#print("mouse at", col, row)
		try:
			if self.nodes[col + (grid_size * row)].color == WHITE:
				self.nodes[col + (grid_size * row)].color = color

			elif self.nodes[col + (grid_size * row)].color == color:
				self.nodes[col + (grid_size * row)].color = WHITE	
		except:
  			print("Out of bounds") 

class Node():

	def __init__(self, parent=None, position=None, color=WHITE):
		self.parent = parent
		self.position = position
		self.neighbors = []
		self.color = color

		self.g = 0
		self.h = 0
		self.f = 0


	def setF(self):
		self.f = self.h + self.g

	def setColor(self, color):
		self.color = color 

	def draw(self, sizeInterval, screen):
		pygame.draw.rect(screen, self.color, (self.position[0] * sizeInterval, self.position[1] * sizeInterval, display_height / grid_size, display_height / grid_size))



def main():

	pygame.init()
	pygame.display.set_caption("A* Algorithm")
	screen = pygame.display.set_mode((display_width, display_height + menu_bar_size))
	screen.fill(BLACK)
	clock = pygame.time.Clock()

	grid = Grid(grid_size)
	initializeGrid(grid)

	running = True

	while running:

		grid.draw(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				grid.button_handler(screen, RED)


		pygame.display.update()
		clock.tick(60)

def initializeGrid(grid):
	for j in range(grid.size):
		for i in range(grid.size):
			node = Node(None, (i,j))
			grid.nodes.append(node)
			#print(node.position)


if __name__ == "__main__":
	main()

'''

def main():

	#Size in pixels of window
	display_width = 1000
	display_height = 1000

	#Number of squares for the sidelenghts
	square_dividers = 10
	
	#Pygame setup
	pygame.init()
	pygame.display.set_caption("A* Algorithm")
	screen = pygame.display.set_mode((display_width, display_height))
	screen.fill((255,255,255))
	clock = pygame.time.Clock()
	tiles = generate_tile_array(square_dividers)

	running = True

	#Starting message boxes
	distSelect = easygui.ynbox("Please select the distance method.", "A* Algorithm", ("Euclidean Distance", "Manhattan Distance"))
	easygui.msgbox("Please select the STARTING point for the A* Algorithm and press ENTER when you are finished", "A* Algorithm")

	#Determines which point the user is selecting
	selectingStart = True
	selectingEnd = False
	selectingWall = False

	#Handles gui messages
	sentEndMsg = False
	sentWallMsg = False

	#Check to see if user input is valid
	validTile = False
	startFound = False
	endFound = False

	while running:

		#Sends messages after selecting stages
		if selectingEnd == True and sentEndMsg == False:
			easygui.msgbox("Please select the ENDING point for the A* Algorithm and press ENTER when you are finished.", "A* Algorithm")
			sentEndMsg = True

		if selectingWall == True and sentWallMsg == False:
			easygui.msgbox("Please select the WALLS for the A* Algorithm and press ENTER when you are finished to START THE ALGORITHM.", "A* Algorithm")
			sentWallMsg = True
		
		#Colors the tiles and draws black lines
		fill_tiles(screen, square_dividers, tiles)
		draw_lines(screen, square_dividers)

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False

			#Determines what square the mouse is on and colors it
			if event.type == pygame.MOUSEBUTTONDOWN and selectingStart:
				button_handler(tiles, square_dividers, screen, 1)

			if event.type == pygame.MOUSEBUTTONDOWN and selectingEnd:
				button_handler(tiles, square_dividers, screen, 2)

			if event.type == pygame.MOUSEBUTTONDOWN and selectingWall:
				button_handler(tiles, square_dividers, screen, 3)

			#Checks if the user presses ENTER and determines what they are selecting
			if event.type == pygame.KEYDOWN:

				if pygame.K_RETURN:

					#User is selecting start node
					if selectingStart == True:
						if check_valid_tile(tiles, 0):
							selectingStart = False
							selectingEnd = True
							start = find_start(tiles)
						else:
							easygui.msgbox("1 STARTING point required! ", "A* Algorithm")

					#User is selecting end node
					elif selectingEnd == True:
						if check_valid_tile(tiles, 1):
							selectingEnd = False
							selectingWall = True
							end = find_end(tiles)
						else:
							easygui.msgbox("1 ENDING point required! ", "A* Algorithm")

					#User is selected wall node(s)
					elif selectingWall == True:
						selectingWall = False

						#Stars the pathfinding algorithm and draws the path
						path = a_star(tiles, start, end, distSelect, screen)
						if path != None:
							drawPath(path, tiles)				


		pygame.display.update()

		clock.tick(60)

#Draws black grid lines on screen
def draw_lines(screen, size):

	line_color = (0,0,0)
	
	sizeInterval = int(screen.get_height() / size)
	
	for x in range(0, size):
		pygame.draw.line(screen, line_color, (x * sizeInterval, 0), (x * sizeInterval, screen.get_height()), 5)
	for x in range(0, size):
		pygame.draw.line(screen, line_color, (0 , x * int(screen.get_width() / size)), (screen.get_height(), x * sizeInterval), 5)

#Colors tiles that need to be colored
def fill_tiles(screen, size, tiles):

	sizeInterval = int(screen.get_height() / size)

	for rowNum, row in enumerate (tiles):

		for tileNum, tile in enumerate (row):

			if tiles[rowNum][tileNum] == 0:
				pygame.draw.rect(screen, (255,255,255), (tileNum * sizeInterval, rowNum * sizeInterval, screen.get_height() / size, screen.get_height() / size))
			if tiles[rowNum][tileNum] == 1:
				pygame.draw.rect(screen, (0,255,0), (tileNum * sizeInterval, rowNum * sizeInterval, screen.get_height() / size, screen.get_height() / size))
			if tiles[rowNum][tileNum] == 2:
				pygame.draw.rect(screen, (255,0,0), (tileNum * sizeInterval, rowNum * sizeInterval, screen.get_height() / size, screen.get_height() / size))
			if tiles[rowNum][tileNum] == 3:
				pygame.draw.rect(screen, (100,100,100), (tileNum * sizeInterval, rowNum * sizeInterval, screen.get_height() / size, screen.get_height() / size))
			if tiles[rowNum][tileNum] == 4:
				pygame.draw.rect(screen, (0,0,255), (tileNum * sizeInterval, rowNum * sizeInterval, screen.get_height() / size, screen.get_height() / size))
			if tiles[rowNum][tileNum] == 5:
				pygame.draw.rect(screen, (255,255,0), (tileNum * sizeInterval, rowNum * sizeInterval, screen.get_height() / size, screen.get_height() / size))

#Creates and array of 0's for the grid
def generate_tile_array(size):
	tileArray = []
	for x in range(0, size):
		row = []
		for x in range(0, size):
			row.append(0)
		tileArray.append(row)
	return(tileArray)

#Determines which square the mouse is in
def button_handler(tiles, size, screen, int):
	mousePos = pygame.mouse.get_pos()
	col = math.ceil(mousePos[0] / (screen.get_height() / size)) - 1
	row = math.ceil(mousePos[1] / (screen.get_height() / size)) - 1

	#print("mouse at", col, row)

	if tiles[row][col] == 0:
		tiles[row][col] = int

	elif tiles[row][col] == int:
		tiles[row][col] = 0

#Check if only one start and end point is found
def check_valid_tile(tiles, int):

	if int == 0:

		start = []	

		for rowNum, row in enumerate (tiles):
			for tileNum, tile in enumerate (row):
				if tiles[rowNum][tileNum] == 1:
					start.append(1)

		if len(start) == 0 or len(start) > 1:
			return 0
		else:
			return 1

	elif int == 1:

		end = []	

		for rowNum, row in enumerate (tiles):
			for tileNum, tile in enumerate (row):
				if tiles[rowNum][tileNum] == 2:
					end.append(1)

		if len(end) == 0 or len(end) > 1:
			return 0
		else:
			return 1

#Finds the start index
def find_start(tiles):
	start = ()
	for rowNum, row in enumerate (tiles):
		for tileNum, tile in enumerate (row):
			if tiles[rowNum][tileNum] == 1:
				start = (rowNum, tileNum)

	if len(start) != 0:
		return start
	else:
		return 0

#Finds the end index
def find_end(tiles):
	end = ()
	for rowNum, row in enumerate (tiles):
		for tileNum, tile in enumerate (row):
			if tiles[rowNum][tileNum] == 2:
				end = (rowNum, tileNum)

	if len(end) != 0:
		return end
	else:
		return 0

class Node():

	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position
		self.neighbors = []

		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, other):
		return self.position == other.position

#Finds a maximum of 9 neighbors of a node
def find_neighbors(current_Node, tiles):

	neighbors = []

	#Top Left Node
	if current_Node.position[0] - 1 >= 0 and current_Node.position[1] - 1 >= 0:

		if (tiles[current_Node.position[0] - 1][current_Node.position[1] - 1] != 3):

			if (tiles[current_Node.position[0] - 1][current_Node.position[1] - 1] != 1 and tiles[current_Node.position[0] - 1][current_Node.position[1] - 1] != 2):

				tiles[current_Node.position[0] - 1][current_Node.position[1] - 1] = 5

			newPosition = (current_Node.position[0] - 1, current_Node.position[1] - 1)
			n1 = Node(current_Node, newPosition)
			neighbors.append(n1)

	#Top Middle Node
	if current_Node.position[0] - 1 >= 0:

		if (tiles[current_Node.position[0] - 1][current_Node.position[1]] != 3):

			if (tiles[current_Node.position[0] - 1][current_Node.position[1]] != 1 and tiles[current_Node.position[0] - 1][current_Node.position[1]] != 2):

				tiles[current_Node.position[0] - 1][current_Node.position[1]] = 5

			newPosition = (current_Node.position[0] - 1, current_Node.position[1])
			n2 = Node(current_Node, newPosition)
			neighbors.append(n2)

	#Top Right Node
	if current_Node.position[0] - 1 >= 0 and current_Node.position[1] + 1 < len(tiles):

		if (tiles[current_Node.position[0] - 1][current_Node.position[1] + 1] != 3):

			if (tiles[current_Node.position[0] - 1][current_Node.position[1] + 1] != 1 and tiles[current_Node.position[0] - 1][current_Node.position[1] + 1] != 2):

				tiles[current_Node.position[0] - 1][current_Node.position[1] + 1] = 5

			newPosition = (current_Node.position[0] - 1, current_Node.position[1] + 1)
			n3 = Node(current_Node, newPosition)
			neighbors.append(n3)

	#Middle Left Node
	if current_Node.position[1] - 1 >= 0:

		if (tiles[current_Node.position[0]][current_Node.position[1] - 1] != 3):

			if (tiles[current_Node.position[0]][current_Node.position[1] - 1] != 1 and tiles[current_Node.position[0]][current_Node.position[1] - 1] != 2):

				tiles[current_Node.position[0]][current_Node.position[1] - 1] = 5

			newPosition = (current_Node.position[0], current_Node.position[1] - 1)
			n4 = Node(current_Node, newPosition)
			neighbors.append(n4)

	#Middle Right Node
	if current_Node.position[1] + 1 < len(tiles):

		if (tiles[current_Node.position[0]][current_Node.position[1] + 1] != 3):

			if (tiles[current_Node.position[0]][current_Node.position[1] + 1] != 1 and tiles[current_Node.position[0]][current_Node.position[1] + 1] != 2):

				tiles[current_Node.position[0]][current_Node.position[1] + 1] = 5

			newPosition = (current_Node.position[0], current_Node.position[1] + 1)
			n5 = Node(current_Node, newPosition)
			neighbors.append(n5)

	#Bottom Left Node
	if current_Node.position[0] + 1 < len(tiles) and current_Node.position[1] - 1 >= 0:

		if (tiles[current_Node.position[0] + 1][current_Node.position[1] - 1] != 3):

			if (tiles[current_Node.position[0] + 1][current_Node.position[1] - 1] != 1 and tiles[current_Node.position[0] + 1][current_Node.position[1] - 1] != 2):

				tiles[current_Node.position[0] + 1][current_Node.position[1] - 1] = 5

			newPosition = (current_Node.position[0] + 1, current_Node.position[1] - 1)
			n6 = Node(current_Node, newPosition)
			neighbors.append(n6)

	#Bottom Middle Node
	if current_Node.position[0] + 1 < len(tiles):

		if (tiles[current_Node.position[0] + 1][current_Node.position[1]] != 3):

			if (tiles[current_Node.position[0] + 1][current_Node.position[1]] != 1 and tiles[current_Node.position[0] + 1][current_Node.position[1]] != 2):

				tiles[current_Node.position[0] + 1][current_Node.position[1]] = 5

			newPosition = (current_Node.position[0] + 1, current_Node.position[1])
			n7 = Node(current_Node, newPosition)
			neighbors.append(n7)

	#Bottom Right Node
	if current_Node.position[0] + 1 < len(tiles) and current_Node.position[1] + 1 < len(tiles):

		if (tiles[current_Node.position[0] + 1][current_Node.position[1] + 1] != 3):

			if (tiles[current_Node.position[0] + 1][current_Node.position[1] + 1] != 1 and tiles[current_Node.position[0] + 1][current_Node.position[1] + 1] != 2):

				tiles[current_Node.position[0] + 1][current_Node.position[1] + 1] = 5

			newPosition = (current_Node.position[0] + 1, current_Node.position[1] + 1)
			n8 = Node(current_Node, newPosition)
			neighbors.append(n8)

	return(neighbors)

#Distance function for algorithm
def heuristic(current_Node, end_Node, distSelect):

	#Euclidean
	if distSelect:
		a = (current_Node.position[0] - end_Node.position[0])**2
		b = (current_Node.position[1] - end_Node.position[1])**2
		c = int(10 * math.sqrt(a + b))
		#print(c)
		return(c)
		#print("current_Node pos", current_Node.position, "end_Node pos", end_Node.position)
		#a = (current_Node.position[0] - end_Node.position[0])**2
		#b = (current_Node.position[1] - end_Node.position[1])**2
		#c = int(math.floor(10 * math.sqrt(a + b)))
		#c = int(10 * math.sqrt(a + b))
		#print(a,b,c)
		#return c

	#Manhattan
	elif not distSelect:

		dstX = abs(current_Node.position[0] - end_Node.position[0])
		dstY = abs(current_Node.position[1] - end_Node.position[1])

		if (dstX > dstY):
			return 14*dstY + 10* (dstX-dstY)
		return 14*dstX + 10 * (dstY-dstX)


		#dX = abs(current_Node.position[0] - end_Node.position[0])
		#dY = abs(current_Node.position[1] - end_Node.position[1])
		#return 10 * (dX + dY)


def a_star(tiles, start, end, distSelect):

	#Initilizes lists and start and end nodes
	openList = []
	closedList = []
	
	start_Node = Node(None, start)
	start_Node.g = 0

	end_Node = Node(None, end)
	end_Node.g = end_Node.h = end_Node.f = 0 

	start_Node.h = heuristic(start_Node, end_Node, distSelect)
	start_Node.f = start_Node.g + start_Node.h
	#print(start_Node.f)

	current_Node = start_Node

	openList.append(current_Node)

	#while (len(openList) > 0):
	while end_Node not in closedList:

		if len(openList) == 0:
			return None

		current_Node = openList[0]
		current_Index = 0

		#Finds node with lowest F score in openList
		for index, node in enumerate(openList):
			if node.f < current_Node.f:
				current_Index = index
				current_Node = openList[current_Index]

		openList.remove(current_Node)
		closedList.append(current_Node)

		#If the algorithm found the end return the path
		if current_Node == end_Node:
			path = []
			current = current_Node
			while current is not None:
				path.append(current.position)
				current = current.parent
			return path[::-1]

		neighbors = find_neighbors(current_Node, tiles)

		#Determine F scores of neighbors and find best path
		for neighbor in neighbors:

			if neighbor not in closedList and neighbor not in openList:					

					openList.append(neighbor)

					neighbor.parent = current_Node

					neighbor.g = current_Node.g + heuristic(neighbor, current_Node, distSelect)
					neighbor.h = heuristic(neighbor, end_Node, distSelect)
					neighbor.f = neighbor.h + neighbor.g

			elif neighbor in openList:
				#print("neighbor.position: ", neighbor.position)
				#print("neighbor.g: ", neighbor.g)
				#print("neighbor heuristic", heuristic(neighbor, start_Node, distSelect))
				
				if neighbor.g < (neighbor.parent.g + heuristic(neighbor, neighbor.parent, distSelect)):
					neighbor.parent = current_Node
					neighbor.g = neighbor.parent.g + heuristic(neighbor, neighbor.parent, distSelect)
					neighbor.f = neighbor.h + neighbor.g
				
				if neighbor.g < current_Node.g:
					neighbor.parent = current_Node
					neighbor.g = current_Node.g + heuristic(neighbor, current_Node, distSelect)
					neighbor.f = neighbor.h + neighbor.g

			print("pos:", neighbor.position,"parent pos:", neighbor.parent.position,"currentNode g:", current_Node.g,"g:", neighbor.g, "h:", neighbor.h, "f:", neighbor.f, neighbor in openList)


		#openList.remove(current_Node)
		#closedList.append(current_Node)


def a_star(tiles, start, end, distSelect, screen):

	start_Node = Node(None, start)
	end_Node = Node(None, end)

	start_Node.g = 0
	start_Node.h = heuristic(start_Node, end_Node, distSelect)
	start_Node.f = start_Node.g + start_Node.h

	end_Node.g = end_Node.h = end_Node.f = 0 

	openSet = []
	closedSet = []

	openSet.append(start_Node)

	while(len(openSet) > 0):

		node = openSet[0]
		for index in range(len(openSet)):
			if (openSet[index].f < node.f or openSet[index].f == node.f):
				if (openSet[index].h < node.h):
					node = openSet[index]

		openSet.remove(node)
		closedSet.append(node)

		if (node == end_Node):
			path = []
			current = node
			while current is not None:
				path.append(current.position)
				current = current.parent
			return path[::-1]

		neighbors = find_neighbors(node, tiles)

		for neighbor in neighbors:

			updatedCost = node.g + heuristic(node, neighbor, distSelect)
			
			if(neighbor in closedSet):
				continue

			elif (updatedCost < neighbor.g):
				neighbor.g = updatedCost
				neighbor.h = heuristic(neighbor, end_Node, distSelect) 
				neighbor.f = neighbor.g + neighbor.h
				neighbor.parent = current_Node

				if(neighbor not in openSet):
					openSet.append(neighbor)

			
			updatedCost = node.g + heuristic(node, neighbor, distSelect)

			if neighbor in closedSet:
				continue

			if neighbor.g == None:
				neighbor.g = node.g


			elif(updatedCost < neighbor.g or neighbor not in openSet):
				neighbor.g = updatedCost
				neighbor.h = heuristic(neighbor, end_Node, distSelect)
				neighbor.f = neighbor.h + neighbor.g
				neighbor.parent = node

				if (neighbor not in openSet):
					openSet.append(neighbor)

			

			print("pos:", neighbor.position,"parent pos:", neighbor.parent.position,"currentNode g:", node.g,"g:", neighbor.g, "h:", neighbor.h, "f:", neighbor.f)


#Colors the found path
def drawPath(path, tiles):
	for coord in path:
		if tiles[coord[0]][coord[1]] != 1 and tiles[coord[0]][coord[1]] != 2:
			tiles[coord[0]][coord[1]] = 4

if __name__ == "__main__":
	main()
'''