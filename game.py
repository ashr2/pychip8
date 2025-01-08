import pygame
import numpy as np
from cpu import CPU
import time
# def main():
#     # Initialize pygame
#     pygame.init()

#     # Create a 64x32 window
#     scale = 10
#     width, height = 64 * scale, 32 * scale
#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption("64x32 Screen with Numpy")

#     # Example 64x32 numpy array initialized with random 0s and 1s
#     # In your real use-case, you would fill or update this array elsewhere
#     cpu = CPU("particle_demo.ch8", super_chip=True)
#     display_pixels = cpu.get_display()
#     key_bindings = [
#         pygame.K_1,
#         pygame.K_2,
#         pygame.K_3,
#         pygame.K_4,
#         pygame.K_q,
#         pygame.K_w,
#         pygame.K_e,
#         pygame.K_r,
#         pygame.K_a,
#         pygame.K_s,
#         pygame.K_d,
#         pygame.K_f,
#         pygame.K_z,
#         pygame.K_x,
#         pygame.K_c,
#         pygame.K_v
#     ]
#     keys_pressed = np.zeros(16, dtype=np.uint8)
#     running = True
#     instructions_per_second = 1400
#     while running:
#         # Event handling
#         for event in pygame.event.get():
#             keys = pygame.key.get_pressed()
#             for i, key in enumerate(key_bindings):
#                 if keys[key]:
#                     keys_pressed[i] = 1
#                 else:
#                     keys_pressed[i] = 0
#             if event.type == pygame.QUIT:
#                 running = False
#         cpu.set_keys_pressed(keys_pressed)
#         # Loop through each pixel in the 2D array
#         cpu.decode_execute()
#         for y in range(height):
#             for x in range(width):
#                 if display_pixels[y // scale][x // scale] == 1:
#                     color = (255, 255, 255)  # White
#                 else:
#                     color = (0, 0, 0)        # Black
#                 # Set the pixel on the screen
#                 screen.set_at((x, y), color)

#         # Update display
#         pygame.display.flip()
#         time.sleep(1.0 / float(instructions_per_second))
#     # Quit the gamdfa
#     pygame.quit()
def main():
    pygame.init()
    scale = 10
    width, height = 64 * scale, 32 * scale
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chip-8 Emulator")

    cpu = CPU("hilo.ch8", super_chip=False)
    display_pixels = cpu.get_display()
    key_bindings = [
    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
    pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v
    ]
    keys_pressed = np.zeros(16, dtype=np.uint8)

    clock = pygame.time.Clock()
    instructions_per_frame = 10  # e.g. do 10 CPU cycles per frame
    running = True

    while running:
        # Limit to 60 frames per second
        dt = clock.tick(60) / 1000.0  # dt in seconds

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update key array
        keys = pygame.key.get_pressed()
        for i, key in enumerate(key_bindings):
            keys_pressed[i] = 1 if keys[key] else 0
        cpu.set_keys_pressed(keys_pressed)

        # Run multiple CPU instructions this frame
        for _ in range(instructions_per_frame):
            cpu.decode_execute()

        # Decrement timers at ~60Hz
        if cpu.delayTimer > 0:
            cpu.delayTimer -= 1
        if cpu.soundTimer > 0:
            cpu.soundTimer -= 1

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
