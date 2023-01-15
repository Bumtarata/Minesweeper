import pygame

from draw_lines_around_rect import draw_lines_around_rect as rect_lines
from restart_button import RestartButton

class BaseWindow:
    """Class representing the base game window and gui."""
    def __init__(self, mines_game):
        """Initialize game window."""
        self.mines_game = mines_game
        self.settings = mines_game.settings
        self.set_window_icon()
        self.create_game_window()
    
    def set_window_icon(self):
        icon_file = './imgs/icon_mine.bmp'
        image = pygame.image.load(icon_file)
        pygame.display.set_icon(image)
    
    def create_game_window(self):
        """Create game window"""
        window_width = ((self.settings.box_width * self.settings.columns) +
            (self.settings.thickness_of_edges * 2))
        window_height = ((self.settings.box_height * (self.settings.rows + 3)) +
            (self.settings.thickness_of_edges * 3))
        pygame.display.set_caption("Minesweeper")
        self.screen = pygame.display.set_mode((window_width, window_height))
        
        # Create a gui instance.
        self.gui = Gui(self)
        
    def fill_bg(self):
        """Fill background with color."""
        self.screen.fill(self.settings.bg_color)

class Gui:
    """Class that manages creation of basic game GUI."""
    def __init__(self, base_window):
        """Initialize the gui and set it properly."""
        self.mines_game = base_window.mines_game
        self.settings = base_window.settings
        self.screen = base_window.screen
        self.screen_rect = base_window.screen.get_rect()
        
        font_file = 'font/DSEG7-Classic/DSEG7Classic-Bold.ttf'
        self.font = pygame.font.Font(font_file, 37)
        self.bright_red = (255, 0, 0)
        
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
        self.body_rect_color = self.settings.bg_color
        
        # Create menu bar rect.
        mb_width = self.screen_rect.width
        mb_height = self.settings.menu_height
        self.menu_bar_rect = pygame.Rect(0, 0, mb_width, mb_height)
        self.menu_bar_rect_color = self.settings.menu_color
        self.screen.fill(self.menu_bar_rect_color, self.menu_bar_rect)
        
        # Create difficulty dropdown menu rect.
        dropdown_left = self.menu_bar_rect.left
        dropdown_top = self.menu_bar_rect.bottom
        dropdown_width = 120
        dropdown_height = 3 * self.settings.box_height
        self.dropdown_rect = pygame.Rect(dropdown_left, dropdown_top,
            dropdown_width, dropdown_height)
        self.dropdown_rect_color = self.settings.menu_color
        
        # Create highscores dropdown menu rect.
        sb_dropdown_left = self.menu_bar_rect.left + 81
        sb_dropdown_top = self.dropdown_rect.top
        sb_dropdown_height = int(self.dropdown_rect.height / 4 * 3)
        sb_dropdown_width = 150
        self.sb_dropdown_rect = pygame.Rect(sb_dropdown_left, sb_dropdown_top,
            sb_dropdown_width, sb_dropdown_height)
        self.sb_dropdown_rect_color = self.settings.menu_color
        
        # Create custom diff menu rect.
        custom_left = self.dropdown_rect.right
        custom_top = dropdown_top
        custom_width = 110
        custom_height = dropdown_height
        self.custom_rect = pygame.Rect(custom_left, custom_top, custom_width,
            custom_height)
        self.custom_rect_color = self.settings.menu_color
        
        # Create head rects.
        hr_width = br_width
        hr_height = self.settings.box_height * 2
        hr_left_edge = br_left_edge
        hr_top_edge = self.settings.thickness_of_edges + mb_height
        
        self.head_rect = pygame.Rect(
            hr_left_edge,
            hr_top_edge,
            hr_width,
            hr_height)
        self.head_rect_color = self.settings.bg_color
        
        self.mines_left_rect = pygame.Rect(
            self.head_rect.left + 7,
            self.head_rect.top + 7,
            90, 46)
        self.mines_left_rect_color = (0, 0, 0)
        
        self.time_rect = pygame.Rect(self.mines_left_rect)
        self.time_rect.right = self.head_rect.right - 7
        self.time_rect.y = self.mines_left_rect.y
        self.time_rect_color = self.mines_left_rect_color
        
        
        # Rect containing everything besides menu bar.
        big_left = 0
        big_top = self.menu_bar_rect.height
        big_width = self.screen_rect.width
        big_height = self.screen_rect.height - self.menu_bar_rect.height
        self.big_rect = pygame.Rect(big_left, big_top, big_width, big_height)
        
        # Return list of rects and its colors tuples.
        all_basic_gui_rects = [
            (self.body_rect, self.body_rect_color),
            (self.head_rect, self.head_rect_color),
            (self.mines_left_rect, self.mines_left_rect_color),
            (self.time_rect, self.time_rect_color),
        ]
        return all_basic_gui_rects
        
    def draw_rects(self, all_rects, smile=None):
        """Draw given rects with given color."""
        for one_rect in all_rects:
            self.screen.fill(one_rect[1], rect=one_rect[0])
        
        # Create and draw restart_button.
        self.restart_button = RestartButton(self.mines_game)
        if smile:
            self.restart_button.draw_button(img_type=smile)
        else:
            self.restart_button.draw_button()
       
    def draw_lines(self):
        """Draw border lines."""
        rect_lines(self.mines_game, self.body_rect, self.screen)     # lines around body_rect
        rect_lines(self.mines_game, self.head_rect, self.screen)     # lines around head_rect
        rect_lines(self.mines_game, self.mines_left_rect, self.screen, thickness=3)  # lines for mines_left_rect
        rect_lines(self.mines_game, self.time_rect, self.screen, thickness=3)        # lines for time_rect
        rect_lines(self.mines_game, self.big_rect, self.screen, inside=True, invert=True)
        
    def show_menu_buttons(self, difficulty=False, highscores=False, clicked=False):
        """Create menu buttons"""
        font = pygame.font.SysFont(self.settings.menu_font_type, 14, bold=True)
        if clicked:
            font_color = (255, 255, 255)
            rect_bg_color = (0, 0, 150)
        elif not clicked:
            font_color = (0, 0, 0)
            rect_bg_color = self.settings.menu_color
        
        # Difficulty button
        if difficulty:
            diff_left = self.menu_bar_rect.left
            diff_top = self.menu_bar_rect.top
            diff_width = 80
            diff_height = self.menu_bar_rect.height
            self.diff_rect = pygame.Rect(diff_top, diff_left, diff_width, diff_height)
            self.screen.fill(rect_bg_color, self.diff_rect)
            diff_text = font.render('Difficulty', True, font_color, rect_bg_color)
            diff_text_rect = diff_text.get_rect()
            diff_text_rect.center = self.diff_rect.center
            diff_text_rect.y += 1
            self.screen.blit(diff_text, diff_text_rect)
        
        # Highscores button
        if highscores:
            sb_left = self.menu_bar_rect.left + 81
            sb_top = self.menu_bar_rect.top
            sb_width = 90
            sb_height = self.menu_bar_rect.height
            self.scoreboard_rect = pygame.Rect(sb_left, sb_top, sb_width, sb_height)
            self.screen.fill(rect_bg_color, self.scoreboard_rect)
            sb_text = font.render('Highscores', True, font_color, rect_bg_color)
            sb_text_rect = sb_text.get_rect()
            sb_text_rect.center = self.scoreboard_rect.center
            sb_text_rect.y += 1
            self.screen.blit(sb_text, sb_text_rect)
    
    def show_mines_left(self, num):
        """Writes number of mines that yet needs to be discovered to the 
        mines_left_rect."""
        mines_num = str(num)
        if len(mines_num) == 2:
            mines_num = f'0{mines_num}'
        elif len(mines_num) == 1:
            mines_num = f'00{mines_num}'
            
        text = self.font.render(mines_num, True, self.bright_red)
        text_rect = text.get_rect()
        text_rect.center = self.mines_left_rect.center
        
        # background numbers
        mines_bg_text = self.font.render('888', True, (80, 0, 0), (0, 0, 0))
        mines_bg_text_rect = mines_bg_text.get_rect()
        mines_bg_text_rect.center = self.mines_left_rect.center
        self.screen.blit(mines_bg_text, mines_bg_text_rect)
        
        self.screen.blit(text, text_rect)
        
    def show_time(self, time_left):
        """Show time_left in time_rect."""
        # background numbers
        timer_bg_text = self.font.render('888', True, (80, 0, 0), (0, 0, 0))
        timer_bg_text_rect = timer_bg_text.get_rect()
        timer_bg_text_rect.center = self.time_rect.center
        self.screen.blit(timer_bg_text, timer_bg_text_rect)
        
        time_left = str(time_left)
        if len(time_left) == 2:
            time_left = f'0{time_left}'
        elif len(time_left) == 1:
            time_left = f'00{time_left}'
            
        text = self.font.render(time_left, True, self.bright_red)
        text_rect = text.get_rect()
        text_rect.center = self.time_rect.center
        self.screen.blit(text, text_rect)