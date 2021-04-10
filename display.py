import pygame
try:
	import numpy as N
	import pygame.surfarray as surfarray
except ImportError:
	raise ImportError, "NumPy and Surfarray are required."

class Display:
	def __init__(self):
		self.running = False

		self.screen_width, self.screen_height = 64, 32

		self.scaling_factor = 6

		pygame.init()
		self.window = pygame.display.set_mode((self.screen_width*self.scaling_factor, 
											   self.screen_height*self.scaling_factor))

		self.screen = pygame.Surface((self.screen_width, self.screen_height))

	def isRunning(self):
		return self.running
		

	def render(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
		self.window.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
		pygame.display.update()




screen_width, screen_height = 64, 32

scaling_factor = 12

x, y = 10, 10
rect_width, rect_height = 2, 2
vel = 2
black = (0, 0, 0)
white = (255, 255, 255)
pygame.init()
win = pygame.display.set_mode((screen_width*scaling_factor, screen_height*scaling_factor))

screen = pygame.Surface((screen_width, screen_height))

run = True
while run:
	pygame.time.delay(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	screen.fill(black)
	pygame.draw.rect(screen, white, (x, y, rect_width, rect_height))

	win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
	pygame.display.update()
pygame.quit()