import pygame

class Picture(pygame.sprite.Sprite):
    """Class representing single picture (used for mines and
    emoticons on restart button."""
    def __init__(self, mines_game, picture_type='mine', clicked=False):
        """Initialize picture Picture type must be one of these: mine, 
        marked_mine, default_smile, win_smile, dead_smile!!!"""
        super().__init__()
        self.settings = mines_game.settings
        
        if picture_type == 'mine':
            self.unscaled_img = pygame.image.load('imgs/mine.bmp')
            box_height = self.settings.box_height
            num = 8
        elif picture_type == 'marked_mine':
            self.unscaled_img = pygame.image.load('imgs/marked_mine.bmp')
            box_height = self.settings.box_height
            num = 15
        elif picture_type == 'default_smile' or picture_type == 'win_smile' or picture_type == 'dead_smile':
            if clicked:
                num = 15
            if not clicked:
                num = 12
            
            if picture_type == 'default_smile':
                self.unscaled_img = pygame.image.load('imgs/default_smile.png')
                box_height = mines_game.window.gui.restart_button.rect.height
            elif picture_type == 'win_smile':
                self.unscaled_img = pygame.image.load('imgs/win_smile.png')
                box_height = mines_game.window.gui.restart_button.rect.height
            elif picture_type == 'dead_smile':
                self.unscaled_img = pygame.image.load('imgs/dead_smile.png')
                box_height = mines_game.window.gui.restart_button.rect.height
        
        self.image = self._scale_img(self.unscaled_img, box_height, num)
        self.rect = self.image.get_rect()
        
    def _scale_img(self, img, box_height, num):
        """Scale given image to proper size."""
        original_size = img.get_size()
        new_height = box_height - num
        new_width = round((original_size[0] / original_size[1]) * new_height)
        
        scaled_img = pygame.transform.scale(img, (new_width, new_height))
        return scaled_img
        