import pygame

from draw_lines_around_rect import draw_lines_around_rect as rect_lines
from settings import Settings

class BaseWindow:
    """Class representing the base game window and gui."""
    def __init__(self):
        """Initialize game window."""
        self.settings = Settings()
        
        # Create game window
        window_width = ((self.settings.box_width * self.settings.columns) +
            (self.settings.thickness_of_edges * 2))
        window_height = ((self.settings.box_height * (self.settings.rows + 2)) +
            (self.settings.thickness_of_edges * 3))
        pygame.display.set_caption("Minesweeper")
        self.screen = pygame.display.set_mode((window_width, window_height))
        
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
        # Create body rect.
        br_width = self.settings.box_width * self.settings.columns
        br_height = self.settings.box_height * self.settings.rows
        br_left_edge = self.settings.thickness_of_edges
        br_top_edge = self.screen_rect.height - (
            self.settings.thickness_of_edges + br_height)
        
        self.body_rect = pygame.Rect(
            br_left_edge,
            br_top_edge, 
            br_width,
            br_height)
        self.body_rect_color = (self.settings.bg_color)
        
        # Create head rects.
        hr_width = br_width
        hr_height = self.settings.box_height * 2
        hr_left_edge = br_left_edge
        hr_top_edge = self.settings.thickness_of_edges
        
        self.head_rect = pygame.Rect(
            hr_left_edge,
            hr_top_edge,
            hr_width,
            hr_height)
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
        
        # Return list of rects and its colors tuples.
        all_basic_gui_rects = [
            (self.body_rect, self.body_rect_color),
            (self.head_rect, self.head_rect_color),
            (self.mines_left_rect, self.mines_left_rect_color),
            (self.time_rect, self.time_rect_color),
            (self.restart_rect, self.restart_rect_color),
        ]
        return all_basic_gui_rects
        
    def draw_rects(self, all_rects):
        """Draw given rects with given color."""
        for one_rect in all_rects:
            self.screen.fill(one_rect[1], rect=one_rect[0])
    
    def draw_lines(self):
        """Draw border lines."""
        rect_lines(self.body_rect, self.screen)     # lines around body_rect
        rect_lines(self.head_rect, self.screen)     # lines around head_rect
        rect_lines(self.mines_left_rect, self.screen, thickness=2)  # lines for mines_left_rect
        rect_lines(self.time_rect, self.screen, thickness=2)        # lines for time_rect
        rect_lines(self.screen_rect, self.screen, inside=True, invert=True)