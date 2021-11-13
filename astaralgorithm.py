'''
    File name: astaralgorithm.py
    Author: Trevor Tomlin
    Date created: 4/7/2020
    Date last modified: 4/21/2020
    Python Version: 3.7.3
'''

import pygame
import math
import heapq

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
YELLOW = (255,255,0)

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
MENU_BAR_SIZE = 250

GRID_SIZE = 20
LINE_WIDTH = 5
LINE_COLOR = BLACK


# Taken from https://towardsdatascience.com/priority-queues-in-python-3baf0bac2097
class PriorityQueue:
	def __init__(self):
		self._queue = []
		self._index = 0

	def is_empty(self):
		return not self._queue
    
	def push(self, item, priority):
		heapq.heappush(self._queue, (priority, self._index, item))
		self._index += 1
    
	def pop(self):
		return heapq.heappop(self._queue)[-1]


class Grid():

	def __init__(self, size=None):
		self.size = size
		self.nodes = []
		self.startNode = None
		self.endNode = None

		for j in range(self.size):
			row = []
			for i in range(self.size):
				node = Node((i,j))
				#node.h = A_STAR.distance(node, self.endNode)
				row.append(node)
			self.nodes.append(row)

	def draw(self, screen):

		sizeInterval = int(DISPLAY_HEIGHT / GRID_SIZE)

		for row in self.nodes:
			for node in row:
				node.draw(sizeInterval, screen)
	
		for x in range(0, GRID_SIZE + 1):
			pygame.draw.line(screen, LINE_COLOR, (x * sizeInterval, 0), (x * sizeInterval, DISPLAY_HEIGHT), 5)
		for x in range(0, GRID_SIZE + 1 ):
			pygame.draw.line(screen, LINE_COLOR, (0 , x * int(DISPLAY_WIDTH / GRID_SIZE)), (DISPLAY_HEIGHT, x * sizeInterval), 5)

	def colorPath(self, path):
		for node in path:
  			if node.color != RED and node.color != GREEN:
  				node.color = YELLOW

	def button_handler(self, screen, color):
		mousePos = pygame.mouse.get_pos()
		row = math.ceil(mousePos[0] / (DISPLAY_HEIGHT / GRID_SIZE)) - 1
		col = math.ceil(mousePos[1] / (DISPLAY_HEIGHT / GRID_SIZE)) - 1

		currentNode = self.nodes[col][row]

		try:

			if currentNode.color != color:

				if color == GREEN:

					if self.startNode != None:

						self.startNode.color = WHITE
						self.startNode = currentNode
						currentNode.color = color
					else:
						self.startNode = currentNode
						currentNode.color = color

				elif color == RED:

					if self.endNode != None:
						self.endNode.color = WHITE
						self.endNode = currentNode
					else:
						self.endNode = currentNode

				self.nodes[col][row].color = color

			elif self.nodes[col][row].color == color:
				self.nodes[col][row].color = WHITE	
		except:
			pass

	def findNeighbors(self, node):

		neighbors = []
		for neighbor in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

			col = node.position[1] + neighbor[1]	
			row = node.position[0] + neighbor[0]

			if col >= 0 and col < self.size:
				if row >= 0 and row < self.size:
					neighbor = self.nodes[col][row]

					if neighbor.color != GRAY:
						if neighbor.color != GREEN and neighbor.color != RED:
							neighbor.color = BLUE

						neighbors.append(neighbor)

		return (neighbors)

class Node():

	def __init__(self, position=None, color=WHITE):
		self.parent = None
		self.position = position
		self.neighbors = []
		self.color = color

		self.g = 0
		self.h = 0
		self.f = 0

	def calcG(self, start):
		self.g = A_STAR.distance(self, start)

	def calcH(self, end):
		self.h = A_STAR.distance(self, end)

	def calcF(self):
		self.f = self.h + self.g

	def setColor(self, color):
		self.color = color 

	def draw(self, sizeInterval, screen):
		pygame.draw.rect(screen, self.color, (self.position[0] * sizeInterval, self.position[1] * sizeInterval, DISPLAY_HEIGHT / GRID_SIZE, DISPLAY_HEIGHT / GRID_SIZE))

class A_STAR():

	def __init__(self, grid):
		self.grid = grid
		self.openSet = []
		self.closedSet = []

	# Euclidean Distance
	@staticmethod
	def distance(start, end):
		return (math.sqrt((end.position[0] - start.position[0])**2 + (end.position[1] - start.position[1])**2))

	def reconstructPath(node):
		path = []

		currentnode = node

		while(currentnode is not None):
			path.append(currentnode)

		return path


	# Code from https://en.wikipedia.org/wiki/A*_search_algorithm
	def start(self):

		openSet = PriorityQueue();
		openSet.push(self.grid.startNode, 0)

		self.grid.startNode.parent = None
		self.grid.startNode.g = 0
		self.grid.startNode.f = A_STAR.distance(self.grid.startNode, self.grid.endNode)

		while not openSet.is_empty():
			current = openSet.pop()

			if current == self.grid.endNode:
				return reconstructPath(current)

			for neighbor in self.grid.findNeighbors(current):

				newGScore = current.g + A_STAR.distance(current, neighbor)

				neighbor.calcG(self.grid.endNode)

				if newGScore < neighbor.g:
					neighbor.parent = current
					neighbor.g = newGScore
					neighbor.f = neighbor.g + A_STAR.distance(neighbor, self.grid.endNode)
					if neighbor not in openSet._queue:
						openSet.push(neighbor, neighbor.f)

		# self.openSet.append(self.grid.startNode)

		# neighbors = self.grid.findNeighbors(self.grid.startNode)

		# for neighbor in neighbors:
		# 	neighbor.parent = self.grid.startNode
		# 	self.openSet.append(neighbor)

		# self.openSet.remove(self.grid.startNode)
		# self.closedSet.append(self.grid.startNode)

		# while len(self.openSet) > 0:

		# 	currentNode = self.openSet[0]

		# 	for node in self.openSet:
		# 		if node.f < currentNode.f:
		# 			currentNode = node
		# 		elif node.f == currentNode.f:
		# 			if node.h < currentNode.h:
		# 				currentNode = node

		# 	if currentNode == self.grid.endNode:
		# 		path = [self.grid.endNode]
		# 		current = self.grid.endNode

		# 		while (current.parent != None):
		# 			path.append(current.parent)
		# 			current = current.parent

		# 		return path[::-1]

		# 	self.openSet.remove(currentNode)
		# 	self.closedSet.append(currentNode)

		# 	for neighbor in self.grid.findNeighbors(currentNode):


		# 		if neighbor not in self.closedSet and neighbor.color != GRAY:
		# 			temp_G = neighbor.g + self.distance(neighbor, currentNode)

		# 			if neighbor not in self.openSet:
		# 				self.openSet.append(neighbor)
		# 			elif temp_G >= neighbor.g:
		# 				continue

		# 			neighbor.g = temp_G
		# 			neighbor.h = self.distance(neighbor, self.grid.endNode)
		# 			neighbor.calcF()
		# 			neighbor.parent = currentNode

def main():

	pygame.init()
	pygame.display.set_caption("A* Algorithm")
	icon = pygame.image.load('icon.png')
	menubar = pygame.image.load('menubar.png')
	pygame.display.set_icon(icon)
	screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT + MENU_BAR_SIZE))
	screen.fill(BLACK)
	clock = pygame.time.Clock()


	grid = Grid(GRID_SIZE)

	running = True

	buttonColor = WHITE

	canSelect = True

	while running:

		screen.blit(menubar, (0, 805))
		pygame.display.flip()

		grid.draw(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


			if event.type == pygame.KEYDOWN:

				if canSelect == True:

					if event.key == pygame.K_s:
						buttonColor = GREEN
					if event.key == pygame.K_e:
						buttonColor = RED
					if event.key == pygame.K_w:
						buttonColor = GRAY
					if event.key == pygame.K_RETURN:
						canSelect = False
						astar = A_STAR(grid)
						path = astar.start()
						grid.colorPath(path)

			if event.type == pygame.MOUSEBUTTONDOWN:
				if canSelect == True:
					grid.button_handler(screen, buttonColor)


		pygame.display.update()
		clock.tick(60)


if __name__ == "__main__":
	main()