# pylint: disable=no-member

# SpaceStoneDodger: Player class

import pygame
import ssd_constants as CST


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


    def handle_movement(self, keys_pressed: list) -> None:
        """ Manages the movement of the player based on key pressing """
        if keys_pressed[pygame.K_a] and self.x - self.SHIP_SPEED > 0: #left key
            self.x -= self.SHIP_SPEED
        if keys_pressed[pygame.K_d] and self.x + self.SHIP_SPEED + self.width < CST.SCREEN_WIDTH: #right key
            self.x += self.SHIP_SPEED
        if keys_pressed[pygame.K_w] and self.y - self.SHIP_SPEED > 0: #up key
            self.y -= self.SHIP_SPEED
        if keys_pressed[pygame.K_s] and self.y + self.SHIP_SPEED + self.height < CST.SCREEN_HEIGHT: #down key
            self.y += self.SHIP_SPEED


    def got_hit(self, game_over_event):
        """ Manages what happens when the player gets hit """
        if self.invul_timer == 0:
            self.health -= 1
            if self.health == 0: pygame.event.post(pygame.event.Event(game_over_event))
            self.invul_timer = CST.PLAYER_INVULNERABILITY_DURATION * CST.FPS
            self.repair_timer = self.REPAIR_TIME # Resetting repair state upon hit


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


    def game_tick_update(self, window):
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