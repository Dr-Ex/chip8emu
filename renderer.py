import pygame
import numpy

class Display:
	def __init__(self, scale, keyboard, speaker):
		self.running = False

		self.keyboard = keyboard
		self.speaker = speaker

		self.screen_width, self.screen_height = 64, 32
		self.scaling_factor = scale

		# Screen buffer for displaying image
		self.buffer = [[False for x in range(self.screen_width)] for x in range(self.screen_height)]

		# Initialise Pygame and the display window
		# As the resolution is small, we draw to a 
		# separate surface and scale that to the window
		pygame.init()
		self.window = pygame.display.set_mode((self.screen_width*self.scaling_factor, 
											   self.screen_height*self.scaling_factor))

		self.screen = pygame.Surface((self.screen_width, self.screen_height))


	def isRunning(self):
		return self.running
		
	def setPixel(self, x, y):
		# Wrap pixel if outside bounds
		if (x > self.screen_width):
			x -= self.screen_width
		elif (x < 0):
			x += self.screen_width

		if (y > self.screen_height):
			y -= self.screen_height
		elif (y < 0):
			y += self.screen_height

		self.buffer[y][x] = not self.buffer[y][x]

		return not self.buffer[y][x]

	def clear(self):
		self.buffer = [[False for x in range(self.screen_width)] for x in range(self.screen_height)]

	def render(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			# if event.type == pygame.KEYDOWN:
			# 	self.keyboard.onKeyDown(pygame.key.get_pressed())
			# if event.type == pygame.KEYUP:
			# 	self.keyboard.onKeyUp(pygame.key.get_pressed())

		#dont forget to clear screen
		#print(len(self.buffer))

		for i in range(len(self.buffer)):
			for j in range(len(self.buffer[i])):

				if self.buffer[i][j]:
					#print("drawing pixel", j, i)
					pygame.draw.rect(self.screen, (255, 255, 255), (j, i, 1, 1))
			
		# Scale the screen surface to the window
		self.window.blit(pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0))
		pygame.display.update()

	def testRender(self):
		self.setPixel(0, 0)
		self.setPixel(5, 2)

	def close(self):
		pygame.quit()


