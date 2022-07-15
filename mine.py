import pygame

from settings import Settings

class Mine(pygame.sprite.Sprite):
    """Class representing single mine."""
    def __init__(self):
        """Initialize mine."""
        super().__init__()
        self.settings = Settings()
        
        self.unscaled_img = pygame.image.load('imgs/mine.bmp')
        self.image = self._scale_img(self.unscaled_img)
        self.rect = self.image.get_rect()
        
    def _scale_img(self, img):
        """Scale given image to proper size."""
        original_size = img.get_size()
        new_height = self.settings.box_height - 8
        new_width = round((original_size[0] / original_size[1]) * new_height)
        
        scaled_img = pygame.transform.scale(img, (new_width, new_height))
        return scaled_img
        