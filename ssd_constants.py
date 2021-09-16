# pylint: disable=no-member

# SpaceStoneDodger: Constants database
import pygame, os


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
ASTEROID_SPEED_MODIFIER_DECEL = 0.9
ASTEROID_SPEED_MODIFIER_ACCEL = 1.1

PLAYER_SHIP_SPEED = 5 # in PIXELS
PLAYER_STARTING_MAX_HEALTH = 3 # in PIXELS
PLAYER_REPAIR_TIME = 5 # how many SECONDS the player's ship takes for fully repairing
PLAYER_INVULNERABILITY_DURATION = 3 # how many SECONDS the player's ship invulnerability lasts

POWER_UP_SPEED = 2
POWER_UP_SPEED_MODIFIER_DECEL = 0.9
POWER_UP_SPEED_MODIFIER_ACCEL = 1.1


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
    )
}


# Assets Constants
ASSET_DIR = "assets"
SHIP_SPRITE = load_image(ASSET_DIR, "Ship.png")
ASTEROID_SPRITE = load_image(ASSET_DIR, "asteroid.png")
SPACE_BG = load_image(ASSET_DIR, "bg_blurry.jpg")
METAL_SCRAP_SPRITE = load_image(ASSET_DIR, "metal_scrap2.png")
TITLE_FONT = os.path.join(ASSET_DIR, "kongtext.ttf") # Font by codeman38 | cody@zone38.net | http://www.zone38.net/

# Custom Pygame Events
PLAYER_HIT = pygame.USEREVENT + 1
PLAYER_DEAD = pygame.USEREVENT + 2
POWER_UP_COLLECTED = pygame.USEREVENT + 3


# Colors
COLOR_WHITE = (255, 255, 255)