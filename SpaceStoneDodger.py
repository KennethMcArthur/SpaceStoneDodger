# This is my first game
# pylint: disable=no-member

import pygame, os, sys
import ssd_player
from random import randint

pygame.init()

# Constants declaration
ASSET_DIR = "assets"
SHIP_SPRITE = pygame.image.load(os.path.join(ASSET_DIR, "Ship.png"))
SPACE_BG = pygame.image.load(os.path.join(ASSET_DIR, 'bg_blurry.jpg'))
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
PLAYER_HIT = pygame.USEREVENT + 1 # Custom event for collisions
PLAYER_DEAD = pygame.USEREVENT + 2


# Super class to give game_tick_update() method to all classes
class Game_element:
    def __init__(self):
        pass

    def game_tick_update(self):
        pass



# A single asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        self.sprite_image = pygame.image.load(os.path.join(ASSET_DIR, "asteroid.png"))
        self.radius = self.sprite_image.get_width() / 2
        self.height = self.sprite_image.get_height()
        self.width = self.sprite_image.get_width()
        self.rect = self.sprite_image.get_rect()
        self.relocate(x, y, speed)
        
    def relocate(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def game_tick_update(self, window):
        self.x -= self.speed
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(self.sprite_image, (self.x, self.y))


# This class is a "group manager", will be used for both asteroids and background stars
class Field(Game_element):
    def __init__(self, howmany, player):
        self.size = howmany
        self.player = player
        self.min_speed = 3
        self.max_speed = 8
        self.elements = [self.new_asteroid() for _ in range(self.size)]

    def new_asteroid(self):
        return Asteroid(SCREEN_WIDTH * 1.5 + randint(0, 100),
                        randint(0, SCREEN_HEIGHT),
                        randint(self.min_speed, self.max_speed))

    def resize(self, newsize):
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
                    newx = SCREEN_WIDTH * 1.5 + randint(0,50)
                    newy = randint(0, SCREEN_HEIGHT)
                    newspeed = randint(self.min_speed, self.max_speed)
                    element.relocate(newx, newy, newspeed)
            element.game_tick_update(window)

            if pygame.sprite.collide_circle(element, self.player):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))
                
        # Inserting new asteroids if size is greater
        self.elements.extend([self.new_asteroid() for _ in range(self.size - len(self.elements))])


class Lifebar(pygame.sprite.Sprite):
    def __init__(self, player):
        self.UI_SPRITE_SIZE = 24
        self.sprite_image = SHIP_SPRITE
        self.sprite_image = pygame.transform.scale(self.sprite_image, (self.UI_SPRITE_SIZE, self.UI_SPRITE_SIZE))
        self.sprite_image = pygame.transform.rotate(self.sprite_image, 90)
        self.x = 0
        self.y = 10
        self.player = player

    def game_tick_update(self, window):
        current_health = self.player.health
        for lifepoint in range(current_health):
            coord_x = SCREEN_WIDTH - (lifepoint+1) * 32
            window.blit(self.sprite_image, (coord_x, self.y))
        if self.player.get_repair_status() > 0:
            newscale = int(self.UI_SPRITE_SIZE * (self.player.get_repair_status() / 100))
            smallsprite = pygame.transform.scale(self.sprite_image, (newscale, newscale))
            coord_x = SCREEN_WIDTH - (current_health+1) * 32 + (self.UI_SPRITE_SIZE // 2 - newscale //2)
            coord_y = self.y + (self.UI_SPRITE_SIZE // 2 - newscale //2)
            window.blit(smallsprite, (coord_x, coord_y))


class Background(Game_element):
    def __init__(self):
        self.sprite_image = SPACE_BG
        self.bg = pygame.transform.scale(self.sprite_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def game_tick_update(self, window):
        window.blit(self.bg, (0,0))





def main():
    # Defining our game window
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    clock = pygame.time.Clock() # a clock object to slow the main loop
    
    num_asteroids = 5

    bg = Background()
    testplayer = ssd_player.Player_pawn(SHIP_SPRITE, 50, SCREEN_HEIGHT // 2)
    testlifebar = Lifebar(testplayer)
    testfield = Field(num_asteroids, testplayer)

    updatelist = [] # Append order is draw order
    updatelist.append(bg)
    updatelist.append(testplayer)
    updatelist.append(testfield)
    updatelist.append(testlifebar)

    test_event_counter = 0

    # This will be our actual main game loop
    while True:
        clock.tick(FPS) # this slows the loop to the defined speed

        test_event_counter += 1

        for event in pygame.event.get():
            # Handling of quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # ensures we quit the program
            
            if event.type == PLAYER_HIT:
                testplayer.got_hit(PLAYER_DEAD)
            if event.type == PLAYER_DEAD:
                updatelist.remove(testplayer)

        # Key press capturing
        keys_pressed = pygame.key.get_pressed() # Gets a list of the key pressed        
        testplayer.handle_movement(keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Drawing sequence
        for gameobj in updatelist:
            gameobj.game_tick_update(WIN) # All classes have this methods
        pygame.display.update()

        if test_event_counter % 400 == 0: # Every 400 ticks
            num_asteroids += 1
            testfield.resize(num_asteroids)
            print("Asteroids: ", num_asteroids)
        
        if test_event_counter % 100 == 0:
            print("Repair state: ", testplayer.get_repair_status())
        



if __name__ == "__main__":
    main()
    