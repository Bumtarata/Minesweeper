import pygame

from base_window import BaseWindow
from body_grid import Grid
from settings import Settings

class Minesweeper:
    """The main class managing game assets and behaviour."""
    
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        
        self.window = BaseWindow()
        self.screen = self.window.screen
        self.settings = Settings()
        
        # Create gui rects.
        self.gui_rects = self.window.gui.create_gui_rects()
        self.body_rect = self.gui_rects[-1][0]
        
        self.body_grid = Grid(self.body_rect)
        
        # Groups for sprites to be drawn.
        self.mines = pygame.sprite.Group()
        self.overlays = pygame.sprite.Group()
        
        # Game flags.
        self.running = True
    
    def run_game(self):
        """Start the main loop for the game."""
        # Fill window screen with color.
        self.window.fill_bg()
        
        # Draw gui rects and lines.
        self.window.gui.draw_rects(self.gui_rects)
        self.window.gui.draw_lines()
        
        # Create gaming grid
        self.field_of_boxes = self.body_grid.create_field_of_boxes()   # passed is body_rect without color
        self.body_grid.draw_lines_between_boxes()
        
        # Prepare and draw mines and display for each box how many adjacent
        # mines are there.
        self.boxes_with_mines = self.body_grid.set_up_mines(self.field_of_boxes)
        for minebox in self.boxes_with_mines:
            mine = minebox.create_mine()
            mine.add(self.mines)
        self.mines.draw(self.screen)
        self.body_grid.check_adj_boxes(self.field_of_boxes)
        self.to_blit = self.body_grid.write_num_of_adj_mines(self.field_of_boxes)
        self.screen.blits(self.to_blit)
        
        # Hide all boxes by displaying overlay on them.
        self.overlays.add(self.body_grid.hide_all_boxes(self.field_of_boxes))
        self.overlays.draw(self.screen)
        
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