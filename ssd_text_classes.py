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
        self.titlerect = self.titletext.get_rect()
        self.titlerect = self.titlerect.move(self.pos_x, self.pos_y)

        self.speed = min(speed, CST.FPS) # Cannot have a speed greater than FPS
        self.speed_break_point = CST.FPS // speed

        self.total_text = text
        self.letters_shown = 0
        self.frame_counter = 0

        self.active = autostart


    def set_text(self, new_text: str) -> None:
        """ Updates the text """
        self.titletext = self.titlefont.render(new_text, True, CST.COLOR_WHITE)


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
    dummy_static_text = StaticText("Center", 32, (CST.SCREEN_WIDTH//2, 100), CST.TXT.CENTER)
    dummy_left_text = StaticText("Left", 32, (50, 50), CST.TXT.LEFT)
    dummy_right_text = StaticText("Right", 32, (CST.SCREEN_WIDTH-50, 150), CST.TXT.RIGHT)
    dummy_animated_text = AnimatedTypedText(
        "This is an animated text, it should appear after 5 seconds, one letter at time",
        12, (50, 300), 20, autostart=False)


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