import pygame
from sprites.enemy import Enemy
from sprites.character import Character
from os import path, listdir
from pygame.locals import *
from settings import *
from attack import Attack
vec = pygame.math.Vector2


class Golem(Enemy):
    def __init__(self, position_x, position_y, model):
        Character.__init__(self, GOLEM_FOLDER, 30, 64, position_x * TILESIZE, position_y * TILESIZE, model, ENEMY_LAYER)
        self.direction = 1
        self.model.enemies.add(self)
