# pylint: disable=no-member

# SpaceStoneDodger: PowerUp and PowerUp Field Classes

import pygame
from random import randint
import ssd_constants as CST
from ssd_constants import pressed
import ssd_field as fld



class PowerUp(pygame.sprite.Sprite):
    """ PowerUp Class: a single power up object """

    # Class constants
    SPRITE_IMAGE = CST.ASTEROID_SPRITE
    HEIGHT = SPRITE_IMAGE.get_height()
    WIDTH = SPRITE_IMAGE.get_width()

    external_speed_modifier = 1

    def __init__(self, x: int, y: int, speed: int) -> None:
        self.radius = PowerUp.WIDTH // 2
        self.rect = PowerUp.SPRITE_IMAGE.get_rect()
        self.relocate(x, y, speed)


    def relocate(self, x: int, y: int, speed: int) -> None:
        """ Used to change the position and speed of a single power up """
        self.x = x
        self.y = y
        self.speed = speed


    def game_tick_update(self, window: pygame.Surface) -> None:
        """ Moves the power up left """
        self.x -= self.speed * PowerUp.external_speed_modifier
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(PowerUp.SPRITE_IMAGE, (self.x, self.y))


    def is_offscreen_left(self) -> bool:
        """ Used to know if the power up is out of screen """
        return self.x < (0 - PowerUp.WIDTH)



class PowerUpField(fld.Field_of):

    def __init__(self, howmany, player):
        self.player = player
        self.Y_OFFSET = PowerUp.HEIGHT // 2
        self.spawn_parameters = {
            "x_from": CST.SCREEN_WIDTH,
            "x_to": CST.SCREEN_WIDTH * 2,
            "y_from": 0 - self.Y_OFFSET,
            "y_to": CST.SCREEN_HEIGHT - self.Y_OFFSET,
            "min_speed": CST.ASTEROID_STARTING_MIN_SPEED,
            "max_speed": CST.ASTEROID_STARTING_MAX_SPEED
        }
        super().__init__(PowerUp, howmany, self.spawn_parameters)


    def handle_movement(self, keys_pressed: list) -> None:
        """ Manages the speed modifier of the field based on key pressing """
        speed_modifier = 1
        if pressed("LEFT", keys_pressed): #left key
            speed_modifier = CST.ASTEROID_SPEED_MODIFIER_DECEL
        if pressed("RIGHT", keys_pressed): #right key
            speed_modifier = CST.ASTEROID_SPEED_MODIFIER_ACCEL

        PowerUp.external_speed_modifier = speed_modifier
        

    def other_stuff_for_each(self, element):
        """ Overriding from super() class to add collision checking """
        # Collisions checking
        if pygame.sprite.collide_circle(element, self.player):
            pygame.event.post(pygame.event.Event(CST.PLAYER_HIT))






# TESTING AREA
if __name__ == "__main__":
    import sys
    import time as t
    import ssd_background as bg
    import ssd_player as plr

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")
    
    num_powerup = 30
    dummyplayer = plr.Player_pawn(50,50)
    testfield = PowerUpField(num_powerup, dummyplayer)
    testbg = bg.Background()

    updatelist = [] # Append order is draw order
    updatelist.append(testbg)
    updatelist.append(testfield)

    test_counter = 1

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
            # Drawing sequence
            for gameobj in updatelist:
                gameobj.game_tick_update(WIN) # All classes have this methods


            pygame.display.update()
