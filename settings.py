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
        self.max_columns = 60   # Be careful about raising max numbers, app might get really
        self.min_columns = 9    # slow or even stop responding. Also it might not fit inside
        self.max_rows = 30      # your screen.
        self.min_rows = 9
        self.max_ratio = 8.1 # number of boxes (columns*rows) / number of mines
        
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