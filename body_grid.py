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
        
    def check_adj_boxes(self, field_of_boxes):
        """For each box checks how many mines are in adjacent boxes."""
        for row in field_of_boxes:
            for box in row:
                box.get_adjacent_boxes(field_of_boxes)
                box.count_adjacent_mines()