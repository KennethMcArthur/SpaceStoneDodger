# pylint: disable=no-member

# SpaceStoneDodger: Background Classe

import pygame
import ssd_constants as cst



class Background:
    """ Game Background Class """

    def __init__(self) -> None:
        self.sprite_image = cst.SPACE_BG
        self.bg = pygame.transform.scale(self.sprite_image, (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))


    def game_tick_update(self, window) -> None:
        window.blit(self.bg, (0,0))