# This is my first game
# pylint: disable=no-member

import pygame, sys
import ssd_constants as cst
import ssd_player as plr
import ssd_asteroid as ast


pygame.init()


class Lifebar(pygame.sprite.Sprite):
    def __init__(self, player):
        self.UI_SPRITE_SIZE = 24
        self.sprite_image = cst.SHIP_SPRITE
        self.sprite_image = pygame.transform.scale(self.sprite_image, (self.UI_SPRITE_SIZE, self.UI_SPRITE_SIZE))
        self.sprite_image = pygame.transform.rotate(self.sprite_image, 90)
        self.x = 0
        self.y = 10
        self.player = player

    def game_tick_update(self, window):
        current_health = self.player.health
        for lifepoint in range(current_health):
            coord_x = cst.SCREEN_WIDTH - (lifepoint+1) * 32
            window.blit(self.sprite_image, (coord_x, self.y))
        if self.player.get_repair_status() > 0:
            newscale = int(self.UI_SPRITE_SIZE * (self.player.get_repair_status() / 100))
            smallsprite = pygame.transform.scale(self.sprite_image, (newscale, newscale))
            coord_x = cst.SCREEN_WIDTH - (current_health+1) * 32 + (self.UI_SPRITE_SIZE // 2 - newscale //2)
            coord_y = self.y + (self.UI_SPRITE_SIZE // 2 - newscale //2)
            window.blit(smallsprite, (coord_x, coord_y))


class Background:
    def __init__(self):
        self.sprite_image = cst.SPACE_BG
        self.bg = pygame.transform.scale(self.sprite_image, (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

    def game_tick_update(self, window):
        window.blit(self.bg, (0,0))





def main():
    # Defining our game window
    WIN = pygame.display.set_mode((cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    clock = pygame.time.Clock() # a clock object to slow the main loop
    
    num_asteroids = 5

    bg = Background()
    testplayer = plr.Player_pawn(50, cst.SCREEN_HEIGHT // 2)
    testlifebar = Lifebar(testplayer)
    testfield = ast.Field(num_asteroids, testplayer)

    updatelist = [] # Append order is draw order
    updatelist.append(bg)
    updatelist.append(testplayer)
    updatelist.append(testfield)
    updatelist.append(testlifebar)

    test_event_counter = 0

    # This will be our actual main game loop
    while True:
        clock.tick(cst.FPS) # this slows the loop to the defined speed

        test_event_counter += 1

        for event in pygame.event.get():
            # Handling of quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # ensures we quit the program
            
            if event.type == cst.PLAYER_HIT:
                testplayer.got_hit(cst.PLAYER_DEAD)
            if event.type == cst.PLAYER_DEAD:
                updatelist.remove(testplayer)

        # Key press capturing
        keys_pressed = pygame.key.get_pressed() # Gets a list of the key pressed        
        testplayer.handle_movement(keys_pressed)

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
    