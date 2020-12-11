import pygame
from settings import *
from os import path


class Map:
    def __init__(self):
        self.__data = []

        with open(path.join(GAME_FOLDER, MAP_FILE), 'rt') as f:
            for line in f:
                self.__data.append(line)

        self.__tilewidth = len(self.__data[0])
        self.__tileheight = len(self.__data)
        self.__width = self.__tilewidth * TILESIZE
        self.__height= self.__tileheight * TILESIZE


    @property
    def data(self):
        return self.__data

class Highscore:
    def __init__(self):
        with open(path.join(GAME_FOLDER, HS_FILE), 'r') as f:
            try:
                self.__data = int(f.read())
            except:
                self.__data = 0
        f.close()

    @property
    def data(self):
        return self.__data

    def new_hs(self, score):
        with open(path.join(GAME_FOLDER, HS_FILE), 'w') as f:
            self.__data = score
            f.write(str(score))
            f.close()