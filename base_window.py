import pygame

from settings import Settings

class Base_window:
    """Class representing the base game window and gui."""
    def __init__(self):
        """Initialize game window."""
        self.settings = Settings()
        
        # Create game window
        pygame.display.set_caption("Minesweeper")
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.fill_bg()
        
        # Create a gui.
        self.gui = Gui(self)
        
    def fill_bg(self):
        """Fill background with color."""
        self.screen.fill(self.settings.bg_color)

class Gui():
    """Class that manages creation of basic game GUI."""
    def __init__(self, base_window):
        """Initialize the gui and set it properly."""
        self.settings = Settings()
        self.screen = base_window.screen
        self.screen_rect = base_window.screen.get_rect()
        
        # Draw the rects.
        self._draw_rects(self._create_gui_rects())
        
    def _create_gui_rects(self):
        """Creates all basic gui rects."""
        # Create head rects.
        self.head_rect = pygame.Rect(0, 0, self.settings.screen_width - 30, 
            self.settings.screen_height // 7 + 10)
        self.head_rect.centerx = self.screen_rect.centerx
        self.head_rect.top = 15
        self.head_rect_color = (150, 150, 150)
        
        self.mines_left_rect = pygame.Rect(
            self.head_rect.top + 10,
            self.head_rect.left + 10,
            self.head_rect.width // 3 - 20,
            self.head_rect.height - 20
        )
        self.mines_left_rect_color = (200, 50, 50)
        
        self.time_rect = pygame.Rect(self.mines_left_rect)
        self.time_rect.right = self.head_rect.right - 5
        self.time_rect.y = self.mines_left_rect.y
        self.time_rect_color = self.mines_left_rect_color
        
        self.restart_rect = pygame.Rect(0, 0, self.mines_left_rect.height,
            self.mines_left_rect.height)
        self.restart_rect.center = self.head_rect.center
        self.restart_rect_color = (230, 230, 0)
        
        # Create body rect.
        self.body_rect = pygame.Rect(
            self.head_rect.left,
            self.head_rect.bottom + 15, 
            self.head_rect.width,
            self.screen_rect.height - self.head_rect.height - 45
        )
        self.body_rect_color = (150, 150, 150)
        
        # Return list of rects and its colors tuples.
        all_basic_gui_rects = [
            (self.head_rect, self.head_rect_color),
            (self.mines_left_rect, self.mines_left_rect_color),
            (self.time_rect, self.time_rect_color),
            (self.restart_rect, self.restart_rect_color),
            (self.body_rect, self.body_rect_color),
        ]
        return all_basic_gui_rects
        
    def _draw_rects(self, all_rects):
        """Draw given rects with given color."""
        for one_rect in all_rects:
            self.screen.fill(one_rect[1], rect=one_rect[0])