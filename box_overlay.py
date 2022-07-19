import pygame

from settings import Settings

class BoxOverlay(pygame.sprite.Sprite):
    """Class representing overlay for each box. This overlay will
    disappear after clicking on it with a mouse."""
    def __init__(self, box):
        """Initialize the overlay for given box."""
        super().__init__()
        self.settings = Settings()
        self.image = self._create_image()
        self.rect = self.image.get_rect()
        
    def _create_image(self):
        """Create proper image of box's overlay."""
        surf = pygame.Surface((self.settings.box_width, self.settings.box_height))
        surf.fill(self.settings.bg_color)
        rect = surf.get_rect()
        line_width = 5
        
        # Draw grey and white lines around box.
        for a in range(line_width):
            wv_start_pos = (rect.bottomleft[0] + a, rect.bottomleft[1] - a)
            wv_end_pos = (rect.topleft[0] + a, rect.topleft[1])
            white_vertical = pygame.draw.line(surf, self.settings.outline_white,
                wv_start_pos, wv_end_pos)
        
        for b in range(line_width):
            wh_start_pos = (rect.topright[0] - b, rect.topright[1] + b)
            wh_end_pos = (rect.topleft[0], rect.topleft[1] + b)
            white_horizontal = pygame.draw.line(surf, self.settings.outline_white,
                wh_start_pos, wh_end_pos)
        
        for c in range(line_width):
            gv_start_pos = (rect.topright[0] - c, rect.topright[1] + c)
            gv_end_pos = (rect.bottomright[0] - c, rect.bottomright[1])
            grey_vertical = pygame.draw.line(surf, self.settings.outline_grey,
                gv_start_pos, gv_end_pos)
        
        for d in range(line_width):
            gh_start_pos = (rect.bottomleft[0] + d, rect.bottomleft[1] - d)
            gh_end_pos = (rect.bottomright[0], rect.bottomright[1] - d)
            grey_horizontal = pygame.draw.line(surf, self.settings.outline_grey,
                gh_start_pos, gh_end_pos)
        
        return surf
        