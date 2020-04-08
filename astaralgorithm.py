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

