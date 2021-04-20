import time
import sys
from renderer import Display
from keyboard import Keyboard
from speaker import Speaker
from cpu import CPU

def main():
	keyboard = Keyboard()
	speaker = Speaker()
	renderer = Display(10, keyboard, speaker)
	cpu = CPU(renderer, keyboard, speaker)

	# First argument should be the rom path
	rom_path = sys.argv[1]

	# Load the rom into memory
	CPU

	then = time.perf_counter()

	fps = 60
	fpsInterval = 1000 // fps
	startTime = then
	elapsed = 0

	running = True
	while running:
		now = time.perf_counter()
		elapsed = now - then

		if (elapsed > fpsInterval):
			CPU.cycle()




if __name__ == "__main__":
	main()