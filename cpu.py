import numpy

class CPU:
        def __init__(self, renderer, keyboard, speaker, debug=True):
                self.renderer = renderer
                self.keyboard = keyboard
                self.speaker = speaker
                self.debug = debug

                # 4k Memory
                self.memory = numpy.empty(4096, dtype=numpy.ubyte)
                
                # General Purpose Registers
                self.vReg = numpy.empty(16, dtype=numpy.ubyte)
                self.iReg = 0

                # Special Purpose Registers
                self.PC = 0
                # self.SP = 0 Stack pointer unused

                # Stack
                #self.stack = numpy.empty(16, dtype=numpy.ushort)
                self.stack = [0 for i in range(16)]

                # Delay and Sound Timers
                self.DT = 0
                self.ST = 0

                # Some instructions require pausing of operation
                self.paused = False

                self.speed = 10

                self.loadDefaultSprites()

        def loadDefaultSprites(self):
                sprites = [
                        0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
                        0x20, 0x60, 0x20, 0x20, 0x70, # 1
                        0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
                        0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
                        0x90, 0x90, 0xF0, 0x10, 0x10, # 4
                        0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
                        0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
                        0xF0, 0x10, 0x20, 0x40, 0x40, # 7
                        0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
                        0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
                        0xF0, 0x90, 0xF0, 0x90, 0x90, # A
                        0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
                        0xF0, 0x80, 0x80, 0x80, 0xF0, # C
                        0xE0, 0x90, 0x90, 0x90, 0xE0, # D
                        0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
                        0xF0, 0x80, 0xF0, 0x80, 0x80  # F
                ]

                # Sprites stored in interpreter memory space beginning at 0x000
                for i in range(len(sprites)):
                        self.memory[i] = sprites[i]


        def loadProgram(self, program, offset=0x200):
                for i in range(len(program)):
                        self.memory[offset + i] = program[i]

        def loadRom(self, fileName):
                program = []

                with open(fileName, 'rb') as f:
                        byte = f.read(1)
                        while byte:
                                #print(byte)
                                program.append(int.from_bytes(byte, byteorder="little"))
                                byte = f.read(1)

                self.loadProgram(program)

        def cycle(self):
                for i in range(self.speed):
                        if not self.paused:
                                opcode = (self.memory[self.PC] << 8 | self.memory[self.PC + 1])
                                self.executeInstruction(opcode);

                if not self.paused:
                        self.updateTimers()

                self.playSound()
                self.renderer.render()
                #print('PC', self.PC)

        def updateTimers(self):
                if (self.DT > 0):
                        self.DT -= 1

                if (self.ST > 0):
                        self.ST -= 1

        def playSound(self):
                # if (self.soundTimer > 0):
                #       self.speaker.play(440)
                # else:
                #       self.speaker.stop()

                return False

        def executeInstruction(self, opcode):
                # if opcode != 0: 
                    # print("EXEC:", opcode)
                # Each instruction is 2 bytes long
                # Inc PC by 2
                self.PC += 2

                # Only need second nibble of high byte
                # Filter it and shift right by 8 bits
                x = (opcode & 0x0F00) >> 8

                # Only need first nibble of low byte 
                y = (opcode & 0x00F0) >> 4

                def zeroSwitch():
                        def CLS():
                                if self.debug:
                                        print("CLS")
                                # Clear the screen
                                self.renderer.clear()

                        def RET():
                                if self.debug:
                                        print("RET")
                                # pop item from stack and store in PC
                                self.PC = self.stack.pop()

                        switch0x0 = {
                                0x00E0: CLS, # 00E0 - CLS
                                0x00EE: RET  # 00EE - RET
                        }

                        operation = switch0x0.get((opcode), lambda: "Invalid opcode {}.".format(opcode))
                        operation()

                def JP():
                        if self.debug:
                                        print("JP")
                        self.PC = (opcode & 0xFFF)

                def CALL():
                        if self.debug:
                                        print("CALL")
                        self.stack.append(self.PC)
                        self.PC = (opcode & 0xFFF)

                def SE():
                        if self.debug:
                                        print("SE")
                        if (self.vReg[x] == (opcode & 0xFF)):
                                self.PC += 2

                def SNE():
                        if self.debug:
                                        print("SNE")
                        if (self.vReg[x] != (opcode & 0xFF)):
                                self.PC += 2

                def SEa():
                        if self.debug:
                                        print("SEa")
                        if (self.vReg[x] == self.vReg[y]):
                                self.PC += 2

                def LD():
                        if self.debug:
                                        print("LD")
                        self.vReg[x] = (opcode & 0xFF)

                def ADD():
                        if self.debug:
                                        print("ADD")
                        self.vReg[x] += (opcode)

                def eightSwitch():
                        def LDb():
                                if self.debug:
                                        print("LDb")
                                self.vReg[x] = self.vReg[y]

                        def OR():
                                if self.debug:
                                        print("OR")
                                self.vReg[x] = self.vReg[x] | self.vReg[y]

                        def AND():
                                if self.debug:
                                        print("AND")
                                self.vReg[x] = self.vReg[x] & self.vReg[y]

                        def XOR():
                                if self.debug:
                                        print("XOR")
                                self.vReg[x] = self.vReg[x] ^ self.vReg[y]

                        def ADDa():
                                if self.debug:
                                        print("ADDa")
                                sum = (self.vReg[x] + self.vReg[y])
                                self.vReg[x] = self.vReg[x] + self.vReg[y]

                                self.vReg[0xF] = 0

                                if (sum > 0xFF):
                                        self.vReg[0xF] = 1

                                self.vReg[x] = sum

                        def SUB():
                                if self.debug:
                                        print("SUB")
                                self.vReg[0xF] = 0

                                if (self.vReg[x] > self.vReg[y]):
                                        self.vReg[0xF] = 1

                                self.vReg[x] -= self.vReg[y]

                        def SHR():
                                if self.debug:
                                        print("SHR")
                                self.vReg[0xF] = (self.vReg[x] & 0x1)

                                self.vReg[x] = self.vReg[x] >> 1

                        def SUBN():
                                if self.debug:
                                        print("SUBN")
                                self.vReg[0xF] = 0

                                if (self.vReg[y] > self.vReg[x]):
                                        self.vReg[0xF] = 1

                                self.vReg[x] = self.vReg[y] - self.vReg[x]

                        def SHL():
                                if self.debug:
                                        print("SHL")
                                self.vReg[0xF] = (self.vReg[x] & 0x80)
                                self.vReg[x] = self.vReg[x] << 1

                        switch0x8 = {
                                0x0: LDb, # 8xy0 - LD Vx, Vy
                                0x1: OR,  # 8xy1 - OR Vx, Vy
                                0x2: AND, # 8xy2 - AND Vx, Vy
                                0x3: XOR, # 8xy3 - XOR Vx, Vy
                                0x4: ADDa,# 8xy4 - ADD Vx, Vy
                                0x5: SUB, # 8xy5 - SUB Vx, Vy
                                0x6: SHR, # 8xy6 - SHR Vx {, Vy}
                                0x7: SUBN,# 8xy7 - SUBN Vx, Vy
                                0xE: SHL  # 8xyE - SHL Vx {, Vy}
                        }

                        operation = switch0x8.get((opcode & 0xF), lambda: "Invalid opcode {}.".format(opcode))
                        operation()

                def SNEa():
                        if self.debug:
                                        print("SNEa")
                        if (self.vReg[x] != self.vReg[y]):
                                self.PC += 2

                def LDa():
                        if self.debug:
                                        print("LDa")
                        self.iReg = (opcode & 0xFFF)

                def JPa():
                        if self.debug:
                                        print("JPa")
                        self.PC = (opcode & 0xFFF) + self.vReg[0]

                def RND():
                        if self.debug:
                                        print("RND")
                        # Generate random number 0-255 then and with
                        # lowest byte of opcode. 

                        rand = 0
                        self.vReg[x] = rand & (opcode & 0xFF)

                def DRW():
                        if self.debug:
                                        print("DRW")
                        width = 8
                        height = (opcode & 0xF)

                        self.vReg[0xF] = 0

                        for row in range(height):
                                sprite = self.memory[self.iReg + row]

                                for col in range(width):
                                        if ((sprite & 0x80) > 0):
                                                if (self.renderer.setPixel(self.vReg[x] + col, self.vReg[y] + row)):
                                                        self.vReg[0xF] = 1

                                        sprite = sprite << 1

                def eSwitch():

                        def SKP():
                                if self.debug:
                                        print("SKP")
                                return False

                        def SKNP():
                                if self.debug:
                                        print("SKNP")
                                return False

                        switch0xE = {
                                0x9E: SKP, # Ex9E - SKP Vx
                                0xA1: SKNP # ExA1 - SKNP Vx
                        }

                        operation = switch0xE.get((opcode & 0xFF), lambda: "Invalid opcode {}.".format(opcode))
                        operation()

                def fSwitch():
                        
                        def LDxdt():
                                if self.debug:
                                        print("LDxdt")
                                self.vReg[x] = self.DT

                        def LDk():
                                if self.debug:
                                        print("LDk")
                                self.paused = True
                                for event in pygame.event.get():
                                        if event.type == pygame.KEYDOWN:
                                                self.paused = not self.keyboard.onNextPress(event.key)

                        def LDdtx():
                                if self.debug:
                                        print("LDdtx")
                                self.DT = self.vReg[x]

                        def LDstx():
                                if self.debug:
                                        print("LDstx")
                                self.ST = self.vReg[x]

                        def ADDi():
                                if self.debug:
                                        print("ADDi")
                                self.iReg += self.vReg[x]

                        def LDfx():
                                if self.debug:
                                        print("LDfx")
                                self.iReg = self.vReg[x] * 5

                        def LDbx():
                                if self.debug:
                                        print("LDbx")
                                self.memory[self.iReg] = int(self.vReg[x] / 100)

                                self.memory[self.iReg + 1] = int((self.vReg[x] % 100) / 10)

                                self.memory[self.iReg + 2] = int(self.vReg[x] % 10)

                        def LDix():
                                if self.debug:
                                        print("LDix")
                                for registerIndex in range(x):
                                        self.memory[self.iReg + registerIndex] = self.vReg[registerIndex]

                        def LDxi():
                                if self.debug:
                                        print("LDxi")
                                for registerIndex in range(x):
                                        self.vReg[registerIndex] = self.memory[self.iReg + registerIndex]

                        switch0xF = {
                                0x07: LDxdt, # Fx07 - LD Vx, DT
                                0x0A: LDk, # Fx0A - LD Vx, K
                                0x15: LDdtx, # Fx15 - LD DT, Vx
                                0x18: LDstx, # Fx18 - LD ST, Vx
                                0x1E: ADDi,# Fx1E - ADD I, Vx
                                0x29: LDfx, # Fx29 - LD F, Vx - ADD I, Vx
                                0x33: LDbx, # Fx33 - LD B, Vx
                                0x55: LDix, # Fx55 - LD [I], Vx
                                0x65: LDxi  # Fx65 - LD Vx, [I]
                        }

                        operation = switch0xF.get((opcode & 0xFF), lambda: "Invalid opcode {}.".format(opcode))
                        operation()

                opSwitch = {
                        0x0000: zeroSwitch,
                        0x1000: JP,   # 1nnn - JP addr
                        0x2000: CALL, # 2nnn - CALL addr
                        0x3000: SE,   # 3xkk - SE Vx, byte
                        0x4000: SNE,  # 4xkk - SNE Vx, byte
                        0x5000: SEa,  # 5xy0 - SE Vx, Vy
                        0x6000: LD,   # 6xkk - LD Vx, byte
                        0x7000: ADD,  # 7xkk - ADD Vx, byte
                        0x8000: eightSwitch,
                        0x9000: SNEa, # 9xy0 - SNE Vx, Vy
                        0xA000: LDa,  # Annn - LD I, addr
                        0xB000: JPa,  # Bnnn - JP V0, addr
                        0xC000: RND,  # Cxkk - RND Vx, byte
                        0xD000: DRW,  # Dxyn - DRW Vx, Vy, nibble
                        0xE000: eSwitch,
                        0xF000: fSwitch
                }
                operation = opSwitch.get((opcode & 0xF000), lambda: "Invalid opcode {}.".format(opcode))
                operation()








