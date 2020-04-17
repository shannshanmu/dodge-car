import models
import constants
import pygame
import random
import time
import sys
import os

if getattr(sys, "frozen", False):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(os.path.abspath(__file__))

introComplete = False
carUP = pygame.image.load(
    basedir + "/assets/images/cars/flame_decorated_F1_cars_small/red_flaming_up.png"
)
# width of car = 39px
# height of car = 100px


def create_intro_world(target_surface):
    iw = models.Intro_world(constants.GREY)
    dividers = models.Road_sprite(
        constants.divider_width, constants.divider_height, constants.WHITE_SMOKE, target_surface
    )
    dividers.initialise_road()
    DodgeCar_title = models.Text_sprite(
        "DodgeCar",
        basedir + "/assets/fonts/EndeavourForever.ttf",
        constants.title_big_text_size,
        0,
        constants.display_height / 2 - constants.title_big_text_size / 2,
        constants.DARK_BLUE,
        constants.title_time,
    )

    Instructions = [
        models.Text_sprite(
            "Use",
            constants.FasterOneFontPath,
            constants.instructions_text_size,
            50,
            200,
            constants.BLACK,
            constants.instructions_time,
        ),
        models.Text_sprite(
            constants.left_arrow,
            constants.NotoColorEmojiFontPath,
            constants.instructions_text_size,
            250,
            200,
            constants.BLACK,
            constants.instructions_time,
        ),
        models.Text_sprite(
            constants.right_arrow,
            constants.NotoColorEmojiFontPath,
            constants.instructions_text_size,
            410,
            200,
            constants.BLACK,
            constants.instructions_time,
        ),
        models.Text_sprite(
            "to",
            constants.FasterOneFontPath,
            constants.instructions_text_size,
            550,
            200,
            constants.BLACK,
            constants.instructions_time,
        ),
        models.Text_sprite(
            "move left/right",
            constants.FasterOneFontPath,
            constants.instructions_text_size,
            0,
            400,
            constants.BLACK,
            constants.instructions_time,
        ),
    ]
    Number3 = models.Text_sprite(
        3, constants.FasterOneFontPath, 300, 0 + 25, 30, constants.RED, constants.countdown_time
    )
    Number2 = models.Text_sprite(
        2, constants.FasterOneFontPath, 300, 250 + 25, 30, constants.RED, constants.countdown_time
    )
    Number1 = models.Text_sprite(
        1,
        constants.FasterOneFontPath,
        300,
        500 + 20,
        30,
        constants.RED,
        constants.countdown_time - 50,
    )
    GO = models.Text_sprite(
        "GO!",
        basedir + "/assets/fonts/Thunderbold.otf",
        300,
        constants.display_width / 2 - 230,
        constants.display_height / 2,
        constants.GREEN,
        constants.countdown_time,
    )
    iw.add_sprite(dividers)
    iw.add_sequence_sprite([DodgeCar_title])
    iw.add_sequence_sprite(Instructions)
    iw.add_sequence_sprite([Number3])
    iw.add_sequence_sprite([Number2])
    iw.add_sequence_sprite([Number1])
    iw.add_sequence_sprite([GO])
    return iw


def create_world(target_surface):
    w = models.World(constants.GREY)
    dividers = models.Road_sprite(
        constants.divider_width, constants.divider_height, constants.WHITE_SMOKE, target_surface
    )
    dividers.initialise_road()
    car = models.Car_sprite(
        basedir + "/assets/images/cars/flame_decorated_F1_cars_small/red_flaming_up.png",
        basedir + "/assets/images/cars/flame_decorated_F1_cars_small/red_flaming_crashed.png",
        target_surface,
    )
    crashed_text = models.Text_sprite(
        "You Crashed",
        constants.FasterOneFontPath,
        80,
        0,
        constants.display_height / 2,
        constants.RED,
        0,
    )
    end_emoji = models.Text_sprite(
        constants.emojis[random.randint(3, 15)],
        constants.NotoColorEmojiFontPath,
        80,
        constants.display_width - 140,
        constants.display_height / 2 - 30,
        constants.BLACK,
        0,
    )
    end_emoji.type = "end_world_emoji"
    crashed_text.type = "end_world_crashed"
    end_emoji.visible = False
    crashed_text.visible = False
    w.add_sprite(dividers)
    w.add_sprite(car)
    w.add_sprite(crashed_text)
    w.add_sprite(end_emoji)
    return w


def game_loop(intro_world, main_world, target_surface):
    gameExit = False
    end_music = False
    bgMusicPlaying = False
    clock = pygame.time.Clock()
    global introComplete
    if not introComplete:
        world = intro_world
    while not gameExit:
        if introComplete:
            world = main_world

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.USEREVENT + 1:
                introComplete = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and introComplete:
                bgMusicPlaying = False
                end_music = False
                pygame.mixer.music.stop()
                world = create_world(target_surface)
                main_world = world
            else:
                world.update(event)
            if introComplete and not bgMusicPlaying:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(basedir + "/assets/music/background/Cyber_Race.ogg")
                pygame.mixer.music.play(-1)
                bgMusicPlaying = True
            if world.ended:
                if not end_music:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(basedir + "/assets/music/end/Game_End_Fade_Out.ogg")
                    pygame.mixer.music.play(0)
                    end_music = True
        world.update(pygame.NOEVENT)
        world.ended = world.detect_collision()
        world.draw(target_surface)
        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.mixer.pre_init()
    pygame.init()

    gameDisplay = pygame.display.set_mode((constants.display_width, constants.display_height))
    pygame.display.set_caption("DodgeCar!")
    intro_world = create_intro_world(gameDisplay)
    world = create_world(gameDisplay)
    pygame.time.set_timer(pygame.USEREVENT + 2, 2000, True)
    pygame.time.set_timer(pygame.USEREVENT + 3, constants.intro_time_before_countdown, True)
    pygame.mixer.music.load(basedir + "/assets/music/background/Cyber_Race.ogg")
    pygame.mixer.music.play(-1)
    game_loop(intro_world, world, gameDisplay)


if __name__ == "__main__":
    main()
