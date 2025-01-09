import numpy as np
import random
class CPU:
    def __init__(self, rom_filename, super_chip=False, debugging=False):
        self.memory = np.zeros(4096, dtype=np.uint16) # Memory is 4kb
        self.display = np.zeros((32, 64), dtype=np.uint8)
        self.pc = 0x0200 # ranges from 0x0000 to 0x1000
        self.I = 0x0000 #16 bit index register
        self.delayTimer = 0x00 # 8 bit delay timer
        self.soundTimer = 0x00 # 8 bit osund timer
        self.registers = np.zeros(16, dtype=np.uint8) #Variable registers
        self.keys_pressed = np.zeros(16, dtype=np.uint8) #Keys pressed
        self.load_rom(rom_filename) #Load font into memory
        self.stack = []
        self.load_font() #Load font into memory
        self.super_chip = super_chip #Super chip configuration
        self.debugging = False
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
            self.memory[0x050 + i] = font
    
    def load_rom(self, filename):
        with open(filename, 'rb') as file:
            rom_bytes = file.read()
        rom_array = np.frombuffer(rom_bytes, dtype=np.uint8)
        for i, byte in enumerate(rom_array):
            self.memory[0x200 + i] = byte

    def set_keys_pressed(self, keys_pressed):
            self.keys_pressed = keys_pressed

    #Opcode functions
    def clear_screen(self):
        self.display.fill(0)

    def pop_stack(self):
        self.pc = self.stack.pop()

    def jump(self, nnn):
        self.pc = nnn

    def pop_stack_addr(self, nnn):
        self.stack.append(self.pc)
        self.pc = nnn

    def set_index(self, nnn):
        self.I = nnn

    def set_register_vx(self, x, nn):
        self.registers[x] = nn

    def add_register_vx(self, x, nn):
        self.registers[x] = self.registers[x] + nn

    def set_index_register(self, nnn):
        self.I = nnn

    def dxyn(self, x, y, n):
        vx = self.registers[x] % 64
        vy = self.registers[y] % 32
        self.registers[0xF] = 0 #Set collision flag to 0
        for row in range(n):
            current_byte = self.memory[self.I + row]
            for col in range(8):
                bit = (current_byte >> (7 - col)) & 1 #Get current bit
                if vy + row < 32 and vx + col < 64:
                    old_pixel = self.display[vy + row][vx + col]
                    if old_pixel == 1 and bit == 1: #Check for collision set flag as needed
                        self.registers[0xF] = 1
                    self.display[vy + row][(vx + col)] ^= bit

    def skip_if_equal(self, x, nn):
        vx = self.registers[x]
        if vx == nn:
            self.pc += 2

    def skip_if_not_equal(self, x, nn):
        vx = self.registers[x]
        if vx != nn:
            self.pc += 2

    def skip_if_x_y_equal(self, x, y):
        vx = self.registers[x]
        vy = self.registers[y]
        if vx == vy:
            self.pc += 2

    def skip_if_x_y_not_equal(self, x, y):
        vx = self.registers[x]
        vy = self.registers[y]
        if vx != vy:
            self.pc += 2

    def skip_if_x_pressed(self, x):
        vx = self.registers[x]
        if(self.keys_pressed[vx] == 1):
            self.pc += 2

    def skip_if_x_not_pressed(self, x):
        vx = self.registers[x]
        if(self.keys_pressed[vx] != 1):
            self.pc += 2

    def set(self, x, y):
        self.registers[x] = self.registers[y]

    def binary_or(self, x, y):
        self.registers[x] |= self.registers[y]

    def binary_and(self, x, y):
        self.registers[x] &= self.registers[y]

    def logical_xor(self, x, y):
        self.registers[x] ^= self.registers[y]

    def add(self, x, y):
        if self.registers[x] + self.registers[y] > 255:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0
        self.registers[x] += self.registers[y]

    def vx_minus_vy(self, x, y):
        vx = self.registers[x]
        vy = self.registers[y]
        if vx > vy:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0
        difference = int(self.registers[x]) - int(self.registers[y])
        self.registers[x] = difference & 0xFF

    def vy_minus_vx(self, x, y):
        vx = self.registers[x]
        vy = self.registers[y]
        if vy > vx:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0
        difference = int(self.registers[y]) - int(self.registers[x])
        self.registers[x] = difference & 0xFF

    def shift_right(self, x, y):
        if(not(self.super_chip)):
            self.registers[x] = self.registers[y]
        self.registers[0xF] = self.registers[x] & 0x1
        self.registers[x] >>= 1
   
    def shift_left(self, x, y):
        if(not(self.super_chip)):
            self.registers[x] = self.registers[y]
        self.registers[0xF] = (self.registers[x] >> 7) & 0x1
        self.registers[x] <<= 1

    def jump_with_offset(self, x, nnn):
        if(not(self.super_chip)):
            self.pc = nnn + self.registers[0x0]
        else:
            self.pc = nnn + self.registers[x]
    
    def random(self,x, nn):
        self.registers[x] = random.randint(0x0, 0xFF) & nn

    def set_vx_to_delay_timer(self, x):
        self.registers[x] = self.delayTimer

    def set_delay_timer_to_vx(self, x):
        self.delayTimer = self.registers[x]

    def set_sound_timer_to_vx(self, x):
        self.soundTimer = self.registers[x]

    def add_to_index(self, x):
        self.I += self.registers[x]
    
    def get_key(self, x):
        try:
            registerPressed = list(self.keys_pressed).index(1)
            self.registers[x] = registerPressed
        except ValueError:
            self.pc -= 2
     
    def set_i_to_font(self, x):
        vx = self.registers[x]
        self.I = 0x050 + 5 * vx

    def binary_decimal_conversion(self, x):
        vx = self.registers[x]
        self.memory[self.I] = (vx // (10 ** 2)) % 10
        self.memory[self.I + 1] = (vx // (10 ** 1)) % 10
        self.memory[self.I + 2] = (vx // (10 ** 0)) % 10
    
    def store_memory(self, x):
        for i in range(x + 1):
            self.memory[self.I + i] = self.registers[i]
            if(not(self.super_chip)):
                self.I += 1

    def load_memory(self, x):
        for i in range(x + 1):
            self.registers[i] = self.memory[self.I + i]
            if(not(self.super_chip)):
                self.I += 1
    
    #Fetch execute decode loop
    def fetch(self):
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        return opcode
    
    def decode_execute(self):
        opcode = self.fetch()
        opcode_decoded = True

        nnn = opcode & 0x0FFF
        nn = opcode & 0x00FF
        n = opcode & 0x000F
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        match opcode & 0xF000:
            case 0x1000:
                self.jump(nnn)
            case 0x2000:
                self.pop_stack_addr(nnn)
            case 0x3000:
                self.skip_if_equal(x, nn)
            case 0x4000:
                self.skip_if_not_equal(x, nn)
            case 0x5000:
                self.skip_if_x_y_equal(x, y)
            case 0x6000:
                self.set_register_vx(x, nn)
            case 0x7000:
                self.add_register_vx(x, nn)
            case 0x8000:
                match opcode & 0xF00F:
                    case 0x8000:
                        self.set(x, y)
                    case 0x8001:
                        self.binary_or(x, y)
                    case 0x8002:
                        self.binary_and(x, y)
                    case 0x8003:
                        self.logical_xor(x, y)
                    case 0x8004:
                        self.add(x, y)
                    case 0x8005:
                        self.vx_minus_vy(x,y)
                    case 0x8006:
                        self.shift_right(x, y)
                    case 0x8007:
                        self.vy_minus_vx(x,y)
                    case 0x800E:
                        self.shift_left(x, y)
                    case _:
                        opcode_decoded = False   
            case 0x9000:
                self.skip_if_x_y_not_equal(x, y)
            case 0xA000:
                self.set_index_register(nnn)
            case 0xB000:
                self.jump_with_offset(x, nnn)
            case 0xC000:
                self.random(x, nn)
            case 0xD000:
                self.dxyn(x, y, n)
            case 0xE000:
                match opcode & 0xF0FF:
                    case 0xE09E:
                        self.skip_if_x_pressed(x)
                    case 0xE0A1:
                        self.skip_if_x_not_pressed(x)
                    case _:
                        opcode_decoded = False
            case 0xF000:
                match opcode & 0xF0FF:
                    case 0xF00A:
                        self.get_key(x)
                    case 0xF007:
                        self.set_vx_to_delay_timer(x)
                    case 0xF015:
                        self.set_delay_timer_to_vx(x)
                    case 0xF018:
                        self.set_sound_timer_to_vx(x)
                    case 0xF01E:
                        self.add_to_index(x)
                    case 0xF029:
                        self.set_i_to_font(x)
                    case 0xF033:
                        self.binary_decimal_conversion(x)
                    case 0xF055:
                        self.store_memory(x)
                    case 0xF065:
                        self.load_memory(x)
                    case _:
                        opcode_decoded = False
            case _:
                if(opcode == 0x00E0):
                    self.clear_screen()
                elif(opcode == 0x00EE):
                    self.pop_stack()
                else:
                    opcode_decoded = False
        
        #print opcodes if debugging on
        if self.debugging:
            if opcode_decoded:
                print(f"Opcode {opcode:04X} decoded")
            else:
                print(f"Opcode {opcode:04X} not decoded successfully")

        if self.delayTimer > 0:
            self.delayTimer -= 1
        if self.soundTimer > 0:
            self.soundTimer -= 1
    
    def get_display(self):
        return self.display
            


    
                
                
