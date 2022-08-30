import pygame

from draw_lines_around_rect import draw_lines_around_rect as rect_lines
from picture import Picture

class RestartButton():
    """Class representing restart button in the middle of gui's head_rect."""
    def __init__(self, mines_game):
        """Initialize class."""
        self.game = mines_game
        self.settings = mines_game.settings
        self.screen = mines_game.screen
        self.sprite_group = self.game.restart_button_group
        
        # Create rect.
        height = self.game.window.gui.mines_left_rect.height
        width = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = self.game.window.gui.head_rect.center
        
    def draw_button(self, img_type='default_smile'):
        """Show chosen image inside rect. You can choose default_smile, win_smile 
        or dead_smile."""
        # Fill rect with background color.
        self.screen.fill(self.settings.bg_color, rect=self.rect)
        
        # Draw lines around rect.
        rect_lines(self.game, self.rect, self.screen, thickness=5, inside=True, invert=True)    # lines inside the rect
        rect_lines(self.game, self.rect, self.screen, thickness=2, singlecolored='grey')    # grey lines outside the rect

        group = self.game.restart_button_group
        img = Picture(self.game, picture_type=img_type)
        img.rect.center = self.rect.center
        self.sprite_group.add(img)
        self.sprite_group.draw(self.screen)
        self.sprite_group.empty()
        
    def click(self):
        """Make clicked graphical effect and restart game."""
        # Recolor inner lines.
        rect_lines(self.game, self.rect, self.screen, thickness=5, inside=True, singlecolored='grey')
        
        # Create inner rect.
        left = self.rect.left + 5 # that 5 is the same as thickness of inner rect_lines
        top = self.rect.top + 5
        width = self.rect.width - 7
        height = width
        click_rect = pygame.Rect(left, top, width, height)
        
        # Fill rect with bg color (will narrow right and bottom line)
        self.screen.fill(self.settings.bg_color, click_rect)
        
        # Draw smaller version of default_smile picture.
        img = Picture(self.game, picture_type='default_smile', clicked=True)
        img.rect.center = click_rect.center
        self.sprite_group.add(img)
        self.sprite_group.draw(self.screen)
        self.sprite_group.empty()
        