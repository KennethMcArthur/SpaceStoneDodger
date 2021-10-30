# pylint: disable=no-member

# SpaceStoneDodger: Game Losing Screen Scene


import pygame
import ssd_constants as CST
import ssd_player as plr
import ssd_asteroid as ast
import ssd_starfield as stf
import ssd_background as bg
import ssd_powerup as pwr
import ssd_text_classes as txt
import ssd_scene_master_class as Scn



class GameLosingScreen(Scn.Scene):
    def scene_related_init(self):
        SIZE_TEXT_BIG = 48
        SIZE_TEXT_SMALL = 18
        TITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT // 2)
        BOTTOM_ROW = CST.SCREEN_HEIGHT - SIZE_TEXT_SMALL

        self.level_background = bg.Background()
        self.text_title = txt.AnimatedTypedText(CST.get_text("LOSE001"), SIZE_TEXT_BIG, (50, CST.SCREEN_HEIGHT // 3), 20)
        self.goto_menu_label = txt.StaticText("[M] " + CST.get_text("LOSE002"), SIZE_TEXT_SMALL, (0, BOTTOM_ROW), CST.TXT.LEFT)
        self.goto_play_label = txt.StaticText("[P] " + CST.get_text("LOSE003"), SIZE_TEXT_SMALL, (CST.SCREEN_WIDTH, BOTTOM_ROW), CST.TXT.RIGHT)
        
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.text_title)
        self.updatelist.append(self.goto_menu_label)
        self.updatelist.append(self.goto_play_label)


    def event_checking(self, this_event: pygame.event) -> None:
        super().event_checking(this_event) # handles quit event
        if this_event.type == pygame.KEYDOWN:
            if this_event.key == pygame.K_m:
                self.quit_loop(CST.SCENES.GAME_MENU)
            if this_event.key == pygame.K_p:
                self.quit_loop(CST.SCENES.GAME_LEVEL)
        

    def load_and_start_music(self):
        # Music stuff
        CST.Jukebox.playsong(CST.MUSIC_LOSINGSCREEN)


    def text_to_update(self):
        self.text_title.set_text(CST.get_text("LOSE001"))
        self.goto_menu_label.set_text("[M] " + CST.get_text("LOSE002"))
        self.goto_play_label.set_text("[P] " + CST.get_text("LOSE003"))



# TESTING
def main_game():
    pygame.init()

    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_lose = GameLosingScreen(WIN)
    next_scene = 0

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = game_lose.run()
        print("Next scene: ", next_scene)



if __name__ == "__main__":
    main_game()