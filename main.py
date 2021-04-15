import time
from renderer import Display
from keyboard import Keyboard
from speaker import Speaker
from cpu import CPU

def main():
	keyboard = Keyboard()
	speaker = Speaker()
	renderer = Display(10, keyboard, speaker)

	fps = 60
	fpsInterval = 1000 // fps
	startTime = then

if __name__ == "__main__":
	main()