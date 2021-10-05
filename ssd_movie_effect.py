# pylint: disable=no-member

# SpaceStoneDodger: Movie Effect utility for cinematics

import pygame
import ssd_constants as CST



class MovieEffect:
    """ Class for movie effect that adds black bands to the screen """
    def __init__(self, bands_height: int) -> None:
        self.WIDTH = CST.SCREEN_WIDTH
        self.original_height = bands_height
        self.current_height = bands_height

        self.upper_band_rect = pygame.Rect(0, 0, self.WIDTH, bands_height)
        self.lower_band_rect = pygame.Rect(0, CST.SCREEN_HEIGHT - bands_height, self.WIDTH, CST.SCREEN_HEIGHT)

        speed = 40

        self.speed = min(speed, CST.FPS) # Cannot have a speed greater than FPS
        self.speed_break_point = CST.FPS // speed
        self.frame_counter = 0


    def hide(self) -> None:
        self.current_height = 0

    def show(self) -> None:
        self.current_height = self.original_height

    def animate(self, speed: int) -> None:
        pass

    def game_tick_update(self, window: pygame.Surface) -> None:

        if self.current_height <= self.original_height:
            self.frame_counter += 1
            
            if self.frame_counter % self.speed_break_point == 0:
                self.frame_counter = 0
                self.current_height += 1

        self.upper_band_rect.update(0, 0, self.WIDTH, self.current_height)
        self.lower_band_rect.update(0, CST.SCREEN_HEIGHT - self.current_height, self.WIDTH, CST.SCREEN_HEIGHT)

        pygame.draw.rect(window, CST.COLOR_WHITE, self.upper_band_rect)
        pygame.draw.rect(window, CST.COLOR_WHITE, self.lower_band_rect)




# TESTING AREA
if __name__ == "__main__":
    import sys
    import time as t
    import ssd_background as bg

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")
    
    testbg = bg.Background()
    movie_effect = MovieEffect(50)

    updatelist = [] # Append order is draw order
    updatelist.append(testbg)
    updatelist.append(movie_effect)


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
                movie_effect.hide()

                
            
            pygame.display.update()