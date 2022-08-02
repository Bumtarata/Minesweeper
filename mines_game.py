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
        
        self.uncovered_boxes = []
        
        # Game flags.
        self.running = True
    
    def _uncover_clicked_box(self, mouse_pos):
        """Uncover the box that has been clicked."""
        for row in self.field_of_boxes:
            for box in row:
                if box.collidepoint(mouse_pos):
                    clicked_box = box
        
        clicked_box.remove_overlay(self)
        self.uncovered_boxes.append(clicked_box)
        for box in self.uncovered_boxes:
            box.draw_border_lines(self.screen)
        self.uncovered_boxes = []
    
    def run_game(self):
        """Start the main loop for the game."""
        # Fill window screen with color.
        self.window.fill_bg()
        
        # Draw gui rects and lines.
        self.window.gui.draw_rects(self.gui_rects)
        self.window.gui.draw_lines()
        
        # Create gaming grid
        self.field_of_boxes = self.body_grid.create_field_of_boxes()   # passed is body_rect without color
        
        # Set up mines and correct adjacent_mines variable for each box.
        self.boxes_with_mines = self.body_grid.set_up_mines(self.field_of_boxes)
        self.body_grid.check_adj_boxes(self.field_of_boxes)
        
        # Hide all boxes by displaying overlay on them.
        self.overlays.add(self.body_grid.hide_all_boxes(self.field_of_boxes))
        self.overlays.draw(self.screen)
        
        while self.running:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._uncover_clicked_box(mouse_pos)
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
if __name__ == '__main__':
    # Make the game instance and run the game.
    game = Minesweeper()
    game.run_game()