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
        SIZE_TEXT_BIG = 48
        SIZE_TEXT_MEDIUM = 24
        SIZE_TEXT_TINY = 14
        TITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.2)
        SUBTITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.2 + 48)
        BOTTOM_TEXT_COORDS_LEFT = (0, CST.SCREEN_HEIGHT - SIZE_TEXT_MEDIUM)
        BOTTOM_TEXT_COORDS_RIGHT = (CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT - SIZE_TEXT_MEDIUM)

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(15)
        self.player = plr.Player_pawn(CST.SCREEN_WIDTH // 2 - 16, CST.SCREEN_HEIGHT // 2 - 16)
        self.text_title = txt.StaticText("Space Stone Dodger", SIZE_TEXT_BIG, TITLE_COORDS, CST.TXT.CENTER)
        self.text_subtitle = txt.StaticText("a simple game where you, well, dodge stones", SIZE_TEXT_TINY, SUBTITLE_COORDS, CST.TXT.CENTER)
        self.text_goto_play = txt.StaticText("[P] Play", SIZE_TEXT_MEDIUM, BOTTOM_TEXT_COORDS_LEFT, CST.TXT.LEFT)
        self.text_goto_tutorial = txt.StaticText("[T] Tutorial", SIZE_TEXT_MEDIUM, BOTTOM_TEXT_COORDS_RIGHT, CST.TXT.RIGHT)
        
        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.player)
        self.updatelist.append(self.text_title)
        self.updatelist.append(self.text_subtitle)
        self.updatelist.append(self.text_goto_play)
        self.updatelist.append(self.text_goto_tutorial)


    def keys_to_check(self, key_list: list):
        self.player.handle_movement(key_list)
        if CST.pressed("P", key_list):
            self.quit_loop(CST.SCENES.GAME_LEVEL)
        if CST.pressed("T", key_list):
            self.quit_loop(CST.SCENES.GAME_TUTORIAL)



class GameTutorial(Scn.Scene):
    def scene_related_init(self):
        SIZE_TEXT_MEDIUM = 28
        SIZE_TEXT_SMALL = 18
        SIZE_TEXT_TINY = 14
        FIRST_COL = 50
        SECOND_COL = 150
        FIRST_ROW = CST.SCREEN_HEIGHT // 4 * 1
        SECOND_ROW = CST.SCREEN_HEIGHT // 4 * 2
        THIRD_ROW = CST.SCREEN_HEIGHT // 4 * 3
        BOTTOM_ROW = CST.SCREEN_HEIGHT - SIZE_TEXT_SMALL

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(15)
        self.player = plr.Player_pawn(FIRST_COL, FIRST_ROW)
        self.player_life_bar = plr.Lifebar(self.player)
        self.asteroid = ast.Asteroid(FIRST_COL, SECOND_ROW, 0)
        self.powerup = pwr.PowerUp(FIRST_COL, THIRD_ROW, 0)
        self.player_label = txt.StaticText("Move with W,A,S,D", SIZE_TEXT_MEDIUM, (SECOND_COL, FIRST_ROW))
        self.asteroid_label = txt.StaticText("Avoid asteroids", SIZE_TEXT_MEDIUM, (SECOND_COL, SECOND_ROW))
        self.powerup_label = txt.StaticText("Collect valuable scraps", SIZE_TEXT_MEDIUM, (SECOND_COL, THIRD_ROW))
        self.player_life_bar_label = txt.StaticText("Your life", SIZE_TEXT_TINY, (CST.SCREEN_WIDTH, 50), CST.TXT.RIGHT)
        self.goto_menu_label = txt.StaticText("[M] back to Menu", SIZE_TEXT_SMALL, (0, BOTTOM_ROW), CST.TXT.LEFT)
        self.goto_play_label = txt.StaticText("[P] Play the game", SIZE_TEXT_SMALL, (CST.SCREEN_WIDTH, BOTTOM_ROW), CST.TXT.RIGHT)

        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.player)
        self.updatelist.append(self.player_life_bar)
        self.updatelist.append(self.asteroid)
        self.updatelist.append(self.powerup)
        self.updatelist.append(self.player_label)
        self.updatelist.append(self.asteroid_label)
        self.updatelist.append(self.powerup_label)
        self.updatelist.append(self.player_life_bar_label)
        self.updatelist.append(self.goto_menu_label)
        self.updatelist.append(self.goto_play_label)


    def keys_to_check(self, key_list: list) -> None:
        self.player.handle_movement(key_list)
        if CST.pressed("M", key_list):
            self.quit_loop(CST.SCENES.GAME_MENU)
        if CST.pressed("P", key_list):
            self.quit_loop(CST.SCENES.GAME_LEVEL)



class GameLevel(Scn.Scene):
    def scene_related_init(self):
        self.num_power_ups = 1
        self.num_asteroids = 2
        self.num_stars = 15
        self.score = 0
        self.asteroid_needed_to_next = 4
        self.asteroid_passed_target_number = 5

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(self.num_stars)
        self.player = plr.Player_pawn(50, CST.SCREEN_HEIGHT // 2)
        self.ui_lifebar = plr.Lifebar(self.player)
        self.asteroid_field = ast.AsteroidField(self.num_asteroids, self.player)
        self.powerup_field = pwr.PowerUpField(self.num_power_ups, self.player)
        self.score_label = txt.StaticText("Score:", 14, (0,0), CST.TXT.LEFT)

        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.powerup_field)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.player)
        self.updatelist.append(self.asteroid_field)
        self.updatelist.append(self.ui_lifebar)
        self.updatelist.append(self.score_label)

        self.set_timer_step(1) # Setting the internal timer

    def timer_duty(self) -> None:
        # What happens when the timer goes off
        """
        TODO: PowerUp spawning rework
        """
        passed = self.asteroid_field.get_how_many_passed()
        if passed >= self.asteroid_passed_target_number:
            self.asteroid_needed_to_next += 1
            self.asteroid_passed_target_number += self.asteroid_needed_to_next
            self.num_asteroids = 2 + self.score // 3
            self.num_power_ups = 1 + self.num_asteroids // 3
            self.asteroid_field.resize(self.num_asteroids)
            self.powerup_field.resize(self.num_power_ups)
            print("Target number is now", self.asteroid_passed_target_number)
            
        print("Asteroids passed: ", passed)
        print("Total asteroids:", len(self.asteroid_field.elements))
        

    def event_checking(self, this_event: pygame.event) -> None:
        super().event_checking(this_event) # for quitting handling
        if this_event.type == CST.PLAYER_HIT:
            self.player.got_hit(CST.PLAYER_DEAD)
        if this_event.type == CST.PLAYER_DEAD:
            self.quit_loop(CST.SCENES.GAME_LOSING_SCREEN)
        if this_event.type == CST.POWER_UP_COLLECTED:
            self.score += 1
            self.score_label.set_text("Score: " + str(self.score))


    def keys_to_check(self, key_list: list) -> None:
        self.player.handle_movement(key_list)
        self.asteroid_field.handle_movement(key_list)
        self.powerup_field.handle_movement(key_list)
        self.starfield.handle_movement(key_list)


    def reset_state(self):
        self.__init__(self.GAME_WINDOW) # Forcing the level to initial state




class GameLosingScreen(Scn.Scene):
    def scene_related_init(self):
        SIZE_TEXT_BIG = 48
        SIZE_TEXT_SMALL = 18
        TITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT // 2)
        BOTTOM_ROW = CST.SCREEN_HEIGHT - SIZE_TEXT_SMALL

        self.level_background = bg.Background()
        self.text_title = txt.StaticText("Sadly, stones Won", SIZE_TEXT_BIG, TITLE_COORDS, CST.TXT.CENTER)
        self.goto_menu_label = txt.StaticText("[M] back to Menu", SIZE_TEXT_SMALL, (0, BOTTOM_ROW), CST.TXT.LEFT)
        self.goto_play_label = txt.StaticText("[P] Play again", SIZE_TEXT_SMALL, (CST.SCREEN_WIDTH, BOTTOM_ROW), CST.TXT.RIGHT)
        
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.text_title)
        self.updatelist.append(self.goto_menu_label)
        self.updatelist.append(self.goto_play_label)

    def keys_to_check(self, key_list: list):
        if CST.pressed("M", key_list):
            self.quit_loop(CST.SCENES.GAME_MENU)
        if CST.pressed("P", key_list):
            self.quit_loop(CST.SCENES.GAME_LEVEL)
  




def main_game():
    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_menu = GameMenu(WIN)
    game_tutorial = GameTutorial(WIN)
    game_level = GameLevel(WIN)
    game_losing_screen = GameLosingScreen(WIN)

    scenelist = [
        game_menu,
        game_tutorial,
        game_level,
        game_losing_screen,
    ]

    next_scene = CST.SCENES.GAME_MENU

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = scenelist[next_scene].run()




if __name__ == "__main__":
    main_game()
    