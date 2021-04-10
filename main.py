from display import Display

def main():
	renderer = Display()

	renderer.running = True

	while renderer.isRunning():
		renderer.render()

if __name__ == "__main__":
	main()