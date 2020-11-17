import pygame
import sys

from pygame.locals import *
from GameView import GameView

class GameController:
    def __init__(self):
        pygame.init()
        self.__GameView = GameView()

    def start(self):
        self.__GameView.set_settings()

        while True:
            self.__GameView.update()
            self.__GameView.set_square()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.__GameView.frames()
