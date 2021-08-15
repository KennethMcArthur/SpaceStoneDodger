# pylint: disable=no-member

# SpaceStoneDodger: Asteroid and Asteroid Field Classes

import pygame
from random import randint
import ssd_constants as CST




class Asteroid(pygame.sprite.Sprite):
    """ Asteroid Class: a single asteroid object """
    def __init__(self, x: int, y: int, speed: int) -> None:
        self.sprite_image = CST.ASTEROID_SPRITE
        self.radius = self.sprite_image.get_width() / 2
        self.height = self.sprite_image.get_height()
        self.width = self.sprite_image.get_width()
        self.rect = self.sprite_image.get_rect()
        self.relocate(x, y, speed)


    def relocate(self, x: int, y: int, speed: int) -> None:
        """ Used to change the position and speed of a single asteroid """
        self.x = x
        self.y = y
        self.speed = speed


    def game_tick_update(self, window: pygame.Surface) -> None:
        self.x -= self.speed
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(self.sprite_image, (self.x, self.y))



# This class is a "group manager" for asteroids
class Field:
    """
    Asteroid Field class

    Parameters:
    -player: the player object, for collisions checking (player Class object)
    """

    y_offset = CST.ASTEROID_SPRITE.get_height() // 2

    def __init__(self, howmany: int, player) -> None:
        self.size = howmany
        self.player = player
        self.min_speed = 3
        self.max_speed = 8
        self.elements = [self.new_asteroid() for _ in range(self.size)]
        self.to_be_deleted = 0


    def new_asteroid(self) -> Asteroid:
        """ Internal method to create a new single asteroid to populate the Field """
        return Asteroid(CST.SCREEN_WIDTH * 1.5 + randint(0, 100),
                        randint(0-Field.y_offset , CST.SCREEN_HEIGHT-Field.y_offset),
                        randint(self.min_speed, self.max_speed))


    def resize(self, newsize: int) -> None:
        """ Resizes the number of asteroids of the screen. The Field acts accordingly """
        self.size = newsize
        self.to_be_deleted = max(0, len(self.elements) - self.size) # Compressed if


    def game_tick_update(self, window: pygame.Surface) -> None:

        for element in self.elements[:]: # TRICK: iterating a COPY of the list allows safe resize of that list
            if element.x < 0 - element.width:
                if self.to_be_deleted > 0: # we ditch this element if there are too many...
                    self.elements.remove(element)
                    self.to_be_deleted -= 1
                    continue
                else:
                    newx = CST.SCREEN_WIDTH + randint(0, CST.SCREEN_WIDTH * 1.5)
                    newy = randint(0-Field.y_offset, CST.SCREEN_HEIGHT-Field.y_offset)
                    newspeed = randint(self.min_speed, self.max_speed)
                    element.relocate(newx, newy, newspeed)

            element.game_tick_update(window)

            # Collisions checking
            if pygame.sprite.collide_circle(element, self.player):
                pygame.event.post(pygame.event.Event(CST.PLAYER_HIT))
                
        # Adding new asteroids if size is greater
        self.elements.extend([self.new_asteroid() for _ in range(self.size - len(self.elements))])







# TESTING AREA
if __name__ == "__main__":
    import sys
    import ssd_background as bg
    import ssd_player as plr

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")

    clock = pygame.time.Clock() # a clock object to slow the main loop
    
    num_asteroids = 100
    dummyplayer = plr.Player_pawn(50,50)
    testfield = Field(num_asteroids, dummyplayer)
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
