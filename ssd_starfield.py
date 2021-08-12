# pylint: disable=no-member

# SpaceStoneDodger: Star and Star Field Classes

import pygame
from random import randint
import ssd_constants as cst



# A single asteroid class
class Star(pygame.sprite.Sprite):
    """ Single asteroid object """

    def __init__(self, x: int, y: int, speed: int) -> None:
        self.RADIUS = 1
        self.COLOR = (125, 125, 125)
        self.relocate(x, y, speed)


    def relocate(self, x: int, y: int, speed: int) -> None:
        """ Used to change the position and speed of a single asteroid """
        self.x = x
        self.y = y
        self.speed = speed


    def game_tick_update(self, window) -> None:
        self.x -= self.speed
        #self.rect.x, self.rect.y = self.x, self.y
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.RADIUS)
        #window.blit(self.sprite_image, (self.x, self.y))



# This class is a "group manager" for asteroids
class Starfield:
    """ Star field manager """
    def __init__(self, howmany: int) -> None:
        self.size = howmany
        self.stars_speed = 2
        self.elements = [self.new_star() for _ in range(self.size)]


    def new_star(self) -> Star:
        """ Internal function to create a new single star to populate the Field """
        return Star(cst.SCREEN_WIDTH * 1.5 + randint(0, cst.SCREEN_WIDTH),
                        randint(0, cst.SCREEN_HEIGHT),
                        self.stars_speed)


    def resize(self, newsize: int) -> None:
        """ Resizes the number of stars of the screen. The Field acts accordingly """
        self.size = newsize


    def game_tick_update(self, window) -> None:
        self.to_be_deleted = max(0, len(self.elements) - self.size) # Compressed if

        for element in self.elements[:]: # TRICK: iterating a COPY of the list allows safe resize of that list
            if element.x < 0 - element.RADIUS*2:
                if self.to_be_deleted > 0: # we ditch this element if there are too many...
                    self.elements.remove(element)
                    self.to_be_deleted -= 1
                    continue
                else:
                    newx = cst.SCREEN_WIDTH * 1.5 + randint(0,50)
                    newy = randint(0, cst.SCREEN_HEIGHT)
                    element.relocate(newx, newy, self.stars_speed)
            element.game_tick_update(window)
                
        # Inserting new stars if size is greater
        self.elements.extend([self.new_star() for _ in range(self.size - len(self.elements))])





if __name__ == "__main__":
    import sys

    pygame.init()

    WIN = pygame.display.set_mode((cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")

    clock = pygame.time.Clock() # a clock object to slow the main loop
    
    num_stars = 15
    testfield = Starfield(num_stars)

    updatelist = [] # Append order is draw order
    updatelist.append(testfield)


    # This will be our actual main game loop
    while True:
        clock.tick(cst.FPS) # this slows the loop to the defined speed

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