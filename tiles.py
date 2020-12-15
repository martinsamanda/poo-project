from abc import ABC, abstractmethod
from os import path, listdir

import pygame
from pygame.locals import *
from settings import *
from attack import Attack


class Tile(ABC, pygame.sprite.Sprite):
    def __init__(self, image_link, position_x, position_y, model):
        super().__init__()
        self._layer = TILE_LAYER
        self.__image = pygame.image.load(path.join(IMG_FOLDER, image_link)).convert_alpha()
        self.__image = pygame.transform.scale(self.__image, (TILESIZE, TILESIZE))
        self.__rect = self.__image.get_rect()
        self.__rect.x = position_x * TILESIZE   
        self.__rect.y = position_y * TILESIZE
        self.model = model

        self.model.tiles.add(self)
        self.model.all_sprites.add(self)

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image


class Unbreakable(Tile):
    def __init__(self, position_x, position_y, model):
        super().__init__(UNBREAKABLE_IMG, position_x, position_y, model)


class Breakable(Tile):
    def __init__(self, position_x, position_y, model):
        super().__init__(BREAKABLE_IMG, position_x, position_y, model)
        # Adiciona o bloco como se fosse um inimigo para poder ser destrutivel
        self.model.destructive_tiles.add(self)


class Coin(Breakable):
    def __init__(self, position_x, position_y, model):
        Tile.__init__(self,COIN_TILE_IMG, position_x, position_y, model)
        #Igual o breakable porém um dia, se tudo der certo, vai aumentar os pontos
        #update: esse dia chegou, funcionou
        self.model.coin_tiles.add(self)


class Portinha(Tile):
    def __init__(self, position_x, position_y, model):
        super().__init__(DOOR_TILE_IMG, position_x, position_y, model)
