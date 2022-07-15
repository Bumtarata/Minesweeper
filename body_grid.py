import pygame

from base_window import Base_window, Gui
from settings import Settings

class Grid():
    """Class for grid in body_rect. This is the main part of the game."""
    def __init__(self, body_rect):
        """Initialize all that's necessary."""
        self.body_rect = body_rect
        self.screen = Base_window().screen
        self.settings = Settings()
    
    def _create_single_gaming_box(self):
        """Creates a single gaming box."""
        single_box_rect = pygame.Rect(0, 0, self.settings.box_width, 
            self.settings.box_height)
        return single_box_rect
    
    def _create_row_of_boxes(self, box_top):
        """Create a single row of gaming boxes in body rect."""
        box_num = 0
        row_of_boxes = []
        for box in range(self.settings.columns):   # box is rect
            box = self._create_single_gaming_box()
            box.left = self.body_rect.left + (box.width * box_num)
            box.top = box_top
            row_of_boxes.append(box)
            box_num += 1
        
        return row_of_boxes
    
    def _create_field_of_boxes(self):
        """Creates whole field of gaming boxes."""
        row_num = 0
        field_of_boxes = []
        for row in range(self.settings.rows):
            box_top = self.body_rect.top + (self.settings.box_height * row_num)
            row = self._create_row_of_boxes(box_top)
            field_of_boxes.append(row)
            row_num += 1
        
        return field_of_boxes
        
    def _draw_lines_between_boxes(self):
        """Draw thin black lines between boxes in body rect."""
        field = self._create_field_of_boxes()
        grey_color = (150, 150, 150)
        
        # Draw vertical lines
        for num in range(self.settings.columns - 1):
            pygame.draw.line(
                surface = self.screen,
                color = grey_color,
                start_pos = field[0][num].topright,
                end_pos = field[-1][num].bottomright,
            )
        
        # Draw horizontal lines
        for num in range(self.settings.rows - 1):
            pygame.draw.line(
                surface = self.screen,
                color = grey_color,
                start_pos = field[num][0].bottomleft,
                end_pos = field[num][-1].bottomright,
            )