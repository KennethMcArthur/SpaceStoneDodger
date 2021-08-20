# pylint: disable=no-member

# SpaceStoneDodger: Asteroid and Asteroid Field Classes

import pygame
from random import randint
import ssd_constants as CST




class Asteroid(pygame.sprite.Sprite):
    """ Asteroid Class: a single asteroid object """

    def __init__(self, x: int, y: int, speed: int) -> None:
        self.deathflag = False
        self.sprite_image = CST.ASTEROID_SPRITE
        self.radius = self.sprite_image.get_width() / 2
        self.height = self.sprite_image.get_height()
        self.width = self.sprite_image.get_width()
        self.rect = self.sprite_image.get_rect()
        self.relocate(x, y, speed)


    def relocate(self, x: int, y: int, speed: int) -> None:
        """ Used to change the position and speed of a single asteroid NOT marked for death """
        if self.deathflag == False:
            self.x = x
            self.y = y
            self.speed = speed


    def game_tick_update(self, window: pygame.Surface) -> bool:
        """ Returns False if the asteroid was bound to death. otherwise is updated regularly """
        if self.deathflag and self.is_offscreen_left():
            return False
        self.x -= self.speed
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(self.sprite_image, (self.x, self.y))
        return True


    def is_offscreen_left(self) -> bool:
        """ Used to know if the asteroid is out of screen """
        return self.x < (0 - self.width)


    def mark_to_death(self) -> bool:
        """ Sets an asteroid up for deletion, if it already wasn't """    
        if self.deathflag == False:
            self.deathflag = True
            return True
        else:
            return False # already flagged for deletion





# This class is a "group manager" for asteroids
class Field:
    """
    Asteroid Field class

    Parameters:
    -player: the player object, for collisions checking (player Class object)
    """

    y_offset = CST.ASTEROID_SPRITE.get_height() // 2

    def __init__(self, howmany: int, player) -> None:
        self.player = player
        self.min_speed = 3
        self.max_speed = 8
        self.elements = [self.new_asteroid() for _ in range(howmany)]


    def random_position(self) -> int:
        """ returns a tuple of random x,y and speed """
        newx = randint(CST.SCREEN_WIDTH, CST.SCREEN_WIDTH*2)
        newy = randint(0-Field.y_offset , CST.SCREEN_HEIGHT-Field.y_offset)
        newspeed = randint(self.min_speed, self.max_speed)
        return newx, newy, newspeed


    def new_asteroid(self) -> Asteroid:
        """ returns a new asteroid at a random point of the spawn location """
        newx, newy, newspeed = self.random_position()
        return Asteroid(newx, newy, newspeed)


    def asteroids_still_alive(self) -> int:
        """ returns the number of asteroids still not flagged for death """
        return len([ast for ast in self.elements if ast.deathflag == False])


    def resize(self, newsize: int) -> None:
        """ Resizes the number of asteroids of the screen """
        oldsize = self.asteroids_still_alive() # ignoring death-flagged asteroids
        if newsize < oldsize: # too much asteroids
            flagged = 0
            i = 0
            while flagged < oldsize - newsize:
                outcome = self.elements[i].mark_to_death()
                flagged += outcome
                i += 1
        elif oldsize < newsize: # need more asteroids
            for _ in range(newsize - oldsize):
                self.elements.append(self.new_asteroid())


    def game_tick_update(self, window: pygame.Surface) -> None:
        """ Updates each asteroid """
        i = 0
        while i < len(self.elements): 
            this_ast = self.elements[i]
            if this_ast.game_tick_update(window): # if update was succesful (asteroid still alive)
                if this_ast.is_offscreen_left():
                    newx, newy, newspeed = self.random_position()
                    this_ast.relocate(newx, newy, newspeed)

                # Collisions checking
                if pygame.sprite.collide_circle(this_ast, self.player):
                    pygame.event.post(pygame.event.Event(CST.PLAYER_HIT))

                i += 1
            else: # the asteroid was marked for death
                self.elements.pop(i)










# TESTING AREA
if __name__ == "__main__":
    import sys
    import ssd_background as bg
    import ssd_player as plr

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")

    clock = pygame.time.Clock() # a clock object to slow the main loop
    
    num_asteroids = 3
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
            
            test_counter = 0


        test_counter += 1
