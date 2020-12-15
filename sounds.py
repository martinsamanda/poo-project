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

    def princess_hit_sound(self):
        princesshit = mixer.Sound(path.join(SOUNDS_FOLDER, PRINCESS_HITTING))
        princesshit.play()
    
    def orc_sound(self):
        orc_sound = mixer.Sound(path.join(SOUNDS_FOLDER, ORC_SOUND))
        orc_sound.play()
