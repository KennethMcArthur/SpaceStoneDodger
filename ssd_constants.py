# pylint: disable=no-member

# SpaceStoneDodger: Constants database
import pygame, os
from collections import defaultdict


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


def pressed(direction: str, pressed_key: list) -> bool:
    """ Returns if one of the corresponding key of a direction is been pressed """
    return any( (pressed_key[binding] for binding in KEYBINDINGS[direction]) )



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
SHIP_SPRITE = load_image(ASSET_DIR, "Ship.png")
ASTEROID_SPRITE = load_image(ASSET_DIR, "asteroid.png")
SPACE_BG = load_image(ASSET_DIR, "purple_space_bg.png") # by Digital Moons (https://digitalmoons.itch.io/)
METAL_SCRAP_SPRITE = load_image(ASSET_DIR, "metal_scrap2.png")
TITLE_FONT = os.path.join(ASSET_DIR, "kongtext.ttf") # Font by codeman38 | cody@zone38.net | http://www.zone38.net/


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


# Text strings database
TEXT_DB = defaultdict(lambda: "???", {
    # Menu text
    1: "a simple game where you, well, dodge stones",
    2: "Play",
    3: "Tutorial",
    # Tutorial text
    100: "Move with W,A,S,D (or arrows)\nBoost the ship with SPACE",
    101: "Avoid asteroids",
    102: "Collect valuable scraps",
    103: "Your life",
    104: "back to Menu",
    105: "Play the game",
    # Game Level text
    200: "Metals",
    201: "Ok Pilot, I'm Navigator and I'll help you in today's mission. Look how cool it sounds when you call it 'mission'",
    202: "Our job is to collect metal scraps from space and then sell it for money, it ain't much but it's honest work, like my grand-grand-father used to say on earth.",
    203: "Today we detected an unusual asteroid activity not far from Quasari Station, this means that we'll surely find a lot of metal parts around there (you know, impacts).\nWe just need to collect as much scraps as we can, and with a Station nearby we could sell the stuff there.",
    204: "Avoid asteroids and don't get hit too much.\nWe can handle a couple of hits, but three strikes and we're out. So try your best.\nOnward to Quasari Station, then.",
    205: "Watch out! Lots of stones ahead!",
    206: "Watch out! An even bigger group ahead!",
    207: "Almost there, but here's a HUGE group!",
    208: "Look at all this treasure! We're going to be RICH!",
    209: "Well, that's weird. I mean: who'd leave all this stuff right next to the station?!",
    210: "Wait...",
    211: "Oh my...we're not close to the station: this IS the station, or what is left.",
    212: "There's no way it's just an accident, We're definitely not safe here.\nLet's go and FAST, we'll figure out what happened later.",
    213: "...to be continued",
    # Game over text
    301: "Sadly, stones Won",
    302: "back to Menu",
    303: "Play again",

})



if __name__ == "__main__":
    print(type(TEXT_DB))
    print(TEXT_DB[303])
    print(TEXT_DB[500])