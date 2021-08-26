# This is my first game
# pylint: disable=no-member

# Thanks to William Hou from
# https://gamedev.stackexchange.com/questions/102586/locking-the-frame-rate-in-pygame
# for a mean to stabilyze the frame rate

import pygame, sys
import time as t
import ssd_constants as CST
import ssd_player as plr
import ssd_asteroid as ast
import ssd_starfield as stf
import ssd_background as bg


pygame.init()



def main():
    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    FRAME_CAP = 1.0 / CST.FPS # How many millisecons needs to pass each frame
    
    num_asteroids = 5
    num_stars = 15

    level_background = bg.Background()
    starfield = stf.Starfield(num_stars)
    player = plr.Player_pawn(50, CST.SCREEN_HEIGHT // 2)
    ui_lifebar = plr.Lifebar(player)
    asteroid_field = ast.AsteroidField(num_asteroids, player)

    updatelist = [] # Append order is draw order
    updatelist.append(level_background)
    updatelist.append(starfield)
    updatelist.append(player)
    updatelist.append(asteroid_field)
    updatelist.append(ui_lifebar)

    test_event_counter = 0

    time = t.time()
    unprocessed = 0

    # Main game loop
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
                
            if event.type == CST.PLAYER_HIT:
                player.got_hit(CST.PLAYER_DEAD)
            if event.type == CST.PLAYER_DEAD:
                updatelist.remove(player)

        # Key state capturing
        keys_pressed = pygame.key.get_pressed() # Gets the bool state of all keyboard buttons

        # Frame stabilyzer
        while unprocessed >= FRAME_CAP:
            unprocessed -= FRAME_CAP
            can_render = True

        # What happens each frame
        if can_render:
            test_event_counter += 1

            player.handle_movement(keys_pressed)
            asteroid_field.handle_movement(keys_pressed)

            # Drawing sequence
            for gameobj in updatelist:
                gameobj.game_tick_update(WIN) # All classes have this methods
            pygame.display.update()

            if test_event_counter % (5*CST.FPS) == 0: # Every 5 seconds
                num_asteroids += 1
                asteroid_field.resize(num_asteroids)
                print("Asteroids: ", num_asteroids)
                test_event_counter = 0
        


if __name__ == "__main__":
    main()
    