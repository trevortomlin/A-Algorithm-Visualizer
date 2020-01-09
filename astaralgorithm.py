'''
    File name: astaralgorithm.py
    Author: Trevor Tomlin
    Date created: 12/23/2019
    Date last modified: 12/28/2019
    Python Version: 3.7.3
'''

import pygame
#import random
import math
import easygui

# tiles = [[0,0,0,0,0],
# 		[0,0,1,0,0],
# 		[0,0,0,0,0],
# 		[0,0,1,0,0],
# 		[0,0,0,0,0]] 

def main():

	display_width = 1000
	display_height = 1000
	square_dividers = 5
	
	pygame.init()


	pygame.display.set_caption("A* Algorithm")

	screen = pygame.display.set_mode((display_width, display_height))

	screen.fill((255,255,255))

	clock = pygame.time.Clock()

	tiles = generate_tile_array(square_dividers)

	running = True

	easygui.msgbox("Please select the STARTING point for the A* Algorithm and press ENTER when you are finished", "A* Algorithm")

	selectingStart = True
	selectingEnd = False
	selectingWall = False
	sentEndMsg = False
	sentWallMsg = False
	validTile = False
	startFound = False
	endFound = False

	while running:

		if selectingEnd == True and sentEndMsg == False:
			easygui.msgbox("Please select the ENDING point for the A* Algorithm and press ENTER when you are finished", "A* Algorithm")
			sentEndMsg = True

		if selectingWall == True and sentWallMsg == False:
			easygui.msgbox("Please select the WALLS for the A* Algorithm and press ENTER when you are finished to START THE ALGORITHM", "A* Algorithm")
			sentWallMsg = True
		
		#generate_tile_array(square_dividers)
		fill_tiles(screen, square_dividers, tiles)
		draw_lines(screen, square_dividers)

		'''
		if startFound == False:
			start = find_start(tiles)
			if start != 0:
				startFound = True
		if endFound == False:
			end = find_end(tiles)
			if end != 0:
				endFound = True
		'''

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN and selectingStart:
				button_handler(tiles, square_dividers, screen, 1)

			if event.type == pygame.MOUSEBUTTONDOWN and selectingEnd:
				button_handler(tiles, square_dividers, screen, 2)

			if event.type == pygame.MOUSEBUTTONDOWN and selectingWall:
				button_handler(tiles, square_dividers, screen, 3)

			if event.type == pygame.KEYDOWN:
				if pygame.K_RETURN:
					if selectingStart == True:
						if check_valid_tile(tiles, 0):
							selectingStart = False
							selectingEnd = True
							start = find_start(tiles)
						else:
							easygui.msgbox("1 STARTING point required! ", "A* Algorithm")

					elif selectingEnd == True:
						if check_valid_tile(tiles, 1):
							selectingEnd = False
							selectingWall = True
							end = find_end(tiles)
						else:
							easygui.msgbox("1 ENDING point required! ", "A* Algorithm")
					elif selectingWall == True:
						selectingWall = False
						#start = find_start(tiles)
						#end = find_end(tiles)
						#print(start, end)
						path = a_star(tiles, start, end)
						#print(path)


			
			#print(event)
		pygame.display.update()

		clock.tick(60)

def draw_lines(screen, size):

	line_color = (0,0,0)
	
	sizeInterval = int(screen.get_height() / size)
	
	for x in range(0, size):
		pygame.draw.line(screen, line_color, (x * sizeInterval, 0), (x * sizeInterval, screen.get_height()), 5)
	for x in range(0, size):
		pygame.draw.line(screen, line_color, (0 , x * int(screen.get_width() / size)), (screen.get_height(), x * sizeInterval), 5)

def fill_tiles(screen, size, tiles):

	sizeInterval = int(screen.get_height() / size)

	for rowNum, row in enumerate (tiles):
		#print(".")
		#print(tiles[rownum])
		for tileNum, tile in enumerate (row):
			#print(tiles[rowNum][tileNum])
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

	#pygame.draw.rect(screen, (0,255,0), (0,0,160,160))

def generate_tile_array(size):
	tileArray = []
	for x in range(0, size):
		row = []
		for x in range(0, size):
			#row.append(random.randint(0, 1))
			row.append(0)
		tileArray.append(row)
	#print(tileArray)
	#print(row)
	return(tileArray)

def button_handler(tiles, size, screen, int):
	mousePos = pygame.mouse.get_pos()
	#print(mousePos)
	col = math.ceil(mousePos[0] / (screen.get_height() / size)) - 1
	row = math.ceil(mousePos[1] / (screen.get_height() / size)) - 1
	#print (col, row)

	if tiles[row][col] == 0:
		tiles[row][col] = int

	elif tiles[row][col] == int:
		tiles[row][col] = 0

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

def find_start(tiles):
	start = ()
	for rowNum, row in enumerate (tiles):
		for tileNum, tile in enumerate (row):
			if tiles[rowNum][tileNum] == 1:
				start = (rowNum, tileNum)
	#print (start)
	if len(start) != 0:
		return start
	else:
		return 0

def find_end(tiles):
	end = ()
	for rowNum, row in enumerate (tiles):
		for tileNum, tile in enumerate (row):
			if tiles[rowNum][tileNum] == 2:
				end = (rowNum, tileNum)
	#print (end)
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


def find_neighbors(current_Node, tiles):

	neighbors = []

	#Top Left Node
	if current_Node.position[0] - 1 >= 0 and current_Node.position[1] - 1 >= 0:
		tiles[current_Node.position[0] - 1][current_Node.position[1] - 1] = 5
		newPosition = (current_Node.position[0] - 1, current_Node.position[1] - 1)
		n1 = Node(current_Node, newPosition)
		neighbors.append(n1)
		#print("top left")

	#Top Middle Node
	if current_Node.position[0] - 1 >= 0:
		tiles[current_Node.position[0] - 1][current_Node.position[1]] = 5
		newPosition = (current_Node.position[0] - 1, current_Node.position[1])
		n2 = Node(current_Node, newPosition)
		neighbors.append(n2)
		#print ("top middle")

	#Top Right Node
	if current_Node.position[0] - 1 >= 0 and current_Node.position[1] + 1 < len(tiles):
		tiles[current_Node.position[0] - 1][current_Node.position[1] + 1] = 5
		newPosition = (current_Node.position[0] - 1, current_Node.position[1] + 1)
		n3 = Node(current_Node, newPosition)
		neighbors.append(n3)
		#print ("top right")

		#Middle Left Node
	if current_Node.position[1] - 1 >= 0:
		tiles[current_Node.position[0]][current_Node.position[1] - 1] = 5
		newPosition = (current_Node.position[0], current_Node.position[1] - 1)
		n4 = Node(current_Node, newPosition)
		neighbors.append(n4)
		#print ("middle left")

		#Middle Right Node
	if current_Node.position[1] + 1 < len(tiles):
		tiles[current_Node.position[0]][current_Node.position[1] + 1] = 5
		newPosition = (current_Node.position[0], current_Node.position[1] + 1)
		n5 = Node(current_Node, newPosition)
		neighbors.append(n5)
		#print ("middle right")

	#Bottom Left Node
	if current_Node.position[0] + 1 < len(tiles) and current_Node.position[1] - 1 >= 0:
		tiles[current_Node.position[0] + 1][current_Node.position[1] - 1] = 5
		newPosition = (current_Node.position[0] + 1, current_Node.position[1] - 1)
		n6 = Node(current_Node, newPosition)
		neighbors.append(n6)
		#print ("bottom left")

	#Bottom Middle Node
	if current_Node.position[0] + 1 < len(tiles):
		tiles[current_Node.position[0] + 1][current_Node.position[1]] = 5
		newPosition = (current_Node.position[0] + 1, current_Node.position[1])
		n7 = Node(current_Node, newPosition)
		neighbors.append(n7)
		#print ("bottom middle")

	#Bottom Right Node
	if current_Node.position[0] + 1 < len(tiles) and current_Node.position[1] + 1 < len(tiles):
		tiles[current_Node.position[0] + 1][current_Node.position[1] + 1] = 5
		newPosition = (current_Node.position[0] + 1, current_Node.position[1] + 1)
		n8 = Node(current_Node, newPosition)
		neighbors.append(n8)
		#print ("bottom middle")

	return(neighbors)


'''
def a_star(tiles, start, end):
	
	start_Node = Node(None, start)
	start_Node.g = 0
	end_Node = Node(None, end)
	end_Node.g = end_Node.h = end_Node.f = 0 
	start_Node.h = ((start_Node.position[0] - end_Node.position[0]) ** 2) + ((start_Node.position[1] - end_Node.position[1]) ** 2)	
	start_Node.f = start_Node.g + start_Node.h
	print (start_Node.f)

	openSet = []
	closedSet = []

	openSet.append(start_Node)
	#tiles[start_Node.position[0]][start_Node.position[1]] = 4

	while len(openSet) > 0:

		current_Node = openSet[0]
		current_Index = 0

		for index, node in enumerate(openSet):
			#print(node)
			if node.f < current_Node.f:
				current_Index = index
				current_Node = openSet[current_Index]

		if current_Node == end_Node:
			print("FINISHED")
			path = []
			current = current_node
			while current is not None:
				path.append(current.position)
				current = current.parent
			return path[::-1]

		openSet.pop(current_Index)
		closedSet.append(current_Node)
		print("len closeset", len(closedSet))
		print("len openset", len(openSet))
		#tiles[current_Node.position[0]][current_Node.position[1]] = 5

		#print(current_Node.position)

		neighbors = []

		#Top Left Node
		if current_Node.position[0] - 1 >= 0 and current_Node.position[1] - 1 >= 0:
			tiles[current_Node.position[0] - 1][current_Node.position[1] - 1] = 5
			newPosition = (current_Node.position[0] - 1, current_Node.position[1] - 1)
			n1 = Node(current_Node, newPosition)
			neighbors.append(n1)
			#print("top left")

		#Top Middle Node
		if current_Node.position[0] - 1 >= 0:
			tiles[current_Node.position[0] - 1][current_Node.position[1]] = 5
			newPosition = (current_Node.position[0] - 1, current_Node.position[1])
			n2 = Node(current_Node, newPosition)
			neighbors.append(n2)
			#print ("top middle")

		#Top Right Node
		if current_Node.position[0] - 1 >= 0 and current_Node.position[1] + 1 < len(tiles):
			tiles[current_Node.position[0] - 1][current_Node.position[1] + 1] = 5
			newPosition = (current_Node.position[0] - 1, current_Node.position[1] + 1)
			n3 = Node(current_Node, newPosition)
			neighbors.append(n3)
			#print ("top right")

		#Middle Left Node
		if current_Node.position[1] - 1 >= 0:
			tiles[current_Node.position[0]][current_Node.position[1] - 1] = 5
			newPosition = (current_Node.position[0], current_Node.position[1] - 1)
			n4 = Node(current_Node, newPosition)
			neighbors.append(n4)
			#print ("middle left")

		#Middle Right Node
		if current_Node.position[1] + 1 < len(tiles):
			tiles[current_Node.position[0]][current_Node.position[1] + 1] = 5
			newPosition = (current_Node.position[0], current_Node.position[1] + 1)
			n5 = Node(current_Node, newPosition)
			neighbors.append(n5)
			#print ("middle right")

		#Bottom Left Node
		if current_Node.position[0] + 1 < len(tiles) and current_Node.position[1] - 1 >= 0:
			tiles[current_Node.position[0] + 1][current_Node.position[1] - 1] = 5
			newPosition = (current_Node.position[0] + 1, current_Node.position[1] - 1)
			n6 = Node(current_Node, newPosition)
			neighbors.append(n6)
			#print ("bottom left")

		#Bottom Middle Node
		if current_Node.position[0] + 1 < len(tiles):
			tiles[current_Node.position[0] + 1][current_Node.position[1]] = 5
			newPosition = (current_Node.position[0] + 1, current_Node.position[1])
			n7 = Node(current_Node, newPosition)
			neighbors.append(n7)
			#print ("bottom middle")

		#Bottom Right Node
		if current_Node.position[0] + 1 < len(tiles) and current_Node.position[1] + 1 < len(tiles):
			tiles[current_Node.position[0] + 1][current_Node.position[1] + 1] = 5
			newPosition = (current_Node.position[0] + 1, current_Node.position[1] + 1)
			n8 = Node(current_Node, newPosition)
			neighbors.append(n8)
			#print ("bottom middle")

		#print(neighbors)

		for neighbor in neighbors:
			if neighbor not in closedSet:

				neighbor.g = current_Node.g + 10
				neighbor.h = ((neighbor.position[0] - end_Node.position[0]) ** 2) + ((neighbor.position[1] - end_Node.position[1]) ** 2)
				neighbor.f = neighbor.g + neighbor.h

			if neighbor not in openSet:
				openSet.append(neighbor)

	return False

'''

def hueristic(current_Node, end_Node):
	return ((current_Node.position[0] - (end_Node.position[0] + 1)) ** 2) + ((current_Node.position[1] - (end_Node.position[1] + 1)) ** 2)

def a_star(tiles, start, end):
	
	start_Node = Node(None, start)
	start_Node.g = 0

	end_Node = Node(None, end)
	end_Node.g = end_Node.h = end_Node.f = 0 

	current_Node = start_Node

	start_Node.h = hueristic(current_Node, end_Node)
	start_Node.f = start_Node.g + start_Node.h

	current_Node = start_Node

	print (start_Node.f)

	neighbors = find_neighbors(current_Node, tiles)
	print (neighbors)
	print(len(neighbors))

	#while current_Node != end_Node:


if __name__ == "__main__":
	main()