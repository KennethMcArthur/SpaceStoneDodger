# pylint: disable=no-member

# SpaceStoneDodger: Asteroid and Asteroid Field Classes

import pygame
from random import randint
import ssd_constants as CST




class Asteroid(pygame.sprite.Sprite):
    """ Asteroid Class: a single asteroid object """

    # Class constants
    SPRITE_IMAGE = CST.ASTEROID_SPRITE
    HEIGHT = SPRITE_IMAGE.get_height()
    WIDTH = SPRITE_IMAGE.get_width()


    def __init__(self, x: int, y: int, speed: int) -> None:
        self.radius = Asteroid.WIDTH // 2
        self.rect = Asteroid.SPRITE_IMAGE.get_rect()
        self.relocate(x, y, speed)


    def relocate(self, x: int, y: int, speed: int) -> None:
        """ Used to change the position and speed of a single asteroid NOT marked for death """
        self.x = x
        self.y = y
        self.speed = speed


    def game_tick_update(self, window: pygame.Surface) -> None:
        """ Returns False if the asteroid was bound to death. otherwise is updated regularly """
        self.x -= self.speed
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(Asteroid.SPRITE_IMAGE, (self.x, self.y))


    def is_offscreen_left(self) -> bool:
        """ Used to know if the asteroid is out of screen """
        return self.x < (0 - Asteroid.WIDTH)







# This class is a "group manager" for asteroids
class Field:
    """
    Asteroid Field class

    Parameters:
    -player: the player object, for collisions checking (player Class object)
    """

    def __init__(self, howmany: int, player) -> None:
        self.player = player
        self.min_speed = 3
        self.max_speed = 8
        self.to_be_deleted = 0
        self.elements = [self.new_asteroid() for _ in range(howmany)]


    def random_position(self) -> int:
        """ returns a tuple of random x,y and speed """
        y_offset = Asteroid.HEIGHT // 2
        newx = randint(CST.SCREEN_WIDTH, CST.SCREEN_WIDTH*2)
        newy = randint(0 - y_offset , CST.SCREEN_HEIGHT - y_offset)
        newspeed = randint(self.min_speed, self.max_speed)
        return newx, newy, newspeed


    def new_asteroid(self) -> Asteroid:
        """ returns a new asteroid at a random point of the spawn location """
        newx, newy, newspeed = self.random_position()
        return Asteroid(newx, newy, newspeed)


    def resize(self, newsize: int) -> None:
        """ Resizes the number of asteroids of the screen """
        self.to_be_deleted = max(0, len(self.elements) - newsize) # Compressed if
        # Adding new asteroids if size is greater
        self.elements.extend([self.new_asteroid() for _ in range(newsize - len(self.elements))])


    def game_tick_update(self, window: pygame.Surface) -> None:
        """ Updates each asteroid """
        i = 0
        while i < len(self.elements): 
            element = self.elements[i]

            if element.is_offscreen_left():
                if self.to_be_deleted > 0: # we ditch this element if there are too many...
                    self.elements.pop(i)
                    self.to_be_deleted -= 1
                    continue
                else:
                    newx, newy, newspeed = self.random_position()
                    element.relocate(newx, newy, newspeed)

            element.game_tick_update(window)

            # Collisions checking
            if pygame.sprite.collide_circle(element, self.player):
                pygame.event.post(pygame.event.Event(CST.PLAYER_HIT))

            i += 1









# TESTING AREA
if __name__ == "__main__":
    import sys
    import ssd_background as bg
    import ssd_player as plr

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")

    clock = pygame.time.Clock() # a clock object to slow the main loop
    
    num_asteroids = 30
    dummyplayer = plr.Player_pawn(50,50)
    testfield = Field(num_asteroids, dummyplayer)
    testbg = bg.Background()

    updatelist = [] # Append order is draw order
    updatelist.append(testbg)
    updatelist.append(testfield)

    test_counter = 1

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

        if test_counter % (10*CST.FPS) == 0: # every 10 seconds
            # stuff to test
            new_asteroid_number = randint(0, 20)
            print(f"Asteroids: {len(testfield.elements)}, new amount: {new_asteroid_number}")
            testfield.resize(new_asteroid_number)

            test_counter = 0


        test_counter += 1
