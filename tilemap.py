import pygame
from settings import *

class Map:
    def __init__(self, filename):
        self.__data = []

        with open(filename, 'rt') as f:
            for line in f:
                self.__data.append(line)

        self.__tilewidth = len(self.__data[0])
        self.__tileheight = len(self.__data)
        self.__width = self.__tilewidth * TILESIZE
        self.__height= self.__tileheight * TILESIZE


    @property
    def data(self):
        return self.__data