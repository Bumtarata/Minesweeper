import pygame

class Picture(pygame.sprite.Sprite):
    """Class representing single mine."""
    def __init__(self, mines_game, picture_type='mine'):
        """Initialize mine. Picture type must be either mine or marked_mine!!!"""
        super().__init__()
        self.settings = mines_game.settings
        
        if picture_type == 'mine':
            self.unscaled_img = pygame.image.load('imgs/mine.bmp')
            num = 8
        elif picture_type == 'marked_mine':
            self.unscaled_img = pygame.image.load('imgs/marked_mine.bmp')
            num = 12
        
        self.image = self._scale_img(self.unscaled_img, num)
        self.rect = self.image.get_rect()
        
    def _scale_img(self, img, num):
        """Scale given image to proper size."""
        original_size = img.get_size()
        new_height = self.settings.box_height - num
        new_width = round((original_size[0] / original_size[1]) * new_height)
        
        scaled_img = pygame.transform.scale(img, (new_width, new_height))
        return scaled_img
        