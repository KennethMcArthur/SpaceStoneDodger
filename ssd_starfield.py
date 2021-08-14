# pylint: disable=no-member

# SpaceStoneDodger: Star and Star Field Classes

import pygame
from random import randint
import ssd_constants as CST




class Star(pygame.sprite.Sprite):
    """ Single star object """

    def __init__(self, x: int, y: int, speed=CST.STARS_SPEED) -> None:
        self.RADIUS = 1
        self.COLOR = (125, 125, 125)
        self.relocate(x, y, speed)


    def relocate(self, x: int, y: int, speed=CST.STARS_SPEED) -> None:
        """ Used to change the position and speed of a star asteroid """
        self.x = x
        self.y = y
        self.speed = speed


    def game_tick_update(self, window) -> None:
        self.x -= self.speed
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.RADIUS)
        



# This class is a "group manager" for stars
class Starfield:
    """ Star field manager """
    def __init__(self, howmany: int) -> None:
        self.size = howmany
        self.elements = [self.new_star() for _ in range(self.size)]
        self.to_be_deleted = 0


    def new_star(self) -> Star:
        """ Internal function to create a new single star to populate the Field """
        return Star(CST.SCREEN_WIDTH + randint(0, CST.SCREEN_WIDTH),
                        randint(0, CST.SCREEN_HEIGHT))


    def resize(self, newsize: int) -> None:
        """ Resizes the number of stars of the screen. The Field acts accordingly """
        self.size = newsize
        self.to_be_deleted = max(0, len(self.elements) - self.size)


    def game_tick_update(self, window) -> None:
        # TRICK: iterating a COPY of the list allows safe resize of that list
        for element in self.elements[:]:
            if element.x < 0 - element.RADIUS*2: # if this element is off screen
                if self.to_be_deleted > 0:
                    self.elements.remove(element)
                    self.to_be_deleted -= 1
                    continue
                else:
                    newx = CST.SCREEN_WIDTH + 10
                    newy = randint(0, CST.SCREEN_HEIGHT)
                    element.relocate(newx, newy)
            element.game_tick_update(window)
                
        # Inserting new stars if size is greater
        self.elements.extend([self.new_star() for _ in range(self.size - len(self.elements))])




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