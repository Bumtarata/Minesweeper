class Settings:
    """ Class to store all settings for Minesweeper."""
    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.thickness_of_edges = 21
        self.bg_color = (195, 195, 195)
        self.outline_white = (245, 245, 245)
        self.outline_grey = (120, 120, 120)
        
        # Single box of mine field settings
        self.box_width = 30
        self.box_height = self.box_width
        
        # Mine field settings
        self.columns = 9
        self.rows = 9
        self.mines = 10