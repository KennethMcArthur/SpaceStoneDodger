# pylint: disable=no-member
# This is my first game


import sys
sys.path.append("src")

import pygame
from src import ssd_constants as CST
from src import ssd_scene_gamemenu as SceneMenu
from src import ssd_scene_gametutorial as SceneTutorial
from src import ssd_scene_gamelevel as SceneLevel
from src import ssd_scene_gamelosingscreen as SceneLose
from src import ssd_scene_gameoptions as SceneOptions
from src import ssd_scene_gamecredits as SceneCredits



pygame.init()



def main_game():
    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_menu = SceneMenu.GameMenu(WIN)
    game_tutorial = SceneTutorial.GameTutorial(WIN)
    game_level = SceneLevel.GameLevel(WIN)
    game_losing_screen = SceneLose.GameLosingScreen(WIN)
    game_options = SceneOptions.GameOptions(WIN)
    game_credits = SceneCredits.GameCredits(WIN)

    scenelist = [
        game_menu,
        game_tutorial,
        game_level,
        game_losing_screen,
        game_options,
        game_credits
    ]

    next_scene = CST.SCENES.GAME_MENU

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = scenelist[next_scene].run()



if __name__ == "__main__":
    main_game()
    