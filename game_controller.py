import pygame
import sys

from pygame.locals import *
from game_view import GameView
from game_model import GameModel
from tilemap import Map
from os import path


class GameController:
    def __init__(self):
        pygame.init()
        self.__GameModel = GameModel(self)
        self.__GameView = GameView(self, self.__GameModel)
        self.__map = None

    def start(self):
        self.__GameView.starting_settings()
        self.load_data()
        self.__GameModel.load_map(self.__map)

        while True:
            self.events()
            self.__GameModel.update_positions()
            self.__GameView.draw()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.__map = Map(path.join(game_folder, 'map.txt'))

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()