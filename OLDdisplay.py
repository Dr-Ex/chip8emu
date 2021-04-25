import pygame
import numpy

class Display:
	def __init__(self, scale):
		self.running = False

		self.screen_width, self.screen_height = 64, 32
		self.scaling_factor = scale

		# Screen buffer for displaying image
		self.buffer = numpy.empty(self.screen_width*self.screen_height, dtype=numpy.bool)

		# Initialise Pygame and the display window
		# As the resolution is small, we draw to a 
		# separate surface and scale that to the window
		pygame.init()
		self.window = pygame.display.set_mode((self.screen_width*self.scaling_factor, 
											   self.screen_height*self.scaling_factor))

		self.screen = pygame.Surface((self.screen_width, self.screen_height))
		print("Display Initialised.")


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

		pixelLoc = x + (y * self.screen_width)

		self.buffer[pixelLoc] ^ 1

		return not self.buffer[pixelLoc]

	def clear(self):
		self.buffer = numpy.empty(self.screen_width*self.screen_height, dtype=numpy.bool)

	def render(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

		#dont forget to clear screen
		#print(len(self.buffer))

		for i in range(len(self.buffer)):
			x = int((i % self.screen_width) * self.scaling_factor)

			y = int(numpy.floor(i / self.screen_width) * self.scaling_factor)

			if (self.buffer[i]):
				print("drawing pixel", x, y)
				pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.scaling_factor, self.scaling_factor))
			
		#print(self.buffer)
		# Scale the screen surface to the window
		self.window.blit(pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0))
		pygame.display.update()

	def testRender(self):
		return True
		#self.setPixel(0, 0)
		#self.setPixel(5, 2)

	def close(self):
		pygame.quit()


