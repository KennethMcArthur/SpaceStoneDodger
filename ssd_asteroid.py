# pylint: disable=no-member

# SpaceStoneDodger: Asteroid and Asteroid Field Classes

import pygame
from random import randint
import ssd_constants as cst



# A single asteroid class
class Asteroid(pygame.sprite.Sprite):
    """
    Asteroid Class
    a single asteroid object

    Parameters:
    -x,y: starting positions (int)
    -speed: how many pixels the asteroid moves each frame (int)
    """
    def __init__(self, x, y, speed):
        self.sprite_image = cst.ASTEROID_SPRITE
        self.radius = self.sprite_image.get_width() / 2
        self.height = self.sprite_image.get_height()
        self.width = self.sprite_image.get_width()
        self.rect = self.sprite_image.get_rect()
        self.relocate(x, y, speed)


    def relocate(self, x, y, speed):
        """
        Used to change the position and speed of a single asteroid

        Parameters:
        -x,y: the new position (int)
        -speed: the new speed in pixels (int)
        """
        self.x = x
        self.y = y
        self.speed = speed


    def game_tick_update(self, window):
        self.x -= self.speed
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(self.sprite_image, (self.x, self.y))



# This class is a "group manager" for asteroids
class Field:
    """
    Asteroid Field class

    Parameters:
    -hoymany: number if starting asteroids on screen (int)
    -player: the player object, for collisions checking (player Class object)
    """
    def __init__(self, howmany, player):
        self.size = howmany
        self.player = player
        self.min_speed = 3
        self.max_speed = 8
        self.elements = [self.new_asteroid() for _ in range(self.size)]


    def new_asteroid(self):
        """
        Internal function to create a new single asteroid to populate the Field
        """
        return Asteroid(cst.SCREEN_WIDTH * 1.5 + randint(0, 100),
                        randint(0, cst.SCREEN_HEIGHT),
                        randint(self.min_speed, self.max_speed))


    def resize(self, newsize):
        """
        Resizes the number of asteroids of the screen. The Field acts accordingly

        Parameters:
        -newsize: the new number of asteroids on the screen (int)
        """
        self.size = newsize


    def game_tick_update(self, window):
        self.to_be_deleted = max(0, len(self.elements) - self.size) # Compressed if

        for element in self.elements[:]: # TRICK: iterating a COPY of the list allows safe resize of that list
            if element.x < 0 - element.width:
                if self.to_be_deleted > 0: # we ditch this element if there are too many...
                    self.elements.remove(element)
                    self.to_be_deleted -= 1
                    continue
                else:
                    newx = cst.SCREEN_WIDTH * 1.5 + randint(0,50)
                    newy = randint(0, cst.SCREEN_HEIGHT)
                    newspeed = randint(self.min_speed, self.max_speed)
                    element.relocate(newx, newy, newspeed)
            element.game_tick_update(window)

            # Collisions checking
            if pygame.sprite.collide_circle(element, self.player):
                pygame.event.post(pygame.event.Event(cst.PLAYER_HIT))
                
        # Inserting new asteroids if size is greater
        self.elements.extend([self.new_asteroid() for _ in range(self.size - len(self.elements))])
