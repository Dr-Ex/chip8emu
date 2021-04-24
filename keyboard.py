class Keyboard:
	def __init__(self):
		self.KEYMAP = {
			"K_1": 0x1,
			"K_2": 0x2,
			"K_3": 0x3,
			"K_4": 0xC,
			"K_q": 0x4,
			"K_w": 0x5,
			"K_e": 0x6,
			"K_r": 0xD,
			"K_a": 0x7,
			"K_s": 0x8,
			"K_d": 0x9,
			"K_f": 0xE,
			"K_z": 0xA,
			"K_x": 0x0,
			"K_c": 0xB,
			"K_v": 0xF
		}

		self.keysPressed = []

		self.onNextKeyPress = None

	def isKeyPressed(self, keyCode):
		return self.keysPressed[keyCode]

	def onKeyDown(self, event):
		for key in event:
			key = self.KEYMAP[key]
			self.keysPressed[key] = True

			if (self.onNextKeyPress != None and self.onNextKeyPress != key):
				self.onNextKeyPress(key)
				self.onNextKeyPress = None

	def onKeyUp(self, event):
		for key in event:
			key = self.KEYMAP[key]
			self.keysPressed[key] = False