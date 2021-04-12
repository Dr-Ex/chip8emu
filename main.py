from renderer import Display
from cpu import CPU

def main():
	renderer = Display(10)

	renderer.running = True

	renderer.testRender()

	while renderer.isRunning():
		renderer.render()
	renderer.close()

if __name__ == "__main__":
	main()