import pygame
import numpy as np
from cpu import CPU

def main():
    # Initialize pygame
    pygame.init()

    # Create a 64x32 window
    scale = 10
    width, height = 64 * scale, 32 * scale
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("64x32 Screen with Numpy")

    # Example 64x32 numpy array initialized with random 0s and 1s
    # In your real use-case, you would fill or update this array elsewhere
    cpu = CPU("ibm.ch8")
    display_pixels = cpu.get_display()

    running = True
    while running:
        # Event handling
        cpu.decode_execute()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Loop through each pixel in the 2D array
        for y in range(height):
            for x in range(width):
                if display_pixels[y // scale][x // scale] == 1:
                    color = (255, 255, 255)  # White
                else:
                    color = (0, 0, 0)        # Black
                # Set the pixel on the screen
                screen.set_at((x, y), color)

        # Update display
        pygame.display.flip()

    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main()
