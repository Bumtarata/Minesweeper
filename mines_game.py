import pygame

from settings import Settings
from base_window import Base_window

class Minesweeper:
    """The main class managing game assets and behaviour."""
    
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = Base_window()
        
        # Game flags.
        self.running = True
    
    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
if __name__ == '__main__':
    # Make the game instance and run the game.
    game = Minesweeper()
    game.run_game()