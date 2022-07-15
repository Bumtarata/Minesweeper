class Settings:
    """ Class to store all settings for Minesweeper."""
    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 315
        self.screen_height = 395
        self.bg_color = (200, 200, 200)
        self.outline_white = (250, 250, 250)
        self.outline_grey = (150, 150, 150)
        
        # Single box of mine field settings
        self.box_width = 31
        self.box_height = self.box_width
        
        # Mine field settings
        self.columns = 9
        self.rows = 9
        self.mines = 10