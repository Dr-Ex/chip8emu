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
	try:
		rom_path = sys.argv[1]
	except IndexError:
		print("Please enter a path")
		exit()
	# Load the rom into memory
	cpu.loadRom(rom_path)

	then = time.perf_counter()

	fps = 50
	fpsInterval = 1000 // fps
	startTime = then
	elapsed = 0

	running = True
	while running:
		now = time.perf_counter()
		elapsed = now - then

		if (elapsed > fpsInterval):
			cpu.cycle()




if __name__ == "__main__":
	main()
