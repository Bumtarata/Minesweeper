class Settings:
    """ Class to store all settings for Minesweeper."""
    def __init__(self, diff='beginner'):
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
        self.difficulty = diff
        if self.difficulty == 'beginner':
            self.columns = 9
            self.rows = 9
            self.mines = 10
        
        elif self.difficulty == 'intermediate':
            self.columns = 16
            self.rows = 16
            self.mines = 40
            
        elif self.difficulty == 'expert':
            self.columns = 30
            self.rows = 16
            self.mines = 99
        
        # Those Nones are just placeholders, numbers will be provided by user.
        elif self.difficulty == 'custom':
            self.columns = None
            self.rows = None
            self.mines = None
        
        # Menu bar settings
        self.menu_height = 20
        self.menu_color = (170, 170, 170)
        self.menu_font_type = 'calibri'