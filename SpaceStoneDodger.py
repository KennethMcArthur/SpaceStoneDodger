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
import ssd_scene_master_class as Scn

pygame.init()




class GameMenu(Scn.Scene):
    def scene_related_init(self):
        TITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.2)
        BOTTOM_TEXT_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.9)
        KEYS_TEXT_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.7)

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(15)
        self.player = plr.Player_pawn(CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT // 2)
        self.text_title = txt.StaticText("Space Stone Dodger", 48, TITLE_COORDS, CST.TXT.CENTER)
        self.text_keys = txt.StaticText("Move with W,A,S,D", 32, KEYS_TEXT_COORDS, CST.TXT.CENTER)
        self.text_bottom = txt.StaticText("(press [SPACE] to begin)", 24, BOTTOM_TEXT_COORDS, CST.TXT.CENTER)
        
        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.player)
        self.updatelist.append(self.text_title)
        self.updatelist.append(self.text_keys)
        self.updatelist.append(self.text_bottom)

    def keys_to_check(self, key_list: list):
        self.player.handle_movement(key_list)
        if CST.pressed("SPACE", key_list):
            self.quit_loop(CST.SCENES.GAME_LEVEL)



class GameLevel(Scn.Scene):
    def scene_related_init(self):
        self.num_power_ups = 3
        self.num_asteroids = 5
        self.num_stars = 15

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(self.num_stars)
        self.player = plr.Player_pawn(50, CST.SCREEN_HEIGHT // 2)
        self.ui_lifebar = plr.Lifebar(self.player)
        self.asteroid_field = ast.AsteroidField(self.num_asteroids, self.player)
        self.powerup_field = pwr.PowerUpField(self.num_power_ups, self.player)

        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.powerup_field)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.player)
        self.updatelist.append(self.asteroid_field)
        self.updatelist.append(self.ui_lifebar)

    def event_checking(self, this_event: pygame.event) -> None:
        super().event_checking(this_event) # for quitting handling
        if this_event.type == CST.PLAYER_HIT:
            self.player.got_hit(CST.PLAYER_DEAD)
        if this_event.type == CST.PLAYER_DEAD:
            self.quit_loop(CST.SCENES.GAME_LOSING_SCREEN)
        if this_event.type == CST.POWER_UP_COLLECTED:
            print("Power Up collected!") # Here we should totally do something more useful

    def keys_to_check(self, key_list: list) -> None:
        self.player.handle_movement(key_list)
        self.asteroid_field.handle_movement(key_list)

    def reset_state(self):
        self.__init__(self.GAME_WINDOW) # Forcing the level to initial state




class GameLosingScreen(Scn.Scene):
    def scene_related_init(self):
        TITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT // 2)
        BOTTOM_TEXT_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.9)

        self.level_background = bg.Background()
        self.text_title = txt.StaticText("Sadly, stones Won", 48, TITLE_COORDS, CST.TXT.CENTER)
        self.text_bottom = txt.StaticText("(press [SPACE] to play again)", 20, BOTTOM_TEXT_COORDS, CST.TXT.CENTER)
        
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.text_title)
        self.updatelist.append(self.text_bottom)

    def keys_to_check(self, key_list: list):
        if CST.pressed("SPACE", key_list):
            self.quit_loop(CST.SCENES.GAME_LEVEL)
  




def main_game():
    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_menu = GameMenu(WIN)
    game_level = GameLevel(WIN)
    game_losing_screen = GameLosingScreen(WIN)

    scenelist = [
        game_menu,
        game_level,
        game_losing_screen,
    ]

    next_scene = 0

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = scenelist[next_scene].run()




if __name__ == "__main__":
    main_game()
    