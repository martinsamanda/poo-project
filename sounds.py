import pygame
import sys
from pygame import mixer
from settings import *


class Sound:
    def __init__(self):
        pygame.mixer.init()

    def background_sound(self):
        pygame.mixer.music.load(path.join(SOUNDS_FOLDER, BACKGROUND_SOUND))
        pygame.mixer.music.play(-1)
        #pygame.mixer.set_volume(0.5)

    def princess_hit_sound(self):
        pygame.mixer.music.load(path.join(SOUNDS_FOLDER, PRINCESS_HITTING))
