# pylint: disable=no-member

# SpaceStoneDodger: Star and Star Field Classes

import pygame
from random import randint
import ssd_constants as CST
import ssd_field as fld
from ssd_constants import pressed



class Star(pygame.sprite.Sprite):
    """ Single star object """
    RADIUS = CST.STAR_SPRITE_RADIUS

    external_speed_modifier = 1

    def __init__(self, x: int, y: int, speed: int) -> None:
        grayshade = randint(50, 125) # Random grey shade to simulate different stars distances
        self.COLOR = (grayshade, grayshade, grayshade)
        self.relocate(x, y, speed)


    def relocate(self, x: int, y: int, speed: int) -> None:
        """ Used to change the position and speed of a star asteroid """
        self.x = x
        self.y = y
        self.speed = speed


    def game_tick_update(self, window) -> None:
        self.x -= self.speed * Star.external_speed_modifier
        if Star.external_speed_modifier == 1:
            pygame.draw.circle(window, self.COLOR, (self.x, self.y), Star.RADIUS)
        else:
            start_pos = (self.x, self.y)
            end_pos = (self.x + 3, self.y)
            pygame.draw.line(window, self.COLOR, start_pos, end_pos, self.RADIUS)
    
    
    def is_offscreen_left(self) -> bool:
        """ Used to know if the asteroid is out of screen """
        return self.x < (0 - Star.RADIUS)




class Starfield(fld.Field_of):
    def __init__(self, howmany: int):
        self.spawn_parameters = {
            "x_from": 0, # temporally set to 0 to have a full screen initial spawn
            "x_to": CST.SCREEN_WIDTH * 2,
            "y_from": 0,
            "y_to": CST.SCREEN_HEIGHT,
            "min_speed": CST.STARS_SPEED,
            "max_speed": CST.STARS_SPEED
        }
        super().__init__(Star, howmany, self.spawn_parameters)
        # After an initial full screen spawn, we set the spawn zone correctly
        self.spawn_parameters["x_from"] = CST.SCREEN_WIDTH

    def handle_movement(self, keys_pressed: list) -> None:
        """ Manages the speed modifier of the field based on key pressing """
        speed_modifier = 1
        if pressed("SPACE", keys_pressed): #left key
            speed_modifier = CST.BOOST_SPEED_MODIFIER

        Star.external_speed_modifier = speed_modifier    

    def other_stuff_for_each(self, element) -> None:
        if self.stop_all:
            if element.speed > 0:
                element.speed = 0.5



# TESTING AREA
if __name__ == "__main__":
    import sys
    import ssd_background as bg

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")

    clock = pygame.time.Clock() # a clock object to slow the main loop
    
    num_stars = 100
    testfield = Starfield(num_stars)
    testbg = bg.Background()

    updatelist = [] # Append order is draw order
    updatelist.append(testbg)
    updatelist.append(testfield)


    # This will be our actual main game loop
    while True:
        clock.tick(CST.FPS) # this slows the loop to the defined speed

        for event in pygame.event.get():
            # Handling of quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # ensures we quit the program
            
        # Key press capturing
        keys_pressed = pygame.key.get_pressed() # Gets a list of the key pressed        

        # Drawing sequence
        for gameobj in updatelist:
            gameobj.game_tick_update(WIN) # All classes have this methods

        pygame.display.update()