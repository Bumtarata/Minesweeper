import pygame

from base_window import BaseWindow
from body_grid import Grid
from settings import Settings

class Minesweeper:
    """The main class managing game assets and behaviour."""
    
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        
        self.settings = Settings()
        self.window = BaseWindow(self)
        self.screen = self.window.screen
        
        # Create gui rects.
        self.gui_rects = self.window.gui.create_gui_rects()
        self.body_rect = self.gui_rects[0][0]
        
        self.body_grid = Grid(self)
        
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
        
    def prep_new_game(self):
        """Resetup everything."""
        groups = [self.mines, self.overlays, self.marked_boxes, 
            self.restart_button_group]
        for group in groups:
            group.empty()
        
        # Reset flags.
        self.active = True
        self.timer_active = False
        
        # Fill window screen with color.
        self.window.fill_bg()
        
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
                            
                elif event.type == self.timer_event:
                    self.add_time()
                elif event.type == self.unclick_event:
                    pygame.time.set_timer(self.timer_event, 0)
                    self.prep_new_game()
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
if __name__ == '__main__':
    # Make the game instance and run the game.
    game = Minesweeper()
    game.run_game()