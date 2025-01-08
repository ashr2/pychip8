import numpy as np
class CPU:
    def __init__(self):
        self.memory = np.array(4096, dtype=np.uint8) # Memory is 4kb
        self.display = np.array((32, 64), dtype=np.uint8)
        self.pc = 0x050 # ranges from 0x0000 to 0x1000
        self.I = 0x0000 #16 bit index register
        self.delayTimer = 0x00 # 8 bit delay timer
        self.soundTimer = 0x00 # 8 bit osund timer
        self.registers = np.array(16, dtype=np.uint8) #Variable registers
        self.load_font() #Load font into memory
        self.stack = []
    
    def load_font(self):
        CHIP8_FONTSET = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]

        for i, font in enumerate(CHIP8_FONTSET):
            self.memory[self.pc + i] = font

    #Opcode functions
    def clear_screen(self):
        for row in range(len(self.display)):
            for col in range(len(row)):
                self.display[row][col] = 0

    def pop_stack(self):
        pass

    def jump(self, nnn):
        self.pc = nnn

    def pop_stack_addr(self, nnn):
        pass

    def set_index(self, nnn):
        self.I = nnn

    def jump_with_offset(self, nnn):
        pass

    def set_register_vx(self, x, nn):
        self.registers[x] = nn

    def add_register_vx(self, x, nn):
        self.registers[x] = self.registers[x] + nn

    def set_index_register(self, nnn):
        pass

    def dxyn(self, x, y, n):
        pass
    
    #Fetch decode execute loop
    def fetch(self):
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2

    def decode_execute(self, opcode):
        #no var cases
        if(opcode == 0x00E0):
            return self.clear_screen
    
        nnn = opcode & 0x0FFF
        nn = opcode & 0x00FF
        n = opcode & 0x000F
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        match opcode & 0xF000:
            case 0x1000:
                self.jump(nnn)
            # case 0x2000:
            #     return self.pop_stack_addr(nnn)
            case 0x6000:
                self.set_register_vx(x, nn)
            case 0x7000:
                self.add_register_vx(x, nn)
            case 0xA000:
                self.add_register_vx(nnn)
            case 0xD000:
                self.dxyn(x, y, n)
            


    
                
                
