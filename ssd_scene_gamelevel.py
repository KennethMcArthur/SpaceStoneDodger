# pylint: disable=no-member

# SpaceStonerDodger: Game Level Scene


import pygame
import ssd_constants as CST
import ssd_player as plr
import ssd_asteroid as ast
import ssd_starfield as stf
import ssd_background as bg
import ssd_powerup as pwr
import ssd_text_classes as txt
import ssd_scene_master_class as Scn



class GameLevel(Scn.Scene):
    def scene_related_init(self):
        self.num_power_ups = 1
        self.num_asteroids = 2
        self.num_stars = 24
        self.score = 0
        self.asteroid_needed_to_next = 4
        self.asteroid_passed_target_number = 5

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(self.num_stars)
        self.player = plr.Player_pawn(50, CST.SCREEN_HEIGHT // 2)
        self.ui_lifebar = plr.Lifebar(self.player)
        self.asteroid_field = ast.AsteroidField(self.num_asteroids, self.player)
        self.powerup_field = pwr.PowerUpField(self.num_power_ups, self.player)
        self.score_label = txt.StaticText("Score:", 14, (0,0), CST.TXT.LEFT)

        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.powerup_field)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.player)
        self.updatelist.append(self.asteroid_field)
        self.updatelist.append(self.ui_lifebar)
        self.updatelist.append(self.score_label)

        self.set_timer_step(1) # Setting the internal timer


    def timer_duty(self) -> None:
        # What happens when the timer goes off
        """
        TODO: PowerUp spawning rework
        """
        passed = self.asteroid_field.get_how_many_passed()
        if passed >= self.asteroid_passed_target_number:
            self.asteroid_needed_to_next += 1
            self.asteroid_passed_target_number += self.asteroid_needed_to_next
            self.num_asteroids = 2 + self.score // 3
            self.num_power_ups = 1 + self.num_asteroids // 3
            self.asteroid_field.resize(self.num_asteroids)
            self.powerup_field.resize(self.num_power_ups)
            print("Target number is now", self.asteroid_passed_target_number)
            
        print("Asteroids passed: ", passed)
        print("Total asteroids:", len(self.asteroid_field.elements))
        

    def event_checking(self, this_event: pygame.event) -> None:
        super().event_checking(this_event) # for quitting handling
        if this_event.type == CST.PLAYER_HIT:
            self.player.got_hit(CST.PLAYER_DEAD)
        if this_event.type == CST.PLAYER_DEAD:
            self.quit_loop(CST.SCENES.GAME_LOSING_SCREEN)
        if this_event.type == CST.POWER_UP_COLLECTED:
            self.score += 1
            self.score_label.set_text("Score: " + str(self.score))


    def keys_to_check(self, key_list: list) -> None:
        self.player.handle_movement(key_list)
        self.asteroid_field.handle_movement(key_list)
        self.powerup_field.handle_movement(key_list)
        self.starfield.handle_movement(key_list)


    def reset_state(self):
        self.__init__(self.GAME_WINDOW) # Forcing the level to initial state

  




# TESTING
def main_game():
    pygame.init()

    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_level = GameLevel(WIN)
    next_scene = 0

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = game_level.run()
        print("Next scene: ", next_scene)



if __name__ == "__main__":
    main_game()
    