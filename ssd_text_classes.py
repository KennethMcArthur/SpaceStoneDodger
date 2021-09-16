# pylint: disable=no-member

# SpaceStoneDodger: Text utility Classes

import pygame
import ssd_constants as CST




class StaticText:
    def __init__(self, text: str, size: int, position: tuple) -> None:
        self.pos_x, self.pos_y = position
        self.titlefont = pygame.font.Font(CST.TITLE_FONT, size)
        self.titletext = self.titlefont.render(text, True, CST.COLOR_WHITE)
        self.center_me()

    def set_text(self, new_text: str) -> None:
        self.titletext = self.titlefont.render(new_text, True, CST.COLOR_WHITE)
        self.center_me()

    def center_me(self):
        self.titlerect = self.titletext.get_rect()
        self.titlerect.center = (self.pos_x, self.pos_y)

    def game_tick_update(self, window: pygame.Surface) -> None:
        window.blit(self.titletext, self.titlerect)