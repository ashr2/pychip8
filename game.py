import pygame
from cpu import CPU

def main():
    # Initialize pygame
    pygame.init()

    # Set up the display: width = 64, height = 32
    screen = pygame.display.set_mode((64, 32))
    pygame.display.set_caption("64x32 Black Screen")

    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Fill screen with black color (R=0, G=0, B=0)
        screen.fill((0, 0, 0))
        
        # Update the display
        pygame.display.flip()
    
    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()
