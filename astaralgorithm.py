'''
    File name: astaralgorithm.py
    Author: Trevor Tomlin
    Date created: 4/7/2020
    Date last modified: 4/8/2020
    Python Version: 3.7.3
'''

import pygame
import math

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
YELLOW = (255,255,0)

display_width = 800
display_height = 800
menu_bar_size = 250

grid_size = 25
line_width = 5
line_color = BLACK


class Grid():

	def __init__(self, size=None):
		self.size = size
		self.nodes = []
		self.startNode = None
		self.endNode = None

		for j in range(self.size):
			for i in range(self.size):
				node = Node(None, (i,j))
				self.nodes.append(node)

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

		currentNode = self.nodes[col + (grid_size * row)]

		#print("mouse at", col, row)
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

				self.nodes[col + (grid_size * row)].color = color

			elif self.nodes[col + (grid_size * row)].color == color:
				self.nodes[col + (grid_size * row)].color = WHITE	
		except:
			pass
  			#print("Out of bounds")

	def findNeighbors(self, node):

  		neighbors = []
  		for neighbor in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
  			#print(node.position, self.size, node.position[0] + neighbor[0], node.position[1] + neighbor[1])
  			try:
  				c = (node.position[0] + neighbor[0]) + (self.size * (node.position[1] + neighbor[1]))
  				#print(c)
  				neighbor = self.nodes[c]
  				#neighbor = self.nodes[(node.position[0] + neighbor[0]) + (self.grid.size * (node.position[1] + neighbor[1]))]
  				#neighbor = (node.position[0] + position[0], node.position[1] + position[1])
  				if neighbor.color != GRAY:
  					if neighbor.color != GREEN and neighbor.color != RED:
  						neighbor.color = BLUE
  					neighbors.append(neighbor)
  					print(neighbor.position)

  			except:
  				pass
  				#print("Out of bounds")
  		#print(neighbors)
  		#print(len(neighbors))
  		return (neighbors)

	def colorPath(self, path):
  		for node in path:
  			if node.color != RED and node.color != GREEN:
  				node.color = YELLOW

class Node():

	def __init__(self, parent=None, position=None, color=WHITE):
		self.parent = parent
		self.position = position
		self.neighbors = []
		self.color = color

		self.g = 0
		self.h = 0
		self.f = 0


	def calcF(self):
		self.f = self.h + self.g

	def setColor(self, color):
		self.color = color 

	def draw(self, sizeInterval, screen):
		pygame.draw.rect(screen, self.color, (self.position[0] * sizeInterval, self.position[1] * sizeInterval, display_height / grid_size, display_height / grid_size))

class A_STAR():

	def __init__(self, grid):
		self.grid = grid
		self.openSet = []
		self.closedSet = []
		#self.currentNode = None


	def distance(self, start, end):
		return int(10 * math.sqrt((end.position[0] - start.position[0])**2 + (end.position[1] - start.position[1])**2))

	def start(self):
		self.openSet.append(self.grid.startNode)

		neighbors = self.grid.findNeighbors(self.grid.startNode)

		for neighbor in neighbors:
			neighbor.parent = self.grid.startNode
			self.openSet.append(neighbor)

		self.openSet.remove(self.grid.startNode)
		self.closedSet.append(self.grid.startNode)

		while len(self.openSet) > 0:

			#print(len(self.openSet))

			currentNode = self.openSet[0]

			for node in self.openSet:
				if node.f < currentNode.f:
					currentNode = node

			if currentNode == self.grid.endNode:
				path = [self.grid.endNode]
				current = self.grid.endNode

				while (current.parent != None):
					path.append(current.parent)
					current = current.parent

				#print(path[::-1])
				return path[::-1]

				print("END")

			self.openSet.remove(currentNode)
			self.closedSet.append(currentNode)

			for neighbor in self.grid.findNeighbors(currentNode):

				if neighbor not in self.closedSet:
					temp_G = neighbor.g + self.distance(currentNode, neighbor)

					if neighbor in self.openSet:
						if (temp_G < neighbor.g):
							neighbor.g = temp_G

					else:
						neighbor.g = temp_G
						self.openSet.append(neighbor)

					neighbor.h = self.distance(neighbor, self.grid.endNode)
					neighbor.calcF()
					neighbor.parent = currentNode


				'''
				print(self.distance(neighbor, self.grid.startNode))
				neighbor.g = self.distance(neighbor, self.grid.startNode)
				neighbor.h = self.distance(neighbor, self.grid.endNode)
				neighbor.calcF()

				tentative_gScore = neighbor.g + self.distance(currentNode, neighbor)

				if tentative_gScore < neighbor.g:
					neighbor.parent = currentNode
					neighbor.g = tentative_gScore
					neighbor.calcF()

					if neighbor not in self.closedSet:
						self.openSet.append(neighbor)


				'''

		#print(self.openSet)

def main():

	pygame.init()
	pygame.display.set_caption("A* Algorithm")
	screen = pygame.display.set_mode((display_width, display_height + menu_bar_size))
	screen.fill(BLACK)
	clock = pygame.time.Clock()

	grid = Grid(grid_size)

	running = True

	buttonColor = WHITE

	while running:

		grid.draw(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_s:
					#print("s")
					buttonColor = GREEN
				if event.key == pygame.K_e:
					#print("e")
					buttonColor = RED
				if event.key == pygame.K_w:
					#print("w")
					buttonColor = GRAY
				if event.key == pygame.K_RETURN:
					#print("return")
					astar = A_STAR(grid)
					path = astar.start()
					grid.colorPath(path)

			if event.type == pygame.MOUSEBUTTONDOWN:
				grid.button_handler(screen, buttonColor)


		pygame.display.update()
		clock.tick(60)


if __name__ == "__main__":
	main()

