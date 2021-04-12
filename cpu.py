import numpy

class Registers:
	def __init__(self):
		# General Purpose Registers
		self.V = numpy.empty(16, dtype=numpy.ubyte)
		self.I = 0

		# Special Purpose Registers
		self.PC = 0
		self.SP = 0

		# Stack
		self.stack = numpy.empty(16, dtype=numpy.ushort)

		# Delay and Sound Timers
		self.DT = 0
		self.ST = 0

	def getV(self, V):
		return self.V[V]

	def setV(self, V, value):
		self.V[V] = value

	def getI(self):
		return self.I

	def setI(self, value):
		self.I = value

	def getSP(self):
		return self.SP

	def setSP(self, value):
		self.SP = value

	def getPC(self):
		return self.PC

	def setPC(self, value):
		self.PC = value

	def getDT(self):
		return self.DT

	def setDT(self, value):
		self.DT = value

	def getST(self):
		return self.ST

	def setST(self, value):
		self.ST = value

	def getStack(self):
		return self.stack



class CPU:
	def __init__(self):
		self.memory = numpy.empty(4096, dtype=numpy.ubyte)
		self.registers = Registers()

