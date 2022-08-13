import pygame

from draw_lines_around_rect import draw_lines_around_rect as rect_lines

class BoxOverlay(pygame.sprite.Sprite):
    """Class representing overlay for each box. This overlay will
    disappear after clicking on it with a mouse."""
    def __init__(self, box, mines_game):
        """Initialize the overlay for given box."""
        super().__init__()
        self.settings = mines_game.settings
        self.mines_game = mines_game
        self.image = self._create_image()
        self.rect = self.image.get_rect()
        
    def _create_image(self):
        """Create proper image of box's overlay."""
        surf = pygame.Surface((self.settings.box_width, self.settings.box_height))
        surf.fill(self.settings.bg_color)
        rect = surf.get_rect()
        
        # Draw grey and white lines around box.
        rect_lines(self.mines_game, rect, surf, thickness=4, inside=True, invert=True)
        
        return surf
        