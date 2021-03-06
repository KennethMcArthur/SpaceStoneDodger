# pylint: disable=no-member

# SpaceStoneDodger: Game Tutorial Class


import pygame
import ssd_constants as CST
import ssd_player as plr
import ssd_asteroid as ast
import ssd_starfield as stf
import ssd_background as bg
import ssd_powerup as pwr
import ssd_text_classes as txt
import ssd_scene_master_class as Scn



class GameTutorial(Scn.Scene):
    def scene_related_init(self):
        SIZE_TEXT_MEDIUM = 24
        SIZE_TEXT_SMALL = 18
        SIZE_TEXT_TINY = 12
        FIRST_COL = 50
        SECOND_COL = 120
        FIRST_ROW = CST.SCREEN_HEIGHT // 4 * 1
        SECOND_ROW = CST.SCREEN_HEIGHT // 4 * 2
        THIRD_ROW = CST.SCREEN_HEIGHT // 4 * 3
        BOTTOM_ROW = CST.SCREEN_HEIGHT - SIZE_TEXT_SMALL

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(15)
        self.player = plr.Player_pawn(FIRST_COL, FIRST_ROW)
        self.player_life_bar = plr.Lifebar(self.player)
        self.asteroid = ast.Asteroid(FIRST_COL, SECOND_ROW, 0)
        self.asteroid.set_scale(48)
        self.powerup = pwr.PowerUp(FIRST_COL, THIRD_ROW, 0)
        self.player_label = txt.AnimatedTypedText(CST.get_text("TUTORIAL001"), SIZE_TEXT_MEDIUM, (SECOND_COL, FIRST_ROW), 1)
        self.asteroid_label = txt.AnimatedTypedText(CST.get_text("TUTORIAL002"), SIZE_TEXT_MEDIUM, (SECOND_COL, SECOND_ROW), 1)
        self.powerup_label = txt.AnimatedTypedText(CST.get_text("TUTORIAL003"), SIZE_TEXT_MEDIUM, (SECOND_COL, THIRD_ROW), 1)
        self.player_life_bar_label = txt.StaticText(CST.get_text("TUTORIAL004"), SIZE_TEXT_TINY, (CST.SCREEN_WIDTH, 50), CST.TXT.RIGHT)
        self.goto_menu_label = txt.StaticText("[M] " + CST.get_text("TUTORIAL005"), SIZE_TEXT_SMALL, (0, BOTTOM_ROW), CST.TXT.LEFT)
        self.goto_play_label = txt.StaticText("[P] " + CST.get_text("TUTORIAL006"), SIZE_TEXT_SMALL, (CST.SCREEN_WIDTH, BOTTOM_ROW), CST.TXT.RIGHT)

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


    def event_checking(self, this_event: pygame.event) -> None:
        super().event_checking(this_event) # handles quit event
        if this_event.type == pygame.KEYDOWN:
            if this_event.key == pygame.K_m:
                self.quit_loop(CST.SCENES.GAME_MENU)
            if this_event.key == pygame.K_p:
                self.quit_loop(CST.SCENES.GAME_LEVEL)


    def text_to_update(self):
        self.player_label.set_text(CST.get_text("TUTORIAL001"))
        self.asteroid_label.set_text(CST.get_text("TUTORIAL002"))
        self.powerup_label.set_text(CST.get_text("TUTORIAL003"))
        self.player_life_bar_label.set_text(CST.get_text("TUTORIAL004"))
        self.goto_menu_label.set_text("[M] " + CST.get_text("TUTORIAL005"))
        self.goto_play_label.set_text("[P] " + CST.get_text("TUTORIAL006"))
        self.player_label.skip_animation()
        self.asteroid_label.skip_animation()
        self.powerup_label.skip_animation()




# TESTING
def main_game():
    pygame.init()

    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_tutorial = GameTutorial(WIN)
    next_scene = 0

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = game_tutorial.run()
        print("Next scene: ", next_scene)



if __name__ == "__main__":
    main_game()
    