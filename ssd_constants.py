# pylint: disable=no-member

# SpaceStoneDodger: Constants database
import pygame, os



# Game Parameters
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500


# Assets Constants
ASSET_DIR = "assets"
SHIP_SPRITE = pygame.image.load(os.path.join(ASSET_DIR, "Ship.png"))
ASTEROID_SPRITE = pygame.image.load(os.path.join(ASSET_DIR, "asteroid.png"))
SPACE_BG = pygame.image.load(os.path.join(ASSET_DIR, 'bg_blurry.jpg'))


# Custom Pygame Events
PLAYER_HIT = pygame.USEREVENT + 1
PLAYER_DEAD = pygame.USEREVENT + 2