import pygame

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
        line_width = 6
        
        # lines around body_rect
        for a in range(line_width):
            gv_start_pos = (self.body_rect.topleft[0] - a,
                self.body_rect.topleft[1] - line_width+1)
            gv_end_pos = (self.body_rect.topleft[0] - a,
                self.body_rect.bottomleft[1] + a)
            grey_vertical = pygame.draw.line(self.screen, self.settings.outline_grey,
                gv_start_pos, gv_end_pos)
        
        for a in range(line_width):
            gh_start_pos = (self.body_rect.topleft[0] - line_width+1,
                self.body_rect.topleft[1] - a)
            gh_end_pos = (self.body_rect.topright[0] + a,
                self.body_rect.topright[1] - a)
            grey_horizontal = pygame.draw.line(self.screen, self.settings.outline_grey,
                gh_start_pos, gh_end_pos)
        
        for a in range(line_width):
            wv_start_pos = (self.body_rect.bottomright[0] + a,
                self.body_rect.bottomright[1] + line_width-1)
            wv_end_pos = (self.body_rect.topright[0] + a,
                self.body_rect.topright[1] - a)
            white_vertical = pygame.draw.line(self.screen, self.settings.outline_white,
                wv_start_pos, wv_end_pos)
        
        for a in range(line_width):
            wh_start_pos = (self.body_rect.bottomright[0] + line_width-1,
                self.body_rect.bottomright[1] + a)
            wh_end_pos = (self.body_rect.bottomleft[0] - a,
                self.body_rect.bottomleft[1] + a)
            white_horizontal = pygame.draw.line(self.screen, self.settings.outline_white,
                wh_start_pos, wh_end_pos)
                
        # lines around head_rect
        for a in range(line_width):
            gv_start_pos = (self.head_rect.topleft[0] - a,
                self.head_rect.topleft[1] - line_width+1)
            gv_end_pos = (self.head_rect.topleft[0] - a,
                self.head_rect.bottomleft[1] + a)
            grey_vertical = pygame.draw.line(self.screen, self.settings.outline_grey,
                gv_start_pos, gv_end_pos)
        
        for a in range(line_width):
            gh_start_pos = (self.head_rect.topleft[0] - line_width+1,
                self.head_rect.topleft[1] - a)
            gh_end_pos = (self.head_rect.topright[0] + a,
                self.head_rect.topright[1] - a)
            grey_horizontal = pygame.draw.line(self.screen, self.settings.outline_grey,
                gh_start_pos, gh_end_pos)
        
        for a in range(line_width):
            wv_start_pos = (self.head_rect.bottomright[0] + a,
                self.head_rect.bottomright[1] + line_width-1)
            wv_end_pos = (self.head_rect.topright[0] + a,
                self.head_rect.topright[1] - a)
            white_vertical = pygame.draw.line(self.screen, self.settings.outline_white,
                wv_start_pos, wv_end_pos)
        
        for a in range(line_width):
            wh_start_pos = (self.head_rect.bottomright[0] + line_width-1,
                self.head_rect.bottomright[1] + a)
            wh_end_pos = (self.head_rect.bottomleft[0] - a,
                self.head_rect.bottomleft[1] + a)
            white_horizontal = pygame.draw.line(self.screen, self.settings.outline_white,
                wh_start_pos, wh_end_pos)
                
        # lines for mines_left_rect
        for a in range(2):
            gv_start_pos = (self.mines_left_rect.topleft[0] - a,
                self.mines_left_rect.topleft[1] - 2+1)
            gv_end_pos = (self.mines_left_rect.topleft[0] - a,
                self.mines_left_rect.bottomleft[1] + a)
            grey_vertical = pygame.draw.line(self.screen, self.settings.outline_grey,
                gv_start_pos, gv_end_pos)
        
        for a in range(2):
            gh_start_pos = (self.mines_left_rect.topleft[0] - 2+1,
                self.mines_left_rect.topleft[1] - a)
            gh_end_pos = (self.mines_left_rect.topright[0] + a,
                self.mines_left_rect.topright[1] - a)
            grey_horizontal = pygame.draw.line(self.screen, self.settings.outline_grey,
                gh_start_pos, gh_end_pos)
        
        for a in range(2):
            wv_start_pos = (self.mines_left_rect.bottomright[0] + a,
                self.mines_left_rect.bottomright[1] + 2-1)
            wv_end_pos = (self.mines_left_rect.topright[0] + a,
                self.mines_left_rect.topright[1] - a)
            white_vertical = pygame.draw.line(self.screen, self.settings.outline_white,
                wv_start_pos, wv_end_pos)
        
        for a in range(2):
            wh_start_pos = (self.mines_left_rect.bottomright[0] + 2-1,
                self.mines_left_rect.bottomright[1] + a)
            wh_end_pos = (self.mines_left_rect.bottomleft[0] - a,
                self.mines_left_rect.bottomleft[1] + a)
            white_horizontal = pygame.draw.line(self.screen, self.settings.outline_white,
                wh_start_pos, wh_end_pos)
        
        # lines for time_rect
        for a in range(2):
            gv_start_pos = (self.time_rect.topleft[0] - a,
                self.time_rect.topleft[1] - 2+1)
            gv_end_pos = (self.time_rect.topleft[0] - a,
                self.time_rect.bottomleft[1] + a)
            grey_vertical = pygame.draw.line(self.screen, self.settings.outline_grey,
                gv_start_pos, gv_end_pos)
        
        for a in range(2):
            gh_start_pos = (self.time_rect.topleft[0] - 2+1,
                self.time_rect.topleft[1] - a)
            gh_end_pos = (self.time_rect.topright[0] + a,
                self.time_rect.topright[1] - a)
            grey_horizontal = pygame.draw.line(self.screen, self.settings.outline_grey,
                gh_start_pos, gh_end_pos)
        
        for a in range(2):
            wv_start_pos = (self.time_rect.bottomright[0] + a,
                self.time_rect.bottomright[1] + 2-1)
            wv_end_pos = (self.time_rect.topright[0] + a,
                self.time_rect.topright[1] - a)
            white_vertical = pygame.draw.line(self.screen, self.settings.outline_white,
                wv_start_pos, wv_end_pos)
        
        for a in range(2):
            wh_start_pos = (self.time_rect.bottomright[0] + 2-1,
                self.time_rect.bottomright[1] + a)
            wh_end_pos = (self.time_rect.bottomleft[0] - a,
                self.time_rect.bottomleft[1] + a)
            white_horizontal = pygame.draw.line(self.screen, self.settings.outline_white,
                wh_start_pos, wh_end_pos)