# This is my first game
# pylint: disable=no-member

import pygame, sys
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

    clock = pygame.time.Clock() # a clock object to slow the main loop
    
    num_asteroids = 5
    num_stars = 15

    level_background = bg.Background()
    starfield = stf.Starfield(num_stars)
    player = plr.Player_pawn(50, CST.SCREEN_HEIGHT // 2)
    ui_lifebar = plr.Lifebar(player)
    asteroid_field = ast.Field(num_asteroids, player)

    updatelist = [] # Append order is draw order
    updatelist.append(level_background)
    updatelist.append(starfield)
    updatelist.append(player)
    updatelist.append(asteroid_field)
    updatelist.append(ui_lifebar)

    test_event_counter = 0

    # This will be our actual main game loop
    while True:
        test_event_counter += 1

        for event in pygame.event.get():
            # Handling of quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # ensures we quit the program
            
            if event.type == CST.PLAYER_HIT:
                player.got_hit(CST.PLAYER_DEAD)
            if event.type == CST.PLAYER_DEAD:
                updatelist.remove(player)

        # Key press capturing
        keys_pressed = pygame.key.get_pressed() # Gets a list of the key pressed        
        player.handle_movement(keys_pressed)

        # Drawing sequence
        for gameobj in updatelist:
            gameobj.game_tick_update(WIN) # All classes have this methods
        pygame.display.update()

        if test_event_counter % 400 == 0: # Every 400 ticks
            num_asteroids += 1
            asteroid_field.resize(num_asteroids)
            print("Asteroids: ", num_asteroids)
        
        clock.tick(CST.FPS) # this slows the loop to the defined speed


if __name__ == "__main__":
    main()
    