import pygame
import numpy as np
from cpu import CPU
import os

def main():
    #Fetch game
    print("Games you have:")
    files = os.listdir("roms/")
    for i, file in enumerate(files):
        print(f"{i}: {file[0:len(file) - 4]}")
    
    done = False
    game = None
    while(not(done)):
        print(f"Enter number (1-{len(files)}) of game you would like to play:")
        game = int(input())
        if game >= 0 and game < len(files):
            done = True
            game = "roms/" + files[game]
        else:
            print(f"Please enter number from 1-{len(files)}")
    
    print(f"Would you like to use super chip emulator")
    super_chip = False
    if(input() == "y"):
        super_chip = True
    
    print(f"Loading {game[5:len(file) - 4]}")
    #Load pygame rendering
    pygame.init()
    scale = 10
    width, height = 64 * scale, 32 * scale
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chip-8 Emulator")

    cpu = CPU(game, super_chip)
    display_pixels = cpu.get_display()
    key_bindings = [
    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
    pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v
    ]
    keys_pressed = np.zeros(16, dtype=np.uint8)

    clock = pygame.time.Clock()
    instructions_per_frame = 1  # e.g. do 10 CPU cycles per frame
    running = True

    while running:
        # Limit to 60 frames per second
        dt = clock.tick(60) / 1000.0  # dt in seconds

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Run multiple CPU instructions this frame
        for _ in range(instructions_per_frame):
            # Update key array
            keys = pygame.key.get_pressed()
            for i, key in enumerate(key_bindings):
                keys_pressed[i] = 1 if keys[key] else 0
            cpu.set_keys_pressed(keys_pressed)
            cpu.decode_execute()

        # Update the display
        for y in range(32):
            for x in range(64):
                color = (255, 255, 255) if display_pixels[y][x] else (0, 0, 0)
                pygame.draw.rect(
                    screen, 
                    color, 
                    pygame.Rect(x * scale, y * scale, scale, scale)
                )

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
