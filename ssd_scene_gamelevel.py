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
import ssd_movie_effect as mov


class GameLevel(Scn.Scene):
    def scene_related_init(self):
        self.keypress_allowed = False
        self.num_power_ups = 0
        self.num_asteroids = 0
        self.num_stars = 24
        self.score = 0

        self.level_background = bg.Background()
        self.starfield = stf.Starfield(self.num_stars)
        self.player = plr.Player_pawn(-50, CST.SCREEN_HEIGHT // 2)
        self.ui_lifebar = plr.Lifebar(self.player)
        self.asteroid_field = ast.AsteroidField(self.num_asteroids, self.player)
        self.powerup_field = pwr.PowerUpField(self.num_power_ups, self.player)
        self.score_label = txt.StaticText("Score" + ":", 14, (0,0), CST.TXT.LEFT)
        self.navigator_text = txt.AnimatedTypedText("", 14, (30, 300), 20, autostart=False)
        self.movie_effect = mov.MovieEffect(80, 20)

        # Append order is draw order
        self.updatelist.append(self.level_background)
        self.updatelist.append(self.powerup_field)
        self.updatelist.append(self.starfield)
        self.updatelist.append(self.player)
        self.updatelist.append(self.asteroid_field)
        self.updatelist.append(self.ui_lifebar)
        self.updatelist.append(self.score_label)
        self.updatelist.append(self.navigator_text)
        self.updatelist.append(self.movie_effect)

        self.timeline = { # Keys are seconds of play, values are methods
            1: self.tml_begin,
            2: self.tml_starting_speech_1,
            10: self.tml_starting_speech_2,
            21: self.tml_starting_speech_3,
            40: self.tml_starting_speech_4,
            54: self.tml_playing_phase_start,
            58: self.tml_playing_phase_1_1,
            68: self.tml_playing_phase_1_2,
            78: self.tml_playing_phase_1_3,
            88: self.tml_calm_before_the_swarm_1,
            93: self.tml_swarm_1,
            98: self.tml_swarm_passed_1,
            103: self.tml_playing_phase_2_1,
            118: self.tml_playing_phase_2_2,
            133: self.tml_playing_phase_2_3,
            148: self.tml_calm_before_the_swarm_2,
            153: self.tml_swarm_2,
            161: self.tml_swarm_passed_2,
            166: self.tml_playing_phase_3_1,
            186: self.tml_playing_phase_3_2,
            206: self.tml_playing_phase_3_3,
            226: self.tml_calm_before_the_swarm_3,
            231: self.tml_swarm_3,
            243: self.tml_swarm_passed_3,
            248: self.tml_end_cinematic_1,
            254: self.tml_end_cinematic_2,
            260: self.tml_end_cinematic_3,
            266: self.tml_end_cinematic_4,
            269: self.tml_end_cinematic_5,
            276: self.tml_end_cinematic_6,
            288: self.tml_end_cinematic_7,
            295: self.tml_end_of_scene,
        }

        self.set_timer_step(1) # Setting the internal timer
        self.timer_seconds_passed = 0


    def timer_duty(self) -> None:
        # What happens when the timer goes off
        self.timer_seconds_passed += 1
        self.check_timeline_progress(self.timer_seconds_passed)
        

    def event_checking(self, this_event: pygame.event) -> None:
        super().event_checking(this_event) # for quitting handling
        if this_event.type == CST.PLAYER_HIT:
            self.player.got_hit(CST.PLAYER_DEAD)
        if this_event.type == CST.PLAYER_DEAD:
            self.quit_loop(CST.SCENES.GAME_LOSING_SCREEN)
        if this_event.type == CST.POWER_UP_COLLECTED:
            self.score += 1
            self.score_label.set_text("Score" + ": " + str(self.score))


    def keys_to_check(self, key_list: list) -> None:
        if not self.keypress_allowed:
            return
        self.player.handle_movement(key_list)
        self.asteroid_field.handle_movement(key_list)
        self.powerup_field.handle_movement(key_list)
        self.starfield.handle_movement(key_list)


    def reset_state(self):
        self.__init__(self.GAME_WINDOW) # Forcing the level to initial state when playing again

  
    # Timeline related methods
    def check_timeline_progress(self, time_now) -> None:
        """ Calls timeline events when it's the right time """
        if not self.timeline:
            return
        next_event_in_line = min(self.timeline.keys())

        while self.timer_seconds_passed > next_event_in_line: # Used to skip phases during tests
            self.timeline.pop(next_event_in_line)
            next_event_in_line = min(self.timeline.keys())

        if time_now == next_event_in_line:
            self.timeline[time_now]()
            self.timeline.pop(time_now)

    def tml_begin(self) -> None:
        """ Beginning of the game """
        self.player.automove_to(50, CST.SCREEN_HEIGHT // 2)

    def tml_starting_speech_1(self) -> None:
        this_event_text = "Ok Pilot, I'm Navigator and I'll help you in today's mission. Look how cool it sounds when you call it 'mission'"
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()

    def tml_starting_speech_2(self) -> None:
        this_event_text = "Our job is to collect metal scraps from space and then sell it for money, it ain't much but it's honest work, like my grand-grand-father used to say on earth."
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()

    def tml_starting_speech_3(self) -> None:
        this_event_text = "Today we detected an unusual asteroid activity not far from Quasari Station, this means that we'll surely find a lot of metal parts around there (you know, impacts).\nWe just need to collect as much scraps as we can, and with a Station nearby we could sell the stuff there."
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()
    
    def tml_starting_speech_4(self) -> None:
        this_event_text = "Avoid asteroids and don't get hit too much.\nWe can handle a couple of hits, but three strikes and we're out. So try your best.\nOnward to Quasari Station, then."
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()

    def tml_playing_phase_start(self) -> None:
        self.movie_effect.start_animation()
        self.navigator_text.hide()
        self.player.user_controlled()
        self.keypress_allowed = True

    def tml_playing_phase_1_1(self) -> None:
        self.num_asteroids = 2
        self.num_power_ups = 1
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_playing_phase_1_2(self) -> None:
        self.num_asteroids = 4
        self.num_power_ups = 2
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_playing_phase_1_3(self) -> None:
        self.num_asteroids = 6
        self.num_power_ups = 3
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_calm_before_the_swarm_1(self) -> None:
        self.num_asteroids = 3
        self.num_power_ups = 2
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)
        self.navigator_text.set_text("Watch out! Lots of stones ahead!")
        self.navigator_text.start()

    def tml_swarm_1(self) -> None:
        self.navigator_text.hide()
        self.num_asteroids = 12
        self.num_power_ups = 5
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_swarm_passed_1(self) -> None:
        self.num_asteroids = 3
        self.num_power_ups = 2
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_playing_phase_2_1(self) -> None:
        self.num_asteroids = 4
        self.num_power_ups = 2
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_playing_phase_2_2(self) -> None:
        self.num_asteroids = 6
        self.num_power_ups = 3
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_playing_phase_2_3(self) -> None:
        self.num_asteroids = 8
        self.num_power_ups = 4
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_calm_before_the_swarm_2(self) -> None:
        self.num_asteroids = 4
        self.num_power_ups = 3
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)
        self.navigator_text.set_text("Watch out! Big group ahead!")
        self.navigator_text.start()

    def tml_swarm_2(self) -> None:
        self.navigator_text.hide()
        self.num_asteroids = 16
        self.num_power_ups = 6
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_swarm_passed_2(self) -> None:
        self.num_asteroids = 4
        self.num_power_ups = 3
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_playing_phase_3_1(self) -> None:
        self.num_asteroids = 6
        self.num_power_ups = 4
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_playing_phase_3_2(self) -> None:
        self.num_asteroids = 8
        self.num_power_ups = 5
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_playing_phase_3_3(self) -> None:
        self.num_asteroids = 10
        self.num_power_ups = 6
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)

    def tml_calm_before_the_swarm_3(self) -> None:
        self.num_asteroids = 5
        self.num_power_ups = 8
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)
        self.navigator_text.set_text("Almost there, but here's a HUGE group!")
        self.navigator_text.start()

    def tml_swarm_3(self) -> None:
        self.navigator_text.hide()
        self.num_asteroids = 25
        self.num_power_ups = 8
        self.asteroid_field.resize(self.num_asteroids)
        self.powerup_field.resize(self.num_power_ups)
        self.num_asteroids = 0
        self.asteroid_field.resize(self.num_asteroids)

    def tml_swarm_passed_3(self) -> None:
        self.num_power_ups = 16
        self.powerup_field.resize(self.num_power_ups)

    def tml_end_cinematic_1(self) -> None:
        self.player.god_mode(True)
        self.keypress_allowed = False
        self.movie_effect.start_animation()
        self.player.automove_to(50, CST.SCREEN_HEIGHT // 2)

    def tml_end_cinematic_2(self) -> None:
        this_event_text = "Look at all this treasure! We're going to be RICH!"
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()

    def tml_end_cinematic_3(self) -> None:
        this_event_text = "Well, that's weird. I mean: who'd leave all this stuff right next to the station?!"
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()

    def tml_end_cinematic_4(self) -> None:
        self.num_power_ups = 60
        self.powerup_field.resize(self.num_power_ups)
        this_event_text = "Wait..."
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()

    def tml_end_cinematic_5(self) -> None:
        this_event_text = "Oh my...we're not close to the station: this IS the station, or what is left."
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()
        self.powerup_field.stop_movements()
        self.starfield.stop_movements()

    def tml_end_cinematic_6(self) -> None:
        this_event_text = "There's no way it's just an accident, We're definitely not safe here.\nLet's go and FAST, we'll figure out what happened later."
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()
    
    def tml_end_cinematic_7(self) -> None:
        this_event_text = "...to be continued"
        self.navigator_text.set_text(this_event_text)
        self.navigator_text.start()
        self.player.automove_to(CST.SCREEN_WIDTH + 100, CST.SCREEN_HEIGHT // 2)

    def tml_end_of_scene(self) -> None:
        """ End of scene, onward to credits! """
        self.quit_loop(CST.SCENES.GAME_MENU)





# TESTING
def main_game():
    pygame.init()

    # Defining our game window
    WIN = pygame.display.set_mode((CST.SCREEN_WIDTH, CST.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Stone Dodger!")

    game_level = GameLevel(WIN)
    next_scene = 0

    # Skipping intro for testing purpose
    #game_level.timer_seconds_passed = 268
    #game_level.keypress_allowed = True
    #game_level.movie_effect.start_animation()
    game_level.player.god_mode(True) # Keep player invulnerable for testing purpose"""

    # Scene sequence, each scene returns the index for the next one
    while True:
        next_scene = game_level.run()
        print("Next scene: ", next_scene)



if __name__ == "__main__":
    main_game()
    