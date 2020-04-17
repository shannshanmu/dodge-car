import pygame
import time

pygame.mixer.pre_init()
pygame.init()
# gameDisplay = pygame.display.set_mode((constants.display_width, constants.display_height))
# pygame.display.set_caption("DodgeCar!")
print(pygame.mixer.music.get_volume())
pygame.mixer.music.load("./assets/music/background/Cyber_Race.ogg")
pygame.mixer.music.play(0)
print(pygame.mixer.music.get_busy())
# pygame.mixer.Sound("assets/music/background/Cyber_Raceconverted.ogg").play(0)
time.sleep(5)
# if event.type == pygame.USEREVENT + 3:
# pygame.mixer.music.stop()
# pygame.mixer.music.load("assets/music/start/321GO.ogg")
# pygame.mixer.music.play(1)

# pygame.mixer.music.stop()
# pygame.mixer.music.stop()
# pygame.mixer.music.load("assets/music/background/Cyber_Race.ogg")
# pygame.mixer.music.play(-1)

# pygame.mixer.music.stop()
# pygame.mixer.music.load("assets/music/end/Game_End_Fade_Out.ogg")
# pygame.mixer.music.play(0)
# pygame.mixer.music.unload()
