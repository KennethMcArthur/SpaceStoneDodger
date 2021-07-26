# pylint: disable=no-member

# SpaceStoneDodger: Player class

import pygame
import ssd_constants as cst


class Player_pawn(pygame.sprite.Sprite):
    """ Player class

    Parameters:
    -start_x: x position of the player (int)
    -start_y: y position of the player (int)
    """
    def __init__(self, start_x, start_y):
        self.sprite_image = cst.SHIP_SPRITE
        self.x = start_x
        self.y = start_y
        self.height = self.sprite_image.get_height()
        self.width = self.sprite_image.get_width()
        self.radius = self.sprite_image.get_width() / 2
        self.rect = self.sprite_image.get_rect()
        self.SHIP_SPEED = 5
        self.health = 3
        self.max_health = 3
        self.invul_timer = 0
        self.REPAIR_TIME = 5 * cst.FPS # Frames required to gain 1 life
        self.repair_timer = self.REPAIR_TIME


    def handle_movement(self, keys_pressed):
        """
        Manages the movement of the player based on key pressing

        Parameters:
        -keys_pressed: what keys are pressed (list)
        """
        if keys_pressed[pygame.K_a] and self.x - self.SHIP_SPEED > 0: #left key
            self.x -= self.SHIP_SPEED
        if keys_pressed[pygame.K_d] and self.x + self.SHIP_SPEED + self.width < cst.SCREEN_WIDTH: #right key
            self.x += self.SHIP_SPEED
        if keys_pressed[pygame.K_w] and self.y - self.SHIP_SPEED > 0: #up key
            self.y -= self.SHIP_SPEED
        if keys_pressed[pygame.K_s] and self.y + self.SHIP_SPEED + self.height < cst.SCREEN_HEIGHT: #down key
            self.y += self.SHIP_SPEED


    def got_hit(self, game_over_event):
        """
        Manages what happens when the player gets hit

        Parameters:
        -game_over_event: the event to be trigged on game over (pygame event)
        """
        if self.invul_timer == 0:
            self.health -= 1
            if self.health == 0: pygame.event.post(pygame.event.Event(game_over_event))
            self.invul_timer = 3 * cst.FPS
            self.repair_timer = self.REPAIR_TIME # Resetting repair state upon hit


    def repair(self):
        """ Checks the repair timer """
        if self.health < self.max_health:
            if self.repair_timer == 0:
                self.health += 1
                self.repair_timer = self.REPAIR_TIME
            else:
                self.repair_timer -= 1


    def get_repair_status(self):
        """ Returns a percentage of the current repair state """
        return 100 - (100 * self.repair_timer) // self.REPAIR_TIME


    def game_tick_update(self, window):
        if self.invul_timer > 0:
            self.invul_timer -= 1
            self.sprite_image.set_alpha(125)
        else:
            self.sprite_image.set_alpha(255)
            self.repair()
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(self.sprite_image, (self.x, self.y))
   