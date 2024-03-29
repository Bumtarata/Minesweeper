import sqlite3

import pygame

from base_window import BaseWindow
from body_grid import Grid
from draw_lines_around_rect import draw_lines_around_rect as rect_lines
from settings import Settings

class Minesweeper:
    """The main class managing game assets and behavior."""
    
    def __init__(self, first_init=True):
        """Initialize the game and create game resources."""
        if first_init:
            pygame.init()
            self.settings = Settings()
            self.custom_settings = {'columns': None, 'rows': None, 'mines': None}
            
            # Create database for keeping high scores and create variable highscore
            self.con = sqlite3.connect('highscore.sqlite3')
            cur = self.con.cursor()
            # create highscore table in database; error means it already exists
            try:
                cur.execute("CREATE TABLE highscore(difficulty, time)")
            except sqlite3.OperationalError:
                pass
            self.highscore = self.get_high_score()  # dictionary (difficulty: time)
            cur.close()
        
        self.window = BaseWindow(self)
        self.screen = self.window.screen
        
        # Fill window screen with color.
        self.window.fill_bg()
        
        # Create main gui rects.
        self.gui_rects = self.window.gui.create_gui_rects()
        self.body_rect = self.gui_rects[0][0]
        
        self.body_grid = Grid(self)
        
        # Draw menu buttons
        self.window.gui.show_menu_buttons(difficulty=True, highscores=True)
        
        # Groups for sprites to be drawn.
        self.mines = pygame.sprite.Group()
        self.overlays = pygame.sprite.Group()
        self.marked_boxes = pygame.sprite.Group()
        self.restart_button_group = pygame.sprite.Group()
        
        # Game flags and other attributes.
        self.running = True
        self.active = True              # tells if user can uncover other boxes
        self.timer_active = False
        self.mines_left = self.settings.mines
        self.time_left = 0              # counts time since first click to body_rect
        
        # flags for menu bar, difficulty menu and so on
        self.diff_highlighted = False
        self.sb_highlighted = False
        self.dropdown_menu_shown = False
        self.sb_dropdown_menu_shown = False
        self.highlighted_dropdown_button = []
        self.custom_menu_shown = False
        self.active_rect = None
        self.input_text = ''
        self.ok_button_highlighted = False
        self.checked_beg = True         # which difficulty is currently selected
        self.checked_int = False
        self.checked_exp = False
        self.checked_cstm = False
        self.dead_smile = False
        self.win_smile = False
        
        # Clock for limiting game's fps.
        self.clock = pygame.time.Clock()
        
    def _uncover_clicked_box(self, mouse_pos):
        """Uncover the box that has been clicked."""
        for row in self.field_of_boxes:
            for box in row:
                if box.collidepoint(mouse_pos):
                    clicked_box = box
        
        if clicked_box.covered:
            clicked_box.covered = False
            uncovering_boxes = [clicked_box]
            
            if clicked_box.has_mine:
                self.show_wrongly_marked_boxes()
                self.active = False
                pygame.time.set_timer(self.timer_event, 0)
                self.timer_active = False
                self.window.gui.restart_button.draw_button('dead_smile')
                self.dead_smile = True
            
            # clicked box doesn't have adjacent mines; uncover all connected
            # boxes without adjacent mines
            elif not clicked_box.adjacent_mines:
                
                while True:
                    copy_uncovering_boxes = list(uncovering_boxes)
                    for box in copy_uncovering_boxes:
                        if not box.adjacent_mines and not box.adj_boxes_checked:
                            for adj_box in box.adjacent_boxes:
                                if adj_box not in uncovering_boxes and adj_box.covered:
                                    uncovering_boxes.append(adj_box)
                                    adj_box.covered = False
                            
                            box.adj_boxes_checked = True
                    
                    if uncovering_boxes == copy_uncovering_boxes:
                        break
            
            uncovering_marked_boxes = []
            for box in uncovering_boxes:
                box.remove_overlay(clicked_box)
                if box.marked:
                    uncovering_marked_boxes.append(box)
            if len(uncovering_marked_boxes) > 0:
                self.mines_left += len(uncovering_marked_boxes)
                self.window.gui.show_mines_left(self.mines_left)
                
    
    def show_wrongly_marked_boxes(self):
        """If clicked on box with mine, highlight boxes wrongly marked as boxes
        with mines."""
        wrongly_marked_boxes = []
        pink = (255, 150, 150)
        for row in self.field_of_boxes:
            for box in row:
                if box.marked and not box.has_mine:
                    wrongly_marked_boxes.append(box)
        
        if len(wrongly_marked_boxes) > 0:
            self.overlays.empty()
            for box in wrongly_marked_boxes:
                pink_overlay = box.create_overlay(color=pink)
                self.overlays.add(pink_overlay)
            
            self.overlays.draw(self.screen)
            self.overlays.empty()
            
            for box in wrongly_marked_boxes:
                box.marked = False
                self.mark_mine(box=box, count=False)
            
    def mark_mine(self, mouse_pos=None, box=None, count=True):
        """Mark with marked_mine sign box that has been clicked.
        Either need to provide with mouse_pos or box."""
        if mouse_pos:
            for row in self.field_of_boxes:
                for box in row:
                    if box.collidepoint(mouse_pos):
                        clicked_box = box
        
        else:
            clicked_box = box
        
        if not clicked_box.marked:
            clicked_box.marked = True
            sign = clicked_box.marked_mine_sign()
            self.marked_boxes.add(sign)
            self.marked_boxes.draw(self.screen)
            self.marked_boxes.empty()
            
            if count == True:
                self.mines_left -= 1
                self.window.gui.show_mines_left(self.mines_left)
        else:
            clicked_box.marked = False
            clicked_box_overlay = clicked_box.create_overlay()
            self.overlays.add(clicked_box_overlay)
            self.overlays.draw(self.screen)
            self.overlays.empty()
            
            self.mines_left += 1
            self.window.gui.show_mines_left(self.mines_left)
            
    def check_winning(self):
        """Check if winning conditions were met. That means either all mines
        were marked correctly or all uncovered boxes that are left are only
        boxes with mines. Returns True if conditions were met."""
        win = False
        if self.mines_left == 0:
            correct_marked_boxes = []
            for row in self.field_of_boxes:
                for box in row:
                    if box.marked and box in self.boxes_with_mines:
                        correct_marked_boxes.append(box)
                        
            if len(correct_marked_boxes) == len(self.boxes_with_mines):
                self.body_grid.uncover_left_boxes(self.field_of_boxes)
                self.active = False
                pygame.time.set_timer(self.timer_event, 0)
                self.timer_active = False
                win = True
                
        else:
            uncovered_boxes = []
            for row in self.field_of_boxes:
                for box in row:
                    if box.covered and not box.marked:
                        uncovered_boxes.append(box)
            if len(uncovered_boxes) == self.mines_left:
                for box in uncovered_boxes:
                    if not box.has_mine:
                        return False
                    else:
                        self.mark_mine(box=box)
                self.active = False
                pygame.time.set_timer(self.timer_event, 0)
                self.timer_active = False
                win = True
                
        if win:
            self.window.gui.restart_button.draw_button('win_smile')
            self.win_smile = True
            return True
        else:
            return False
    
    def get_high_score(self, diff='all'):
        """Get scores from database (either for currently chosen difficulty or
        for all three difficulties). Diff argument takes 'all' or 
        'beginner', or 'intermediate' or 'expert'.
        Returns dictionary where keys are difficulty levels and values are times"""
        cur = self.con.cursor()
        if diff == 'all':
            querry = "SELECT * FROM highscore"
        else:
            querry = f"SELECT difficulty, time FROM highscore WHERE difficulty='{diff}'"
        highscore = cur.execute(querry).fetchall()
        cur.close()
        highscore_dict = dict()
        for score in highscore:
            highscore_dict.update({score[0]: score[1]})
        return highscore_dict
    
    def update_highscore(self):
        """Updates highscore in proper row in database (based on selected
        difficulty) and in self.highscore dict."""
        row = self.settings.difficulty
        
        if row in self.highscore:
            querry = f"UPDATE highscore SET time={self.time_left} WHERE difficulty='{row}'"
        else:
            querry = f"INSERT INTO highscore VALUES ('{row}', {self.time_left})"
        
        # update database
        cur = self.con.cursor()
        cur.execute(querry)
        self.con.commit()
        # update self.highscore dict
        self.highscore.update({row: self.time_left})
        
    def compare_time_to_highscore(self):
        """Compares currently achieved time to high score. Returns True if 
        current time is better than time in high score."""
        if self.highscore[self.settings.difficulty] > self.time_left:
            return True
        else:
            return False
    
    def add_time(self):
        """Count seconds that passed since the first click on body_rect."""
        self.time_left += 1
        self.window.gui.show_time(self.time_left)
    
    def highlight_menu_button(self, mouse_pos):
        """Highlight menu button, when cursor is over it."""
        rects = [self.window.gui.diff_rect, self.window.gui.scoreboard_rect]
        for rect in rects:
            if rect.collidepoint(mouse_pos):
                if rect == rects[0] and self.diff_highlighted == False:
                    self.diff_highlighted = True
                    self.window.gui.show_menu_buttons(difficulty=True, clicked=True)
                    
                elif rect == rects[1] and self.sb_highlighted == False:
                    self.sb_highlighted = True
                    self.window.gui.show_menu_buttons(highscores=True, clicked=True)
        
        if not rects[0].collidepoint(mouse_pos) and rects[1].collidepoint(mouse_pos):
            if self.diff_highlighted:
                self.diff_highlighted = False
                self.window.gui.show_menu_buttons(difficulty=True)
        
        elif rects[0].collidepoint(mouse_pos) and not rects[1].collidepoint(mouse_pos):
            if self.sb_highlighted:
                self.sb_highlighted = False
                self.window.gui.show_menu_buttons(highscores=True)
        
        elif not rects[0].collidepoint(mouse_pos) and not rects[1].collidepoint(mouse_pos):
            if self.dropdown_menu_shown and not self.custom_menu_shown:
                if not self.window.gui.dropdown_rect.collidepoint(mouse_pos):
                    self.diff_highlighted = False
                    self.window.gui.show_menu_buttons(difficulty=True)
            
            elif self.dropdown_menu_shown:
                hover_over_dropdown = self.window.gui.dropdown_rect.collidepoint(mouse_pos)
                hover_over_custom = self.window.gui.custom_rect.collidepoint(mouse_pos)
                if not hover_over_dropdown and not hover_over_custom:
                    self.diff_highlighted = False
                    self.window.gui.show_menu_buttons(difficulty=True)
                    
            elif self.diff_highlighted:
                self.diff_highlighted = False
                self.window.gui.show_menu_buttons(difficulty=True)
                
            elif self.sb_dropdown_menu_shown:
                if not self.window.gui.sb_dropdown_rect.collidepoint(mouse_pos):
                    self.sb_highlighted = False
                    self.window.gui.show_menu_buttons(highscores=True)
            
            elif self.sb_highlighted:
                self.sb_highlighted = False
                self.window.gui.show_menu_buttons(highscores=True)
    
    def create_dropdown_window(self):
        """Create dropdown window of difficulty menu. It needs to be called by a
        method which will display it on screen."""
        dd_rect = self.window.gui.dropdown_rect
        
        # Create rects for individual difficulty option.
        self.diff_opt_rects = []
        num_of_options = 4
        for num in range(num_of_options):
            rect_width = dd_rect.width
            rect_height = dd_rect.height / num_of_options
            rect_left = dd_rect.left
            rect_top =(dd_rect.top + 1) + (rect_height * num)
            rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)
            self.diff_opt_rects.append(rect)
        
        button_tuples = []      # list of tuples consisting of rect and its text string
        checked_button = self.settings.difficulty
        for opt_rect in self.diff_opt_rects:
            if opt_rect == self.diff_opt_rects[0]:
                if checked_button == 'beginner':
                    opt_text_string = 'Beginner    \u2713'
                else:
                    opt_text_string = 'Beginner'
            elif opt_rect == self.diff_opt_rects[1]:
                if checked_button == 'intermediate':
                    opt_text_string = 'Intermediate    \u2713'
                else:
                    opt_text_string = 'Intermediate'
            elif opt_rect == self.diff_opt_rects[2]:
                if checked_button == 'expert':
                    opt_text_string = 'Expert    \u2713'
                else:
                    opt_text_string = 'Expert'
            elif opt_rect == self.diff_opt_rects[3]:
                if checked_button == 'custom':
                    opt_text_string = 'Custom    \u2713      >'
                else:
                    opt_text_string = 'Custom            >'
            
            button_tuples.append((opt_rect, opt_text_string))
        return button_tuples
        
    def create_sb_dropdown_window(self):
        """Create dropdown window of highscores menu. It needs to be called by a 
        method which will display it on screen."""
        sb_dd_rect = self.window.gui.sb_dropdown_rect
        
        # Create rects for individual diff settings scores.
        sb_opt_rects = []
        num_of_diffs = 3    # I won't track scores of custom diff
        for num in range(num_of_diffs):
            rect_width = sb_dd_rect.width
            rect_height = sb_dd_rect.height / num_of_diffs
            rect_left = sb_dd_rect.left
            rect_top =(sb_dd_rect.top + 1) + (rect_height * num)
            rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)
            sb_opt_rects.append(rect)
        
        rect_text_tuples = []   # list of tuples of rects and its texts
        for rect in sb_opt_rects:
            if rect == sb_opt_rects[0]:
                rect_text = 'Beginner:'
            elif rect == sb_opt_rects[1]:
                rect_text = 'Intermediate:'
            elif rect == sb_opt_rects[2]:
                rect_text = 'Expert:'
            rect_text_tuples.append((rect, rect_text))
        return rect_text_tuples
    
    def show_dropdown_window(self, button_tuples, just_button=False, highlight=False):
        """Displays dropdown window on screen. It takes as argument button tuples
        of rects and its texts."""
        dd_rect = self.window.gui.dropdown_rect
        dd_rect_color = self.window.gui.dropdown_rect_color
        
        if not just_button:
            # Fill dd_rect with color
            self.screen.fill(dd_rect_color, dd_rect)
            self.dropdown_menu_shown = True
            
        if highlight:
            button_color = (0, 0, 150)
            text_color = (255, 255, 255)
        else:
            button_color = dd_rect_color
            text_color = (0, 0, 0)
        
        # button_tuples contains four tuples.
        if len(button_tuples) != 2:
            for button in button_tuples:
                dd_font = pygame.font.SysFont('segoeuisymbol', 14)
                dd_text = dd_font.render(button[1], True, text_color, button_color)
                dd_text_rect = dd_text.get_rect(left=button[0].left+10, top=button[0].top)
                self.screen.blit(dd_text, dd_text_rect)
        # button_tuples contains just one tuple, so without this code below index
        # references would be messed up.
        else:
            self.screen.fill(button_color, button_tuples[0])
            dd_font = pygame.font.SysFont('segoeuisymbol', 14)
            dd_text = dd_font.render(button_tuples[1], True, text_color, button_color)
            dd_text_rect = dd_text.get_rect(left=button_tuples[0].left+10, top=button_tuples[0].top)
            self.screen.blit(dd_text, dd_text_rect)
            
        rect_lines(self, dd_rect, self.screen, thickness=1, inside=True, singlecolored='black')
        
    def show_sb_dropdown_menu(self, rect_text_tuples):
        """Displays highscores menu on screen. It takes as argument tuples of 
        rects and texts."""
        sb_dd_rect = self.window.gui.sb_dropdown_rect
        sb_dd_rect_color = self.window.gui.sb_dropdown_rect_color
        
        self.screen.fill(sb_dd_rect_color, sb_dd_rect)
        self.sb_dropdown_menu_shown = True
        
        text_color = (0, 0, 0)
        for elem in rect_text_tuples:
            sb_font = pygame.font.SysFont('segoeuisymbol', 14)
            sb_text = sb_font.render(elem[1], True, text_color, sb_dd_rect_color)
            sb_text_rect = sb_text.get_rect(left=elem[0].left+10, top=elem[0].top)
            self.screen.blit(sb_text, sb_text_rect)
        
        # show times next to difficulty levels
        for score in self.highscore:
            if score == 'beginner':
                score_rect = rect_text_tuples[0][0]
            elif score == 'intermediate':
                score_rect = rect_text_tuples[1][0]
            elif score == 'expert':
                score_rect = rect_text_tuples[2][0]
            score_text = sb_font.render(
                str(self.highscore[score])+'s', True, text_color, sb_dd_rect_color)
            score_text_rect = score_text.get_rect(right=score_rect.right-10,
                top=score_rect.top)
            self.screen.blit(score_text, score_text_rect)
            
        rect_lines(self, sb_dd_rect, self.screen, thickness=1, inside=True, singlecolored='black')
    
    def highlight_dropdown_buttons(self, mouse_pos):
        """Highlight buttons in dropdown window if hovering over them."""
        if self.dropdown_menu_shown:
            button_tuples = self.create_dropdown_window()
            
            for one in button_tuples:
                if one[0].collidepoint(mouse_pos) and one not in self.highlighted_dropdown_button:
                    self.show_dropdown_window(one, just_button=True, highlight=True)
                    self.highlighted_dropdown_button.append(one)
                
                elif not one[0].collidepoint(mouse_pos) and one in self.highlighted_dropdown_button:
                    if one != button_tuples[-1]:
                        self.show_dropdown_window(one, just_button=True)
                        self.highlighted_dropdown_button.remove(one)
                    else:
                        if not self.window.gui.custom_rect.collidepoint(mouse_pos):
                            self.hide_dropdown_window()
                            self.show_dropdown_window(self.create_dropdown_window())
                            self.highlighted_dropdown_button.clear()
                            
        
            if button_tuples[-1][0].collidepoint(mouse_pos) and not self.custom_menu_shown:
                self.show_custom_diff_window()
    
    def change_difficulty(self, mouse_pos):
        """When clicked on one of difficulty buttons in dropdown window, 
        recreate game window according to newly set difficulty."""
        rects = self.diff_opt_rects
        new_difficulty = None
        if rects[0].collidepoint(mouse_pos):
            # Beginner difficulty is chosen.
            new_difficulty = 'beginner'
        elif rects[1].collidepoint(mouse_pos):
            # Intermediate difficulty is chosen.
            new_difficulty = 'intermediate'
        elif rects[2].collidepoint(mouse_pos):
            # Expert difficulty is chosen
            new_difficulty = 'expert'
        elif self.custom_tuples[-1][0].collidepoint(mouse_pos) and self.custom_menu_shown:
            # Custom difficulty is chosen.
            new_difficulty = 'custom'
        
        if new_difficulty != None and (self.settings.difficulty != new_difficulty or self.settings.difficulty == 'custom'):
            # difficulty is going to be changed
            self.settings = Settings(diff=new_difficulty)
            if new_difficulty == 'custom':
                self.settings.columns = self.custom_settings['columns']
                self.settings.rows = self.custom_settings['rows']
                self.settings.mines = self.custom_settings['mines']
            else:
                self.custom_settings = {'columns': None, 'rows': None, 'mines': None}
            
            pygame.time.set_timer(self.timer_event, 0)
            self.__init__(first_init=False)
            self.prep_new_game()
    
    def create_custom_diff_window(self):
        """Create menu window to set custom difficulty."""
        # create window rect
        custom_rect = self.window.gui.custom_rect
        
        # Create three rects inside custom_rect. Those will be for columns, 
        # rows and mines settings. Plus one additional rect for ok button.
        custom_setting_rects = []
        for a in range(4):
            width = custom_rect.width
            height = custom_rect.height / 4
            left = custom_rect.left
            top = custom_rect.top + 1 + (a * height)
            rect = pygame.Rect(left, top, width, height)
            
            # Create rects to which player will write numbers for custom settings.
            num_width = 35
            num_height = rect.height - 6
            num_left = rect.right - (num_width + 5)
            num_top = rect.top + ((rect.height - num_height) / 2)
            num_rect = pygame.Rect(num_left, num_top, num_width, num_height)
            
            # create ok button (it has different size than the other rects
            if a == 3:
                width = rect.width - 40
                correct_rect = pygame.Rect(left, top, width, height)
                correct_rect.center = rect.center
                custom_setting_rects.append(correct_rect)
            else:
                custom_setting_rects.append((rect, num_rect))
        
        # create tuples of base rect, its text and rect into which users will
        # be able to write.
        for rect in list(custom_setting_rects):
            if rect == custom_setting_rects[0]:
                custom_setting_rects[0] = (custom_setting_rects[0][0], 'Columns: ',
                    custom_setting_rects[0][1])
            elif rect == custom_setting_rects[1]:
                custom_setting_rects[1] = (custom_setting_rects[1][0], 'Rows: ',
                    custom_setting_rects[1][1])
            elif rect == custom_setting_rects[2]:
                custom_setting_rects[2] = (custom_setting_rects[2][0], 'Mines: ',
                    custom_setting_rects[2][1])
            else:
                custom_setting_rects[3] = (custom_setting_rects[3], 'OK')
        return custom_setting_rects # elements of list are tuples of rect and text
        
    def show_custom_diff_window(self, ok_highlighted=False, just_ok=False):
        """Self explanatory name of method. just_ok means, that only ok button
        will be redrawn."""
        self.custom_tuples = self.create_custom_diff_window()
        self.ok_tuple = self.custom_tuples[-1]
        custom_rect = self.window.gui.custom_rect
        custom_rect_color = self.window.gui.custom_rect_color
        self.custom_menu_shown = True
        
        text_color = (0, 0, 0)
        font = pygame.font.SysFont('segoeuisymbol', 14)
        if ok_highlighted and just_ok:
            custom_rect_color = (0, 0, 150)
            text_color = (255, 255, 255)
        
        if not just_ok:
            # Fill custom_rect with custom_rect_color
            self.screen.fill(custom_rect_color, custom_rect)
            
            current_settings = [self.settings.columns, self.settings.rows, self.settings.mines]
            for element in self.custom_tuples:
                text = font.render(element[1], True, text_color, custom_rect_color)
                text_rect = text.get_rect(left=element[0].left+10, top=element[0].top)
                if element == self.custom_tuples[-1]:
                    text_rect.center = self.custom_tuples[-1][0].center
                self.screen.blit(text, text_rect)
                
                if element != self.custom_tuples[-1]:
                # show numbers of columns, rows and mines if they were set   
                    going_to_write = False
                    numfont = pygame.font.SysFont(self.settings.menu_font_type,
                        element[-1].height-4, bold=True)
                    if element == self.custom_tuples[0] and self.custom_settings['columns']:
                        text_surf = numfont.render(str(self.custom_settings['columns']), True, (0, 0, 0))
                        going_to_write = True
                    elif element == self.custom_tuples[1] and self.custom_settings['rows']:
                        text_surf = numfont.render(str(self.custom_settings['rows']), True, (0, 0, 0))
                        going_to_write = True
                    elif element == self.custom_tuples[2] and self.custom_settings['mines']:
                        text_surf = numfont.render(str(self.custom_settings['mines']), True, (0, 0, 0))
                        going_to_write = True
                    if going_to_write:
                        text_rect = text_surf.get_rect(center=element[-1].center)
                        self.screen.blit(text_surf, text_rect)
                    
                    # draw lines around rect where user can write custom settings
                    rect_lines(self, element[-1], self.screen, thickness=1,
                        singlecolored='black')
        else:
            text = font.render(self.ok_tuple[1], True, text_color, custom_rect_color)
            text_rect = text.get_rect(center=self.ok_tuple[0].center)
            self.screen.fill(custom_rect_color, self.ok_tuple[0])
            self.screen.blit(text, text_rect)
            
        rect_lines(self, custom_rect, self.screen, thickness=1, inside=True, singlecolored='black')
    
    def write_to_custom_diff_window(self, event, active=True):
        """Write into columns, rows and mines options in custom diff window.
        User needs to click to rect, then write numbers and then confirm by 
        hitting enter"""
        deactivate_rect = False
        return_clicked = False
        if active:
            color = (255, 255, 255)
        else:
            color = self.settings.menu_color
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(self.input_text) > 0:
                    written_number = int(self.input_text)
                    
                    if self.active_rect == self.custom_tuples[0][-1]:
                        if written_number < self.settings.min_columns:
                            written_number = self.settings.min_columns
                        elif written_number > self.settings.max_columns:
                            written_number = self.settings.max_columns
                        self.custom_settings['columns'] = written_number
                        written_setting = 'columns'
                    
                    elif self.active_rect == self.custom_tuples[1][-1]:
                        if written_number < self.settings.min_rows:
                            written_number = self.settings.min_rows
                        elif written_number > self.settings.max_rows:
                            written_number = self.settings.max_rows
                        self.custom_settings['rows'] = written_number
                        written_setting = 'rows'
                    
                    else:
                        try:
                            size = self.custom_settings['columns'] * self.custom_settings['rows']
                            ratio = size / written_number
                            if ratio > self.settings.max_ratio:
                                if size % self.settings.max_ratio == 0:
                                    written_number = size / self.settings.max_ratio
                                else:
                                    written_number = int(size / self.settings.max_ratio) + 1
                            self.custom_settings['mines'] = written_number
                            written_setting = 'mines'
                        except TypeError:
                        # Either columns or rows were not filled.
                            active = False
                
                color = self.settings.menu_color
                deactivate_rect = True
                return_clicked = True
            
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            
            else:
                try:
                    num = int(event.unicode)
                    # mines rect can contain 3 characters, columns and rows only 2 characters
                    if self.active_rect == self.custom_tuples[2][-1]:
                        max_chars = 3
                    else:
                        max_chars = 2
                    if len(self.input_text)+1 <= max_chars:
                            self.input_text += event.unicode
                except ValueError:
                # pressed key is not number
                    pass
        
        # highlight box for writing
        self.screen.fill(color, self.active_rect)
        
        # If self.custom_settings contains some filled numbers, show them in
        # proper rects. If user clicks to writing rect, it will become white 
        # and blank
        going_to_write = False
        if len(self.input_text) > 0 and active and not return_clicked:
            text = self.input_text
            going_to_write = True
        elif active and return_clicked:
            text = str(self.custom_settings[written_setting])
            going_to_write = True
        elif not active:
            if self.active_rect == self.custom_tuples[0][-1] and self.custom_settings['columns']:
                text = str(self.custom_settings['columns'])
                going_to_write = True
            elif self.active_rect == self.custom_tuples[1][-1] and self.custom_settings['rows']:
                text = str(self.custom_settings['rows'])
                going_to_write = True
            elif self.active_rect == self.custom_tuples[2][-1] and self.custom_settings['mines']:
                text = str(self.custom_settings['mines'])
                going_to_write = True
            
        if going_to_write:
            font = pygame.font.SysFont(self.settings.menu_font_type,
                self.active_rect.height-4, bold=True)
            text_surf = font.render(text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.active_rect.center)
            self.screen.blit(text_surf, text_rect)
        if deactivate_rect:
            self.active_rect = None
        
    def hide_dropdown_window(self):
        """Another self explanatory name of method."""
        top = self.window.gui.head_rect.top - 20
        height = self.window.gui.head_rect.height + 30
        need_to_clear_rect = pygame.Rect(0, top, self.screen.get_rect().width, height)
        self.screen.fill(self.settings.bg_color, need_to_clear_rect)
        # Draw gui rects and lines.
        redraw_rects = list(self.gui_rects)
        redraw_rects.remove(self.gui_rects[0])
        # Redraw restart button with proper smile.
        if self.win_smile:
            self.window.gui.draw_rects(redraw_rects, smile='win_smile')
        elif self.dead_smile:
            self.window.gui.draw_rects(redraw_rects, smile='dead_smile')
        else:
            self.window.gui.draw_rects(redraw_rects)
        self.window.gui.draw_lines()
        # Write mines left.
        self.window.gui.show_mines_left(self.mines_left)
        # Show proper time on timer.
        self.window.gui.show_time(self.time_left)
        
        self.dropdown_menu_shown = False
        self.custom_menu_shown = False
        self.sb_dropdown_menu_shown = False
        self.ok_highlighted = False
        self.active_rect = None
    
    def prep_new_game(self):
        """Resetup everything."""
        groups = [self.mines, self.overlays, self.marked_boxes, 
            self.restart_button_group]
        for group in groups:
            group.empty()
        
        # Reset flags.
        self.active = True
        self.timer_active = False
        self.win_smile = False
        self.dead_smile = False
        
        # Draw gui rects and lines.
        self.window.gui.draw_rects(self.gui_rects)
        self.window.gui.draw_lines()
        
        # Create gaming grid
        self.field_of_boxes = self.body_grid.create_field_of_boxes()   # passed is body_rect without color
        
        # Set up mines and correct adjacent_mines variable for each box.
        self.boxes_with_mines = self.body_grid.set_up_mines(self.field_of_boxes)
        self.body_grid.check_adj_boxes(self.field_of_boxes)
        
        # Hide all boxes by displaying overlay on them.
        self.overlays.add(self.body_grid.hide_all_boxes(self.field_of_boxes))
        self.overlays.draw(self.screen)
        self.overlays.empty()
        
        # Write mines left.
        self.mines_left = self.settings.mines
        self.window.gui.show_mines_left(self.mines_left)
        
        # Prepare timer.
        self.time_left = 0
        self.window.gui.show_time(self.time_left)
        self.timer_event = pygame.USEREVENT + 1
        
        # Prepare unclick event for restart_button.
        self.unclick_event = pygame.USEREVENT + 2
        
    def run_game(self):
        """Start the main loop for the game."""
        self.prep_new_game()
        
        while self.running:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    button_clicked = pygame.mouse.get_pressed()
                    if self.active:
                        if self.window.gui.body_rect.collidepoint(mouse_pos):
                            if not self.timer_active and (button_clicked[0] or button_clicked[2]):
                            # first click to body_rect starts the timer
                                self.timer_active = True
                                pygame.time.set_timer(self.timer_event, 1000)
                                
                            if button_clicked[0]:   # left button
                                self._uncover_clicked_box(mouse_pos)
                            
                            elif button_clicked[2]: # right button
                                self.mark_mine(mouse_pos)
                                
                            self.check_winning()
                            if self.check_winning():
                            # game has been won
                                
                                if self.settings.difficulty in self.highscore.keys() and self.compare_time_to_highscore():
                                # achieved time is better than time in
                                # high score --> update highscore
                                    self.update_highscore()
                                
                                elif not self.settings.difficulty in self.highscore.keys():
                                # highscore in this diff setting hasn't been won
                                # until now --> add new highscore
                                    self.update_highscore()
                    
                    # restart button clicked
                    if (self.window.gui.restart_button.rect.collidepoint(mouse_pos)
                        and button_clicked[0] and not self.custom_menu_shown):
                        self.window.gui.restart_button.click()
                        pygame.time.set_timer(self.unclick_event, 250, loops=1)
                    
                    # events for handling menu bar and changing difficulty
                    diff_rect = self.window.gui.diff_rect
                    scoreboard_rect = self.window.gui.scoreboard_rect
                    if button_clicked[0] and diff_rect.collidepoint(mouse_pos) and not self.dropdown_menu_shown:
                        self.show_dropdown_window(self.create_dropdown_window())
                    elif button_clicked[0] and self.dropdown_menu_shown and not diff_rect.collidepoint(mouse_pos) and not self.custom_menu_shown:
                        self.change_difficulty(mouse_pos)
                        
                    elif button_clicked[0] and self.custom_menu_shown:
                        for rect in self.custom_tuples:
                            if rect[0].collidepoint(mouse_pos) and rect != self.custom_tuples[-1]:
                                if not self.active_rect == rect[2]:
                                    if self.active_rect != None:
                                        self.write_to_custom_diff_window(event, active=False)
                                    self.input_text = ''
                                    self.active_rect = rect[2]
                                    
                            elif rect[0].collidepoint(mouse_pos) and rect == self.custom_tuples[-1]:
                                dict_values = self.custom_settings.values()
                                if None not in dict_values:
                                    self.change_difficulty(mouse_pos)
                                    
                    elif button_clicked[0] and scoreboard_rect.collidepoint(mouse_pos) and not self.sb_dropdown_menu_shown:
                        self.show_sb_dropdown_menu(self.create_sb_dropdown_window())
                
                # timer
                elif event.type == self.timer_event:
                    self.add_time()
                # event handling that simple animation when clicking on
                # restart button
                elif event.type == self.unclick_event:
                    pygame.time.set_timer(self.timer_event, 0)
                    self.prep_new_game()
            
                # mainly events for highlighting rects in menu bar
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.highlight_menu_button(mouse_pos)
                    if self.dropdown_menu_shown and self.diff_highlighted:
                        self.highlight_dropdown_buttons(mouse_pos)
                        
                        if self.custom_menu_shown:
                            if self.ok_tuple[0].collidepoint(mouse_pos) and not self.ok_button_highlighted:
                                self.show_custom_diff_window(ok_highlighted=True,
                                    just_ok=True)
                                self.ok_button_highlighted = True
                                
                            elif not self.ok_tuple[0].collidepoint(mouse_pos) and self.ok_button_highlighted:
                                self.show_custom_diff_window(just_ok=True)
                                self.ok_button_highlighted = False
                        
                    elif self.dropdown_menu_shown and not self.diff_highlighted:
                        self.hide_dropdown_window()
                    
                    elif self.sb_dropdown_menu_shown and not self.sb_highlighted:
                        self.hide_dropdown_window()
                
                # event for checking for writing in custom difficulty settings
                if self.active_rect != None and (event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN):
                    self.write_to_custom_diff_window(event)
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
            # Limit game's fps
            self.clock.tick(20)
            
if __name__ == '__main__':
    # Make the game instance and run the game.
    game = Minesweeper()
    game.run_game()