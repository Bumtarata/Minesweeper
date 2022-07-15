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
        
        # Create a gui.
        self.gui = Gui(self)
        
    def fill_bg(self):
        """Fill background with color."""
        self.screen.fill(self.settings.bg_color)

class Gui:
    """Class that manages creation of basic game GUI."""
    def __init__(self, base_window):
        """Initialize the gui and set it properly."""
        self.settings = Settings()
        self.screen = base_window.screen
        self.screen_rect = base_window.screen.get_rect()
        
    def create_gui_rects(self):
        """Creates all basic gui rects."""
        # Create head rects.
        self.head_rect = pygame.Rect(0, 0, self.settings.screen_width - 36, 
            self.settings.screen_height // 7 + 10)
        self.head_rect.centerx = self.screen_rect.centerx
        self.head_rect.top = 22
        self.head_rect_color = (self.settings.bg_color)
        
        self.mines_left_rect = pygame.Rect(
            self.head_rect.left + 15,
            self.head_rect.top + 10,
            self.head_rect.width // 3 - 20,
            self.head_rect.height - 20)
        self.mines_left_rect_color = (100, 25, 25)
        
        self.time_rect = pygame.Rect(self.mines_left_rect)
        self.time_rect.right = self.head_rect.right - 15
        self.time_rect.y = self.mines_left_rect.y
        self.time_rect_color = self.mines_left_rect_color
        
        self.restart_rect = pygame.Rect(0, 0, self.mines_left_rect.height,
            self.mines_left_rect.height)
        self.restart_rect.center = self.head_rect.center
        self.restart_rect_color = (230, 230, 0)
        
        # Create body rect.
        self.body_rect = pygame.Rect(
            self.head_rect.left,
            self.head_rect.bottom + 13, 
            self.head_rect.width,
            self.screen_rect.height - self.head_rect.height - 50)
        self.body_rect_color = (self.settings.bg_color)
        
        # Return list of rects and its colors tuples.
        all_basic_gui_rects = [
            (self.head_rect, self.head_rect_color),
            (self.mines_left_rect, self.mines_left_rect_color),
            (self.time_rect, self.time_rect_color),
            (self.restart_rect, self.restart_rect_color),
            (self.body_rect, self.body_rect_color),
        ]
        return all_basic_gui_rects
        
    def draw_rects(self, all_rects):
        """Draw given rects with given color."""
        for one_rect in all_rects:
            self.screen.fill(one_rect[1], rect=one_rect[0])
            
    def draw_lines(self):
        """Draw border lines."""
        # Draw white lines.
        white_color = self.settings.outline_white
        outer_white_lines = pygame.draw.lines(self.screen, color=white_color,
            closed=False, points=[self.screen_rect.bottomleft,
                self.screen_rect.topleft, self.screen_rect.topright],
            width = 10)
            
        head_white_lines = pygame.draw.lines(self.screen, color=white_color,
            closed=False, points=[self.head_rect.bottomleft,
                self.head_rect.bottomright, self.head_rect.topright],
            width = 5)
            
        mines_left_white_lines = pygame.draw.lines(self.screen, color=white_color,
            closed=False, points=[self.mines_left_rect.bottomleft,
                self.mines_left_rect.bottomright, self.mines_left_rect.topright],
            width = 2)
            
        time_white_lines = pygame.draw.lines(self.screen, color=white_color,
            closed=False, points=[self.time_rect.bottomleft,
                self.time_rect.bottomright, self.time_rect.topright],
            width = 2)
        
        body_white_lines = pygame.draw.lines(self.screen, color=white_color,
            closed=False, points=[self.body_rect.bottomleft,
                self.body_rect.bottomright, self.body_rect.topright],
            width = 5)
        
        # Draw grey lines.
        grey_color = self.settings.outline_grey
        outer_grey_lines = pygame.draw.lines(self.screen, color=grey_color,
            closed=False, points=[self.screen_rect.bottomleft,
                self.screen_rect.bottomright, self.screen_rect.topright],
            width = 10)
            
        head_grey_lines = pygame.draw.lines(self.screen, color=grey_color,
            closed=False, points=[self.head_rect.bottomleft,
                self.head_rect.topleft, self.head_rect.topright],
            width = 5)
        
        mines_left_grey_lines = pygame.draw.lines(self.screen, color=grey_color,
            closed=False, points=[self.mines_left_rect.bottomleft,
                self.mines_left_rect.topleft, self.mines_left_rect.topright],
            width = 2)
            
        time_grey_lines = pygame.draw.lines(self.screen, color=grey_color,
            closed=False, points=[self.time_rect.bottomleft,
                self.time_rect.topleft, self.time_rect.topright],
            width = 2)
        
        body_grey_lines = pygame.draw.lines(self.screen, color=grey_color,
            closed=False, points=[self.body_rect.bottomleft,
                self.body_rect.topleft, self.body_rect.topright],
            width = 5)
            