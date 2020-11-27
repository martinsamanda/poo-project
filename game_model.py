import pygame
from sprites import *
from os import path


class GameModel:
    def __init__(self, controller):
        self.__GameController = controller
        self.__all_sprites = pygame.sprite.Group()
        self.__characters = pygame.sprite.Group()
        self.__enemies = pygame.sprite.Group()
        self.__tiles = pygame.sprite.Group()

        self.__princess = None

        self.__map_data = []

    @property
    def all_sprites(self):
        return self.__all_sprites

    @property
    def princess(self):
        return self.__princess

    @property
    def enemies(self):
        return self.__enemies

    @property
    def characters(self):
        return self.__characters

    @property
    def tiles(self):
        return self.__tiles

    def load_map(self, map):
        for row, tiles in enumerate(map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Unbreakable('', col, row, self)
                if tile == 'P':
                    self.__princess = Princess(self, col, row)

    def update_positions(self):
        self.__all_sprites.update()

        #Checa se é preciso abaixar a tela
        if self.__princess.rect.bottom >= SCREEN_HEIGHT /3:
            self.__princess.pos.y -= abs(self.__princess.vel.y)
            for tile in self.__tiles:
                tile.rect.y -= abs(self.__princess.vel.y)
                if tile.rect.bottom < 0:
                    tile.kill()

    def end(self):
        for sprite in self.__all_sprites:
            sprite.kill()

