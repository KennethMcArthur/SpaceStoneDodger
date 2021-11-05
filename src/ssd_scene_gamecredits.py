# pylint: disable=no-member

# SpaceStoneDodger: Game Credit Class


import pygame
import ssd_constants as CST
import ssd_starfield as stf
import ssd_background as bg
import ssd_text_classes as txt
import ssd_scene_master_class as Scn



class CreditsMovingText(txt.StaticText):
    """ New type of static text that moves. Yeah, it's silly. """

    default_text_speed = 1
    boosted_text_speed = 5
    is_boosted = False


    def game_tick_update(self, window: pygame.Surface):
        super().game_tick_update(window)
        # Moving text up, ready for the next frame
        self.pos_y -= CreditsMovingText.get_current_speed()
        self.place_me()


    def is_offscreen_top(self) -> bool:
        """ Returns if the text is outside the top boundary of the screen """
        return self.pos_y < (0 - self.titlerect.height)


    @classmethod
    def get_current_speed(cls) -> int:
        """ Returns the current speed (boosted or not) """
        # if is_boosted is False, boosted_text_speed will be multiplied by zero
        return max(cls.default_text_speed, cls.boosted_text_speed * cls.is_boosted)


    @classmethod
    def set_speeds(cls, new_def_speed: int, new_boosted_speed: int) -> None:
        """ Allows setting a new base speed for text """
        cls.default_text_speed = new_def_speed
        cls.boosted_text_speed = new_boosted_speed


    @classmethod
    def boost(cls, state: bool) -> None:
        """ Allows to set the value of is_boosted variable """
        cls.is_boosted = state





class GameCredits(Scn.Scene):
    def scene_related_init(self):
        SIZE_TEXT_BIGTITLE = 48
        SIZE_TEXT_CATEGORIES = 24
        SIZE_TEXT_REGULAR = 18
        CENTER_X = CST.SCREEN_WIDTH // 2

        self.CREDIT_SPEED = 1 # text speed in pixels
        self.CREDIT_BOOSTED_SPEED = self.CREDIT_SPEED * 5

        FIRST_POS = CST.SCREEN_HEIGHT + SIZE_TEXT_BIGTITLE
        BLANK_ROW = 50
        self.pos_y_list = [ # This list contains the y distance of a text from the previous one
            FIRST_POS, #(0) Space Stone Dodger
            BLANK_ROW * 3, #(1) - CODING -
            SIZE_TEXT_REGULAR * 2, #(2) Simone Kenneth Canova
            BLANK_ROW * 3, #(3) - GRAPHICS -
            BLANK_ROW * 2, #(4) Font by
            SIZE_TEXT_REGULAR * 2, #(5) codeman38
            SIZE_TEXT_REGULAR * 2, #(6) (http://www.zone38.net)
            BLANK_ROW * 2, #(7) Background
            SIZE_TEXT_REGULAR * 2, #(8) Digital Moons
            SIZE_TEXT_REGULAR * 2, #(9) (https://digitalmoons.itch.io)
            BLANK_ROW * 2, #(10) All other graphics:
            SIZE_TEXT_REGULAR * 2, #(11) Simone "Kenneth" Canova
            BLANK_ROW * 3, #(12) - SOUNDS -
            BLANK_ROW * 2, #(13) Sounds for impact and death:
            SIZE_TEXT_REGULAR * 2, #(14) Kenney
            SIZE_TEXT_REGULAR * 2, #(15) (https://kenney.nl)
            BLANK_ROW * 2, #(16) Sound for text tick:
            SIZE_TEXT_REGULAR * 2, #(17) qubodup
            SIZE_TEXT_REGULAR * 2, #(18) (https://opengameart.org/users/qubodup)
            BLANK_ROW * 2, #(19) Sound for scrap metals:
            SIZE_TEXT_REGULAR * 2, #(20) Mixkit.co
            SIZE_TEXT_REGULAR * 2, #(21) (https://mixkit.co)
            BLANK_ROW * 3, #(22) - MUSICS -
            BLANK_ROW * 2, #(23) Neon Lights
            SIZE_TEXT_REGULAR * 2, #(24) (https://www.joystock.org)
            BLANK_ROW * 2, #(25) Power Bots
            SIZE_TEXT_REGULAR * 2, #(26) (https://www.dl-sounds.com/royalty-free/power-bots-loop)
            BLANK_ROW * 2, #(27) Background Loop Melodic Techno #04 by Zen Man
            SIZE_TEXT_REGULAR * 2, #(28) (https://pixabay.com/users/zen_man-4257870)
            BLANK_ROW * 2, #(29) Bensound Sci-Fi
            SIZE_TEXT_REGULAR * 2, #(30) (https://www.bensound.com)
            BLANK_ROW * 6, #(31) Thank you for playing!
        ]

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(15)

        self.text_bigtitle = CreditsMovingText("", SIZE_TEXT_BIGTITLE, (CENTER_X, self.get_row(0)), CST.TXT.CENTER)
        self.text_coding_title = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(1)), CST.TXT.CENTER)
        self.text_coding_content = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(2)), CST.TXT.CENTER)
        self.text_graphics_title = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(3)), CST.TXT.CENTER)
        self.text_font_title = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(4)), CST.TXT.CENTER)
        self.text_font_creator = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(5)), CST.TXT.CENTER)
        self.text_font_link = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(6)), CST.TXT.CENTER)
        self.text_background_title = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(7)), CST.TXT.CENTER)
        self.text_background_creator = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(8)), CST.TXT.CENTER)
        self.text_background_link = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(9)), CST.TXT.CENTER)
        self.text_other_graphics_title = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(10)), CST.TXT.CENTER)
        self.text_other_graphics_author = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(11)), CST.TXT.CENTER)
        self.text_sounds_title = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(12)), CST.TXT.CENTER)
        self.text_sounds_impactdeath = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(13)), CST.TXT.CENTER)
        self.text_sounds_impactdeath_creator = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(14)), CST.TXT.CENTER)
        self.text_sounds_impactdeath_link = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(15)), CST.TXT.CENTER)
        self.text_sounds_texttick = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(16)), CST.TXT.CENTER)
        self.text_sounds_texttick_creator = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(17)), CST.TXT.CENTER)
        self.text_sounds_texttick_link = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(18)), CST.TXT.CENTER)
        self.text_sounds_powerup = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(19)), CST.TXT.CENTER)
        self.text_sounds_powerup_creator = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(20)), CST.TXT.CENTER)
        self.text_sounds_powerup_link = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(21)), CST.TXT.CENTER)
        self.text_music_title = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(22)), CST.TXT.CENTER)
        self.text_music_songname1 = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(23)), CST.TXT.CENTER)
        self.text_music_songauthor1 = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(24)), CST.TXT.CENTER)
        self.text_music_songname2 = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(25)), CST.TXT.CENTER)
        self.text_music_songauthor2 = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(26)), CST.TXT.CENTER)
        self.text_music_songname3 = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(27)), CST.TXT.CENTER)
        self.text_music_songauthor3 = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(28)), CST.TXT.CENTER)
        self.text_music_songname4 = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(29)), CST.TXT.CENTER)
        self.text_music_songauthor4 = CreditsMovingText("", SIZE_TEXT_REGULAR, (CENTER_X, self.get_row(30)), CST.TXT.CENTER)
        self.text_final_thanks = CreditsMovingText("", SIZE_TEXT_CATEGORIES, (CENTER_X, self.get_row(31)), CST.TXT.CENTER)

        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.text_bigtitle)
        self.updatelist.append(self.text_coding_title)
        self.updatelist.append(self.text_coding_content)
        self.updatelist.append(self.text_graphics_title)
        self.updatelist.append(self.text_font_title)
        self.updatelist.append(self.text_font_creator)
        self.updatelist.append(self.text_font_link)
        self.updatelist.append(self.text_background_title)
        self.updatelist.append(self.text_background_creator)
        self.updatelist.append(self.text_background_link)
        self.updatelist.append(self.text_other_graphics_title)
        self.updatelist.append(self.text_other_graphics_author)
        self.updatelist.append(self.text_sounds_title)
        self.updatelist.append(self.text_sounds_impactdeath)
        self.updatelist.append(self.text_sounds_impactdeath_creator)
        self.updatelist.append(self.text_sounds_impactdeath_link)
        self.updatelist.append(self.text_sounds_texttick)
        self.updatelist.append(self.text_sounds_texttick_creator)
        self.updatelist.append(self.text_sounds_texttick_link)
        self.updatelist.append(self.text_sounds_powerup)
        self.updatelist.append(self.text_sounds_powerup_creator)
        self.updatelist.append(self.text_sounds_powerup_link)
        self.updatelist.append(self.text_music_title)
        self.updatelist.append(self.text_music_songname1)
        self.updatelist.append(self.text_music_songauthor1)
        self.updatelist.append(self.text_music_songname2)
        self.updatelist.append(self.text_music_songauthor2)
        self.updatelist.append(self.text_music_songname3)
        self.updatelist.append(self.text_music_songauthor3)
        self.updatelist.append(self.text_music_songname4)
        self.updatelist.append(self.text_music_songauthor4)
        self.updatelist.append(self.text_final_thanks)

        self.text_to_update()
        CreditsMovingText.set_speeds(self.CREDIT_SPEED, self.CREDIT_BOOSTED_SPEED)


    def load_and_start_music(self):
        # Music stuff
        CST.Jukebox.playsong(CST.MUSIC_MENU)


    def keys_to_check(self, key_list):
        # Speed up if SPACE is pressed
        CreditsMovingText.boost(False)
        if CST.pressed("SPACE", key_list):
            CreditsMovingText.boost(True)

        # I'm secretly overriding this method to do stuff each frame
        # Quit after the last text
        if self.text_final_thanks.is_offscreen_top():
            CST.Jukebox.stopmusic()
            counter = 0
            for element in self.updatelist: # Resetting text positions
                if isinstance(element, CreditsMovingText):
                    element.pos_y = self.get_row(counter)
                    counter += 1
            self.quit_loop(CST.SCENES.GAME_MENU)
        

    def get_row(self, row: int) -> int:
        """ Returns the additive y position from a list """
        return sum(self.pos_y_list[:row+1])


    def text_to_update(self):
        self.text_bigtitle.set_text("Space Stone Dodger")
        self.text_coding_title.set_text(f"- {CST.get_text('CREDITS001').upper()} -")
        self.text_coding_content.set_text("Simone 'Kenneth' Canova")
        self.text_graphics_title.set_text(f"- {CST.get_text('CREDITS002').upper()} -")
        self.text_font_title.set_text(f"{CST.get_text('CREDITS003').capitalize()}:")
        self.text_font_creator.set_text("codeman38")
        self.text_font_link.set_text("http://www.zone38.net")
        self.text_background_title.set_text(f"{CST.get_text('CREDITS004').capitalize()}:")
        self.text_background_creator.set_text("Digital Moons")
        self.text_background_link.set_text("https://digitalmoons.itch.io")
        self.text_other_graphics_title.set_text(f"{CST.get_text('CREDITS005').capitalize()}:")
        self.text_other_graphics_author.set_text("Simone 'Kenneth' Canova")
        self.text_sounds_title.set_text(f"- {CST.get_text('CREDITS006').upper()} -")
        self.text_sounds_impactdeath.set_text(f"{CST.get_text('CREDITS007').capitalize()}:")
        self.text_sounds_impactdeath_creator.set_text("Kenney.nl")
        self.text_sounds_impactdeath_link.set_text("https://kenney.nl")
        self.text_sounds_texttick.set_text(f"{CST.get_text('CREDITS008').capitalize()}:")
        self.text_sounds_texttick_creator.set_text("qubodup")
        self.text_sounds_texttick_link.set_text("https://opengameart.org/users/qubodup")
        self.text_sounds_powerup.set_text(f"{CST.get_text('CREDITS009').capitalize()}:")
        self.text_sounds_powerup_creator.set_text("Mixkit.co")
        self.text_sounds_powerup_link.set_text("https://mixkit.co")
        self.text_music_title.set_text(f"- {CST.get_text('CREDITS010').upper()} -")
        self.text_music_songname1.set_text("Neon Lights")
        self.text_music_songauthor1.set_text("https://www.joystock.org")
        self.text_music_songname2.set_text("Power Bots")
        self.text_music_songauthor2.set_text("https://www.dl-sounds.com")
        self.text_music_songname3.set_text("Techno #04 by Zen Man")
        self.text_music_songauthor3.set_text("https://pixabay.com/users/zen_man-4257870")
        self.text_music_songname4.set_text("Bensound Sci-Fi")
        self.text_music_songauthor4.set_text("https://www.bensound.com")
        self.text_final_thanks.set_text(f"{CST.get_text('CREDITS011')}")


# TESTING
def main_game():
    pygame.init()

    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_credits = GameCredits(WIN)
    next_scene = 0

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = game_credits.run()
        print("Next scene: ", next_scene)



if __name__ == "__main__":
    main_game()
    