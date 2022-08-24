import pygame

from base_window import BaseWindow
from body_grid import Grid
from draw_lines_around_rect import draw_lines_around_rect as rect_lines
from settings import Settings

class Minesweeper:
    """The main class managing game assets and behaviour."""
    
    def __init__(self, first_init=True):
        """Initialize the game and create game resources."""
        if first_init:
            pygame.init()
            
            self.settings = Settings()
        
        self.window = BaseWindow(self)
        self.screen = self.window.screen
        
        # Fill window screen with color.
        self.window.fill_bg()
        
        # Create gui rects.
        self.gui_rects = self.window.gui.create_gui_rects()
        self.body_rect = self.gui_rects[0][0]
        
        self.body_grid = Grid(self)
        
        # Draw menu buttons
        self.window.gui.show_menu_buttons(difficulty=True, scoreboard=True)
        
        # Groups for sprites to be drawn.
        self.mines = pygame.sprite.Group()
        self.overlays = pygame.sprite.Group()
        self.marked_boxes = pygame.sprite.Group()
        self.restart_button_group = pygame.sprite.Group()
        
        # Game flags and other attributes.
        self.running = True
        self.active = True
        self.timer_active = False
        self.mines_left = self.settings.mines
        self.time_left = 0
        self.diff_highlighted = False
        self.sb_highlighted = False
        self.dropdown_menu_shown = False
        self.highlighted_dropdown_button = []
        self.checked_beg = True
        self.checked_int = False
        self.checked_exp = False
        self.checked_cstm = False
        
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
                self.show_wrnogly_marked_boxes()
                self.active = False
                pygame.time.set_timer(self.timer_event, 0)
                self.timer_active = False
                self.window.gui.restart_button.draw_button('dead_smile')
            
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
                
    
    def show_wrnogly_marked_boxes(self):
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
        """Check if winning conditions were met."""
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
                    self.mark_mine(box=box)
                self.active = False
                pygame.time.set_timer(self.timer_event, 0)
                self.timer_active = False
                win = True
                
        if win:
            self.window.gui.restart_button.draw_button('win_smile')
    
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
                    self.window.gui.show_menu_buttons(scoreboard=True, clicked=True)
        
        if not rects[0].collidepoint(mouse_pos) and rects[1].collidepoint(mouse_pos):
            if self.diff_highlighted:
                self.diff_highlighted = False
                self.window.gui.show_menu_buttons(difficulty=True)
        
        elif rects[0].collidepoint(mouse_pos) and not rects[1].collidepoint(mouse_pos):
            if self.sb_highlighted:
                self.sb_highlighted = False
                self.window.gui.show_menu_buttons(scoreboard=True)
        
        elif not rects[0].collidepoint(mouse_pos) and not rects[1].collidepoint(mouse_pos):
            if self.dropdown_menu_shown:
                if not self.window.gui.dropdown_rect.collidepoint(mouse_pos):
                    self.diff_highlighted = False
                    self.window.gui.show_menu_buttons(difficulty=True)
                
            elif self.diff_highlighted:
                self.diff_highlighted = False
                self.window.gui.show_menu_buttons(difficulty=True)
                
            elif self.sb_highlighted:
                self.sb_highlighted = False
                self.window.gui.show_menu_buttons(scoreboard=True)
    
    def create_dropdown_window(self):
        """Create dropdown window of difficulty menu. It needs to be called by 
        method which will display it on screen."""
        dd_rect = self.window.gui.dropdown_rect
        
        # Create rects for individual difficulty option.
        self.diff_opt_rects = []
        num_of_options = 4
        for num in range(1, num_of_options+1):
            rect_left = dd_rect.left
            rect_top = (dd_rect.top + 2) * num
            rect_width = dd_rect.width
            rect_height = dd_rect.height / num_of_options
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
            else:
                if checked_button == 'custom':
                    opt_text_string = 'Custom    \u2713'
                else:
                    opt_text_string = 'Custom'
            
            button_tuples.append((opt_rect, opt_text_string))
        return button_tuples
    
    def show_dropdown_window(self, button_tuples, just_button=False, highlight=False):
        """Calls create_dropdown_window method and displays dropdown window on
        screen. It takes as argument button tuples of rects and its texts."""
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
                self.screen.fill(button_color, button[0])
                dd_font = pygame.font.SysFont('segoeuisymbol', 14)
                dd_text = dd_font.render(button[1], True, text_color, button_color)
                dd_text_rect = dd_text.get_rect(left=button[0].left+10, top=button[0].top)
                self.screen.blit(dd_text, dd_text_rect)
        # button_tuples contains just one tuple, so without this code index references
        # would be messed up.
        else:
            self.screen.fill(button_color, button_tuples[0])
            dd_font = pygame.font.SysFont('segoeuisymbol', 14)
            dd_text = dd_font.render(button_tuples[1], True, text_color, button_color)
            dd_text_rect = dd_text.get_rect(left=button_tuples[0].left+10, top=button_tuples[0].top)
            self.screen.blit(dd_text, dd_text_rect)
            
        rect_lines(self, dd_rect, self.screen, thickness=1, inside=True, singlecolored='black')
    
    def highlight_dropdown_buttons(self, mouse_pos):
        """Highlight buttons in dropdown window if hovering over them."""
        if self.dropdown_menu_shown:
            button_tuples = self.create_dropdown_window()
            
            for one in button_tuples:
                if one[0].collidepoint(mouse_pos) and one not in self.highlighted_dropdown_button:
                    self.show_dropdown_window(one, just_button=True, highlight=True)
                    self.highlighted_dropdown_button.append(one)
                
                elif not one[0].collidepoint(mouse_pos) and one in self.highlighted_dropdown_button:
                    self.show_dropdown_window(one, just_button=True)
                    self.highlighted_dropdown_button.remove(one)
    
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
        
        if new_difficulty != None and self.settings.difficulty != new_difficulty:
            # difficulty is going to be changed
            self.settings = Settings(diff=new_difficulty)
            pygame.time.set_timer(self.timer_event, 0)
            self.__init__(first_init=False)
            self.prep_new_game()
    
    def hide_dropdown_menu(self):
        top = self.window.gui.head_rect.top - 20
        height = self.window.gui.head_rect.height + 30
        need_to_clear_rect = pygame.Rect(0, top, self.screen.get_rect().width, height)
        self.screen.fill(self.settings.bg_color, need_to_clear_rect)
        # Draw gui rects and lines.
        redraw_rects = list(self.gui_rects)
        redraw_rects.remove(self.gui_rects[0])
        self.window.gui.draw_rects(redraw_rects)
        self.window.gui.draw_lines()
        # Write mines left.
        self.window.gui.show_mines_left(self.mines_left)
        # Show proper time on timer.
        self.window.gui.show_time(self.time_left)
        
        self.dropdown_menu_shown = False
    
    def prep_new_game(self):
        """Resetup everything."""
        groups = [self.mines, self.overlays, self.marked_boxes, 
            self.restart_button_group]
        for group in groups:
            group.empty()
        
        # Reset flags.
        self.active = True
        self.timer_active = False
        
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
                        
                    if self.window.gui.restart_button.rect.collidepoint(mouse_pos) and button_clicked[0]:
                        self.window.gui.restart_button.click()
                        pygame.time.set_timer(self.unclick_event, 250, loops=1)
                        
                    diff_rect = self.window.gui.diff_rect
                    if button_clicked[0] and diff_rect.collidepoint(mouse_pos) and not self.dropdown_menu_shown:
                        button_tuples = self.create_dropdown_window()
                        self.show_dropdown_window(button_tuples)
                    elif button_clicked[0] and self.dropdown_menu_shown:
                        self.change_difficulty(mouse_pos)
                            
                elif event.type == self.timer_event:
                    self.add_time()
                elif event.type == self.unclick_event:
                    pygame.time.set_timer(self.timer_event, 0)
                    self.prep_new_game()
            
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.highlight_menu_button(mouse_pos)
                    if self.dropdown_menu_shown and self.diff_highlighted:
                        self.highlight_dropdown_buttons(mouse_pos)
                        
                    elif self.dropdown_menu_shown and not self.diff_highlighted:
                        self.hide_dropdown_menu()
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
            # Limit game's fps
            self.clock.tick(20)
            
if __name__ == '__main__':
    # Make the game instance and run the game.
    game = Minesweeper()
    game.run_game()