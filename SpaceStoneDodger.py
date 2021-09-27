# pylint: disable=no-member
# This is my first game



import pygame
import ssd_constants as CST
import ssd_scene_gamemenu as SceneMenu
import ssd_scene_gametutorial as SceneTutorial
import ssd_scene_gamelevel as SceneLevel
import ssd_scene_gamelosingscreen as SceneLose




pygame.init()




def main_game():
    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_menu = SceneMenu.GameMenu(WIN)
    game_tutorial = SceneTutorial.GameTutorial(WIN)
    game_level = SceneLevel.GameLevel(WIN)
    game_losing_screen = SceneLose.GameLosingScreen(WIN)

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
    