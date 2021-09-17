# pylint: disable=no-member

# SpaceStoneDodger: Text utility Classes

import pygame
import ssd_constants as CST




class StaticText:
    """ Class for centered text """
    def __init__(self, text: str, size: int, position: tuple) -> None:
        self.pos_x, self.pos_y = position
        self.titlefont = pygame.font.Font(CST.TITLE_FONT, size)
        self.set_text(text)

    def set_text(self, new_text: str) -> None:
        """ Updates the text """
        self.titletext = self.titlefont.render(new_text, True, CST.COLOR_WHITE)
        self.center_me()

    def center_me(self):
        """ Properly centers the text """
        self.titlerect = self.titletext.get_rect()
        self.titlerect.center = (self.pos_x, self.pos_y)

    def game_tick_update(self, window: pygame.Surface) -> None:
        window.blit(self.titletext, self.titlerect)



class AnimatedTypedText:
    """ Class for animated text """
    def __init__(self, text: str, size: int, position: tuple, speed: int) -> None:
        """ Speed is a positive integer, FPS are divided by speed:
            1: one letter per second
            2: one letter every half a second
            ...and so on """
        self.pos_x, self.pos_y = position
        self.titlefont = pygame.font.Font(CST.TITLE_FONT, size)
        self.set_text(text) # setting up the full text for rect calculations
        self.titlerect = self.titletext.get_rect()
        self.titlerect = self.titlerect.move(self.pos_x, self.pos_y)

        self.speed = speed
        self.speed_break_point = CST.FPS // speed

        self.total_text = text
        self.letters_shown = 0
        self.frame_counter = 0

    def set_text(self, new_text: str) -> None:
        """ Updates the text """
        self.titletext = self.titlefont.render(new_text, True, CST.COLOR_WHITE)

    def game_tick_update(self, window: pygame.Surface) -> None:
        if self.letters_shown < len(self.total_text):
            self.frame_counter += 1
            
            if self.frame_counter % self.speed_break_point == 0:
                self.frame_counter = 0
                self.letters_shown += 1
            self.set_text(self.total_text[:self.letters_shown])

        window.blit(self.titletext, self.titlerect)





# TESTING AREA
if __name__ == "__main__":
    import sys
    import time as t
    import ssd_background as bg

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")
    
    testbg = bg.Background()
    dummy_static_text = StaticText("Testo Statico", 32, (CST.SCREEN_WIDTH//2, 100))
    dummy_animated_text = AnimatedTypedText("Testo animato molto bene, davvero", 12, (50, 300), 30)


    updatelist = [] # Append order is draw order
    updatelist.append(testbg)
    updatelist.append(dummy_static_text)
    updatelist.append(dummy_animated_text)

    test_counter = 1

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
            # Drawing sequence
            for gameobj in updatelist:
                gameobj.game_tick_update(WIN) # All classes have this methods


            pygame.display.update()