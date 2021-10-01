# pylint: disable=no-member

# SpaceStoneDodger: Text utility Classes

import pygame
import ssd_constants as CST




class StaticText:
    """ Class for text """
    def __init__(self, text: str, size: int, position: tuple, alignment: int = 0) -> None:
        self.alignment = alignment # Default is left
        self.pos_x, self.pos_y = position
        self.titlefont = pygame.font.Font(CST.TITLE_FONT, size)
        self.set_text(text)

    def set_text(self, new_text: str) -> None:
        """ Updates the text """
        self.titletext = self.titlefont.render(new_text, True, CST.COLOR_WHITE)
        self.place_me()

    def place_me(self):
        """ Places the text at the proper coords based on alignment """
        self.titlerect = self.titletext.get_rect()
        if self.alignment == CST.TXT.LEFT:
            self.titlerect.topleft = (self.pos_x, self.pos_y)
        elif self.alignment == CST.TXT.CENTER:
            self.titlerect.center = (self.pos_x, self.pos_y)
        elif self.alignment == CST.TXT.RIGHT:
            self.titlerect.topright = (self.pos_x, self.pos_y)

    def game_tick_update(self, window: pygame.Surface) -> None:
        window.blit(self.titletext, self.titlerect)



class AnimatedTypedText:
    """ Class for animated text """
    def __init__(self, text: str, size: int, position: tuple, speed: int, autostart: bool = True) -> None:
        """ Speed is a positive integer, FPS are divided by speed:
            1: one letter per second
            2: one letter every half a second
            ...and so on """
        self.pos_x, self.pos_y = position
        self.titlefont = pygame.font.Font(CST.TITLE_FONT, size)
        self.set_text(text) # setting up the full text for rect calculations
            
        #self.titlerect = self.titletext.get_rect()
        #self.titlerect = self.titlerect.move(self.pos_x, self.pos_y)

        self.speed = min(speed, CST.FPS) # Cannot have a speed greater than FPS
        self.speed_break_point = CST.FPS // speed

        self.total_text = text
        self.letters_shown = 0
        self.frame_counter = 0

        self.active = autostart



    def set_text(self, new_text: str) -> None:
        """ Updates the text """
        #self.titletext = self.titlefont.render(new_text, True, CST.COLOR_WHITE)
        self.rows_and_rects = {}
        char_height = self.titlefont.size(new_text)[1]
        row_count = 0
        for row in self.rowify(new_text):
            this_row_surface = self.titlefont.render(row, True, CST.COLOR_WHITE)
            this_row_y = self.pos_y + row_count * char_height
            self.rows_and_rects[row] = this_row_surface.get_rect().move(self.pos_x, this_row_y)
            row_count += 1


    def rowify(self, new_text: str) -> list:
        final_row_list = []
        for phrase in new_text.split('\n'):
            max_width = self.calculate_max_width(phrase, CST.SCREEN_WIDTH)
            while len(phrase) > max_width:
                if ' ' in phrase[:max_width]:
                    right_space = phrase[:max_width].rfind(' ')
                else:
                    right_space = max_width

                final_row_list.append(phrase[:right_space].strip())
                phrase = phrase[right_space:].lstrip()
            final_row_list.append(phrase)
        return final_row_list


    def calculate_max_width(self, text: str, right_limit: int) -> int:
        """ Calculates how many characters a text can have without breaking the right limit """
        max_chars = len(text)
        while self.titlefont.size(text[:max_chars])[0]+self.pos_x >= right_limit:
            max_chars -= 1
        return max_chars


    def start(self):
        """ Forces the text to start its animation """
        self.active = True


    def game_tick_update(self, window: pygame.Surface) -> None:
        if self.active:
            if self.letters_shown < len(self.total_text):
                self.frame_counter += 1
                
                if self.frame_counter % self.speed_break_point == 0:
                    self.frame_counter = 0
                    self.letters_shown += 1
                self.set_text(self.total_text[:self.letters_shown])
            
            for row in self.rows_and_rects.keys():
                this_row = self.titlefont.render(row, True, CST.COLOR_WHITE)
                window.blit(this_row, self.rows_and_rects[row])






# TESTING AREA
if __name__ == "__main__":
    import sys
    import time as t
    import ssd_background as bg

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")
    
    testbg = bg.Background()
    dummy_static_text = StaticText("Center", 32, (CST.SCREEN_WIDTH//2, 100), CST.TXT.CENTER)
    dummy_left_text = StaticText("Left", 32, (50, 50), CST.TXT.LEFT)
    dummy_right_text = StaticText("Right", 32, (CST.SCREEN_WIDTH-50, 150), CST.TXT.RIGHT)
    dummy_animated_text = AnimatedTypedText(
        "This is an animated text, it should appear after 5 seconds, one letter at time. But actually I'm doing tests on the text-wrapping, so don't expect much animation.\nAlso this line is forced on a new line because it should work. Hopefully.",
        12, (50, 300), 20, autostart=True)

    updatelist = [] # Append order is draw order
    updatelist.append(testbg)
    updatelist.append(dummy_static_text)
    updatelist.append(dummy_left_text)
    updatelist.append(dummy_right_text)
    updatelist.append(dummy_animated_text)

    test_counter = 0

    FRAME_CAP = 1.0 / CST.FPS # How many millisecons needs to pass
    time = t.time()
    unprocessed = 0

    while True:
        can_render = False
        time_2 = t.time()
        passed = time_2 - time
        unprocessed += passed
        time = time_2

        for event in pygame.event.get():
            # Handling of quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # ensures we quit the program
        
        while unprocessed >= FRAME_CAP:
            unprocessed -= FRAME_CAP
            can_render = True

        if can_render:
            # put everything inside here
            test_counter += 1

            # Drawing sequence
            for gameobj in updatelist:
                gameobj.game_tick_update(WIN) # All classes have this methods

            if test_counter == 5*CST.FPS: # after 5 seconds...
                dummy_animated_text.start()
            
            pygame.display.update()