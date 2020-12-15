from sprites.princess.princess import Princess
from sprites.enemy import Enemy
from sprites.orc import Orc
from sprites.golem import Golem
from sprites.black_golem import BlackGolem
from sprites.white_golem import WhiteGolem
from sprites.tiles.tiles import *
from persistence import Map, Highscore
import pygame
from pygame.locals import *
from settings import *


class GameModel:
    def __init__(self, controller):
        self.__GameController = controller
        self.__all_sprites = pygame.sprite.LayeredUpdates()
        self.__characters = pygame.sprite.Group()
        self.__enemies = pygame.sprite.Group()
        self.__tiles = pygame.sprite.Group()
        self.__destructive_tiles = pygame.sprite.Group()
        self.__coin_tiles = pygame.sprite.Group()
        self.__door_tile = None
        self.__princess = None
        

        self.score = 0
        self.__highscore = Highscore()
        self.__map = []

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

    @property
    def destructive_tiles(self):
        return self.__destructive_tiles

    @property
    def coin_tiles(self):
        return self.__coin_tiles
    
    @property
    def door_tile(self):
        return self.__door_tile

    @property
    def controller(self):
        return self.__GameController

    @property
    def highscore(self):
        return self.__highscore

    def load_map(self):
        self.__map = Map()
        for row, tiles in enumerate(self.__map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Unbreakable(col, row, self)
                if tile == '2':
                    Breakable(col, row, self)
                if tile == 'P':
                    self.__princess = Princess(col, row, self)
                if tile == 'O':
                    Orc(col, row, self)
                if tile == 'G':
                    Golem(col, row, self)
                if tile == 'B':
                    BlackGolem(col, row, self)   
                if tile == 'W':
                    WhiteGolem(col, row, self)
                if tile == 'C':
                    Coin(col, row, self)
                if tile == 'D':
                    self.__door_tile = Portinha(col, row, self)

    def update_positions(self):
        self.__all_sprites.update()
        #Abaixa a tela caso passe de uma certa altura e mata os sprites que não aparecem mais
        if self.__princess.rect.bottom > SCREEN_HEIGHT /3 and self.__door_tile.rect.bottom - self.__princess.rect.bottom > TILESIZE/2:
            self.__princess.pos.y -= abs(self.__princess.vel.y)
            for tile in self.__tiles:
                tile.rect.y -= abs(self.__princess.vel.y)
                if tile.rect.bottom < 0:
                    tile.kill()


    def end(self):
        for sprite in self.__all_sprites:
            sprite.kill()
