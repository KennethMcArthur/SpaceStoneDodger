# pylint: disable=no-member

# SpaceStoneDodger: Game Menu Class


import pygame
import ssd_constants as CST
import ssd_player as plr
import ssd_asteroid as ast
import ssd_starfield as stf
import ssd_background as bg
import ssd_powerup as pwr
import ssd_text_classes as txt
import ssd_scene_master_class as Scn



class GameMenu(Scn.Scene):
    def scene_related_init(self):
        SIZE_TEXT_BIG = 48
        SIZE_TEXT_MEDIUM = 24
        SIZE_TEXT_TINY = 14
        TITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.2)
        SUBTITLE_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT * 0.2 + 48)
        BOTTOM_TEXT_COORDS_LEFT = (0, CST.SCREEN_HEIGHT - SIZE_TEXT_MEDIUM)
        BOTTOM_TEXT_COORDS_RIGHT = (CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT - SIZE_TEXT_MEDIUM)
        OPTION_COORDS = (CST.SCREEN_WIDTH // 2, CST.SCREEN_HEIGHT - SIZE_TEXT_TINY)

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(15)
        self.player = plr.Player_pawn(CST.SCREEN_WIDTH // 2 - 16, CST.SCREEN_HEIGHT // 2 - 16)
        self.text_title = txt.StaticText("Space Stone Dodger", SIZE_TEXT_BIG, TITLE_COORDS, CST.TXT.CENTER)
        self.text_subtitle = txt.StaticText(CST.get_text("MENU001"), SIZE_TEXT_TINY, SUBTITLE_COORDS, CST.TXT.CENTER)
        self.text_goto_play = txt.StaticText("[P] " + CST.get_text("MENU002"), SIZE_TEXT_MEDIUM, BOTTOM_TEXT_COORDS_LEFT, CST.TXT.LEFT)
        self.text_goto_tutorial = txt.StaticText("[T] " + CST.get_text("MENU003"), SIZE_TEXT_MEDIUM, BOTTOM_TEXT_COORDS_RIGHT, CST.TXT.RIGHT)
        self.text_goto_options = txt.StaticText("[O] " + CST.get_text("MENU004"), SIZE_TEXT_TINY, OPTION_COORDS, CST.TXT.CENTER)
        
        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.player)
        self.updatelist.append(self.text_title)
        self.updatelist.append(self.text_subtitle)
        self.updatelist.append(self.text_goto_play)
        self.updatelist.append(self.text_goto_tutorial)
        self.updatelist.append(self.text_goto_options)


    def keys_to_check(self, key_list: list):
        self.player.handle_movement(key_list)
        

    def event_checking(self, this_event: pygame.event) -> None:
        super().event_checking(this_event) # handles quit event
        if this_event.type == pygame.KEYDOWN:
            if this_event.key == pygame.K_o:
                self.quit_loop(CST.SCENES.GAME_OPTIONS)
            if this_event.key == pygame.K_p:
                self.quit_loop(CST.SCENES.GAME_LEVEL)
            if this_event.key == pygame.K_t:
                self.quit_loop(CST.SCENES.GAME_TUTORIAL)
            if this_event.key == pygame.K_c:
                self.quit_loop(CST.SCENES.GAME_CREDITS)


    def load_and_start_music(self):
        # Music stuff
        CST.Jukebox.playsong(CST.MUSIC_MENU)


    def text_to_update(self):
        self.text_subtitle.set_text(CST.get_text("MENU001"))
        self.text_goto_play.set_text("[P] " + CST.get_text("MENU002"))
        self.text_goto_tutorial.set_text("[T] " + CST.get_text("MENU003"))
        self.text_goto_options.set_text("[O] " + CST.get_text("MENU004"))


# TESTING
def main_game():
    pygame.init()

    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_menu = GameMenu(WIN)
    next_scene = 0

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = game_menu.run()
        print("Next scene: ", next_scene)



if __name__ == "__main__":
    main_game()
    