from random import choice

import pygame

from base_window import BaseWindow, Gui
from box import Box
from settings import Settings

class Grid():
    """Class for grid in body_rect. This is the main part of the game."""
    def __init__(self, body_rect):
        """Initialize all that's necessary."""
        self.body_rect = body_rect
        self.screen = BaseWindow().screen
        self.settings = Settings()
    
    def _create_row_of_boxes(self, box_top):
        """Create a single row of gaming boxes in body rect."""
        box_num = 0
        row_of_boxes = []
        for box in range(self.settings.columns):   # box is rect
            box = Box()
            box.left = self.body_rect.left + (box.width * box_num)
            box.top = box_top
            row_of_boxes.append(box)
            box_num += 1
        
        return row_of_boxes
    
    def create_field_of_boxes(self):
        """Creates whole field of gaming boxes."""
        row_num = 0
        field_of_boxes = []
        for row in range(self.settings.rows):
            box_top = self.body_rect.top + (self.settings.box_height * row_num)
            row = self._create_row_of_boxes(box_top)
            field_of_boxes.append(row)
            row_num += 1
        
        return field_of_boxes
        
    def hide_all_boxes(self, field_of_boxes):
        """For every box in field_of_boxes create overlay."""
        list_of_overlays = []
        for row in field_of_boxes:
            for box in row:
                overlay = box.create_overlay()
                list_of_overlays.append(overlay)
        
        return list_of_overlays
        
    def set_up_mines(self, field_of_boxes):
        """Place mines to field of boxes."""
        boxes_with_mines = []
        for num in range(self.settings.mines):
            while True:
                # Pick a random box.
                random_row = choice(field_of_boxes)
                random_box = choice(random_row)
                
                if random_box.has_mine:
                    # Box already has a mine, pick another one.
                    continue
                else:
                    # Box doesn't have mine, so place one there.
                    random_box.has_mine = True
                    boxes_with_mines.append(random_box)
                
                break
        return boxes_with_mines
        
    def draw_lines_between_boxes(self):
        """Draw thin black lines between boxes in body rect."""
        field = self.create_field_of_boxes()
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
    
    def check_adj_boxes(self, field_of_boxes):
        """For each box checks how many mines are in adjacent boxes."""
        for row in field_of_boxes:
            row_idx = field_of_boxes.index(row)
            
            for box in row:
                box_idx = row.index(box)
                # Skip boxes with mines on them.
                if box.has_mine:
                    continue
                
                # Get rows of interest where boxes of interest will be looked for.
                rows_of_interest = []
                # Check whether the box is in the first of last row.
                if row_idx == 0:
                    rows_of_interest.extend(field_of_boxes[row_idx:row_idx+2])
                        
                elif row_idx + 1 == self.settings.rows:
                    rows_of_interest.extend(field_of_boxes[row_idx-1:row_idx+1])
                
                elif row_idx > 0 and row_idx < self.settings.rows - 1:
                    rows_of_interest.extend(field_of_boxes[row_idx-1:row_idx+2])
                
                # Get boxes of interest from rows of interest.
                boxes_of_interest = []
                
                for row_of_int in rows_of_interest:
                    # Check whether the box is in the currently iterated row.
                    if box in row_of_int:
                        # Check whether the box is in the first or last column.
                        if box_idx == 0:
                            boxes_of_interest.append(row_of_int[box_idx+1])
                        elif box_idx + 1 == self.settings.columns:
                            boxes_of_interest.append(row_of_int[box_idx-1])
                        else:
                            boxes_of_interest.extend(
                                [row_of_int[box_idx-1], row_of_int[box_idx+1]])
                    
                    else:
                        # Check whether the box is in the first of last column.
                        if box_idx == 0:
                            boxes_of_interest.extend(row_of_int[box_idx:box_idx+2])
                        elif box_idx + 1 == self.settings.columns:
                            boxes_of_interest.extend(row_of_int[box_idx-1:box_idx+1])
                        elif box_idx > 0 and box_idx < self.settings.columns - 1:
                            boxes_of_interest.extend(row_of_int[box_idx-1:box_idx+2])
                
                # Count boxes with mines in boxes_of_interest
                num_of_mines = 0
                for box_of_int in boxes_of_interest:
                    if box_of_int.has_mine:
                        num_of_mines += 1
                box.adjacent_mines = num_of_mines
      