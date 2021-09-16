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
import ssd_powerup as pwr
import ssd_text_classes as txt

pygame.init()



def game_level(WIN: pygame.Surface) -> bool:

    FRAME_CAP = 1.0 / CST.FPS # How many millisecons needs to pass each frame

    num_power_ups = 1    
    num_asteroids = 5
    num_stars = 15

    level_background = bg.Background()
    starfield = stf.Starfield(num_stars)
    player = plr.Player_pawn(50, CST.SCREEN_HEIGHT // 2)
    ui_lifebar = plr.Lifebar(player)
    asteroid_field = ast.AsteroidField(num_asteroids, player)
    powerup_field = pwr.PowerUpField(num_power_ups, player)

    updatelist = [] # Append order is draw order
    updatelist.append(level_background)
    updatelist.append(powerup_field)
    updatelist.append(starfield)
    updatelist.append(player)
    updatelist.append(asteroid_field)
    updatelist.append(ui_lifebar)

    frame_counter = 0

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
                return True # Returning True on player death
            if event.type == CST.POWER_UP_COLLECTED:
                print("Power Up collected!") # Here we should totally do something more useful

        # Key state capturing
        keys_pressed = pygame.key.get_pressed() # Gets the bool state of all keyboard buttons

        # Frame stabilyzer
        while unprocessed >= FRAME_CAP:
            unprocessed -= FRAME_CAP
            can_render = True

        # What happens each frame
        if can_render:
            frame_counter += 1

            player.handle_movement(keys_pressed)
            asteroid_field.handle_movement(keys_pressed)

            # Drawing sequence
            for gameobj in updatelist:
                gameobj.game_tick_update(WIN) # All classes have this methods
            pygame.display.update()

            if frame_counter % (5*CST.FPS) == 0: # Every 5 seconds
                num_asteroids += 1
                asteroid_field.resize(num_asteroids)
                print("Asteroids: ", num_asteroids)
                frame_counter = 0

    return False

def game_menu(WIN: pygame.Surface) -> None:

    seconds = 10

    TITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.2)
    BOTTOM_TEXT_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.9)
    KEYS_TEXT_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.7)

    level_background = bg.Background()
    player = plr.Player_pawn(CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT // 2)
    text_title = txt.StaticText("Space Stone Dodger", 48, TITLE_COORDS)
    text_keys = txt.StaticText("Move with W,A,S,D", 32, KEYS_TEXT_COORDS)
    text_bottom = txt.StaticText("Game starting in 10 seconds", 24, BOTTOM_TEXT_COORDS)
    

    updatelist = [] # Append order is draw order
    updatelist.append(level_background)
    updatelist.append(player)
    updatelist.append(text_title)
    updatelist.append(text_keys)
    updatelist.append(text_bottom)
    

    frame_counter = 0

    time = t.time()
    unprocessed = 0
    FRAME_CAP = 1.0 / CST.FPS # How many millisecons needs to pass each frame
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
                
        # Key state capturing
        keys_pressed = pygame.key.get_pressed() # Gets the bool state of all keyboard buttons

        # Frame stabilyzer
        while unprocessed >= FRAME_CAP:
            unprocessed -= FRAME_CAP
            can_render = True

        # What happens each frame
        if can_render:
            frame_counter += 1

            player.handle_movement(keys_pressed)

            # Drawing sequence
            for gameobj in updatelist:
                gameobj.game_tick_update(WIN) # All classes have this methods
            pygame.display.update()

            if frame_counter % (1*CST.FPS) == 0: # every second
                seconds -= 1
                text_bottom.set_text("Game starting in " + str(seconds) + " seconds")
                frame_counter = 0
                if seconds == 0: return # Moving on to next Scene


def game_losing_screen(WIN: pygame.Surface) -> None:

    seconds = 5

    TITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT // 2)
    BOTTOM_TEXT_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.9)

    level_background = bg.Background()
    text_title = txt.StaticText("Sadly, stones Won", 48, TITLE_COORDS)
    text_bottom = txt.StaticText("Game Menu in 5 seconds", 20, BOTTOM_TEXT_COORDS)
    

    updatelist = [] # Append order is draw order
    updatelist.append(level_background)
    updatelist.append(text_title)
    updatelist.append(text_bottom)

    frame_counter = 0

    time = t.time()
    unprocessed = 0
    FRAME_CAP = 1.0 / CST.FPS # How many millisecons needs to pass each frame
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
                
        # Key state capturing
        #keys_pressed = pygame.key.get_pressed() # Gets the bool state of all keyboard buttons

        # Frame stabilyzer
        while unprocessed >= FRAME_CAP:
            unprocessed -= FRAME_CAP
            can_render = True

        # What happens each frame
        if can_render:
            frame_counter += 1

            # Drawing sequence
            for gameobj in updatelist:
                gameobj.game_tick_update(WIN) # All classes have this methods
            pygame.display.update()

            if frame_counter % (1*CST.FPS) == 0: # every second
                seconds -= 1
                text_bottom.set_text("Game Menu in " + str(seconds) + " seconds")
                frame_counter = 0
                if seconds == 0: return # Moving on to next Scene    





def main_game():
    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    # Scene order
    while True:
        game_menu(WIN)
        player_lose = game_level(WIN)
        if player_lose:
            game_losing_screen(WIN)



if __name__ == "__main__":
    main_game()
    