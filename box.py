import pygame
from pygame import Rect

from box_overlay import BoxOverlay
from mine import Mine
from settings import Settings

class Box(Rect):
    """Class representing single box."""
    def __init__(self):
        """Initialize the box."""
        self.settings = Settings()
        
        # Position and size
        self.left = 0
        self.top = 0
        self.width = self.settings.box_width
        self.height = self.width
        
        # Inherit from Rect motherclass.
        super().__init__(self.left, self.top, self.width, self.height)
        
        # Other attributes
        self.covered = True
        self.has_mine = False
        self.adjacent_mines = None
        self.adjacent_boxes = []
        self.adj_boxes_checked = False
        
    def create_mine(self):
        """Create mine in the box."""
        self.mine = Mine()
        self.mine.rect.center = self.center
        return self.mine
        
    def create_overlay(self):
        """Hide box by displaying box overlay on it."""
        self.overlay = BoxOverlay(self)
        self.overlay.rect.center = self.center
        return self.overlay
        
    def remove_overlay(self, mines_game):
        """Remove overlay and show what's under it."""
        mines_game.overlays.remove(self.overlay)
        mines_game.screen.fill(self.settings.bg_color, rect=self)
        if self.has_mine == False and self.adjacent_mines:
            # box doesn't have mine but have adjacent mines; write num of adj mines
            num = self.write_adjacent_mines()[0]
            num_rect = self.write_adjacent_mines()[1]
            mines_game.screen.blit(num, num_rect)
            self.draw_border_lines(mines_game.screen)
            self.covered = False
        
        elif self.has_mine:
            # box has mine; show all mines
            for box in mines_game.boxes_with_mines:
                mines_game.screen.fill(self.settings.bg_color, rect=box)
                mine = box.create_mine()
                mines_game.mines.add(mine)
            mines_game.mines.draw(mines_game.screen)
            for box in mines_game.boxes_with_mines:
                box.draw_border_lines(mines_game.screen)
                box.covered = False
            
        elif self.has_mine == False and not self.adjacent_mines:
            self.draw_border_lines(mines_game.screen)
        
        
    def draw_border_lines(self, surface):
        """Draw thin lines around given rect."""
        vertices = (self.topleft, self.topright, self.bottomright, self.bottomleft)
        pygame.draw.lines(surface, self.settings.outline_grey, True, vertices)
        
    def get_adjacent_boxes(self, field_of_boxes):
        """Get all adjacent boxes and add them into self.adjacent_boxes."""
        for row in field_of_boxes:
            if self in row:
                row_idx = field_of_boxes.index(row)
                box_idx = row.index(self)
                
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
                    if self in row_of_int:
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
                            
                self.adjacent_boxes.extend(boxes_of_interest)
                return
                
    def count_adjacent_mines(self):
        """Assign proper number to self.adjacent_mines if there are any
        adjacent mines."""
        num_of_mines = 0
        for box in self.adjacent_boxes:
            if box.has_mine:
                num_of_mines += 1
        if num_of_mines > 0:
            self.adjacent_mines = num_of_mines
    
    def write_adjacent_mines(self):
        """Write to box number of adjacent mines."""
        blue_color = (0, 0, 255)
        green_color = (0, 130, 0)
        red_color = (255, 0, 0)
        dark_blue = (0, 0, 150)
        dark_red = (140, 0, 0)
        wierd_green = (0, 140, 140)
        purple_color = (140, 0, 140)
        black_color = (30, 30, 30)
        
        color_dict = {
            '1': blue_color,
            '2': green_color,
            '3': red_color,
            '4': dark_blue,
            '5': dark_red,
            '6': wierd_green,
            '7': purple_color,
            '8': black_color,
        }
        
        font = pygame.font.Font(None, 40)
        font.bold = True
        
        text_color = color_dict[f'{str(self.adjacent_mines)}']
        text = font.render(str(self.adjacent_mines), True, text_color, (self.settings.bg_color))
        text_rect = text.get_rect()
        text_rect.center = self.center
        text_rect.x += 1
        text_rect.y += 2
    
        return text, text_rect