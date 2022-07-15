import pygame

from base_window import Base_window
from body_grid import Grid
from settings import Settings

class Minesweeper:
    """The main class managing game assets and behaviour."""
    
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        
        self.screen = Base_window()
        self.settings = Settings()
        
        # Create gui rects.
        self.gui_rects = self.screen.gui._create_gui_rects()
        self.body_rect = self.gui_rects[-1][0]
        
        self.body_grid = Grid(self.body_rect)
        
        # Game flags.
        self.running = True
    
    def run_game(self):
        """Start the main loop for the game."""
        # Fill window screen with color.
        self.screen.fill_bg()
        
        # Draw gui rects and lines.
        self.screen.gui._draw_rects(self.gui_rects)
        self.screen.gui._draw_lines()
        
        # Create gaming grid
        self.body_grid._create_field_of_boxes()        # passed is body_rect without color
        self.body_grid._draw_lines_between_boxes()
        
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