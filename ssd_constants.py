# pylint: disable=no-member

# SpaceStoneDodger: Constants database
import pygame, os, json
from collections import defaultdict

pygame.mixer.init()


# HELPER FUNCTIONS
# ----------------

def load_image(asset_folder: str, filename: str) -> pygame.Surface:
    """ Error handling image loading function """
    fullname = os.path.join(asset_folder, filename)
    try:
        return pygame.image.load(fullname)
    except Exception as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)


def load_audio(audio_asset_folder: str, filename: str) -> pygame.mixer.Sound:
    """ Error handling audio loading function """
    fullname = os.path.join(audio_asset_folder, filename)
    try:
        return pygame.mixer.Sound(fullname)
    except Exception as message:
        print("Cannot load audio:", filename)
        raise SystemExit(message)


def pressed(direction: str, pressed_key: list) -> bool:
    """ Returns if one of the corresponding key of a direction is been pressed """
    return any( (pressed_key[binding] for binding in KEYBINDINGS[direction]) )


def get_text(text_db_id: str) -> str:
    """ Returns a string from the database based on provided id """
    return TextDB.get_text(text_db_id)


def set_text_db(chosen_language: dict) -> None:
    """ Allows to set a language as the current """
    TextDB.set_text_db(chosen_language)


def get_every_languages() -> list():
    """ Returns a list with every language dictionaries """
    filelist = [langfile for langfile in os.listdir(TRANSLATIONS_FOLDER)
                if langfile.endswith(".json")]

    langlist = []
    for langfile in filelist:
        fullpath = os.path.join(TRANSLATIONS_FOLDER, langfile)
        with open(fullpath, "r") as myfile:
            this_lang = json.load(myfile)
            # Every file NEEDS to have LANGUAGE key
            if this_lang.get("LANGUAGE", None):
                langlist.append(this_lang)

    return langlist


def set_music_volume(new_volume: float) -> None:
    """ Sets the main music volume """
    AudioSettings.set_music_volume(new_volume)


def get_music_volume() -> float:
    """ Returns the current main music volume """
    return AudioSettings.get_volumes()[1]


def set_sfx_volume(new_volume: float) -> None:
    AudioSettings.set_sfx_volume(new_volume)


def get_sfx_volume() -> float:
    """ Returns the current main sfx volume """
    return AudioSettings.get_volumes()[0]




# CONSTANTS LIST
# --------------

# Game Parameters
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500

STARS_SPEED = 2
STAR_SPRITE_RADIUS = 1

ASTEROID_STARTING_MIN_SPEED = 3
ASTEROID_STARTING_MAX_SPEED = 8

BOOST_SPEED_MODIFIER = 2

PLAYER_SHIP_SPEED = 5 # in PIXELS
PLAYER_STARTING_MAX_HEALTH = 3 # in PIXELS
PLAYER_REPAIR_TIME = 5 # how many SECONDS the player's ship takes for fully repairing
PLAYER_INVULNERABILITY_DURATION = 3 # how many SECONDS the player's ship invulnerability lasts

POWER_UP_SPEED = 3

AUDIO_SFX_VOLUME = 0.2
AUDIO_MUSIC_VOLUME = 0.2



# Key Bindings
KEYBINDINGS = {
    "UP": (
        pygame.K_w,
        pygame.K_UP
    ),
    "DOWN": (
        pygame.K_s,
        pygame.K_DOWN
    ),
    "LEFT": (
        pygame.K_a,
        pygame.K_LEFT
    ),
    "RIGHT": (
        pygame.K_d,
        pygame.K_RIGHT
    ),
    "SPACE": (
        pygame.K_SPACE,
    ),
    "P": (
        pygame.K_p,
    ),
    "M": (
        pygame.K_m,
    ),
    "T": (
        pygame.K_t,
    ),
}


# Assets Constants
ASSET_DIR = "assets"
AUDIO_ASSET_DIR = "Audio"
AUDIO_SFX_DIR = os.path.join(ASSET_DIR, AUDIO_ASSET_DIR, "SFX")
AUDIO_MUSIC_DIR = os.path.join(ASSET_DIR, AUDIO_ASSET_DIR, "MUSIC")
TRANSLATIONS_FOLDER = "lang"
SHIP_SPRITE = load_image(ASSET_DIR, "Ship.png")
ASTEROID_SPRITE = load_image(ASSET_DIR, "asteroid.png")
SPACE_BG = load_image(ASSET_DIR, "purple_space_bg.png") # by Digital Moons (https://digitalmoons.itch.io/)
METAL_SCRAP_SPRITE = load_image(ASSET_DIR, "metal_scrap2.png")
TITLE_FONT = os.path.join(ASSET_DIR, "kongtext.ttf") # Font by codeman38 | cody@zone38.net | http://www.zone38.net/
SFX_POWERUP_COLLECTED = load_audio(AUDIO_SFX_DIR, "sci-fi-positive-notification.wav")
SFX_TEXT_TICK = load_audio(AUDIO_SFX_DIR, "tick_001b.ogg")

# Custom Pygame Events
PLAYER_HIT = pygame.USEREVENT + 1
PLAYER_DEAD = pygame.USEREVENT + 2
POWER_UP_COLLECTED = pygame.USEREVENT + 3


# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)



# Scenes
class SCENES:
    """ Object that groups all scenes """
    GAME_MENU = 0
    GAME_TUTORIAL = 1
    GAME_LEVEL = 2
    GAME_LOSING_SCREEN = 3


# Text alignment
class TXT:
    LEFT = 0
    CENTER = 1
    RIGHT = 2



# OBJECTS
# -------

class TextDB:
    """ Inner class to manage languages and text """
    current_text_db = { "LANGUAGE": "no_language_loaded"}
    placeholder_text = "???" # To be displayed if the language selected doesn't have a key

    # Setting English as default language (if present)
    for lang in get_every_languages():
        if lang["LANGUAGE"].lower() == "english":
            current_text_db = lang

    @classmethod
    def get_text(cls, text_db_id: str) -> str:
        """ Returns a string from the database based on provided id """
        return cls.current_text_db.get(text_db_id, cls.placeholder_text)

    @classmethod
    def set_text_db(cls, chosen_language: dict) -> None:
        """ Sets a language dict as the current one """
        cls.current_text_db = chosen_language


class AudioSettings:
    """ Inner class to manage audio level across scenes """

    sfx_volume = AUDIO_SFX_VOLUME
    music_volume = AUDIO_MUSIC_VOLUME

    @classmethod
    def get_volumes(cls) -> tuple:
        """ Returns a tuple of floats (sfx_audio, music_audio) """
        return (cls.sfx_volume, cls.music_volume)

    @classmethod
    def set_sfx_volume(cls, new_volume: float) -> None:
        """ Sets the current volume for sfx clamped into 0.0 and 1.0 """
        new_volume = max(0.0, min(1.0, new_volume))
        cls.sfx_volume = new_volume

    @classmethod
    def set_music_volume(cls, new_volume: float) -> None:
        """ Sets the current volume for music clamped into 0.0 and 1.0 """
        new_volume = max(0.0, min(1.0, new_volume))
        cls.music_volume = new_volume




# Testing
if __name__ == "__main__":
    print(get_text("LOSE003"))