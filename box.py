from pygame import Rect

from mine import Mine
from settings import Settings

class Box(Rect):
    """Class representing single box."""
    def __init__(self):
        """Initialize the box."""
        self.settings = Settings()
        
        # Position and size
        self.left = 0
        self.top = 0
        self.width = self.settings.box_width
        self.height = self.settings.box_height
        
        # Inherit from Rect motherclass.
        super().__init__(self.left, self.top, self.width, self.height)
        
        # Flags
        self.has_mine = False
        self.adjacent_mines = None
        
    def create_mine(self):
        """Create mine in the box."""
        self.mine = Mine()
        self.mine.rect.center = self.center
        return self.mine