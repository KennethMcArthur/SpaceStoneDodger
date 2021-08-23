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


# CONSTANTS LIST
# --------------

# Game Parameters
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
STARS_SPEED = 2
ASTEROID_STARTING_MIN_SPEED = 3
ASTEROID_STARTING_MAX_SPEED = 8
ASTEROID_SPEED_MODIFIER_DECEL = 0.9
ASTEROID_SPEED_MODIFIER_ACCEL = 1.1


# Assets Constants
ASSET_DIR = "assets"
SHIP_SPRITE = load_image(ASSET_DIR, "Ship.png")
ASTEROID_SPRITE = load_image(ASSET_DIR, "asteroid.png")
SPACE_BG = load_image(ASSET_DIR, 'bg_blurry.jpg')


# Custom Pygame Events
PLAYER_HIT = pygame.USEREVENT + 1
PLAYER_DEAD = pygame.USEREVENT + 2



