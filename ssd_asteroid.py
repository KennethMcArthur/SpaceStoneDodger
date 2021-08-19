# pylint: disable=no-member

# SpaceStoneDodger: Asteroid and Asteroid Field Classes

import pygame
from random import randint
import ssd_constants as CST




class Asteroid(pygame.sprite.Sprite):
    """ Asteroid Class: a single asteroid object """

    asteroid_list = []

    def __init__(self, x: int, y: int, speed: int) -> None:
        Asteroid.asteroid_list.append(self)
        self.deathflag = False
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


    def game_tick_update(self, window: pygame.Surface) -> bool:
        if self.is_offscreen_left() and self.deathflag:
            Asteroid.asteroid_list.remove(self)
            return False
        self.x -= self.speed
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(self.sprite_image, (self.x, self.y))
        return True


    def is_offscreen_left(self) -> bool:
        """ Used to know if the asteroid is out of screen """
        return self.x < (0 - self.width)


    def mark_to_death(self) -> bool:
        if self.deathflag == False:
            self.deathflag = True
            return True
        else:
            return False # already flagged for deletion


    @staticmethod
    def asteroids_still_alive() -> int:
        """ returns the number of asteroids still not flagged for death """
        return len([ast for ast in Asteroid.asteroid_list if ast.deathflag == False])

   




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
        for _ in range(howmany):
            self.new_asteroid()

    def random_position(self):
        newx = CST.SCREEN_WIDTH * 1.5 + randint(0, 100)
        newy = randint(0-Field.y_offset , CST.SCREEN_HEIGHT-Field.y_offset)
        newspeed = randint(self.min_speed, self.max_speed)
        return newx, newy, newspeed

    def new_asteroid(self) -> Asteroid:
        newx, newy, newspeed = self.random_position()
        return Asteroid(newx, newy, newspeed)


    def resize(self, newsize: int) -> None:
        """ Resizes the number of asteroids of the screen """
        oldsize = Asteroid.asteroids_still_alive() # ignoring death-flagged asteroids
        if newsize < oldsize: # too much asteroids
            flagged = 0
            i = 0
            while flagged < oldsize - newsize:
                outcome = Asteroid.asteroid_list[i].mark_to_death()
                flagged += outcome
                i += outcome
        elif oldsize < newsize: # need more asteroids
            for _ in range(newsize - oldsize):
                self.new_asteroid()


    def game_tick_update(self, window: pygame.Surface) -> None:

        i = 0
        while i < len(Asteroid.asteroid_list):
            if Asteroid.asteroid_list[i].game_tick_update(window): # if update was succesful (asteroid still alive)
                if Asteroid.asteroid_list[i].is_offscreen_left():
                    newx, newy, newspeed = self.random_position()
                    Asteroid.asteroid_list[i].relocate(newx, newy, newspeed)

                # Collisions checking
                if pygame.sprite.collide_circle(Asteroid.asteroid_list[i], self.player):
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
