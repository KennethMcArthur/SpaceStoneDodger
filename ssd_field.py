# pylint: disable=no-member

# SpaceStoneDodger: Field Class, from which every type of field should inherit

import pygame
from random import randint
import ssd_constants as CST



# New generic Field class
class Field_of:
    def __init__(self, of_what, howmany: int, spawn_parameters: dict) -> None:
        self.base_element_class = of_what
        self.spawn_parameters = spawn_parameters
        self.to_be_deleted = 0
        self.elements = [self.new_element() for _ in range(howmany)]
        self.how_many_passed = 0


    def random_position(self, spwn_par: dict) -> int:
        """ returns a tuple of random x,y inside the spawn zone and speed """
        newx = randint(spwn_par.get("x_from", 0), spwn_par.get("x_to", 0))
        newy = randint(spwn_par.get("y_from", 0), spwn_par.get("y_to", 0))
        newspeed = randint(spwn_par.get("min_speed", 0), spwn_par.get("max_speed", 0))
        return newx, newy, newspeed


    def new_element(self):
        """ returns a new asteroid at a random point of the spawn location """
        newx, newy, newspeed = self.random_position(self.spawn_parameters)
        return self.base_element_class(newx, newy, newspeed)


    def resize(self, newsize: int) -> None:
        """ Resizes the number of asteroids on the screen """
        self.to_be_deleted = max(0, len(self.elements) - newsize) # Compressed if
        # Adding new asteroids if size is greater
        self.elements.extend([self.new_element() for _ in range(newsize - len(self.elements))])


    def other_stuff_for_each(self, element):
        """ Other functions to call for each element, aside from game_tick_update() """
        pass


    def get_how_many_passed(self) -> int:
        return self.how_many_passed


    def game_tick_update(self, window: pygame.Surface) -> None:
        """ Updates each field element """
        i = 0
        while i < len(self.elements): 
            element = self.elements[i]

            if element.is_offscreen_left():
                self.how_many_passed += 1 # Keeping track of how many elements have passed
                if self.to_be_deleted > 0: # we ditch this element if there are too many...
                    self.elements.pop(i)
                    self.to_be_deleted -= 1
                    continue
                else:
                    newx, newy, newspeed = self.random_position(self.spawn_parameters)
                    element.relocate(newx, newy, newspeed)

            element.game_tick_update(window)
            self.other_stuff_for_each(element)

            i += 1


