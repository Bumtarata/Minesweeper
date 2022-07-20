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
        
        # Flags
        self.has_mine = False
        self.adjacent_mines = None
        
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
        if self.has_mine == False and self.adjacent_mines > 0:
            num = self.write_adjacent_mines()[0]
            num_rect = self.write_adjacent_mines()[1]
            mines_game.screen.blit(num, num_rect)
        elif self.has_mine:
            for row in mines_game.field_of_boxes:
                for box in row:
                    if box.has_mine:
                        mines_game.screen.fill(self.settings.bg_color, rect=box)
                        mine = box.create_mine()
                        mines_game.mines.add(mine)
            mines_game.mines.draw(mines_game.screen)
        
        
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