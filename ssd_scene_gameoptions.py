# pylint: disable=no-member

# SpaceStoneDodger: Game Option Class


import pygame
import ssd_constants as CST
import ssd_background as bg
import ssd_text_classes as txt
import ssd_scene_master_class as Scn



class GameOptions(Scn.Scene):
    def scene_related_init(self):
        SIZE_TEXT_BIG = 34
        SIZE_TEXT_MEDIUM = 24
        SIZE_TEXT_SMALL = 18
        SIZE_TEXT_TINY = 12
        CENTERSCREEN = CST.SCREEN_WIDTH // 2
        FIRST_ROW = CST.SCREEN_HEIGHT // 4 * 1
        SECOND_ROW = FIRST_ROW + 50
        THIRD_ROW = CST.SCREEN_HEIGHT // 4 * 3
        BOTTOM_ROW = CST.SCREEN_HEIGHT - SIZE_TEXT_SMALL

        self.dummy_sound = CST.SFX_POWERUP_COLLECTED

        self.level_background = bg.Background()
        self.volumes_title = txt.StaticText(CST.get_text("OPTIONS003"), SIZE_TEXT_BIG, (CENTERSCREEN, FIRST_ROW - SIZE_TEXT_BIG *1.5), CST.TXT.CENTER)
        self.sounds_label = txt.StaticText(self.get_sound_string(), SIZE_TEXT_MEDIUM, (CENTERSCREEN, FIRST_ROW), CST.TXT.CENTER)
        self.music_label = txt.StaticText(self.get_music_string(), SIZE_TEXT_MEDIUM, (CENTERSCREEN, SECOND_ROW), CST.TXT.CENTER)
        self.language_title = txt.StaticText(CST.get_text("OPTIONS004"), SIZE_TEXT_BIG, (CENTERSCREEN, THIRD_ROW - SIZE_TEXT_BIG *1.5), CST.TXT.CENTER)
        self.language_label = txt.StaticText(self.get_language_string(), SIZE_TEXT_MEDIUM, (CENTERSCREEN, THIRD_ROW), CST.TXT.CENTER)    
        self.goto_menu_label = txt.StaticText("[M] " + CST.get_text("TUTORIAL005"), SIZE_TEXT_SMALL, (0, BOTTOM_ROW), CST.TXT.LEFT)

        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.volumes_title)
        self.updatelist.append(self.sounds_label)
        self.updatelist.append(self.music_label)
        self.updatelist.append(self.language_title)
        self.updatelist.append(self.language_label)
        self.updatelist.append(self.goto_menu_label)



    def event_checking(self, this_event: pygame.event) -> None:
        super().event_checking(this_event) # handles quit event
        if this_event.type == pygame.KEYDOWN:
            if this_event.key == pygame.K_q:
                CST.set_sfx_volume(CST.get_sfx_volume() - 0.1)
                self.play_dummy_sound()
            if this_event.key == pygame.K_e:
                CST.set_sfx_volume(CST.get_sfx_volume() + 0.1)
                self.play_dummy_sound()
            if this_event.key == pygame.K_a:
                CST.set_music_volume(CST.get_music_volume() - 0.1)
            if this_event.key == pygame.K_d:
                CST.set_music_volume(CST.get_music_volume() + 0.1)
            if this_event.key == pygame.K_l:
                self.cycle_language()
            if this_event.key == pygame.K_m:
                self.quit_loop(CST.SCENES.GAME_MENU)
        self.update_all_text()


    def get_sound_string(self) -> str:
        """ Builds the string for sound option """
        return f"[Q] <- {CST.get_text('OPTIONS001')}: {int(round(CST.get_sfx_volume(), 1) * 10)} -> [E]"

    def get_music_string(self) -> str:
        """ Builds the string for music option """
        return f"[A] <- {CST.get_text('OPTIONS002')}: {int(round(CST.get_music_volume(), 1) * 10)} -> [D]"

    def get_language_string(self) -> str:
        """ The current language string """
        return f"[L] {CST.get_text('LANGUAGE')}"

    def cycle_language(self) -> None:
        """ Sets the next language in list as current """
        languagelist = CST.get_every_languages()
        # Finding this language index
        this_lang_index = 0
        for language in languagelist:
            if language["LANGUAGE"] == CST.get_text("LANGUAGE"):
                this_lang_index = languagelist.index(language)
                print("Index found:", this_lang_index)
                break

        this_lang_index = (this_lang_index + 1) % len(languagelist)
        print("New Index:", this_lang_index)
        CST.set_text_db(languagelist[this_lang_index])

    def play_dummy_sound(self) -> None:
        """ Updates the sfx volume and plays the dummy sound """
        self.dummy_sound.set_volume(CST.get_sfx_volume())
        self.dummy_sound.play()

    def update_all_text(self) -> None:
        """ Forces all text to update """
        self.sounds_label.set_text(self.get_sound_string())
        self.music_label.set_text(self.get_music_string())
        self.language_label.set_text(self.get_language_string())
        self.goto_menu_label.set_text("[M] " + CST.get_text("TUTORIAL005"))
        self.volumes_title.set_text(CST.get_text("OPTIONS003"))
        self.language_title.set_text(CST.get_text("OPTIONS004"))
        


# TESTING
def main_game():
    pygame.init()

    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_tutorial = GameOptions(WIN)
    next_scene = 0

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = game_tutorial.run()
        print("Next scene: ", next_scene)



if __name__ == "__main__":
    main_game()
    