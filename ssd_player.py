# pylint: disable=no-member

# SpaceStoneDodger: Player class

import pygame
import ssd_constants as CST
from ssd_constants import pressed


class Player_pawn(pygame.sprite.Sprite):
    """ Player class """

    def __init__(self, start_x: int, start_y: int) -> None:
        self.sprite_image = CST.SHIP_SPRITE
        self.x = start_x
        self.y = start_y
        self.height = self.sprite_image.get_height()
        self.width = self.sprite_image.get_width()
        self.radius = self.sprite_image.get_width() / 2
        self.rect = self.sprite_image.get_rect()
        self.SHIP_SPEED = CST.PLAYER_SHIP_SPEED
        self.health = CST.PLAYER_STARTING_MAX_HEALTH
        self.max_health = CST.PLAYER_STARTING_MAX_HEALTH
        self.invul_timer = 0
        self.REPAIR_TIME = CST.PLAYER_REPAIR_TIME * CST.FPS # Frames required to gain 1 life
        self.repair_timer = self.REPAIR_TIME

        self.end_cinematic_x_pos = 0
        self.end_cinematic_y_pos = 0
        self.cpu_controlled = False


    def handle_movement(self, k_pressed: list) -> None:
        """ Manages the movement of the player based on key pressing """
        if self.cpu_controlled:
            return
        if pressed("LEFT", k_pressed) and self.x - self.SHIP_SPEED > 0:
            self.x -= self.SHIP_SPEED
        if pressed("RIGHT", k_pressed) and self.x + self.SHIP_SPEED + self.width < CST.SCREEN_WIDTH:
            self.x += self.SHIP_SPEED
        if pressed("UP", k_pressed) and self.y - self.SHIP_SPEED > 0:
            self.y -= self.SHIP_SPEED
        if pressed("DOWN", k_pressed) and self.y + self.SHIP_SPEED + self.height < CST.SCREEN_HEIGHT:
            self.y += self.SHIP_SPEED


    def got_hit(self, game_over_event):
        """ Manages what happens when the player gets hit """
        if self.invul_timer == 0:
            self.health -= 1
            if self.health == 0:
                pygame.event.post(pygame.event.Event(game_over_event))
            self.invul_timer = CST.PLAYER_INVULNERABILITY_DURATION * CST.FPS
            self.repair_timer = self.REPAIR_TIME # Resetting repair state upon hit


    def is_invulnerable(self) -> bool:
        """ Checks if the player is still invulnerable after a hit """
        return self.invul_timer != 0


    def repair(self) -> None:
        """ Checks the repair timer """
        if self.health < self.max_health:
            if self.repair_timer == 0:
                self.health += 1
                self.repair_timer = self.REPAIR_TIME
            else:
                self.repair_timer -= 1


    def get_repair_status(self) -> int:
        """ Returns a percentage of the current repair state """
        return 100 - (100 * self.repair_timer) // self.REPAIR_TIME


    def user_controlled(self) -> None:
        """ Give control back to the user """
        self.cpu_controlled = False


    def automove_to(self, x: int, y: int) -> None:
        """ Sets where the ship should go in automove """
        self.cpu_controlled = True
        self.end_cinematic_x_pos = x
        self.end_cinematic_y_pos = y


    def automove(self):
        """ Moves the ship automatically """
        if self.x < self.end_cinematic_x_pos:
            self.x += self.SHIP_SPEED
        if self.x > self.end_cinematic_x_pos:
            self.x -= self.SHIP_SPEED
        if self.y < self.end_cinematic_y_pos:
            self.y += self.SHIP_SPEED
        if self.y > self.end_cinematic_y_pos:
            self.y -= self.SHIP_SPEED


    def game_tick_update(self, window):
        if self.cpu_controlled:
            self.automove()

        if self.invul_timer > 0:
            self.invul_timer -= 1
            self.sprite_image.set_alpha(125)
        else:
            self.sprite_image.set_alpha(255)
            self.repair()
        
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(self.sprite_image, (self.x, self.y))
   




class Lifebar(pygame.sprite.Sprite):
    def __init__(self, player: Player_pawn) -> None:
        self.UI_SPRITE_SIZE = 24
        self.sprite_image = CST.SHIP_SPRITE
        self.sprite_image = pygame.transform.scale(self.sprite_image, (self.UI_SPRITE_SIZE, self.UI_SPRITE_SIZE))
        self.sprite_image = pygame.transform.rotate(self.sprite_image, 90)
        self.x = 0
        self.y = 10
        self.player = player

    def game_tick_update(self, window):
        current_health = self.player.health
        for lifepoint in range(current_health):
            coord_x = CST.SCREEN_WIDTH - (lifepoint+1) * 32
            window.blit(self.sprite_image, (coord_x, self.y))
        if self.player.get_repair_status() > 0:
            newscale = int(self.UI_SPRITE_SIZE * (self.player.get_repair_status() / 100))
            smallsprite = pygame.transform.scale(self.sprite_image, (newscale, newscale))
            coord_x = CST.SCREEN_WIDTH - (current_health+1) * 32 + (self.UI_SPRITE_SIZE // 2 - newscale //2)
            coord_y = self.y + (self.UI_SPRITE_SIZE // 2 - newscale //2)
            window.blit(smallsprite, (coord_x, coord_y))










# TESTING AREA
if __name__ == "__main__":
    import sys
    import time as t
    import ssd_background as bg

    pygame.init()

    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Test Field")
    
    testbg = bg.Background()
    player = Player_pawn(50, 50)

    updatelist = [] # Append order is draw order
    updatelist.append(testbg)
    updatelist.append(player)

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

            if test_counter == 10*CST.FPS: # after 10 seconds...
                print("Automoved")
                player.automove_to(300,100)
                
            
            pygame.display.update()