# pylint: disable=no-member

# SpaceStoneDodger: Movie Effect utility for cinematics

import pygame
import ssd_constants as CST



class MovieEffect:
    """ Class for movie effect that adds black bands to the screen """
    def __init__(self, bands_height: int, animation_speed: int) -> None:
        self.original_height = bands_height
        self.current_height = bands_height

        self.upper_band_rect = pygame.Rect(0, 0, CST.SCREEN_WIDTH, bands_height)
        self.lower_band_rect = pygame.Rect(0, CST.SCREEN_HEIGHT - bands_height, CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT)

        # We divide FPS by animation_speed to find after how many frames we "tick"
        # Also, we pick the lesser between speed and FPS to avoid division issues
        self.frames_break_point = CST.FPS // min(animation_speed, CST.FPS)
        self.frame_counter = 0
        self.increment = 0 # Used to modify the height of bands during animation


    def hide(self) -> None:
        """ Hides both bands by forcing their current height to zero """
        self.current_height = 0


    def show(self) -> None:
        """ Instantly shows both bands by forcing their current height to max """
        self.current_height = self.original_height


    def start_animation(self) -> None:
        """ Starts the animation by changing the internal value of self.increment
            based on self.current_height, this produces two different animations """
        increment_values = {0: 1, self.original_height: -1}
        self.increment = increment_values.get(self.current_height, 0) # Compressed if


    def _animation_over(self) -> bool:
    	""" Internal method that checks if the current height is at one of the edges """
    	return self.current_height == 0 or self.current_height == self.original_height


    def game_tick_update(self, window: pygame.Surface) -> None:
    	# Checks if the animation is in progress
        if self.increment != 0:
            self.frame_counter += 1
            
            if self.frame_counter % self.frames_break_point == 0:
                self.frame_counter = 0
                self.current_height += self.increment
                # Stops the animation if needed
                if self._animation_over():
                    self.increment = 0

            self.upper_band_rect.update(0, 0, CST.SCREEN_WIDTH, self.current_height)
            self.lower_band_rect.update(0, CST.SCREEN_HEIGHT - self.current_height, CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT)

        pygame.draw.rect(window, CST.COLOR_BLACK, self.upper_band_rect)
        pygame.draw.rect(window, CST.COLOR_BLACK, self.lower_band_rect)




# TESTING AREA
if __name__ == "__main__":
    import sys
    import time as t
    import ssd_background as bg

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")
    
    testbg = bg.Background()
    movie_effect = MovieEffect(50, 20)

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
                movie_effect.start_animation()

                
            
            pygame.display.update()