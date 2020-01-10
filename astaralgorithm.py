'''
    File name: astaralgorithm.py
    Author: Trevor Tomlin
    Date created: 12/23/2019
    Date last modified: 1/9/2020
    Python Version: 3.7.3
'''

import pygame
import math
import easygui

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
						path = a_star(tiles, start, end, distSelect)
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
def hueristic(current_Node, end_Node, distSelect):

	#Euclidean
	if distSelect:
		a2 = (current_Node.position[0] - end_Node.position[0]) ** 2
		b2 = (current_Node.position[1] - end_Node.position[1]) ** 2
		return int(math.floor(10 * math.sqrt(a2 + b2)))

	#Manhattan
	elif not distSelect:
		deltaX = abs(current_Node.position[0] - end_Node.position[0])
		deltaY = abs(current_Node.position[1] - end_Node.position[1])
		return 10 * (deltaX + deltaY)

def a_star(tiles, start, end, distSelect):

	#Initilizes lists and start and end nodes
	openList = []
	closedList = []
	
	start_Node = Node(None, start)
	start_Node.g = 0

	end_Node = Node(None, end)
	end_Node.g = end_Node.h = end_Node.f = 0 

	start_Node.h = hueristic(start_Node, end_Node, distSelect)
	start_Node.f = start_Node.g + start_Node.h

	current_Node = start_Node

	openList.append(current_Node)

	while (len(openList) > 0):

		current_Node = openList[0]
		current_Index = 0

		#Finds node with lowest F score in openList
		for index, node in enumerate(openList):
			if node.f < current_Node.f:
				current_Index = index
				current_Node = openList[current_Index]

		#If the algorithm found the end return the path
		if current_Node == end_Node:
			path = []
			current = current_Node
			while current is not None:
				path.append(current.position)
				current = current.parent
			return path[::-1]

		openList.remove(current_Node)
		closedList.append(current_Node)

		neighbors = find_neighbors(current_Node, tiles)

		#Determine F scores of neighbors and fidn best path
		for neighbor in neighbors:

			if neighbor not in closedList and neighbor not in openList:					

					openList.append(neighbor)

					neighbor.parent = current_Node

					neighbor.g = hueristic(neighbor, start_Node, distSelect)
					neighbor.h = hueristic(neighbor, end_Node, distSelect)
					neighbor.f = neighbor.h + neighbor.g

#Colors the found path
def drawPath(path, tiles):
	for coord in path:
		if tiles[coord[0]][coord[1]] != 1 and tiles[coord[0]][coord[1]] != 2:
			tiles[coord[0]][coord[1]] = 4


if __name__ == "__main__":
	main()